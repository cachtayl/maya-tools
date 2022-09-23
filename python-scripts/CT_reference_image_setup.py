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

import maya.mel
import pymel.core as pm

class CT_Ref_Img_Setup(object):

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
        self.front_img_plane = ''
        self.front_img_browser = pm.textFieldButtonGrp(
            label='Front Image Path: ',
            editable=False,
            buttonLabel = 'Browse',
            buttonCommand=self.generate_front_image)
        self.front_offset_x = pm.floatSliderGrp(
            label='Offset X:', dragCommand=self.front_offset_drag_x, minValue=-5.0, maxValue=5.0, visible = False, parent=layout)
        self.front_offset_y = pm.floatSliderGrp(
            label='Offset Y:', dragCommand=self.front_offset_drag_y, minValue=-5.0, maxValue=5.0,visible = False, parent=layout)
        self.side_img_plane = ''
        self.side_img_browser = pm.textFieldButtonGrp(
            label='Side Image Path: ',
            editable=False,
            buttonLabel = 'Browse',
            buttonCommand=self.generate_side_image)
        self.side_offset_x = pm.floatSliderGrp(
            label='Offset X:', dragCommand=self.side_offset_drag_x, minValue=-5.0, maxValue=5.0, visible = False, parent=layout)
        self.side_offset_y = pm.floatSliderGrp(
            label='Offset Y:', dragCommand=self.side_offset_drag_y, minValue=-5.0, maxValue=5.0, visible = False, parent=layout)
        pm.separator(h=3)
    def generate_front_image(self, *args):
        # Only works for Windows File Explorer for now
        # Later: check os at runtime and then change dialogStyle
        self.front_img_path = pm.fileDialog2(fileMode = 1, dialogStyle = 1)
        pm.textFieldButtonGrp(self.front_img_browser, edit = True, text=self.front_img_path[0])
        #delete existing front planes
        if self.front_img_plane != '':
            pm.delete(self.front_img_plane)
        self.front_img_plane = pm.imagePlane(name = 'front', fileName = self.front_img_path[0])
        pm.floatSliderGrp(self.front_offset_x, edit=True, visible=True)
        pm.floatSliderGrp(self.front_offset_y, edit=True, visible=True)
    
    def generate_side_image(self, *args):
        # Only works for Windows File Explorer for now
        # Later: check os at runtime and then change dialogStyle
        self.side_img_path = pm.fileDialog2(fileMode = 1, dialogStyle = 1)
        pm.textFieldButtonGrp(self.side_img_browser, edit = True, text=self.side_img_path[0])
        #delete existing side planes
        if self.side_img_plane != '':
            pm.delete(self.side_img_plane)
        self.side_img_plane = pm.imagePlane(name = 'side', fileName = self.side_img_path[0])
        pm.floatSliderGrp(self.side_offset_x, edit=True, visible=True)
        pm.floatSliderGrp(self.side_offset_y, edit=True, visible=True)
        pm.rotate(self.side_img_plane, 0, 90, 0)
    
    # interactive effects
    def front_offset_drag_x(self, *args):
        pm.move(self.front_offset_x.getValue(), self.front_img_plane, x=True)
    def front_offset_drag_y(self, *args):
        pm.move(self.front_offset_y.getValue(), self.front_img_plane, y=True)

    def side_offset_drag_x(self, *args):
        pm.move(self.side_offset_x.getValue(), self.side_img_plane, x=True)

    def side_offset_drag_y(self, *args):
        pm.move(self.side_offset_y.getValue(), self.side_img_plane, y=True)
    def overridePanelLayout(self):
        #Creates a Three Panes Bottom Split panel layout that is optimized for aligning the reference images
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
                        -unParent -l \"Persp View\" -cam persp;}" ),
                        "modelPanel -edit -l \"Persp View\"  -cam \"persp\" $panelName"),
                        (False,
                        "Side View",
                        "modelPanel",
                        ("{global int $gUseMenusInPanels;\
                        modelPanel -mbv $gUseMenusInPanels\
                        -unParent -l \"Side View\" -cam side;}" ),
                        "modelPanel -edit -l \"Side View\"  -cam \"side\" $panelName"),
                        (False,
                        "Front View",
                        "modelPanel",
                        ("{global int $gUseMenusInPanels;\
                        modelPanel -mbv $gUseMenusInPanels\
                        -unParent -l \"Front View\" -cam front;}" ),
                        "modelPanel -edit -l \"Front View\"  -cam \"front\" $panelName")
                ]
        )
        maya.mel.eval('setNamedPanelLayout( "CT Ref Img Panel Layout" )')

ref_imgs = CT_Ref_Img_Setup()
ref_imgs.createWindow()
