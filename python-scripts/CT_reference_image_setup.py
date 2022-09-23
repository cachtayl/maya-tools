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
        self.front = ImagePlane('Front')
        pm.separator(h=10)
        self.side = ImagePlane('Side')

        self.applybtn = pm.button(
            label="Apply and Close", command=self.apply_close)

    def apply_close(self, *args):
        try:
            # grp the imgs
            self.grp_ref = pm.group(
                self.front.plane, self.side.plane, name='references')
            # make Reference Layer
            pm.select(self.grp_ref)
            self.layer_ref = pm.createDisplayLayer(name='ref_pics')
            pm.setAttr(self.layer_ref+'.displayType', 2)
            # closes window
            pm.deleteUI(self.window, window=True)
        except:
            raise Exception('Must import front and side reference images.')

    def overridePanelLayout(self):
        # Creates a Three Panes Bottom Split panel layout that is optimized for aligning the reference images
        pm.panelConfiguration(
            label="CT Ref Img Panel Layout",
            sceneConfig=True,
            configString="paneLayout -e -cn \"bottom3\" -ps 1 100 50 -ps 2 50 50 -ps 3 50 50 $gMainPane;",
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
            label='Horizontal Offset:', dragCommand=self.drag_horiz, minValue=-10.0, maxValue=10.0, enable=False)
        self.offset_vert = pm.floatSliderGrp(
            label='Vertical Offset:', dragCommand=self.drag_vert, minValue=-10.0, maxValue=10.0, enable=False)
        self.scale = pm.floatSliderGrp(
            label='Scale:', dragCommand=self.drag_scale, minValue=-5.0, maxValue=5.0, enable=False)

    def generate_image(self, *args):
        # only works for Windows File Explorer for now *Later* check os at runtime and then change dialogStyle
        self.path = pm.fileDialog2(fileMode=1, dialogStyle=1)
        pm.textFieldButtonGrp(self.browser, edit=True, text=self.path[0])
        # overwrite plane
        if self.plane != '':
            pm.delete(self.plane)
        self.plane = pm.imagePlane(
            name=self.view + '_Reference', fileName=self.path[0])
        pm.floatSliderGrp(self.offset_horiz, edit=True, enable=True)
        pm.floatSliderGrp(self.offset_vert, edit=True, enable=True)
        pm.floatSliderGrp(self.scale, edit=True, enable=True)
        if self.view == 'Side':
            pm.rotate(self.plane, 90, y=True)
    
    def drag_scale(self, *args):
        pm.scale( self.plane, self.scale.getValue(),self.scale.getValue(), self.scale.getValue(), xyz=True)
        
    def drag_horiz(self, *args):
        if self.view == 'Front':
            pm.move(self.offset_horiz.getValue(), self.plane, x=True)
        else:
            pm.move(self.offset_horiz.getValue(), self.plane, z=True)

    def drag_vert(self, *args):
        pm.move(self.offset_vert.getValue(), self.plane, y=True)


ref_imgs = Ref_gui()
ref_imgs.createWindow()
