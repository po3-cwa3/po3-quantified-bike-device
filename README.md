po3-quantified-bike
===================
<h2>Code structure</h2>
<p>This repository contains the code used for the device of the BOSS - Bike Of StatS. The folder 'arduino' contains the sketches that have to be installed on the Arduino controller. The folder 'raspberry' contains the code that should be installed on the Raspberry Pi. More information can be found in the README.md files in those folers.</p>
<h2>User manual</h2>
<p>When using the device, it is important to know the meaning of the LEDs and the functions of the buttons.
On the prototype, these are indicated with paper labels:</p>
<ul>
<li>Button "Take Picture": When pressed during an active trip, a picture is taken (Picture LED should be blue) and send to either the remote server or the local filesystem. When finished, the Picture LED should be green for some time.
<li>Button "Live/Batch": Toggle wether the data should be sent directly to the remote server or stored in the local database.
<li>Button "Batch upload": When pressed (if an active internet connection is available), all data stored in the local MySQL database is sent to the remote server and removed from the local filesystem.
<li>Button "Start Trip" (this is the only blue button, attached to the breadboard, this button should be pressed twice for every action): When pressed (twice), it starts or stops a trip (The "Trip LED" indicates wether a trip is active or not).
<li>LED "Active Trip": Red if a trip is active. Off if no trip is active.
<li>LED "Picture": Blue if a picture is being taken. Green if taking a picture and storing it succeeded. Red if taking the picture or storing it failed. Off if no picture action is taking place.
<li>LED "Batch upload": Blue if a batch upload is going on. Green if the batch upload succeeded. Red if the batch upload failed. Off if no batch upload is taking place.
<li>LED "Connection": Green if an internet connection is available (needed for batch uploads and live trips). Off if no internet connection is available.
<li>LED "Live/Batch": Red if new trips will be started in live mode. Off if new trips will be started in batch mode (all data will be collected on the device and sent to the remote server using the batch upload button).
</ul>
<p>The GPS module will show a LED blinking every ~2 s when the position cannot be determined correctly. When the LED is only blinking every ~15 s, the GPS module has a fix and will send coordinates to the device.</p>
<p>When booting the device, it will take the Raspberry Pi a few seconds to start the application.</p>

