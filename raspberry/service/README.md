<h1>BOSS - Raspberry Pi application</h1>
<h2>Configuration and installation</h2>
<h3>Packages</h3>
<p>First install the following packages:
<ul>
<li>apt-get install python-mysqldb
<li>pip install socketIO-client
<li>pip install picamera 
<li>pip install httplib2
<li>pip install pyserial
</ul>
</p>
<h3>Local MySQL database</h3>
<p>Then install a mysql-server (apt-get install mysql-server) and create a new database and apply the script in ../database/.</p>
<h3>Configuration</h3>
<p>Create a file config.py based on config.example.py (in the same directory) and update the configuration parameters.</p>
<h3>Start the application on boot</h3>
<p>Add the following lines to the file at /etc/rc.local (as root): 
<ul>
<li>sudo ln -s /dev/serial/by-id/[arduino-id] /dev/arduino1
<li>[absolute path of installation]/raspberry/service/main.py &
</ul>
<h3>Other</h3>
<p>
Also make sure that camera support is enabled on your Raspberry Pi using the raspi-config tool.
</p>
