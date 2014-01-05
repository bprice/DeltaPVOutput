class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def getFloat (connection,inv,string):
    theReturn = float("0")
    cmd = inv.getCmdStringFor(string)
    connection.write(cmd)
    response = connection.read(100)
    value = inv.getValueFromResponse(response)
    if isFloat(value):
       theReturn = float(value)
    return theReturn

def getString(connection,inv,string):
    theReturn = str("")
    cmd = inv.getCmdStringFor(string)
    connection.write(cmd)
    response = connection.read(100)
    value = inv.getValueFromResponse(response)
    theReturn = str(value)
    return theReturn

import time, subprocess,serial,sys,string,ConfigParser
from deltaInv import DeltaInverter
from time import localtime, strftime

if __name__ == '__main__':

    t_commands = ["getalarms","getdata","getlivedata","getinfo","gethistory","synctime"]
    if len(sys.argv)>=4:
    
      t_command = str(sys.argv[1])
      t_port = str(sys.argv[2])
      t_id = int(sys.argv[3])
      
      connection = serial.Serial(t_port,19200,timeout=0.2);
      localtime = time.localtime(time.time())   
 
      t_date = '{0}'.format(strftime('%Y%m%d'))
      t_time = '{0}'.format(strftime('%H:%M:%S'))

      inv1 = DeltaInverter(t_id) #init Inverter

      for case in switch(t_command.lower()):
        if case(t_commands[0]): #getalarms
           print "Fehler -------"
           break
        if case(t_commands[1]): pass #getdata
        if case(t_commands[2]): #getlivedata
           cmd = inv1.getCmdStringFor('DC Volts1')
           connection.write(cmd)
           response = connection.read(100)
           #if no response the inverter is asleep
           if response:
             t_DcVolts1 = float("0")
             value = inv1.getValueFromResponse(response)
             if isFloat(value):
               t_DcVolts1 = float(value)
             t_DcCur1 = getFloat(connection,inv1,'DC Cur1')
             t_DcPow1 = t_DcVolts1*t_DcCur1
             t_DcVolts2 = getFloat(connection,inv1,'DC Volts2')
             t_DcCur2 = getFloat(connection,inv1,'DC Cur2')
             t_DcPow2 = t_DcVolts2*t_DcCur2
             t_AcVolts = getFloat(connection,inv1,'AC Volts')
             t_AcCur = getFloat(connection,inv1,'AC Current')
             t_AcPow = getFloat(connection,inv1,'AC Power')
             t_AcFreq = getFloat(connection,inv1,'AC Freq')
             t_Eff = (t_AcPow/t_DcPow1)*100
             #t_DcTemp = getFloat(connection,inv1,'DC Temp')
             t_AcTemp = getFloat(connection,inv1,'AC Temp')
             t_DcTemp = t_AcTemp
             t_AcTotal = getFloat(connection,inv1,'Day Wh')/1000
             print t_date+"-"+t_time+" %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f OK" %(t_DcVolts1, t_DcCur1, t_DcPow1, t_DcVolts2, t_DcCur2, t_DcPow2, t_AcVolts, t_AcCur, t_AcPow, t_AcFreq, t_Eff, t_DcTemp, t_AcTemp, t_AcTotal )
           else:
             print "No response from inverter - shutdown?"
           break
        if case(t_commands[4]): #gethistory
           cmd = inv1.getCmdStringFor('Day Wh')
           connection.write(cmd)
           response = connection.read(100)
           #if no response the inverter is asleep
           if response:
             t_day = float("0")
             value = inv1.getValueFromResponse(response)
             if isFloat(value):
               t_day = float(value)/1000
             t_week = getFloat(connection,inv1,'Week Wh')
             t_week = t_week/10
             t_month = getFloat(connection,inv1,'Month Wh')
             t_month = t_month/10
             t_year = getFloat(connection,inv1,'Year Wh')
             t_year = t_year/10
             t_total = getFloat(connection,inv1,'Total Wh')
             t_total = t_total/10
             print "Global State:          Run"
             print "Inverter State:        Run"
             print "Channel 1 Dc/Dc State: MPPT"
             print "Alarm State:           No Alarm"
             print ""
             print "Daily Energy               = "+"%.3f"%(t_day)+" kWh"
             print "Weekly Energy              = "+"%.3f"%(t_week)+" kWh"
             print "Monthly Energy             = "+"%.3f"%(t_month)+" kWh"
             print "Yearly Energy              = "+"%.3f"%(t_year)+" kWh"
             print "Total Energy               = "+"%.3f"%(t_total)+" kWh"
             print "Partial Energy             = "+"%.3f"%(t_total)+" kWh"
           else:
             print "No response from inverter - shutdown?"
           break
        if case(t_commands[3]): #getinfo
           cmd = inv1.getCmdStringFor('Part')
           connection.write(cmd)
           response = connection.read(100)
           #if no response the inverter is asleep
           if response:
             value = inv1.getValueFromResponse(response)
             t_Part = str(value)
             t_Serial = getString(connection,inv1,'Serial')
             t_FW = getString(connection,inv1,'FW Version')
             t_Version = getString(connection,inv1,'Inverter Type')

             print "Part Number: " + t_Part +"\n"
             print "Serial Number: " + t_Serial +"\n"
             print "Firmware: " + t_FW +"\n"
             print "Inverter Version" + t_Version
           else:
             print "No response from inverter - shutdown?"
           break
        if case(t_commands[5]): #synctime
           print "Not avalable"
           break
        if case(): #default
           print " DeltaSolivia.py [command] [port] [inverter ID] \n\n"
           print " commands:\n"
           print "\n".join(t_commands)
           break
        connection.close()
    else:
        #print " DeltaSolivia.py [command] [port] [inverter ID] \n\n"
        #print " commands:\n"
        #print "\n".join(t_commands)
        #print "\n"
        
        Config = ConfigParser.ConfigParser()
        Config.read("./config.ini")
        inverters = Config.sections()
        #print inverters
        
        for x in range (0,len(inverters)):
          section = str(inverters[x])
          try:
            SystemID =  Config.getint(section,'SystemID')
          except:
            SystemID = 0
          try:
            APIKey =  Config.get(section,'APIKey')
          except:
            APIKey = ""
          try:
            Port =  Config.get(section,'Port')
          except:
            Port = "/dev/ttyUSB0"
          try:
            PortSpeed =  Config.getint(section,'PortSpeed')
          except:
            PortSpeed = 19200
          try:
            InvNo =  Config.getint(section,'InvNo')
          except:
            InvNo = 1

          #print SystemID
          #print APIKey
          #print Port
          #print PortSpeed
          #print InvNo
          
          connection = serial.Serial(Port,PortSpeed,timeout=0.2);
          localtime = time.localtime(time.time())

          t_date = 'd={0}'.format(strftime('%Y%m%d'))
          t_time = 't={0}'.format(strftime('%H:%M'))

          inv1 = DeltaInverter(InvNo) #init Inverter 1
          #Get the Daily Energy thus far
          cmd = inv1.getCmdStringFor('Day Wh')
          connection.write(cmd)
          response = connection.read(100)
          #if no response the inverter is asleep
          if response:
            value = inv1.getValueFromResponse(response)
            t_energy = 'v1={0}'.format(value)

            #instanteous power
            cmd = inv1.getCmdStringFor('AC Power')
            connection.write(cmd)
            response = connection.read(100)
            value = inv1.getValueFromResponse(response)
            t_power = 'v2={0}'.format(value)

            #AC Voltage
            cmd = inv1.getCmdStringFor('AC Volts')
            connection.write(cmd)
            response = connection.read(100)
            value = inv1.getValueFromResponse(response)
            t_volts = 'v6={0}'.format(value)

            #Temp - this appears to be onboard somewhere not the heatsink
            cmd = inv1.getCmdStringFor('DC Temp')
            connection.write(cmd)
            response = connection.read(100)
            value = inv1.getValueFromResponse(response)
            t_temp = 'v5={0}'.format(value)

            #Send it all off to PVOutput.org
            cmd = ['/usr/bin/curl',
                '-d', t_date,
                '-d', t_time,
                '-d', t_energy,
                '-d', t_power,
                '-d', t_volts,
                '-d', t_temp,
                '-H', 'X-Pvoutput-Apikey: ' + APIKey,
                '-H', 'X-Pvoutput-SystemId: ' + str(SystemID),
                'http://pvoutput.org/service/r1/addstatus.jsp']
            #print cmd
            ret = subprocess.call (cmd)
          else:
            print "No response from inverter - shutdown? No Data sent to PVOutput.org"
          connection.close()
