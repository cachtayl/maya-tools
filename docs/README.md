<p></p>
<div>
    <h1> Scripts </h1>
    <h3><b>Tools:</b></h3>
    <ul>
        <li><a href="#-ct-prop-rig-generator">CT Simple Prop Rig</a></li>
        <li><a href="#-ct-reference-images-setup">CT Reference Images</a></li>
    </ul>
</div>
<div>
    <!-- CT Prop Rig Generator -->
    <h1> CT Prop Rig Generator</h1>
    <img src="./media/ct_ui_prop_rig_generator.JPG" alt="CT Prop Rig Generator GUI">
    <p>This script generates the industry standard's prop rig for you<br>Helpful for artists who want to skip the repetitive task 
    of making your model <b>production ready</b>, which includes master/offset controllers, parenting hierarchy, and coloring/naming.</p>
    <p><b>Important Note: </b> The controllers are centered around your prop's pivot point</p>
    <p><b>How to use it:</b>
    <br>1. Select the model you want to rig
    <br>2. Make sure the model's pivot point is placed where you want the controllers to be centered
    <br>3. Run Script
    <br>4. Customize your controllers in the pop-up window
    <br>5. Click on the "Apply and Close" button when done with customization</p>
    <p><b>Master CTRL Name: </b><br>Text field to name the master controller. Will execute after clicking "Apply and Close"</p>
    <p><b>Color: </b><br>Color index slider to interactively change the color of the controller</p>
    <p><b>Radius: </b><br>Float slider to interactively change the radius of the controller</p>
    <p><b>Offset CTRL Name: </b><br>Text field to name the offset controller. Will execute after clicking "Apply and Close"</p>
    <p><b>"Apply and Close" button: </b>
    <br>a) Makes the master controller parent of offset
    <br>b) Places model in a "geo" group, as a level of abstraction (in case the model ever changes)
    <br>c) Makes the offset controller parent of the "geo" group </p>
    <br>
    <!-- CT Reference Images Setup -->
    <h1> CT Reference Images Setup</h1>
    <img src="./media/ct_ui_reference_images_generator.JPG" alt="CT Reference Images GUI">
    <p>This script generates an interface that will simplify your reference image setup to a few clicks. <br>Helpful for Maya artists who want to quickly setup their reference images and make them aligned, grouped, and in a reference layer.</p>
    <p><b>Important Note:</b> Currently only available for Windows.</p>
    <p><b>How to use it:</b>
    <br>1. Run Script
    <br>2. Choose your Front and Side reference images(jpg or png)
    <br>3. Adjust the images with the sliders to make them aligned where you want them
    <br>4. Click "Apply and Close"</p>
    <p><b>Image Path: </b><br>By pressing the "Browse" button you will be able to select an .jpg or .png file from your File Explorer.</p>
    <p><b>Horizontal Offset: </b><br>Slider that interactively offsets the image horizontally</p>
    <p><b>Vertical Offset: </b><br>Slider that interactively offsets the image vertically</p>
    <p><b>Scale: </b><br>Slider that interactively scales the image in all dimensions</p>
    <p><b>"Apply and Close" button: </b>
    <br>a) Groups the image planes into <code>references</code>
    <br>b) Creates a Reference Layer for the group</p>
    <br>
</div>