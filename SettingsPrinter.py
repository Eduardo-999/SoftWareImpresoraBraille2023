from flet import *
from IBE2 import Printer_Device
import sqlite3
from pyModbusTCP.client import ModbusClient

class TabSettings(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
    # Parameters for USB connection
        self.Button_Connect = FloatingActionButton(
            icon=icons.USB_OFF,
            tooltip="disconnected",
            bgcolor=colors.GREEN_100,
            expand=True,
            on_click=self.Fun_Button_Connect
        )
        self.DropdownComPorts = Dropdown(
            label="Puertos COM",
            hint_text="Seleccione el puerto a conectar",
            expand=True
        )
        self.DropdownSpeeds = Dropdown(
            label="Velocidades",
            hint_text="Seleccione la velocidad de transmición",
            expand=True
        )
        self.Button_Led = FloatingActionButton(
            icon=icons.LIGHT_MODE,
            bgcolor=colors.GREEN_100,
            tooltip="Led OFF",
            shape=RoundedRectangleBorder(radius=5),
            expand=True,
            on_click=self.Fun_Button_LED
            # width=100,
            # mini=True
        )
        self.TextToSend = TextField(
            label="Ingrese texto a enviar..",
            multiline=True,
            value="...",
            expand=True
        )
        self.Button_Send = FloatingActionButton(
            icon=icons.SEND,
            on_click=self.Fun_Button_Send,
            bgcolor=colors.BLUE_GREY,
            shape=RoundedRectangleBorder(radius=5),
            # width=100,
            # mini=True,
            # text="Enviar",
            expand=True
        )
        self.Button_Solenoid = FloatingActionButton(
            # icon=ft.icons.SEND,
            on_click=self.Fun_Button_Solenoid,
            bgcolor=colors.GREEN_100,
            shape=RoundedRectangleBorder(radius=5),
            # width=100,
            # mini=True,
            text="S",
            tooltip="solenoid deactivated",
            expand=True
        )
        self.PrinterBraille = Printer_Device("ImpBraille")
        for PORTUSB in self.PrinterBraille.Update_Ports():
            self.DropdownComPorts.options.append(dropdown.Option(PORTUSB))
        for SPEEDUSB in self.PrinterBraille.Speeds:
            self.DropdownSpeeds.options.append(dropdown.Option(SPEEDUSB))
        # Parameters for Bluetooth connection
        self.DropdownComPortsBT = Dropdown(
            label="Puertos Bluetooth",
            hint_text="Seleccione el puerto a conectar"
        )
        self.DropdownSpeedsBT = Dropdown(
            label="Transfer Speed",     hint_text="choose the speed of data transfer"
        )
        self.DropdownDevicesBT = Dropdown(
            label="Devices",
            hint_text="choose device",
            expand=True,
            on_change=self.Fun_Show_SelectedDeviceBT
        )
        self.TableDevicesBT = DataTable(
            columns=[
                DataColumn(Text("Device name")),
                DataColumn(Text("Port")),
                DataColumn(Text("Speed")),
            ],
            expand=True
        )
        self.TestDevice = FloatingActionButton(  # Button for test device
            icon=icons.SETTINGS,
            text="Test Device",
            expand=True,
            on_click=self.Fun_Open_TestDeviceDialog
        )
        self.NameDeviceBT = TextField(
            label="Name Device",
            hint_text="Name of the device"
        )
        self.BtnSaveDeviceBT = FloatingActionButton(
            icon=icons.SAVE,
            tooltip="Save Bluetooth Device",
            on_click=self.Fun_Save_BTDevice,
            expand=1
        )
        self.ButtonCloseDialogBTParameters = FloatingActionButton(
            icon=icons.CLOSE,
            tooltip="Close",
            expand=1,
            on_click=self.Fun_Close_BTParametersDialog
        )
        self.AddDeviceBluetooth = FloatingActionButton(
            icon=icons.ADD,
            text="Add Bluetooth Device",
            on_click=self.Fun_Open_BTParametersDialog,
            expand=True
        )
        self.DeleteDeviceBT = FloatingActionButton(
            icon=icons.DELETE,
            text="Delete Bluetooth Device",
            on_click=self.Fun_Delete_BTDevice,
            expand=True
        )
        self.BTParametersDialog = AlertDialog(
            modal=True,
            title=Text("Add Bluetooth Device"),
            content=Column(
                [
                    self.NameDeviceBT,
                    self.DropdownComPortsBT,
                    self.DropdownSpeedsBT,
                    Row(
                        [
                            self.BtnSaveDeviceBT,
                            self.ButtonCloseDialogBTParameters
                        ]
                    )
                ]
            )
        ) 
        self.BtnConectDevice = FloatingActionButton( # Button for conect to device bluetooth
            icon=icons.BLUETOOTH_DISABLED, 
            on_click=self.Fun_ButtonBT_Connect,
            tooltip="disconnected",
            bgcolor=colors.WHITE24
        )
        self.BtnLedDeviceBT = FloatingActionButton( # Button for Led on/off
            icon=icons.TOGGLE_ON_OUTLINED,   
            on_click=self.Fun_Button_BTLED,
            tooltip="Led OFF",
            bgcolor=colors.WHITE24
        )
        self.BtnCloseTestDevice = FloatingActionButton( # Button for close dialog
            icon=icons.CLOSE,
            on_click=self.Fun_Close_TestBTDevice,
            tooltip="Close",
            bgcolor=colors.WHITE24
            )
        self.BotonSolenoidBT = FloatingActionButton( # Button for solenoid on/off
            #icon=ft.icons.SEND,
            text="S",
            on_click=self.Fun_Button_SolenoidBT,
            bgcolor=colors.WHITE24,
            tooltip="solenoid deactivated"
        )
        self.BtnSendTextBT = FloatingActionButton( # Button for send text to bluetooth device
            icon=icons.SEND,
            on_click=self.Fun_Button_EnviarBT,
            bgcolor=colors.WHITE24,
            tooltip="Send text"
        )
        self.TextToSendBT = TextField( # Text to send to bluetooth device
            label="Ingrese texto a enviar..",
            multiline=True,
            value="...",
        )
        self.TestDeviceDialog = AlertDialog( # Alert Dialog for Test Devices Bluetooth
            modal=True,
            title=Text("Test Device"),
            content=Column(
                [
                    self.BtnConectDevice, 
                    Row(
                        [
                            self.BtnLedDeviceBT, 
                            self.BotonSolenoidBT
                        ]
                    ), 
                    self.TextToSendBT,
                    self.BtnSendTextBT, 
                    self.BtnCloseTestDevice
                ]
            )
        )
        # parameters for Wifi connection
        self.client = ModbusClient(auto_open=False)
        self.BtnAddDeviceWiFi = FloatingActionButton(  # Add device WiFi
            icon=icons.ADD,
            text="Add WiFi Device",
            on_click=self.Fun_Open_WiFiParametersDialog,
            expand=True
        )
        self.BtnSaveDeviceWiFi = FloatingActionButton(  # Button for save device WiFi
            icon=icons.SAVE,
            tooltip="Save WiFi Device",
            on_click=self.Fun_Save_WiFiDevice,
            expand=True
        )
        self.BtnCloseDialogWiFi = FloatingActionButton(  # Button for close dialog
            icon=icons.CLOSE,
            tooltip="Close",
            expand=True,
            on_click=self.Fun_Close_WiFiParametersDialog
        )
        self.BtnDeleteDeviceWiFi = FloatingActionButton(  # Delete device WiFi
            icon=icons.DELETE,
            text="Delete WiFi Device",
            on_click=self.Fun_Delete_WiFiDevice,
            expand=True
        )
        self.DevicesWiFi = Dropdown(  # Show devices WiFi
            label="Devices",
            hint_text="choose device",
            on_change=self.Fun_Show_SelectedDeviceWiFi,
            expand=True
        )
        self.TableDevicesWiFi = DataTable(  # Table for show devices WiFi
            columns=[
                DataColumn(Text("Device name")),
                DataColumn(Text("IP")),
                DataColumn(Text("Port")),
            ],
            expand=True
        )
        
        self.BtnConnectServer = FloatingActionButton(
            on_click=self.Fun_ConnectServer,
            icon=icons.SIGNAL_WIFI_CONNECTED_NO_INTERNET_4,
            bgcolor=colors.BLUE_GREY,
            shape=RoundedRectangleBorder(radius=5),
            # width=100,
            # height=50,
            mini=True,
            tooltip="Desconectado",
            expand=True
        )
        self.BtnTCP = FloatingActionButton(
            icon=icons.LIGHT_MODE,
            tooltip="Led off",
            bgcolor=colors.BLUE_GREY,
            on_click=self.Fun_Button_TCP,
            shape=RoundedRectangleBorder(radius=5),
            # width=100,
            # height=50,
            mini=True,
            expand=True
        )
        self.slider = Slider(
            min=0,
            max=65536,
            divisions=16,
            label="{value}",
            on_change=self.Fun_Send_VarSlider,
            expand=True
        )
        self.BtnSendMultipleRegisters = FloatingActionButton(
            icon=icons.SEND,
            on_click=self.Fun_Write_MultipleRegisters,
            bgcolor=colors.GREEN_50,
            shape=RoundedRectangleBorder(radius=5),
            mini=True,
            tooltip="Send",
            expand=True
        )
        self.Addres = TextField(value="0", tooltip="Address", expand=True)
        self.Value = TextField(value="0", tooltip="Value", expand=True)
        self.boards = Column(
            [
                Row(
                    [
                        Text(value="ID", width=35),
                        Text(value="Address", expand=1),
                        Text(value="Value", expand=1)
                    ]
                ),
                Row([Text(value="1", width=35), self.Addres, self.Value])
            ],
            # width=350, height=100
            expand=True
        )
        self.NameDeviceWiFi = TextField( 
            label="Name Device", 
            hint_text="Name of the device"
        )
        self.IPaddress = TextField(label="Direccion IP") # Parameters for connect to server
        self.PortWiFi = TextField(value="502", label="Puerto IP")
        self.WiFiParametersDialog = AlertDialog(  # Alert Dialog for add device WiFi
            modal=True,
            title=Text("Add WiFi Device"),
            content=Column(
                [
                    self.NameDeviceWiFi, 
                    self.IPaddress, 
                    self.PortWiFi, 
                    Row(
                        [
                            self.BtnSaveDeviceWiFi, 
                            self.BtnCloseDialogWiFi
                        ]
                    )
                ]
            )
        )

        self.bs = BottomSheet(
            Container(
                Column(
                    [
                        Text("!PRINTER IS NOT CONNECTED¡", color="red",
                             size=20, font_family="Helvetica"),
                        ElevatedButton("Close", on_click=self.Fun_Close_BottomSheet),
                    ],
                    tight=True,
                ),
                padding=10
            )
        )
        self.page.overlay.append(self.bs)
        self.TerminalConnection = TextField(
            label="Terminal",
            multiline=True,
            tooltip="Terminal",
            max_lines=2,
            min_lines=1,
            value="Build successful!",
            text_size=12
        )
        self.tabitems = [
            Tab(
                text="USB",
                icon=icons.USB,
                content=Container(
                    content=Column(
                        [
                            self.DropdownComPorts,
                            self.DropdownSpeeds,
                            Row(
                                [
                                    self.Button_Connect,
                                    self.Button_Led,
                                    self.Button_Solenoid
                                ]
                            ),
                            self.TextToSend,
                            self.Button_Send
                        ]
                    ),
                    gradient=LinearGradient(
                        begin=alignment.top_center,
                        end=alignment.bottom_center,
                        colors=[colors.WHITE, colors.BLUE_GREY_200]
                    ),
                    margin=10,
                    padding=10,
                    alignment=alignment.center,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print(
                        "Clickable transparent with Ink clicked!"),

                )
            ),
            Tab(
                text="Bluetooth",
                icon=icons.BLUETOOTH,
                content=Container(
                    content=Column(
                        [
                            self.DropdownDevicesBT,
                            self.TableDevicesBT,
                            Row(
                                [
                                    self.AddDeviceBluetooth,
                                    self.DeleteDeviceBT,
                                    self.TestDevice
                                ]
                            )
                        ]
                    ),
                    gradient=LinearGradient(
                        begin=alignment.top_center,
                        end=alignment.bottom_center,
                        colors=[colors.WHITE, colors.BLUE_GREY_200]
                    ),
                    margin=10,
                    padding=10,
                    alignment=alignment.center,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print(
                        "Clickable transparent with Ink clicked!")
                )
            ),
            Tab(
                text="Wifi",
                icon=icons.WIFI,
                content=Row(
                    [
                        Container(
                            content=Column(
                                [
                                    self.DevicesWiFi,
                                    self.TableDevicesWiFi,
                                    Row([self.BtnAddDeviceWiFi,
                                         self.BtnDeleteDeviceWiFi])
                                ]
                            ),
                            gradient=LinearGradient(
                                begin=alignment.top_center,
                                end=alignment.bottom_center,
                                colors=[colors.WHITE, colors.BLUE_GREY_200]
                            ),
                            margin=10,
                            padding=10,
                            alignment=alignment.center,
                            border_radius=10,
                            ink=True,
                            on_click=lambda e: print(
                                "Clickable transparent with Ink clicked!"),
                            expand=True
                        ),
                        Container(
                            content=Column(
                                [
                                    Row([self.BtnConnectServer, self.BtnTCP]),
                                    self.slider,
                                    self.boards,
                                    self.BtnSendMultipleRegisters
                                ]
                            ),
                            gradient=LinearGradient(
                                begin=alignment.top_center,
                                end=alignment.bottom_center,
                                colors=[colors.WHITE, colors.BLUE_GREY_200]
                            ),
                            margin=10,
                            padding=10,
                            alignment=alignment.center,
                            border_radius=10,
                            ink=True,
                            on_click=lambda e: print(
                                "Clickable transparent with Ink clicked!"),
                            expand=True
                        )
                    ],
                    # expand=True
                )
            ),
            Tab(
                text="Braille parameters",
                icon=icons.SETTINGS_OUTLINED,
                content=Container(
                    content=Text("Settings for Braille parameters"),
                    gradient=LinearGradient(
                        begin=alignment.top_center,
                        end=alignment.bottom_center,
                        colors=[colors.WHITE, colors.BLUE_GREY_200]
                    ),
                    margin=10,
                    padding=10,
                    alignment=alignment.center,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print(
                        "Clickable transparent with Ink clicked!")
                )
            ),
        ]
        self.Windows = Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=self.tabitems,
            on_change=self.Fun_Tab_Change,
            scrollable=True,
            expand=True
        )

    def build(self):
        return self.Windows

    def Fun_Tab_Change(self, e):
        if self.Windows.selected_index == 0:
            print("USB")
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(self.Fun_Add_DevicesUSB(e))
        elif self.Windows.selected_index == 1:
            print("Bluetooth")
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(self.Fun_Add_DevicesBT(e))
        elif self.Windows.selected_index == 2:
            print("Wifi")
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(self.Fun_Add_DevicesWiFi(e))
        elif self.Windows.selected_index == 3:
            print("Braille parameters")
        self.update()
        self.page.update()

    def Fun_Button_Connect(self, e):  # button connect device USB
        if self.PrinterBraille.Connected:  # if the device is connected
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(self.PrinterBraille.DisconnectPrinter())
            if not self.PrinterBraille.Connected:  # if the device is disconnected
                self.Button_Connect.tooltip = "disconnected"  # Change state of the button
                self.Button_Connect.icon = icons.USB_OFF
                self.Button_Connect.bgcolor = colors.GREEN_100
        else:  # if the device is disconnected
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(self.PrinterBraille.ConnectPrinterByPort(
                self.DropdownComPorts.value, self.DropdownSpeeds.value))
            if self.PrinterBraille.Connected:  # if the device is connected
                self.Button_Connect.tooltip = "Conected"  # Change state of the button
                self.Button_Connect.icon = icons.USB
                self.Button_Connect.bgcolor = colors.BLUE_200
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Conected at: " + self.DropdownComPorts.value + \
                    " whit the speed: " + self.DropdownSpeeds.value + " bauds"

        self.page.update()
        self.update()

    def Fun_Button_LED(self, e):
        if self.PrinterBraille.Connected:  # if the device is connected
            if not self.PrinterBraille.LedState:  # if the led is off
                # send the command to turn on the led
                self.PrinterBraille.DeviceSerial.write('A'.encode('utf-8'))
                self.PrinterBraille.DeviceSerial.write('\n'.encode(
                    'utf-8'))  # send the command to turn on the led
                self.TerminalConnection.value = self.TerminalConnection.value + \
                    '\n' + str(self.PrinterBraille.DataRead())
                self.Button_Led.tooltip = "Led ON"
                self.Button_Led.icon = icons.TOGGLE_ON_ROUNDED
                self.Button_Led.bgcolor = colors.BLUE_200
                self.PrinterBraille.LedState = not self.PrinterBraille.LedState
            else:
                self.PrinterBraille.DeviceSerial.write('B'.encode('utf-8'))
                self.PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
                self.TerminalConnection.value = self.TerminalConnection.value + \
                    '\n' + str(self.PrinterBraille.DataRead())
                self.Button_Led.tooltip = "Led OFF"
                self.Button_Led.icon = icons.TOGGLE_ON_OUTLINED
                self.Button_Led.bgcolor = colors.GREEN_100
                self.PrinterBraille.LedState = not self.PrinterBraille.LedState
        else:
            self.Fun_Show_BottomSheet(e)
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' "!Printer is not coneccted!"
        self.page.update()
        self.update()

    def Fun_Show_BottomSheet(self, e):
        self.bs.open = True
        self.bs.update()

    def Fun_Close_BottomSheet(self, e):
        self.bs.open = False
        self.bs.update()

    def Fun_Button_Solenoid(self, e):  # button solenoid
        if self.PrinterBraille.Connected:
            if not self.PrinterBraille.SolenoidState:
                self.Button_Solenoid.tooltip = "solenoid activated"
                # BotonSolenoid.icon = ft.icons.LIGHT_MODE_OUTLINED
                self.Button_Solenoid.bgcolor = colors.BLUE_200
                self.PrinterBraille.DeviceSerial.write('F:500'.encode('utf-8'))
                self.PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
                self.update()
                self.page.update()
                self.TerminalConnection.value = self.TerminalConnection.value + \
                    '\n' + str(self.PrinterBraille.DataRead())
                self.PrinterBraille.SolenoidState = not self.PrinterBraille.SolenoidState
                self.Button_Solenoid.tooltip = "solenoid deactivated"
                self.Button_Solenoid.bgcolor = colors.GREEN_100
                self.PrinterBraille.SolenoidState = not self.PrinterBraille.SolenoidState
        else:
            self.Fun_Show_BottomSheet(e)
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' "!Printer is not coneccted!"
        self.page.update()
        self.update()

    def Fun_Button_Send(self, e):
        if self.PrinterBraille.Connected:
            for elemento in self.TextToSend.value:
                self.PrinterBraille.DeviceSerial.write(
                    elemento.encode('utf-8'))
            self.PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(self.PrinterBraille.DataRead())
        else:
            self.Fun_Show_BottomSheet(e)
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' "!Printer is not coneccted!"
        self.page.update()
        self.update()

    def Fun_Add_DevicesUSB(self, e):
        try:
            self.DropdownComPorts.options.clear()
            self.DropdownSpeeds.options.clear()
            for PORTUSB in self.PrinterBraille.Update_Ports():
                self.DropdownComPorts.options.append(dropdown.Option(PORTUSB))
            for SPEEDUSB in self.PrinterBraille.Speeds:
                self.DropdownSpeeds.options.append(dropdown.Option(SPEEDUSB))
            return "Devices added successfully"
        except Exception as ex:
            return ex

    def Fun_Add_DevicesBT(self, e):
        try:
            self.DropdownComPortsBT.options.clear() # Clear the dropdown Bluetooth devices
            self.DropdownSpeedsBT.options.clear() 
            self.DropdownDevicesBT.options.clear()
            for PORTBT in self.PrinterBraille.Update_Ports():  # Add the Comports to the dropdown Bluetooth devices
                self.DropdownComPortsBT.options.append(dropdown.Option(PORTBT))
            for SpeedBT in self.PrinterBraille.Speeds:  # Add the Speeds to the dropdown Bluetooth devices
                self.DropdownSpeedsBT.options.append(dropdown.Option(SpeedBT))
            GeneralConexion = sqlite3.connect(
                'Database/MyDataBase.sqlite3')  # Connect to the database
            Cursor = GeneralConexion.cursor()  # Create a cursor
            # Read all devices from the table Devices
            Cursor.execute("SELECT * FROM Devices")
            BluetoothDevicesList = Cursor.fetchall()  # Save the devices in a list
            if len(BluetoothDevicesList) == 0:
                self.DeleteDeviceBT.disabled = True
            else:
                self.DeleteDeviceBT.disabled = False
            for Device_BT in BluetoothDevicesList:
                self.DropdownDevicesBT.options.append(
                    dropdown.Option(Device_BT[1]))
            GeneralConexion.close()
            return "Devices added successfully"
        except Exception as ex:
            return ex

    def Fun_Add_DevicesWiFi(self, e):
        try:
            self.DevicesWiFi.options.clear()
            GeneralConexion = sqlite3.connect('Database/MyDataBase.sqlite3')
            Cursor = GeneralConexion.cursor()
            # Read all devices from the table WiFiDevices
            Cursor.execute("SELECT * FROM WiFiDevices")
            WifiDevicesList = Cursor.fetchall()
            if len(WifiDevicesList) == 0:
                self.BtnDeleteDeviceWiFi.disabled = True
            else:
                self.BtnDeleteDeviceWiFi.disabled = False
            for WifiDevice in WifiDevicesList:
                self.DevicesWiFi.options.append(dropdown.Option(WifiDevice[1]))
            GeneralConexion.close()
            return "Devices added successfully"

        except Exception as ex:
            return ex

    def Fun_Show_SelectedDeviceBT(self, e):
        try:
            # Connect to the database
            conexion3 = sqlite3.connect('Database/MyDataBase.sqlite3')
            cursor3 = conexion3.cursor()  # Create a cursor
            # Read all devices from the table Devices
            cursor3.execute("SELECT * FROM Devices")
            DevicesList3 = cursor3.fetchall()  # Save the devices in a list
            for Device3 in DevicesList3:  # Show the COMPORT and the Speed with the selected device
                if Device3[1] == self.DropdownDevicesBT.value:
                    self.TableDevicesBT.rows.clear()  # Delete content of the table
                    self.TableDevicesBT.rows.append(  # Add the new content to the table
                        DataRow(
                            cells=[
                                DataCell(Text(Device3[1])),  # Name
                                DataCell(Text(Device3[2])),  # Port
                                DataCell(Text(str(Device3[3])))  # Speed
                            ]
                        )
                    )
                    break
            conexion3.close()  # Close the connection
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(ex)
        self.update()
        self.page.update()

    def Fun_Open_BTParametersDialog(self, e): # function to open the dialog BTParametersDialog
        self.page.dialog = self.BTParametersDialog
        self.BTParametersDialog.open = True
        try:
            self.page.update()
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(ex)

    def Fun_Close_BTParametersDialog(self, e):  # function to close the dialog BTParametersDialog
        self.BTParametersDialog.open = False
        try:
            self.page.update()
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(ex)

    def Fun_Save_BTDevice(self, e): # function to save the new device in the database
        try:
            conexion2 = sqlite3.connect('Database/MyDataBase.sqlite3') # Connect to the database
            cursor2 = conexion2.cursor()  # Create a cursor
            cursor2.execute(
                "CREATE TABLE IF NOT EXISTS Devices (id INTEGER PRIMARY KEY, name TEXT, port TEXT, speed INTEGER)")  # Create the table Devices if it does not exist
            cursor2.execute("INSERT INTO Devices VALUES (NULL,?,?,?)",
                            (self.NameDeviceBT.value, self.DropdownComPortsBT.value, int(self.DropdownSpeedsBT.value)))  # Insert the new device in the table Devices
            conexion2.commit()  # Save the changes
            cursor2.execute("SELECT * FROM Devices") # Read all devices from the table Devices
            rows = cursor2.fetchall()  # Save the devices in a list
            row = rows[len(rows)-1]  # Save the last device in the list
            self.DropdownDevicesBT.options.append(dropdown.Option(row[1])) # Add the new device to the dropdown Devices Bluetooth
            self.DeleteDeviceBT.disabled = False
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Device saved successfully " + "ID -> " + \
                str(row[0]) + " Name -> " + row[1] + " Port -> " + \
                row[2] + " Speed -> " + str(row[3])  # Show the message
            conexion2.close()  # Close the connection
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(ex)  # Show the error
        self.update()
        self.page.update()

    def Fun_Delete_BTDevice(self, e): # function to delete the selected device bluetooth from the database
        try:       
            conexion4 = sqlite3.connect('Database/MyDataBase.sqlite3') # Connect to the database
            cursor4 = conexion4.cursor() # Create a cursor
            cursor4.execute("SELECT * FROM Devices") # Read all devices from the table Devices
            DevicesList4 = cursor4.fetchall() # Save the devices in a list
            if len(DevicesList4) > 0: # if devices is more than 0 Delete the selected device from the list of devices
                cursor4.execute("DELETE FROM Devices WHERE name = " + "'" + self.DropdownDevicesBT.value + "'") # Delete the selected device from the table Devices 
                conexion4.commit() # Save the changes
                option = self.Fun_Find_optionBT(self.DropdownDevicesBT.value)
                if option != None:
                    self.DropdownDevicesBT.options.remove(option)
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Device deleted successfully"
                self.TableDevicesBT.rows.clear() # Delete content of the table
                if len(self.DropdownDevicesBT.options) == 0:
                    self.DeleteDeviceBT.disabled = True
            else:
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "There are no devices to delete"
            conexion4.close() # Close the connection
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(ex)
        self.update()
        self.page.update()
    def Fun_Find_optionBT(self, option_name): # function to find in the bluetooth devices dropdown
        for option in self.DropdownDevicesBT.options:
            if option_name == option.key:
                return option
        return None
    def Fun_Open_TestDeviceDialog(self, e): # function to open the dialog testDeviceDialog
        self.page.dialog = self.TestDeviceDialog
        self.TestDeviceDialog.open = True
        try:
            self.page.update()
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(ex)
    
    def Fun_Close_TestBTDevice(self, e): # function to close the dialog testDeviceDialog
        self.TestDeviceDialog.open = False
        try:
            self.page.update()
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' + str(ex)
   
    def Fun_ButtonBT_Connect(self, e): # button connect device Bluetooth
        NameDeviceSelected3 = self.DropdownDevicesBT.value
        try:
            conexion3 = sqlite3.connect('Database/MyDataBase.sqlite3')
            cursor3 = conexion3.cursor()
            cursor3.execute("SELECT * FROM Devices")
            DevicesList3 = cursor3.fetchall() 
            for Device3 in DevicesList3: # Show the COMPORT and the Speed with the selected device
                if Device3[1] == NameDeviceSelected3:
                    PortBTSelect = Device3[2] # Port
                    SpeedBTSelect = Device3[3] # Speed
                    break
        
            if self.PrinterBraille.Connected: # If the device is connected, disconnect it
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' +  str(self.PrinterBraille.DisconnectPrinter())
                if not self.PrinterBraille.Connected:
                    self.BtnConectDevice.tooltip = "disconnected"
                    self.BtnConectDevice.icon = icons.BLUETOOTH_DISABLED
                    self.BtnConectDevice.bgcolor = colors.WHITE24
                else:
                    self.TerminalConnection.value = self.TerminalConnection.value + '\n ' + "The conexion is not finished"
            else: # If the device is not connected, connect it
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(self.PrinterBraille.ConnectPrinterByPort(PortBTSelect, str(SpeedBTSelect)))
                if self.PrinterBraille.Connected:
                    self.BtnConectDevice.tooltip = "Conected"
                    self.BtnConectDevice.icon = icons.BLUETOOTH_CONNECTED
                    self.BtnConectDevice.bgcolor = colors.BLUE_300
                    self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Port -> " + PortBTSelect + '\n' + "Speed -> " + str(SpeedBTSelect)
                    self.update()
                    self.page.update()
                else:
                    self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "The conexion is not finished"
            conexion3.close()
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(ex)
        self.update()
        self.page.update()
    
    def Fun_Button_BTLED(self, e):
        if self.PrinterBraille.Connected:
            if not self.PrinterBraille.LedState:
                self.PrinterBraille.DeviceSerial.write('A'.encode('utf-8'))
                self.PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
                self.TerminalConnection.value = self.TerminalConnection.value + \
                    '\n' + str(self.PrinterBraille.DataRead())
                self.BtnLedDeviceBT.tooltip = "Bluetooth ON"
                self.BtnLedDeviceBT.icon = icons.TOGGLE_ON_ROUNDED
                self.BtnLedDeviceBT.bgcolor = colors.BLUE_200
                self.PrinterBraille.LedState = not self.PrinterBraille.LedState
            else:
                self.PrinterBraille.DeviceSerial.write('B'.encode('utf-8'))
                self.PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
                self.TerminalConnection.value = self.TerminalConnection.value + \
                    '\n' + str(self.PrinterBraille.DataRead())
                self.BtnLedDeviceBT.tooltip = "Bluetooth OFF"
                self.BtnLedDeviceBT.icon = icons.TOGGLE_ON_OUTLINED
                self.BtnLedDeviceBT.bgcolor = colors.WHITE24
                self.PrinterBraille.LedState = not self.PrinterBraille.LedState
        else:
            self.Fun_Show_BottomSheet(e)
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' "!Printer is not coneccted!"
        self.page.update()
        self.update()    

    def Fun_Button_SolenoidBT(self, e): # button SolenoidBT
        if self.PrinterBraille.Connected:
            if not self.PrinterBraille.SolenoidState:
                self.BotonSolenoidBT.tooltip = "solenoid activated"
                self.BotonSolenoidBT.bgcolor = colors.BLUE_200
                self.PrinterBraille.DeviceSerial.write('F:500'.encode('utf-8'))
                self.PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
                self.update()
                self.page.update()
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(self.PrinterBraille.DataRead())
                self.PrinterBraille.SolenoidState = not self.PrinterBraille.SolenoidState
                self.BotonSolenoidBT.tooltip = "solenoid deactivated"
                self.BotonSolenoidBT.bgcolor = colors.WHITE24
                self.PrinterBraille.SolenoidState = not self.PrinterBraille.SolenoidState
        else:
            self.Fun_Show_BottomSheet(e)
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' "!Printer is not coneccted!"
        self.page.update()
    
    def Fun_Button_EnviarBT(self, e): # button send text Bluetooth
        if self.PrinterBraille.Connected:
            for elemento in self.TextToSendBT.value:
                self.PrinterBraille.DeviceSerial.write(elemento.encode('utf-8'))
            self.PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(self.PrinterBraille.DataRead())
        else:
            self.Fun_Show_BottomSheet(e)
            self.TerminalConnection.value = self.TerminalConnection.value + \
                '\n' "!Printer is not coneccted!"
        self.page.update()
    

    
    def Fun_Open_WiFiParametersDialog(self, e): # function to open the dialog WiFiParametersDialog
        self.page.dialog = self.WiFiParametersDialog
        self.WiFiParametersDialog.open = True
        try:
            self.page.update()
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(ex)

    def Fun_Close_WiFiParametersDialog(self, e): # function to close the dialog WiFiParametersDialog
        self.WiFiParametersDialog.open = False
        self.page.update()
    
    def Fun_Save_WiFiDevice(self, e): # the Table WiFiDevices content is: ID, Name, IPaddress and Port
        try:
            conexionWifi = sqlite3.connect('Database/MyDataBase.sqlite3') # open the database
            cursorWiFi = conexionWifi.cursor() # create the cursor
            cursorWiFi.execute(
                "CREATE TABLE IF NOT EXISTS WiFiDevices (id INTEGER PRIMARY KEY, name TEXT, ip TEXT, port INTEGER)") # create the table if not exist
            cursorWiFi.execute("INSERT INTO WiFiDevices VALUES (NULL,?,?,?)",
                           (self.NameDeviceWiFi.value, self.IPaddress.value, int(self.PortWiFi.value))) # insert the data in the table
            conexionWifi.commit() # save the data
            cursorWiFi.execute("SELECT * FROM WiFiDevices") # select all the data
            rows = cursorWiFi.fetchall() # save the data in a variable
            row = rows[len(rows)-1]  # save the last data in a variable
            self.DevicesWiFi.options.append(dropdown.Option(row[1])) # add the name of the device in the dropdown
            self.BtnDeleteDeviceWiFi.disabled = False # enable the button to delete the device
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Device saved successfully " + " ID -> " + str(row[0]) + " Name -> " + row[1] + " IP -> " + row[2] + " Port -> " + str(row[3]) # show the message in the terminal
            conexionWifi.close() # close the database
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(ex)
        self.update()
        self.page.update()
   
    def Fun_Find_OptionWiFi(self, option_name):  # function to find in the WiFi devices dropdown the selected device
        for optionWifi in self.DevicesWiFi.options:
            if option_name == optionWifi.key:
                return optionWifi
        return None
    
    def Fun_Delete_WiFiDevice(self, e): # function to delete the device WiFi from the database
        try:       
            conexionWifidel = sqlite3.connect('Database/MyDataBase.sqlite3') # open the database
            cursorFifedel = conexionWifidel.cursor() # create the cursor
            cursorFifedel.execute("SELECT * FROM WiFiDevices") # select all the data
            DevicesListWifiDevices = cursorFifedel.fetchall()  # get the list of devices
            # if devices is more than 0 Delete the selected device from the list of devices
            if len(DevicesListWifiDevices) > 0:  # if devices is more than 0
                cursorFifedel.execute("DELETE FROM WiFiDevices WHERE name = " + "'" + self.DevicesWiFi.value + "'") # delete the device from the database 
                conexionWifidel.commit() # save the data
                optionWifi = self.Fun_Find_OptionWiFi(self.DevicesWiFi.value) # find the device in the dropdown list 
                if optionWifi != None: # if the device is found
                    self.DevicesWiFi.options.remove(optionWifi) # remove the device from the dropdown list 
                self.TableDevicesWiFi.rows.clear() # Delete content of the table
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Device deleted successfully"
                if len(self.DevicesWiFi.options) == 0: # if the list of devices is empty disable the button to delete the device
                    self.BtnDeleteDeviceWiFi.disabled = True
            else:
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "There are no devices to delete"
            conexionWifidel.close() # close the database
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(ex)
        self.update()
        self.page.update()
    
    def Fun_Show_SelectedDeviceWiFi(self, e): # function to show the device WiFi selected
        NameDeviceSelectedWiFi = self.DevicesWiFi.value
        try:
            conexionWiFi = sqlite3.connect('Database/MyDataBase.sqlite3') # open the database
            cursorWiFi = conexionWiFi.cursor() # create the cursor
            cursorWiFi.execute("SELECT * FROM WiFiDevices") # select all the data
            DevicesListWiFi = cursorWiFi.fetchall() # get the list of devices
            for DeviceWiFi in DevicesListWiFi: # Show the IP and the Port with the selected device
                if DeviceWiFi[1] == NameDeviceSelectedWiFi:
                    self.TableDevicesWiFi.rows.clear() # Delete content of the table   
                    self.TableDevicesWiFi.rows.append( # Add the new content
                        DataRow(
                            cells=[
                                    DataCell(Text(DeviceWiFi[1])), 
                                    DataCell(Text(DeviceWiFi[2])), 
                                    DataCell(Text(str(DeviceWiFi[3])))
                                ]
                        )
                    )
                    break
            conexionWiFi.close() # close the database
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(ex)
        self.update()
        self.page.update()
    
    def Fun_ConnectServer(self, e):
        NameDeviceSelectedWiFi = self.DevicesWiFi.value
        try:
            conexionWiFi = sqlite3.connect('Database/MyDataBase.sqlite3')
            cursorWiFi = conexionWiFi.cursor()
            cursorWiFi.execute("SELECT * FROM WiFiDevices")
            DevicesListWiFi = cursorWiFi.fetchall()
            for DeviceWiFi in DevicesListWiFi:
                if DeviceWiFi[1] == NameDeviceSelectedWiFi:
                    IP_WiFiDevice = DeviceWiFi[2] 
                    PORT_WiFiDevice = str(DeviceWiFi[3])
                    break
            SERVER_HOST = IP_WiFiDevice
            SERVER_PORT = PORT_WiFiDevice
            
            if not self.PrinterBraille.ServerState:
                self.client.host = SERVER_HOST
                self.client.port = int(SERVER_PORT)
                self.client.auto_open = True
                if self.client.open():
                    self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Server connected successfully" + \
                        "\n" + SERVER_HOST + " " + SERVER_PORT
                    self.PrinterBraille.ServerState = True
                    self.BtnConnectServer.icon = icons.SIGNAL_WIFI_4_BAR
                    self.BtnConnectServer.tooltip = "Desconectar"
                    self.BtnConnectServer.bgcolor = colors.GREEN_500
                else:
                    self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Server not connected" + \
                        "\n" + SERVER_HOST + " Port: " + str(SERVER_PORT)
                    self.PrinterBraille.ServerState = False
                    self.BtnConnectServer.icon = icons.SIGNAL_WIFI_CONNECTED_NO_INTERNET_4
            else:
                self.client.close()
                self.BtnConnectServer.icon = icons.SIGNAL_WIFI_CONNECTED_NO_INTERNET_4
                self.BtnConnectServer.tooltip = "Conectar"
                self.BtnConnectServer.bgcolor = colors.BLUE_GREY
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Server disconnected successfully" + \
                    "\n" + SERVER_HOST + " Port: " + str(SERVER_PORT)
                self.PrinterBraille.ServerState = False
            conexionWiFi.close()
        except Exception as ex:
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + str(ex)  
        self.update()
        self.page.update()
    def Fun_Button_TCP(self, e):
        if self.PrinterBraille.ServerState:
            if not self.PrinterBraille.LedState:
                self.BtnTCP.icon = icons.LIGHT_MODE
                self.BtnTCP.tooltip = "Led on"
                self.BtnTCP.bgcolor = colors.GREEN_500
                self.client.write_single_register(0, 1)
                self.PrinterBraille.LedState = not self.PrinterBraille.LedState
            else:
                self.BtnTCP.icon = icons.LIGHT_MODE
                self.BtnTCP.bgcolor = colors.BLUE_GREY
                self.BtnTCP.tooltip = "Led off"
                self.client.write_single_register(0, 0)
                self.PrinterBraille.LedState = not self.PrinterBraille.LedState
        else:
            self.Fun_Show_BottomSheet(e)
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Server not connected"
        self.update()
        self.page.update()
    def Fun_Send_VarSlider(self, e):
        if self.PrinterBraille.ServerState:
            Valor = int(self.slider.value)
            if (Valor < 65536):
                self.client.write_single_register(1, Valor)
        else:
            self.Fun_Show_BottomSheet(e)
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Server not connected"
        self.update()
        self.page.update()
    def Fun_Write_MultipleRegisters(self, e):
        if self.PrinterBraille.ServerState:
            Values = self.Value.value.split(",")
            Values = [int(i) for i in Values]
            if len(Values) > 1:
                self.client.write_multiple_registers(int(self.Addres.value), Values)
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Addres -> " + \
                    self.Addres.value + " Values -> " + str(Values)
            else:
                self.client.write_single_register(int(self.Addres.value), Values[0])
                self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Addres -> " + \
                    self.Addres.value + " Value -> " + str(Values[0])
                
        else:
            self.Fun_Show_BottomSheet(e)
            self.TerminalConnection.value = self.TerminalConnection.value + '\n' + "Server not connected"
        self.update()
        self.page.update()
    