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
        #adding labels and text fields
        #textfieldgrp
        self.master_name = pm.textFieldGrp(label='Master CTRL Name:',text=self.prop+'_master_CTRL', parent=layout)
        self.master_color = pm.colorIndexSliderGrp(label='Color:',minValue=5, maxValue=20, value= 14, parent=layout)
        pm.separator(h = 10)
        self.offset_name = pm.textFieldGrp(label='Offset CTRL Name:', text=self.prop+'_offset_CTRL', parent=layout)
        self.offset_color = pm.colorIndexSliderGrp(label='Color:', minValue=5, maxValue=20, value= 16, parent=layout)
        
        self.applybtn = pm.button(label="Apply and Close",command=self.ct_Rigging)

    def ct_Rigging(self, *args):
        # holds transform node
        master_name = self.master_name.getText()
        master_color = self.master_color.getValue() - 1
        offset_name = self.offset_name.getText()
        offset_color = self.offset_color.getValue() - 1
        
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

        # Create the CTRLS with radius bigger than the boundingBox

        master_ctrl = pm.circle(c=(0,0,0), r=radius +
                                radius * 0.5, name=master_name)
        pm.rotate(master_ctrl, 90, 0, 0)
        #freeze transformations
        pm.makeIdentity(master_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)
        pm.setAttr(master_name + "Shape.overrideEnabled", True)
        pm.setAttr(master_name + "Shape.overrideColor", master_color)

        offset_ctrl = pm.circle(c=(0,0,0), r=radius +
                                radius * 0.3, name=offset_name)
        pm.rotate(offset_ctrl, 90, 0, 0)
        #freeze transformations
        pm.makeIdentity(offset_ctrl[0], apply=True,
                        scale=True, translate=True, rotate=True)
        pm.setAttr(offset_name + "Shape.overrideEnabled", True)
        pm.setAttr(offset_name + "Shape.overrideColor", offset_color)


        # Parenting Ctrls
        pm.parent(offset_ctrl, master_ctrl, s=True, r=True)
        geo_grp_name = pm.group(self.prop, name= self.prop + '_GEO_GRP')
        pm.parentConstraint(offset_ctrl, geo_grp_name, maintainOffset = True)
        #delete history of ctrl
        pm.delete(master_ctrl, ch=True)
        #closes window
        pm.deleteUI(self.window, window = True)


propRig= CT_PropRig()
propRig.createWindow()
