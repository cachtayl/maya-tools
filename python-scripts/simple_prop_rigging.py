'''
Created September 2022
@author- camtaylor1999@gmail.com

Simple Prop Rig - a script that does conventional prop rigging for you
https://github.com/cachtayl/maya-tools

Future GUI:
Window with help menu option that opens doc in github
checkbox = center the prop/leave in current place
float slider that changes the size of master ctrl
float slider that changes the size of offset ctrl(max = mastr radius)
color picker for ctrls

Usage:  Select object in scene and execute this script
Output: Master and Offset controllers parented to a group holding the prop

Note: 
1) Moves prop to the origin
2) Ctrls will be centered around the pivot of the prop

'''
from cgitb import text
from doctest import master
import pymel.core as pm
from functools import partial

class CT_PropRig(object):

    def __init__(self):
        #window name and set up, variables
        self.window="CT_Window"
        self.title="Simple Prop Rig"
        self.size=(400,400)
        # get the first object that's selected
        try:
            self.prop = pm.selected()[0]
        except IndexError:
            raise IndexError(
                'Nothing selected, unsure what to run on. Please select something')
        
    def createWindow(self):
        #if already window, then delete
        if pm.window(self.window,exists=True):
            pm.deleteUI(self.window,window=True)
        self.window=pm.window(
                              self.window,
                              title=self.title,
                              widthHeight = self.size,
                              menuBar=False,
                              )
        uilayout= pm.columnLayout( adjustableColumn=True, rowSpacing=10)
        self.windowItems(uilayout)
        pm.showWindow()
   
    def windowItems(self,layout):
        prop_transform = self.prop.getTransform()

        # Grab pivot in worldSpace
        # Assume the mesh's rotate pivot = scale pivot
        pivot = self.prop.getPivots(worldSpace=True)[0]
        print(pivot)
        # center the prop by the pivot
        pm.move(0, 0, 0, prop_transform, rotatePivotRelative=True)

        bb = pm.exactWorldBoundingBox(prop_transform)
        bb_min_x = bb[0]  # x-min of object in world space
        bb_max_x = bb[3]  # x-max of object in world space

        radius = max(bb_max_x, abs(bb_min_x))

        # Intialize CTRLS

        self.master_ctrl = pm.circle(c=(0,0,0), r=radius + radius * 0.5, name=self.prop+'_master_CTRL')
        pm.rotate(self.master_ctrl, 90, 0, 0)
        pm.setAttr(self.master_ctrl[0] + "Shape.overrideEnabled", True)
        pm.setAttr(self.master_ctrl[0] + "Shape.overrideColor", 4)

        self.offset_ctrl = pm.circle(c=(0,0,0), r=radius + radius * 0.3, name=self.prop+'_offset_CTRL')
        pm.rotate(self.offset_ctrl, 90, 0, 0)
        pm.setAttr(self.offset_ctrl[0] + "Shape.overrideEnabled", True)
        pm.setAttr(self.offset_ctrl[0] + "Shape.overrideColor", 4)

        #freeze transformations
        pm.makeIdentity(self.master_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)
        pm.makeIdentity(self.offset_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)

        #UI elements
        self.master_name = pm.textFieldGrp(label='Master CTRL Name:',text=self.prop+'_master_CTRL', parent=layout)
        self.master_color = pm.colorIndexSliderGrp(label='Color:',minValue=5, maxValue=20, dragCommand=self.master_drag_color, parent=layout)
        
        pm.separator(h = 10)
        
        self.offset_name = pm.textFieldGrp(label='Offset CTRL Name:', text=self.prop+'_offset_CTRL', parent=layout)
        self.offset_color = pm.colorIndexSliderGrp(label='Color:', minValue=5, maxValue=20, dragCommand=self.offset_drag_color, parent=layout)
        
        
        self.applybtn = pm.button(label="Apply and Close",command=self.ct_Rigging)
    
    def ct_Rigging(self, *args):
        # holds transform node
        master_name = self.master_name.getText()
        offset_name = self.offset_name.getText()

        pm.rename(self.master_ctrl[0], master_name)
        pm.rename(self.offset_ctrl[0], offset_name)
        
        #freeze transformations
        pm.makeIdentity(self.master_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)
        pm.makeIdentity(self.offset_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)

        # Parenting Ctrls
        pm.parent(offset_name, master_name, s=True, r=True)
        geo_grp_name = pm.group(self.prop, name= self.prop + '_GEO_GRP')
        pm.parentConstraint(self.offset_ctrl, geo_grp_name, maintainOffset = True)
        #delete history of ctrl
        pm.delete(self.master_ctrl, ch=True)
        #closes window
        pm.deleteUI(self.window, window = True)
    
    def master_drag_color(self):
        pm.setAttr(self.master_ctrl[0] + "Shape.overrideEnabled", True)
        pm.setAttr(self.master_ctrl[0] + "Shape.overrideColor", self.master_color.getValue())
    
    def offset_drag_color(self):
        pm.setAttr(self.offset_ctrl[0] + "Shape.overrideEnabled", True)
        pm.setAttr(self.offset_ctrl[0] + "Shape.overrideColor", self.offset_color.getValue())

propRig= CT_PropRig()
propRig.createWindow()
