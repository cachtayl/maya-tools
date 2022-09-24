'''
Created September 2022
@author- camtaylor1999@gmail.com

Prop Rig Generator- a script that does conventional prop rigging for you
https://github.com/cachtayl/maya-tools

Usage:  Select object in scene and execute this script
Output: Master and Offset controllers parented to a group holding the prop

Future GUI Ideas:
Checkbox to lock the prop transforms and make not selectable

Automated Steps: 
1) Moves the model, by the pivot, to the origin
2) Creates master/offset ctrls centered around the pivot of the model
3) Opens up UI customization window for the new Ctrls
    a) interactive color and radius sliders
    b) text field for name
4) Apply and Close Button
    a) Parent master to offset
    b) Place model in a group as a level of abstraction (in case the model ever changes)
    c) Parent constrains the group to the offset Ctrl
'''
import math
import pymel.core as pm


class CT_Prop_Rig(object):

    def __init__(self):
        # window name and set up, variables
        self.window = "CT_Window"
        self.title = "Simple Prop Rig"
        self.size = (200, 200)
        # get the first object that's selected
        try:
            self.prop = pm.selected()[0]
        except IndexError:
            raise IndexError(
                'Nothing selected, unsure what to run on. Please select something')

    def createWindow(self):
        # if already window, then delete
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)
        self.window = pm.window(
            self.window,
            title=self.title,
            rtf=True,
            menuBar=False,
        )
        uilayout = pm.columnLayout(adjustableColumn=True, rowSpacing=10)
        self.windowItems(uilayout)
        pm.showWindow()
        pm.window(self.window, e=True, width=200, height=200)

    def windowItems(self, layout):
        prop_transform = self.prop.getTransform()

        # center the prop by the pivot
        pm.move(0, 0, 0, prop_transform, rotatePivotRelative=True)

        bb = pm.exactWorldBoundingBox(prop_transform)
        bb_min_x = bb[0]  # x-min of object in world space
        bb_max_x = bb[3]  # x-max of object in world space
        bb_min_z = bb[2]  # z-min of object in world space
        bb_max_z = bb[5]  # z-max of object in world space

        # default radius = furthest vertex of the prop's projection on xz plane
        def hypot(x, z): return math.sqrt(x*x + z*z)
        radius = max(hypot(bb_min_x, bb_min_z), hypot(bb_min_x, bb_max_z), hypot(
            bb_max_x, bb_min_z), hypot(bb_max_x, bb_max_z))

        self.master = Controller('Master', self.prop, radius + radius * 0.1)
        
        pm.separator(h=10)
        
        self.offset = Controller('Offset', self.prop, radius)
        pm.select(self.offset.ctrl, deselect=True)

        self.applybtn = pm.button(
            label="Apply and Close", command=self.apply_close)

    def apply_close(self, *args):
        self.master.finalize()
        self.offset.finalize()
        # parenting Ctrls
        pm.parent(self.offset.ctrl, self.master.ctrl, s=True, r=True)
        geo_grp_name = pm.group(self.prop, name=self.prop + '_GEO_GRP')
        pm.parentConstraint(self.offset.ctrl, geo_grp_name,
                            maintainOffset=True)
        # delete history of ctrl
        pm.delete(self.master.ctrl, ch=True)
        # closes window
        pm.deleteUI(self.window, window=True)

class Controller(object):
    def __init__(self, purpose, prop, radius):
        self.purpose = purpose
        self.prop = prop
        self.ctrl = pm.circle(
            c=(0, 0, 0), r=radius, name=self.prop+'_'+purpose+'_CTRL')
        pm.rotate(self.ctrl, 90, 0, 0)
        pm.setAttr(self.ctrl[0] + "Shape.overrideEnabled", True)
        pm.setAttr(self.ctrl[0] + "Shape.overrideColor", 4)
        
        self.freeze()
        # UI elements
        self.name = pm.textFieldGrp(
            label=purpose + ' CTRL name:', text=self.prop+'_'+purpose+'_CTRL')
        self.color = pm.colorIndexSliderGrp(
            label='Color:', minValue=5, maxValue=20, dragCommand=self.drag_color)
        self.radius = pm.floatSliderGrp(
            label='Radius:', minValue=radius, maxValue=radius*3.0, dragCommand=self.drag_radius)

    # final touches
    def finalize(self, *args):
        pm.rename(self.ctrl[0], self.name.getText())
        self.freeze()

    # freeze transformations
    def freeze(self):
        pm.makeIdentity(self.ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)

    # interactive effects
    def drag_radius(self, *args):
        pm.circle(self.ctrl, edit=True,
                  radius=self.radius.getValue())

    def drag_color(self):
        pm.setAttr(self.ctrl[0] + "Shape.overrideEnabled", True)
        pm.setAttr(
            self.ctrl[0] + "Shape.overrideColor", self.color.getValue())


propRig = CT_Prop_Rig()
propRig.createWindow()
