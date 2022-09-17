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

Note: Will center your prop to the origin, the center of the ctrls will be the pivot point of your prop

'''
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
                              menuBar=False)
        uilayout= pm.columnLayout( adjustableColumn=True, rowSpacing=10)
        self.windowItems(uilayout)
        pm.showWindow()
   
    def windowItems(self,layout):
        #adding labels and text fields
        #textfieldgrp
        self.master_name = pm.textFieldGrp(label='Master CTRL Name:',placeholderText=self.prop+'_master_CTRL', parent=layout)
        self.master_color = pm.colorIndexSliderGrp(label='Color:',minValue=14, maxValue=20, parent=layout)
        self.offset_name = pm.textFieldGrp(label='Offset CTRL Name:', placeholderText=self.prop+'_offset_CTRL', parent=layout)
        self.offset_color = pm.colorIndexSliderGrp(label='Color:', minValue=14, maxValue=20, parent=layout)
        # pm.button(label="Apply",command=partial(self.ct_Rigging, master_name, master_color, offset_name, offset_color))
        self.applybtn = pm.button(label="Apply",command=self.ct_Rigging)

    def ct_Rigging(self, *args):
        # holds transform node
        master_name = self.master_name.getText()
        master_color = self.master_color.getValue()
        offset_name = self.offset_name.getText()
        offset_color = self.offset_color.getValue()
        
        prop_transform = self.prop.getTransform()  
        # center the prop by the pivot
        pm.move(0, 0, 0, prop_transform, rotatePivotRelative=True)

        # Grab pivot in worldSpace
        # Assume the mesh's rotate pivot = scale pivot
        # pivot = prop.getPivots(worldSpace=True)[0]

        bb = pm.exactWorldBoundingBox(prop_transform)
        bb_min_x = bb[0]  # x-min of object in world space
        bb_max_x = bb[3]  # x-max of object in world space

        radius = max(bb_max_x, abs(bb_min_x))

        # Create the CTRLS with radius bigger than the boundingBox

        master_ctrl = pm.circle(c=(0, 0, 0), r=radius +
                                radius * 0.5, name=master_name)
        pm.rotate(master_ctrl, 90, 0, 0)
        pm.makeIdentity(master_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)

        offset_ctrl = pm.circle(c=(0, 0, 0), r=radius +
                                radius * 0.3, name=offset_name)
        pm.rotate(offset_ctrl, 90, 0, 0)
        pm.makeIdentity(offset_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)

        # Basic parenting Hierarchy
        pm.parent(offset_ctrl, master_ctrl, s=True, r=True)
        geo_grp_name = pm.group(self.prop, name= self.prop + '_GEO_GRP')
        pm.parentConstraint(offset_ctrl, geo_grp_name)

propRig= CT_PropRig()
propRig.createWindow()
