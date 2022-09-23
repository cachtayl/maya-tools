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
- Scale sliders for the image planes
- Naming text fields

Automated Steps:
'''

import maya.mel
import pymel.core as pm


class Ref_gui(object):

    def __init__(self):
        # window name and set up, variables
        self.window = "CT_Window"
        self.title = "Reference Images Generator"
        self.size = (200, 20)
        self.overridePanelLayout()

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
        pm.window(self.window, e=True, width=200, height=1)

    def windowItems(self, layout):
        # UI elements
        front = ImagePlane('Front')
        pm.separator(h=10)
        side = ImagePlane('Side')

    def overridePanelLayout(self):
        # Creates a Three Panes Bottom Split panel layout that is optimized for aligning the reference images
        pm.panelConfiguration(
            label="CT Ref Img Panel Layout",
            sceneConfig=True,
            configString="paneLayout -e -cn \"bottom3\" -ps 1 100 35 -ps 2 50 65 -ps 3 50 65 $gMainPane;",
            addPanel=[
                (False,
                         "Persp View",
                         "modelPanel",
                         ("{global int $gUseMenusInPanels;\
                        modelPanel -mbv $gUseMenusInPanels\
                        -unParent -l \"Persp View\" -cam persp;}"),
                         "modelPanel -edit -l \"Persp View\"  -cam \"persp\" $panelName"),
                (False,
                 "Side View",
                 "modelPanel",
                 ("{global int $gUseMenusInPanels;\
                        modelPanel -mbv $gUseMenusInPanels\
                        -unParent -l \"Side View\" -cam side;}"),
                 "modelPanel -edit -l \"Side View\"  -cam \"side\" $panelName"),
                (False,
                 "Front View",
                 "modelPanel",
                 ("{global int $gUseMenusInPanels;\
                        modelPanel -mbv $gUseMenusInPanels\
                        -unParent -l \"Front View\" -cam front;}"),
                 "modelPanel -edit -l \"Front View\"  -cam \"front\" $panelName")
            ]
        )
        maya.mel.eval('setNamedPanelLayout( "CT Ref Img Panel Layout" )')


class ImagePlane(object):
    def __init__(self, view):
        self.view = view
        self.plane = ''
        self.browser = pm.textFieldButtonGrp(
            label=view + ' Image Path: ',
            editable=False,
            buttonLabel='Browse',
            buttonCommand=self.generate_image)
        self.offset_horiz = pm.floatSliderGrp(
            label='Horizontal Offset:', dragCommand=self.drag_horiz, minValue=-5.0, maxValue=5.0, visible=False)
        self.offset_vert = pm.floatSliderGrp(
            label='Vertical Offset:', dragCommand=self.drag_vert, minValue=-5.0, maxValue=5.0, visible=False)

    def generate_image(self, *args):
        # only works for Windows File Explorer for now *Later* check os at runtime and then change dialogStyle
        self.path = pm.fileDialog2(fileMode=1, dialogStyle=1)
        pm.textFieldButtonGrp(self.browser, edit=True, text=self.path[0])
        # overwrite plane
        if self.plane != '':
            pm.delete(self.plane)
        self.plane = pm.imagePlane(
            name=self.view + '_Reference', fileName=self.path[0])
        pm.floatSliderGrp(self.offset_horiz, edit=True, visible=True)
        pm.floatSliderGrp(self.offset_vert, edit=True, visible=True)
        if self.view == 'Side':
            pm.rotate(self.plane, 90, y=True)

    def drag_horiz(self, *args):
        if self.view == 'Front':
            pm.move(self.offset_horiz.getValue(), self.plane, x=True)
        else:
            pm.move(self.offset_horiz.getValue(), self.plane, z=True)

    def drag_vert(self, *args):
        pm.move(self.offset_vert.getValue(), self.plane, y=True)


ref_imgs = Ref_gui()
ref_imgs.createWindow()
