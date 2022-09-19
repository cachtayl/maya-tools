<p></p>
<div>
    <h1> Scripts </h1>
    <h3><b>Tools:</b></h3>
    <ul>
        <li><a href="#-ct-prop-rig-generator">CT Simple Prop Rig</a></li>
    </ul>
</div>
<div>
    <!-- CT Prop Rig Generator -->
    <h1> CT Prop Rig Generator</h1>
    <img src="./media/ct_ui_prop_rig_generator.JPG" alt="CT Prop Rig Generator GUI">
    <p>This script generates the industry standard's prop rig for you<br>Helpful for artists who want to skip the repetitive task 
    of making your model <b>production ready</b>, which includes master/offset controllers, parenting hierarchy, and coloring/naming.</p>
    <p><b>How to use it:</b>
    <br>1. Select the model you want to rig
    <br>2. Run Script
    <br>3. Customize your controllers in the pop-up window
    <br>4. Click on the "Apply and Close" button when done with customization</p>
    <p><b>Master CTRL Name: </b><br>Text field to name the master controller. Will execute after clicking "Apply and Close"</p>
    <p><b>Color: </b><br>Color index slider to interactively change the color of the controller</p>
    <p><b>Radius: </b><br>Float slider to interactively change the radius of the controller</p>
    <p><b>Offset CTRL Name: </b><br>Text field to name the offset controller. Will execute after clicking "Apply and Close"</p>
    <p><b>"Apply and Close" button: </b>
    <br>a) Makes the master controller parent of offset
    <br>b) Places model in a "geo" group, as a level of abstraction (in case the model ever changes)
    <br>c) Makes the offset controller parent of the "geo" group </p>
    <br>
</div>