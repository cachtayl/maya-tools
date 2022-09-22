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
import pymel.core as pm
class CT_Ref_Img_Setup(object):

    def __init__(self):
        # window name and set up, variables
        self.window = "CT_Window"
        self.title = "Reference Images Generator"
        self.size = (200, 200)

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
        # UI elements
        self.front_name = pm.textFieldGrp(
            label='Front Ref Image Name:', text='front_', parent=layout)
        self.front_offset_x = pm.floatSliderGrp(
            label='Offset X:', dragCommand=self.front_offset_drag_x, parent=layout)
        self.front_offset_y = pm.floatSliderGrp(
            label='Offset Y:', dragCommand=self.front_offset_drag_y, parent=layout)
        self.front_img_browser = pm.textFieldButtonGrp(
            label='Image Name: ',
            editable=False,
            buttonLabel = 'Browse',
            buttonCommand=self.generate_front_image)
        pm.separator(h=10)
        
        self.side_name = pm.textFieldGrp(
            label='Side Ref Image Name:', text='side_', parent=layout)
        self.side_offset_x = pm.floatSliderGrp(
            label='Offset X:', dragCommand=self.side_offset_drag_x, parent=layout)
        self.side_offset_y = pm.floatSliderGrp(
            label='Offset Y:', dragCommand=self.side_offset_drag_y, parent=layout)
        #only works for Windows for now(Later: check os at runtime and then change dialogStyle)
        # self.side_img_path = pm.fileDialog2(fileMode = 1, dialogStyle = 1)
        # self.side_img_plane = pm.imagePlane(fileName = self.side_img_path[0])
        # pm.rotate(self.side_img_plane, 0, 90, 0)

        self.applybtn = pm.button(
            label="Apply and Close", command=self.apply_close)
    def generate_front_image(self, *args):
        # Only works for Windows File Explorer for now
        #(Later: check os at runtime and then change dialogStyle)
        self.front_img_path = pm.fileDialog2(fileMode = 1, dialogStyle = 1)
        self.front_img_plane = pm.imagePlane( fileName = self.front_img_path[0])
        self.front_img_browser = pm.textFieldButtonGrp(edit =True, text=self.front_img_path[0])
    def apply_close(self, *args):
        # holds transform node
        front_name = self.front_name.getText()
        side_name = self.side_name.getText()

        pm.imagePlane(self.front_img_plane, e=True, name=front_name)
        pm.imagePlane(self.side_img_plane, e=True, name=side_name)

        # closes window
        pm.deleteUI(self.window, window=True)

    # interactive effects
    def front_offset_drag_x(self, *args):
        pass
    def front_offset_drag_y(self, *args):
        pass

    def side_offset_drag_x(self):
        pass

    def side_offset_drag_y(self):
        pass

ref_imgs = CT_Ref_Img_Setup()
ref_imgs.createWindow()
