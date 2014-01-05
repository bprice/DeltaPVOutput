DeltaPVOutput for WebSolarLog www.websolarlog.com
=============

A series of python scripts to use RS485 Serial from Delta Inverter to PVOutput.org and compatable with WebSolarLog 

DeltaInverter Module has two major functions:
Generation of Command Strings to be sent over RS485 to the inverter

Parsing of response strings received from the inverter, this is done in two forms:
1) Obtain the raw values using getValueFromResponse 
2) Obtain a formatted response using getFormattedResponse which will contain the instruction/value/unit tuple

A list of instructions known is also in the module, obtained from https://code.google.com/p/pvbeancounter/issues/detail?id=251 

DeltaPVOutput - simply queries the inverter and posts the result to PVOutput.org with no arguments.

You will need to insert your systemID and API Key naturally in config.ini to work without arguments. An example layout can be found in config.ini.example

Run via crontab to poll periodically

WebSolarLog 
=============

This allows WebSolarLog to run DeltaPvOutput

1) cd to WebSolarLog (/usr/share/nginx/www/websolarlog)
2) cd to devices (./classes/devices)
3) git clone https://github.com/bprice/DeltaPVOutput.git DeltaSoliviaPy


