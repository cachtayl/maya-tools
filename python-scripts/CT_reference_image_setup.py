'''
Created September 2022
@author- camtaylor1999@gmail.com

Reference Image Generator- a script that will setup your reference images in less steps
https://github.com/cachtayl/maya-tools

Usage:  Execute the script and finalize your preferences in the pop-up window
Output: Free image planes with front and side profiles
        Layers for these image planes

Future GUI Ideas:
- Dropdown menu for measurement unit
- Specify how many alignment planes you want to use
- Scale and Alignment sliders for the image planes
- Naming text fields

Automated Steps:


'''
import math
import pymel.core as pm


class CT_Prop_Rig(object):

    def __init__(self):
        # window name and set up, variables
        self.window = "CT_Window"
        self.title = "Reference Images Generator"
        self.size = (200, 200)
        # get the first object that's selected
        try:
            self.prop = pm.selected()[0]
        except IndexError:
            raise IndexError(
                'Nothing selected, unsure what to run on. Please select something')

    def createWindow(self):
        # delete existing windows
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

        # intialize CTRLS

        self.master_ctrl = pm.circle(
            c=(0, 0, 0), r=radius + radius * 0.1, name=self.prop+'_master_CTRL')
        pm.rotate(self.master_ctrl, 90, 0, 0)
        pm.setAttr(self.master_ctrl[0] + "Shape.overrideEnabled", True)
        pm.setAttr(self.master_ctrl[0] + "Shape.overrideColor", 4)

        self.offset_ctrl = pm.circle(
            c=(0, 0, 0), r=radius, name=self.prop+'_offset_CTRL')
        pm.rotate(self.offset_ctrl, 90, 0, 0)
        pm.setAttr(self.offset_ctrl[0] + "Shape.overrideEnabled", True)
        pm.setAttr(self.offset_ctrl[0] + "Shape.overrideColor", 4)

        # deselect the circle so the user can see the color change interactively
        pm.select(self.offset_ctrl, deselect=True)

        # freeze transformations
        pm.makeIdentity(self.master_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)
        pm.makeIdentity(self.offset_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)

        # UI elements
        self.master_name = pm.textFieldGrp(
            label='Master CTRL Name:', text=self.prop+'_master_CTRL', parent=layout)
        self.master_color = pm.colorIndexSliderGrp(
            label='Color:', minValue=5, maxValue=20, dragCommand=self.master_drag_color, parent=layout)
        self.master_radius = pm.floatSliderGrp(
            label='Radius:', minValue=radius + radius*0.10, maxValue=radius*3.0, dragCommand=self.master_drag_radius, parent=layout)

        pm.separator(h=10)

        self.offset_name = pm.textFieldGrp(
            label='Offset CTRL Name:', text=self.prop+'_offset_CTRL', parent=layout)
        self.offset_color = pm.colorIndexSliderGrp(
            label='Color:', minValue=5, maxValue=20, dragCommand=self.offset_drag_color, parent=layout)
        self.offset_radius = pm.floatSliderGrp(
            label='Radius:', minValue=radius, maxValue=radius*3.0, dragCommand=self.offset_drag_radius, parent=layout)

        self.applybtn = pm.button(
            label="Apply and Close", command=self.apply_close)

    def apply_close(self, *args):
        # holds transform node
        master_name = self.master_name.getText()
        offset_name = self.offset_name.getText()

        pm.rename(self.master_ctrl[0], master_name)
        pm.rename(self.offset_ctrl[0], offset_name)

        # freeze transformations
        pm.makeIdentity(self.master_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)
        pm.makeIdentity(self.offset_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)

        # parenting Ctrls
        pm.parent(offset_name, master_name, s=True, r=True)
        geo_grp_name = pm.group(self.prop, name=self.prop + '_GEO_GRP')
        pm.parentConstraint(self.offset_ctrl, geo_grp_name,
                            maintainOffset=True)
        # delete history of ctrl
        pm.delete(self.master_ctrl, ch=True)
        # closes window
        pm.deleteUI(self.window, window=True)

    # interactive effects
    def master_drag_radius(self, *args):
        pm.circle(self.master_ctrl, edit=True,
                  radius=self.master_radius.getValue())

    def offset_drag_radius(self, *args):
        pm.circle(self.offset_ctrl, edit=True,
                  radius=self.offset_radius.getValue())

    def master_drag_color(self):
        pm.setAttr(self.master_ctrl[0] + "Shape.overrideEnabled", True)
        pm.setAttr(
            self.master_ctrl[0] + "Shape.overrideColor", self.master_color.getValue())

    def offset_drag_color(self):
        pm.setAttr(self.offset_ctrl[0] + "Shape.overrideEnabled", True)
        pm.setAttr(
            self.offset_ctrl[0] + "Shape.overrideColor", self.offset_color.getValue())


propRig = CT_Prop_Rig()
propRig.createWindow()
