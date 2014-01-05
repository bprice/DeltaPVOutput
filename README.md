DeltaPVOutput optimised for  WebSolarLog www.websolarlog.com
=============

A python scripts to use RS485 Serial from Delta Inverter to PVOutput.org. It is will work with multiple delta inverters  and is compatible with WebSolarLog (http://www.websolarlog.com/)

DeltaInverter Module has two major functions:
Generation of Command Strings to be sent over RS485 to the inverter

Parsing of response strings received from the inverter, this is done in two forms:
1) Obtain the raw values using getValueFromResponse
2) Obtain a formatted response using getFormattedResponse which will contain the instruction/value/unit tuple

A list of instructions known is also in the module, obtained from https://code.google.com/p/pvbeancounter/issues/detail?id=251

DeltaPVOutput - simply queries the inverter and posts the result to PVOutput.org with no arguments.

You will need to insert your:
•	PvOutput systemID
•	PvOutout API Key 
•	Serial port eg /dev/ttyUSB0
•	Port speed eg 19200
•	Inverter Number eg 1

in config.ini to work without arguments. If you have multiple inverters simply create a second system configuration.  Eg

[Inverter1]
SystemID: 00000
APIKey: 0000000000000000000000000000000000000000
Port: /dev/ttyUSB0
PortSpeed: 19200
InvNo: 1

[Inverter2]
SystemID: 00000
APIKey: 0000000000000000000000000000000000000000
Port: /dev/ttyUSB0
PortSpeed: 19200
InvNo: 2 


 This example layout can be found in config.ini.example
Run via crontab to poll periodically

WebSolarLog
=============

This allows WebSolarLog to run DeltaPvOutput

1) Follow instructions installing WebSolarLog (http://www.websolarlog.com/index.php/installation-manual-for-websolarlog/)
2) change to WebSolarLog installation directory (eg /usr/share/nginx/www/websolarlog)

3) change to the devices directory (eg ./classes/devices)

4)clone  DeltaPVOutput into DeltaSoliviaPy directory (eg git clone https://github.com/bprice/DeltaPVOutput.git DeltaSoliviaPy)



