import serial, time
import serial.tools.list_ports

class Printer_Device:
    def __init__(self, name):
        self.name = name
        self.DeviceSerial = serial
        self.Connected = False
        self.LedState = False
        self.SolenoidState = False
        self.ServerState = False
        self.Drivers = ["SparkFun Electronics"]
        self.Speeds = ['9600', '19200', '38400','57600','115200','460800']
        self._Ports = []
        self.comlist = serial.tools.list_ports.comports()
        
    def Update_Ports(self):
        """This function updates the list of ports available in the computer"""
        try: # Try to update the list of ports
            self._Ports.clear() # Clear the list of ports
            for element in self.comlist:
                self._Ports.append(element.device)
            return self._Ports
        except Exception as ex:
            self.Connected = False
            return ex
        
    def ConnectPrinterByPort(self, _Port, _Speed):
        """This function connects to the printer Braille in the selected port and speed"""
        try: # Try to connect to the printer
            if not self.Connected: # If printer is not connected
                self.DeviceSerial= serial.Serial(_Port, int(_Speed), write_timeout=1) # Connect to the printer in the selected port and speed 
                time.sleep(0.3)
                self.Connected = True
                return "Printer connected successfully"
            else: # If printer is connected
                return "Printer already connected"
        except Exception as ex: # If there is an error
            self.Connected = False
            return ex
            
    def DisconnectPrinter(self):
        """This function disconnects the printer Braille"""
        try: # Try to disconnect the printer
            if self.Connected: # If printer is connected
                self.DeviceSerial.close() # Close the connection
                time.sleep(1) # Wait 1 second
                self.Connected = False # Set the connection state to False
                return "Printer disconnected successfully"
            else: # If printer is not connected
                return "Printer already disconnected"
        except Exception as ex: # If there is an error
            #self.Connected = False
            return ex
    def DataRead(self):
        """This function reads the data sent by the printer"""
        DataR = ""
        self.DeviceSerial.flushInput()
        try:
            while self.DeviceSerial.in_waiting == 0: # Wait until there is data
                pass
            DataR = self.DeviceSerial.read_until(b';').decode('ascii')
            return DataR
        except Exception as ex:
            return ex

    def Escribe(self, dato):
        self.DeviceSerial.flushOutput()
        if self.DeviceSerial.writable():
            self.DeviceSerial.write(dato.encode('ascii'))
        self.DeviceSerial.flush()   

    def Percutor(self):
        if self.Connected:
            self.Escribe("C") #O:0;")
            #print("Percuta")
        else:
            #print("Impresora no conectada")
            pass
