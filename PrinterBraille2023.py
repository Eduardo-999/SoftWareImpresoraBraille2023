import flet as ft
from pyModbusTCP.client import ModbusClient
import sqlite3
import IBE2
import ManageGoogleDrive
import FilesUploaded



def main(page: ft.Page):
    client = ModbusClient(auto_open=False)
    PrinterBraille = IBE2.Printer_Device("ImpBraille")
    app = FilesUploaded.FilesGoogleDrive()
    page.title = "Printer Braille 2023"
    # functions 
    # function to translate the text to braille
    def TranslateText(e):
        TextInput.value = "Hello" #GoogleDocs.get_text()
        TextToTranslate.value = TextInput.value
        page.update()
    # function to clear the text
    def ClearText(e):
        TextInput.value = ""
        TextToTranslate.value = ""
        page.update()
    # function to open the file explorer
    def ShowListFilesGoogleDrive(e):
        
        #default_tasks = #["Finish homework", "Walk the dog", "Do laundry"]
        app.AddListOfTasks(e, [File[1] for File in ManageGoogleDrive.Get_ListFiles() ])
        
        """#print(ManageGoogleDrive.Get_ListFiles())
        # Delete content of the table
        TableShowFilesGD.rows.clear()
        # Add the new content
        # (id, name, mimeType, size, createdTime)
        for File in ManageGoogleDrive.Get_ListFiles():
            TableShowFilesGD.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Icon(name="INSERT_DRIVE_FILE", color="#c1c1c1")),
                        ft.DataCell(ft.Text(File[1])),# on_double_tap=lambda e: print("Double tap"), on_tap=lambda e: print("One tap:")), 
                        ft.DataCell(ft.Text(File[3])), 
                        ft.DataCell(ft.Text(File[4])),
                        #ft.DataCell(ft.Text(File[0])),
                        ft.DataCell(
                                ft.TextButton(text="Descargar", on_click=lambda e: print(File[0], File[1]))# ManageGoogleDrive.DownloadFile(File[0], File[1]))
                        )
                    ],
                    selected=False,
                    on_select_changed=lambda e: print(f"row select changed"),
                )
            )"""
        page.update()
    def SearchWord(e):
        app.SearchExternal(e, SearchWordGD.value.lower())
        page.update()
    def AddFileGD(e):
        app.add_clickedExternal(TextfieldAddFileGD.value)
    def on_keyboard(e: ft.KeyboardEvent):
        print(e)
        if e.key == "S" and e.ctrl:
            page.show_semantics_debugger = not page.show_semantics_debugger
            page.update()
    def route_change(route):
        Paginas = ["/", "/USB", "/Bluetooth", "/WiFi", "/Configuracion"]
        print(Paginas[rail.selected_index] + " :: " + str(route))
        page.views.clear()
        if Paginas[rail.selected_index] == "/":
            page.views.append(PaginaInicio)
        elif Paginas[rail.selected_index] == "/USB":
            page.views.append(PaginaUSB)
        elif Paginas[rail.selected_index] == "/Bluetooth":
            page.views.append(PaginaBluetooth)
        elif Paginas[rail.selected_index] == "/WiFi":
            page.views.append(PaginaWiFi)
        elif Paginas[rail.selected_index] == "/Configuracion":
            page.views.append(PaginaConfiguracion)
        page.update()

    def InitFunction(e):
        # try to add the devices bluetooth and WiFi to the dropdown 
        try:
            GeneralConexion = sqlite3.connect('Database/MyDataBase.sqlite3')
            Cursor = GeneralConexion.cursor()
            # Read all devices from the table Devices
            Cursor.execute("SELECT * FROM Devices")
            DevicesBluetoothList = Cursor.fetchall()
            if len(DevicesBluetoothList) == 0:
                DeleteDeviceBT.disabled = True
            else:
                DeleteDeviceBT.disabled = False
            for Device_BT in DevicesBluetoothList:
                Devices.options.append(ft.dropdown.Option(Device_BT[1]))
            # Read all devices from the table WiFiDevices
            Cursor.execute("SELECT * FROM WiFiDevices")
            WifiDevicesList = Cursor.fetchall()
            if len(WifiDevicesList) == 0:
                DeleteDeviceWiFi.disabled = True
            else:
                DeleteDeviceWiFi.disabled = False
            for WifiDevice in WifiDevicesList:
                DevicesWiFi.options.append(ft.dropdown.Option(WifiDevice[1]))
        except Exception as ex:
            print("Error al abrir la base de datos:", ex)
        # Add the COMPORTS and speeds to the dropdown Bluetooth devices
        for PORTBT in PrinterBraille.Update_Ports():
            PortBluetooth.options.append(ft.dropdown.Option(PORTBT))
        for SpeedBT in PrinterBraille.Speeds:
            SpeedDataTransfer.options.append(ft.dropdown.Option(SpeedBT))
        # Add the COMPORTS and speeds to the dropdown USB devices
        for PORTUSB in PrinterBraille.Update_Ports():
            MenuPuertosCOM.options.append(ft.dropdown.Option(PORTUSB))
        for SPEEDUSB in PrinterBraille.Speeds:
            MenuVelocidades.options.append(ft.dropdown.Option(SPEEDUSB))

    def show_bs(e):
        bs.open = True
        bs.update()

    def close_bs(e):
        bs.open = False
        bs.update()
    # button connect device USB
    def Btn_Conectar(e):
        if PrinterBraille.Connected:
            PrinterBraille.DisconnectPrinter()
            if not PrinterBraille.Connected:
                BotonConectar.tooltip = "disconnected"
                BotonConectar.icon = ft.icons.USB_OFF
                BotonConectar.bgcolor = ft.colors.GREEN_100
                
                TerminalConexion.value = "Device disconnected"
            else:
                TerminalConexion.value = "The conexion is not finished"
        else:
            PrinterBraille.ConnectPrinterByPort(
                MenuPuertosCOM.value, MenuVelocidades.value)
            if PrinterBraille.Connected:
                BotonConectar.tooltip = "Conected"
                BotonConectar.icon = ft.icons.USB
                BotonConectar.bgcolor = ft.colors.BLUE_200

                TerminalConexion.value = "Conected at: " + MenuPuertosCOM.value + \
                    " whit the speed: " + MenuVelocidades.value + " bauds"
            else:
                TerminalConexion.value = "connection error"
        page.update()
    # button connect device Bluetooth
    def conect_BTDevice(e):
        NameDeviceSelected3 = Devices.value
        try:
            conexion3 = sqlite3.connect('Database/MyDataBase.sqlite3')
            cursor3 = conexion3.cursor()
            cursor3.execute("SELECT * FROM Devices")
            DevicesList3 = cursor3.fetchall()
            # Show the COMPORT and the Speed with the selected device
            for Device3 in DevicesList3:
                if Device3[1] == NameDeviceSelected3:
                    PortBTSelect = Device3[2] # Port
                    SpeedBTSelect = Device3[3]# Speed
                    break
        
            if PrinterBraille.Connected:
                PrinterBraille.DisconnectPrinter()
                if not PrinterBraille.Connected:
                    BtnConectDevice.tooltip = "disconnected"
                    BtnConectDevice.icon = ft.icons.BLUETOOTH_DISABLED
                    BtnConectDevice.bgcolor = ft.colors.WHITE24
                    TerminalConexion.value = "Device disconnected"
                else:
                    TerminalConexion.value = "The conexion is not finished"
            else:
                PrinterBraille.ConnectPrinterByPort(
                    PortBTSelect, str(SpeedBTSelect))
                if PrinterBraille.Connected:
                    BtnConectDevice.tooltip = "Conected"
                    BtnConectDevice.icon = ft.icons.BLUETOOTH_CONNECTED
                    BtnConectDevice.bgcolor = ft.colors.BLUE_300
                    TerminalConexion.value = "Conected at: " + PortBTSelect+ \
                        " whit the speed: " + str(SpeedBTSelect) + " bauds"
                else:
                    TerminalConexion.value = "connection error"
        except Exception as ex:
            print("Error al abrir la base de datos:", ex)
        page.update()
    # button solenoid
    def Btn_Solenoid(e):
        if PrinterBraille.Connected:
            if not PrinterBraille.SolenoidState:
                
                BotonSolenoid.tooltip = "solenoid activated"
                #BotonSolenoid.icon = ft.icons.LIGHT_MODE_OUTLINED
                BotonSolenoid.bgcolor = ft.colors.BLUE_200
                PrinterBraille.DeviceSerial.write('F:500'.encode('utf-8'))
                PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
                page.update()
                TerminalConexion.value = PrinterBraille.DataRead()
                PrinterBraille.SolenoidState = not PrinterBraille.SolenoidState
                BotonSolenoid.tooltip = "solenoid deactivated"
                BotonSolenoid.bgcolor = ft.colors.GREEN_100
                PrinterBraille.SolenoidState = not PrinterBraille.SolenoidState
        else:
            show_bs(e)
            TerminalConexion.value = "!NO CONECTADO!"
        page.update()
    # button SolenoidBT
    def Btn_SolenoidBT(e):
        if PrinterBraille.Connected:
            if not PrinterBraille.SolenoidState:
                BotonSolenoidBT.tooltip = "solenoid activated"
                BotonSolenoidBT.bgcolor = ft.colors.BLUE_200
                PrinterBraille.DeviceSerial.write('F:500'.encode('utf-8'))
                PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
                page.update()
                TerminalConexion.value = PrinterBraille.DataRead()
                PrinterBraille.SolenoidState = not PrinterBraille.SolenoidState
                BotonSolenoidBT.tooltip = "solenoid deactivated"
                BotonSolenoidBT.bgcolor = ft.colors.WHITE24
                PrinterBraille.SolenoidState = not PrinterBraille.SolenoidState
        else:
            show_bs(e)
            TerminalConexion.value = "!NO CONECTADO!"
        page.update()
    # button led
    def Btn_LED(e):
        if PrinterBraille.Connected:
            if not PrinterBraille.LedState:
                BotonLed.tooltip = "Led ON"
                BotonLed.icon = ft.icons.LIGHT_MODE_OUTLINED
                BotonLed.bgcolor = ft.colors.BLUE_200
                PrinterBraille.DeviceSerial.write('A'.encode('utf-8'))
                PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))

                TerminalConexion.value = PrinterBraille.DataRead()
                PrinterBraille.LedState = not PrinterBraille.LedState
            else:
                BotonLed.tooltip = "Led OFF"
                BotonLed.icon = ft.icons.LIGHT_MODE
                BotonLed.bgcolor = ft.colors.GREEN_100
                PrinterBraille.DeviceSerial.write('B'.encode('utf-8'))
                PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
                TerminalConexion.value = PrinterBraille.DataRead()
                PrinterBraille.LedState = not PrinterBraille.LedState
        else:
            show_bs(e)
            TerminalConexion.value = "!NO CONECTADO!"
        page.update()
    # button led Bluetooth
    def led_BTDevice(e):
        if PrinterBraille.Connected:
            if not PrinterBraille.LedState:
                BtnLedDeviceBT.tooltip = "Led ON"
                BtnLedDeviceBT.icon = ft.icons.TOGGLE_ON_ROUNDED
                
                BtnLedDeviceBT.bgcolor = ft.colors.BLUE_200
                PrinterBraille.DeviceSerial.write('A'.encode('utf-8'))
                PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))

                TerminalConexion.value = PrinterBraille.DataRead()
                PrinterBraille.LedState = not PrinterBraille.LedState
            else:
                BtnLedDeviceBT.tooltip = "Led OFF"
                BtnLedDeviceBT.icon = ft.icons.TOGGLE_ON_OUTLINED
                BtnLedDeviceBT.bgcolor = ft.colors.WHITE24
                PrinterBraille.DeviceSerial.write('B'.encode('utf-8'))
                PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
                TerminalConexion.value = PrinterBraille.DataRead()
                PrinterBraille.LedState = not PrinterBraille.LedState
        else:
            show_bs(e)
            TerminalConexion.value = "!NO CONECTADO!"
        page.update()
    # button send text USB
    def Btn_Enviar(e):
        if PrinterBraille.Connected:
            for elemento in TextToSend.value:
                PrinterBraille.DeviceSerial.write(elemento.encode('utf-8'))
            PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
            TerminalConexion.value = PrinterBraille.DataRead()
        else:
            show_bs(e)
            TerminalConexion.value = "!NO CONECTADO!"
        page.update()

    # button send text Bluetooth
    def Btn_EnviarBT(e):
        if PrinterBraille.Connected:
            for elemento in TextToSendBT.value:
                PrinterBraille.DeviceSerial.write(elemento.encode('utf-8'))
            PrinterBraille.DeviceSerial.write('\n'.encode('utf-8'))
            TerminalConexion.value = PrinterBraille.DataRead()
        else:
            show_bs(e)
            TerminalConexion.value = "!NO CONECTADO!"
        page.update()
    def conectaServidor(e):
        NameDeviceSelectedWiFi = DevicesWiFi.value
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
            
            if not PrinterBraille.ServerState:
                # client(host=SERVER_HOST, port=int(SERVER_PORT), auto_open=True)
                client.host = SERVER_HOST
                client.port = int(SERVER_PORT)
                client.auto_open = True
                print(client.host, client.port)
                if client.open():
                    TerminalConexion.value = "Servidor Conectado correctamemnte..." + \
                        "\n" + SERVER_HOST + " " + SERVER_PORT
                    PrinterBraille.ServerState = True
                    ConectarServidor.icon = ft.icons.SIGNAL_WIFI_4_BAR
                    ConectarServidor.tooltip = "Desconectar"
                    ConectarServidor.bgcolor = ft.colors.GREEN_500
                else:
                    TerminalConexion.value = "Servidor No conectado --> " + \
                        SERVER_HOST + " Puerto: " + str(SERVER_PORT)
                    PrinterBraille.ServerState = False
                    ConectarServidor.icon = ft.icons.SIGNAL_WIFI_CONNECTED_NO_INTERNET_4
            else:
                ConectarServidor.icon = ft.icons.SIGNAL_WIFI_CONNECTED_NO_INTERNET_4
                ConectarServidor.tooltip = "Conectar"
                ConectarServidor.bgcolor = ft.colors.BLUE_GREY
                TerminalConexion.value = "Servidor desconectado correctamente"
                PrinterBraille.ServerState = False
                client.close()
        except Exception as ex:
            print("Error al abrir la base de datos:", ex)   
        page.update()

    def BtnTCP(e):
        if PrinterBraille.ServerState:
            if not PrinterBraille.LedTCP_State:
                BotonTCP.icon = ft.icons.LIGHT_MODE
                BotonTCP.tooltip = "Apagar LED"
                BotonTCP.bgcolor = ft.colors.GREEN_500
                client.write_single_register(0, 1)
                PrinterBraille.LedTCP_State = not PrinterBraille.LedTCP_State
            else:
                BotonTCP.icon = ft.icons.LIGHT_MODE
                BotonTCP.bgcolor = ft.colors.BLUE_GREY
                BotonTCP.tooltip = "Encender LED"
                client.write_single_register(0, 0)
                PrinterBraille.LedTCP_State = not PrinterBraille.LedTCP_State
        else:
            show_bs(e)
            TerminalConexion.value = "!NO CONECTADO!"
        page.update()

    def slider_changed(e):
        if PrinterBraille.ServerState:
            Valor = int(Barra.value)
            if (Valor < 65536):
                client.write_single_register(1, Valor)
        else:
            show_bs(e)
            TerminalConexion.value = "!NO CONECTADO!"
        page.update()
    
    def EscribeMultiplesRegistros(e):
        if PrinterBraille.ServerState:
            Values = Value.value.split(",")
            Values = [int(i) for i in Values]
            if len(Values) > 1:
                client.write_multiple_registers(int(Addres.value), Values)
                TerminalConexion.value = "Addres -> " + \
                    Addres.value + " Values -> " + str(Values)
            else:
                client.write_single_register(int(Addres.value), Values[0])
                TerminalConexion.value = "Addres -> " + \
                    Addres.value + " Value -> " + str(Values[0])
        else:
            show_bs(e)
            TerminalConexion.value = "!NO CONECTADO!"
        page.update()
    # function to open the dialog FilesGoogleDriveDialog
    def open_FilesGoogleDrive(e):
        page.dialog = FilesGoogleDriveDialog
        FilesGoogleDriveDialog.open = True
        try:
            page.update()
            ShowListFilesGoogleDrive(e)
        except Exception as ex:
            print("Error al actualizar la pagina: ", ex)
    # function to open the dialog BTParametersDialog
    def open_BTParameters(e):
        page.dialog = BTParametersDialog
        BTParametersDialog.open = True
        try:
            page.update()
        except Exception as ex:
            print("Error al actualizar la pagina: ", ex)
    # function to open the dialog WiFiParametersDialog
    def open_WiFiParameters(e):
        page.dialog = WiFiParametersDialog
        WiFiParametersDialog.open = True
        try:
            page.update()
        except Exception as ex:
            print("Error al actualizar la pagina: ", ex)
    # function to open the dialog testDeviceDialog
    def open_TestDevice(e):
        page.dialog = TestDeviceDialog
        TestDeviceDialog.open = True
        try:
            page.update()
        except Exception as ex:
            print("Error al actualizar la pagina: ", ex)
    # function to close the dialog testDeviceDialog
    def close_TestDevice(e):
        TestDeviceDialog.open = False
        page.update()
    # function to close the dialog BTParametersDialog
    def close_dlg(e):
        BTParametersDialog.open = False
        page.update()
    # function to close the dialog WiFiParametersDialog
    def close_dlgWiFi(e):
        WiFiParametersDialog.open = False
        page.update()
    # function to close the dialog FilesGoogleDriveDialog
    def close_dlgFilesGoogleDrive(e):
        FilesGoogleDriveDialog.open = False
        page.update()
    def save_BTDevice(e):
        try:
            conexion2 = sqlite3.connect('Database/MyDataBase.sqlite3')
            cursor2 = conexion2.cursor()
            cursor2.execute(
                "CREATE TABLE IF NOT EXISTS Devices (id INTEGER PRIMARY KEY, name TEXT, port TEXT, speed INTEGER)")
            cursor2.execute("INSERT INTO Devices VALUES (NULL,?,?,?)",
                           (NameDevice.value, PortBluetooth.value, int(SpeedDataTransfer.value)))
            conexion2.commit()
            cursor2.execute("SELECT * FROM Devices")
            rows = cursor2.fetchall()
            row = rows[len(rows)-1]
            print("ID -> " + str(row[0]) + " Name -> " + row[1] +
                  " Port -> " + row[2] + " Speed -> " + str(row[3]))
            Devices.options.append(ft.dropdown.Option(row[1]))
            DeleteDeviceBT.disabled = False
            print("Device Saved")
        except Exception as ex:
            print("Error al abrir la base de datos:", ex)
        page.update()
    # function to save the device WiFi in the database
    # the Table WiFiDevices content is: ID, Name, IPaddress and Port
    def save_WiFiDevice(e):
        try:
            conexionWifi = sqlite3.connect('Database/MyDataBase.sqlite3')
            cursorWiFi = conexionWifi.cursor()
            cursorWiFi.execute(
                "CREATE TABLE IF NOT EXISTS WiFiDevices (id INTEGER PRIMARY KEY, name TEXT, ip TEXT, port INTEGER)")
            cursorWiFi.execute("INSERT INTO WiFiDevices VALUES (NULL,?,?,?)",
                           (NameDeviceWiFi.value, IPaddress.value, int(PortWiFi.value)))
            conexionWifi.commit()
            cursorWiFi.execute("SELECT * FROM WiFiDevices")
            rows = cursorWiFi.fetchall()
            row = rows[len(rows)-1]
            print("ID -> " + str(row[0]) + " Name -> " + row[1] +
                  " IP -> " + row[2] + " Port -> " + str(row[3]))
            DevicesWiFi.options.append(ft.dropdown.Option(row[1]))
            DeleteDeviceWiFi.disabled = False
            print("Device Saved")
        except Exception as ex:
            print("Error al abrir la base de datos:", ex)
        page.update()
    # function to find in the bluetooth devices dropdown
    def find_optionBT(option_name):
        for option in Devices.options:
            if option_name == option.key:
                return option
        return None
    # function to find in the WiFi devices dropdown
    def find_optionWiFi(option_name):
        for optionWifi in DevicesWiFi.options:
            if option_name == optionWifi.key:
                return optionWifi
        return None
    def delete_BTDevice(e):
        try:       
            conexion4 = sqlite3.connect('Database/MyDataBase.sqlite3')
            cursor4 = conexion4.cursor()
            cursor4.execute("SELECT * FROM Devices")
            DevicesList4 = cursor4.fetchall()
            # if devices is more than 0 Delete the selected device from the list of devices
            if len(DevicesList4) > 0:
                cursor4.execute("DELETE FROM Devices WHERE name = " + "'" + Devices.value + "'")
                conexion4.commit()
                option = find_optionBT(Devices.value)
                if option != None:
                    Devices.options.remove(option)
                print("Device Deleted")
                # Delete content of the table
                TableDevices.rows.clear()
                if len(Devices.options) == 0:
                    DeleteDeviceBT.disabled = True
            else:
                print("No devices to delete")
        except Exception as ex:
            print("Error al abrir la base de datos:", ex)
        page.update()
    # function to delete the device WiFi from the database
    def delete_WiFiDevice(e):
        try:       
            conexionWifidel = sqlite3.connect('Database/MyDataBase.sqlite3')
            cursorFifedel = conexionWifidel.cursor()
            cursorFifedel.execute("SELECT * FROM WiFiDevices")
            DevicesListWifiDevices = cursorFifedel.fetchall()
            # if devices is more than 0 Delete the selected device from the list of devices
            if len(DevicesListWifiDevices) > 0:
                cursorFifedel.execute("DELETE FROM WiFiDevices WHERE name = " + "'" + DevicesWiFi.value + "'")
                conexionWifidel.commit()
                optionWifi = find_optionWiFi(DevicesWiFi.value)
                if optionWifi != None:
                    DevicesWiFi.options.remove(optionWifi)
                print("Device Deleted")
                # Delete content of the table
                TableDevicesWiFi.rows.clear()
                if len(DevicesWiFi.options) == 0:
                    DeleteDeviceWiFi.disabled = True
            else:
                print("No devices to delete")
        except Exception as ex:
            print("Error al abrir la base de datos:", ex)
        page.update()
    def ShowSelectedDevice(e):
        NameDeviceSelected3 = Devices.value
        print("Selected destination:" + NameDeviceSelected3)
        try:
            conexion3 = sqlite3.connect('Database/MyDataBase.sqlite3')
            cursor3 = conexion3.cursor()
            cursor3.execute("SELECT * FROM Devices")
            DevicesList3 = cursor3.fetchall()
            # Show the COMPORT and the Speed with the selected device
            for Device3 in DevicesList3:
                if Device3[1] == NameDeviceSelected3:
                    # Delete content of the table
                    TableDevices.rows.clear()
                    # Add the new content
                    TableDevices.rows.append(ft.DataRow(
                        cells=[
                                ft.DataCell(ft.Text(Device3[1])), # Name
                                ft.DataCell(ft.Text(Device3[2])), # Port
                                ft.DataCell(ft.Text(str(Device3[3]))) # Speed
                            ]
                        )
                    )
                    print(TerminalConexion.value)
                    break
        except Exception as ex:
            print("Error al abrir la base de datos:", ex)
        page.update()
    # function to show the device WiFi selected
    def ShowSelectedDeviceWiFi(e):
        NameDeviceSelectedWiFi = DevicesWiFi.value
        print("Selected destination:" + NameDeviceSelectedWiFi)
        try:
            conexionWiFi = sqlite3.connect('Database/MyDataBase.sqlite3')
            cursorWiFi = conexionWiFi.cursor()
            cursorWiFi.execute("SELECT * FROM WiFiDevices")
            DevicesListWiFi = cursorWiFi.fetchall()
            # Show the IP and the Port with the selected device
            for DeviceWiFi in DevicesListWiFi:
                if DeviceWiFi[1] == NameDeviceSelectedWiFi:
                    # Delete content of the table
                    TableDevicesWiFi.rows.clear()
                    # Add the new content
                    TableDevicesWiFi.rows.append(ft.DataRow(
                        cells=[
                                ft.DataCell(ft.Text(DeviceWiFi[1])), 
                                ft.DataCell(ft.Text(DeviceWiFi[2])), 
                                ft.DataCell(ft.Text(str(DeviceWiFi[3])))
                            ]
                        )
                    )
                    print(TerminalConexion.value)
                    break
        except Exception as ex:
            print("Error al abrir la base de datos:", ex)
        page.update()
    
    
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        bgcolor=ft.colors.RED_50,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME_OUTLINED,
                selected_icon=ft.icons.HOME,
                label="Inicio"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.USB_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.USB_OUTLINED),
                label="USB"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.BLUETOOTH,
                selected_icon_content=ft.Icon(ft.icons.BLUETOOTH),
                label_content=ft.Text("Bluetooth")
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SIGNAL_WIFI_STATUSBAR_NULL,
                selected_icon_content=ft.Icon(
                    ft.icons.SIGNAL_WIFI_STATUSBAR_4_BAR_OUTLINED),
                label_content=ft.Text("WiFi")
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Cnfiguración")
            )
        ],
        # lambda e: print("Selected destination:", e.control.selected_index) #CambiaCuerpo, #lambda e: t.selected_index = e.control.selected_index, #print("Selected destination:", e.control.selected_index),
        on_change=route_change
    )

    # Add a textfield to the container
    TextToTranslate = ft.TextField(
        # set the label
        label = "Translated", 
        # set number of lines
        multiline = True, 
        # set the initial value
        value="...",
        # set max lines
        max_lines=18,
        # set the text style
        #text_style = ft.TextStyle(color=ft.colors.WHITE, size=20, weight=ft.FontWeight.BOLD, font_family="Arial"),
        # set the align of the text
        #text_align=ft.alignment.center
        #text_align: TextAlign = TextAlign.NONE,
        )
    # Enter the text to be translated
    TextInput = ft.TextField(
        # set the label
        label = "Text to be translated", 
        # set number of lines
        multiline = True, 
        # set the initial value
        value="...",
        # set max lines
        max_lines=18
        )
    
    # Button to translate the text
    BtnTranslate = ft.FloatingActionButton(
        icon=ft.icons.TRANSLATE, 
        on_click=TranslateText)
    # Button to clear the text
    BtnClear = ft.FloatingActionButton(
        icon=ft.icons.CLEAR,
        on_click=ClearText)
    # Button to select the file to be translated, this file is uploaded in Google Drive
    BtnSelectFile = ft.FloatingActionButton(
        icon=ft.icons.FILE_OPEN_SHARP,
        on_click=lambda e: print(app.Selected_File(e))
    )
    # Button to open the alert dialog
    BtnOpenAlertFilesGD = ft.FloatingActionButton(
        icon=ft.icons.ADD_TO_DRIVE_ROUNDED,
        on_click=open_FilesGoogleDrive)
    # Button to close the alert dialog
    BtnClose_dlgFilesGoogleDrive = ft.FloatingActionButton(
        icon=ft.icons.CLOSE,
        on_click=close_dlgFilesGoogleDrive
        )
    # Datatable to show the files in Google Drive
    TableShowFilesGD = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text(" ")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Size")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Type"))
        ]

    )
    # Textfield to search word 
    SearchWordGD=ft.TextField(hint_text="Search tasks", on_change=SearchWord, expand=True)
    # Textfield to add new file
    TextfieldAddFileGD = ft.TextField(hint_text="What needs to be done?", expand=True)
    # Button to add new File
    ButtonAddFileGD=ft.FloatingActionButton(icon=ft.icons.ADD, on_click=AddFileGD) 
    # Alert dialog to show the files in Google Drive
    FilesGoogleDriveDialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Files in Google Drive"),
        content = ft.Column(
            [
                ft.Text("Select the file to be translated"),
                ft.Row([
                        TextfieldAddFileGD, 
                        ButtonAddFileGD,
                        SearchWordGD
                        ]),
                app,
                ft.Row([BtnClose_dlgFilesGoogleDrive, BtnSelectFile])
            ]
        )
    )
    
    ContLeft = ft.Container(  # Container de INICIO
        # Add a textfield to the container
        content=ft.Column(
            [
                TextInput
            ]),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.AMBER,
        expand=1,
        ink=True,
        border_radius=10,
        on_click=lambda e: print("Clickable transparent with Ink clicked!")
    )
    ContRight = ft.Container(  # Container de INICIO
        # Add a textfield to the container
        content=ft.Column(
            [
                TextToTranslate
            ]),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.AMBER,
        expand=1,
        ink=True,
        border_radius=10,
        on_click=lambda e: print("Clickable transparent with Ink clicked!")
    )

    c1 = ft.Container(  # Container de INICIO
        # Add a textfield to the container
        content=ft.Row(
            [
                ContLeft, ft.Column([BtnOpenAlertFilesGD, BtnTranslate, BtnClear]), ContRight
            ]),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.AMBER,
        expand=1,
        ink=True,
        border_radius=10,
        on_click=lambda e: print("Clickable transparent with Ink clicked!")
    )

    Parametros = ft.Text(value="Parámetros", color="green", size=36)
    BotonConectar = ft.FloatingActionButton(
        icon=ft.icons.USB_OFF, 
        tooltip="disconnected",
        bgcolor=ft.colors.GREEN_100,
        on_click=Btn_Conectar
        )
    MenuPuertosCOM = ft.Dropdown(
        label="Puertos COM", hint_text="Seleccione el puerto a conectar")
    MenuVelocidades = ft.Dropdown(
        label="Velocidades", hint_text="Seleccione la velocidad de transmición")
    TerminalConexion = ft.TextField(
        label="Terminal", multiline=True, tooltip="Terminal")
    BotonLed = ft.FloatingActionButton(
        icon=ft.icons.LIGHT_MODE,
        bgcolor=ft.colors.GREEN_100,
        tooltip="Led OFF",
        shape=ft.RoundedRectangleBorder(radius=5),
        on_click=Btn_LED,
        width=100,
        mini=True
    )
    TextToSend = ft.TextField(
        label="Ingrese texto a enviar..",
        multiline=True,
        value="...",
    )
    BotonEnviar = ft.FloatingActionButton(
        icon=ft.icons.SEND,
        on_click=Btn_Enviar,
        bgcolor=ft.colors.BLUE_GREY,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=100,
        mini=True,
        text="Enviar"
    )
    # Button solenoid
    BotonSolenoid = ft.FloatingActionButton(
        #icon=ft.icons.SEND,
        on_click=Btn_Solenoid,
        bgcolor=ft.colors.GREEN_100,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=100,
        mini=True,
        text="S",
        tooltip="solenoid deactivated"
    )
    c2 = ft.Container(  # Container de Conexion USB
        content=ft.Column([Parametros, MenuPuertosCOM, MenuVelocidades, ft.Row(
            [BotonConectar, BotonLed, BotonSolenoid]), TextToSend, BotonEnviar]),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.GREEN_100,
        expand=1,
        border_radius=10,
        ink=True,
        #on_click=lambda e: print("Clickable without Ink clicked!")
    )
    
    NameDevice = ft.TextField(
        label="Name Device", hint_text="Name of the device")
    AddDeviceBluetooth = ft.FloatingActionButton(
        icon=ft.icons.ADD, text="Add Bluetooth Device", on_click=open_BTParameters)
    DeleteDeviceBT = ft.FloatingActionButton(
        icon=ft.icons.DELETE, text="Delete Bluetooth Device", on_click=delete_BTDevice)
    PortBluetooth = ft.Dropdown(
        label="Puertos Bluetooth", hint_text="Seleccione el puerto a conectar")
    SpeedDataTransfer = ft.Dropdown(
        label="Transfer Speed", hint_text="choose the speed of data transfer")
    BtnSaveDevice = ft.FloatingActionButton(
        icon=ft.icons.SAVE, tooltip="Save Bluetooth Device", on_click=save_BTDevice, expand=1)
    ButtonCloseDialog = ft.FloatingActionButton(
        icon=ft.icons.CLOSE, tooltip="Close", expand=1, on_click=close_dlg)
    BTParametersDialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add Bluetooth Device"),
        content=ft.Column([NameDevice, PortBluetooth, SpeedDataTransfer, ft.Row(
            [BtnSaveDevice, ButtonCloseDialog])])
    )
    Devices = ft.Dropdown(
        label="Devices", hint_text="choose device", on_change=ShowSelectedDevice)    
    TableDevices = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Device name")),
                ft.DataColumn(ft.Text("Port")),
                ft.DataColumn(ft.Text("Speed")),
            ]
        )
    
    # Button for test device
    TestDevice = ft.FloatingActionButton(
        icon=ft.icons.SETTINGS, text="Test Device", on_click=open_TestDevice)
    # Button for conect to device bluetooth
    BtnConectDevice = ft.FloatingActionButton(
        icon=ft.icons.BLUETOOTH_DISABLED, 
        on_click=conect_BTDevice,
        tooltip="disconnected",
        bgcolor=ft.colors.WHITE24
        )
    # Button for Led on/off
    BtnLedDeviceBT = ft.FloatingActionButton(
        icon=ft.icons.TOGGLE_ON_OUTLINED,   
        on_click=led_BTDevice,
        tooltip="Led OFF",
        bgcolor=ft.colors.WHITE24
        )
    # Button for close dialog
    BtnCloseTestDevice = ft.FloatingActionButton(   
        icon=ft.icons.CLOSE,
        on_click=close_TestDevice,
        tooltip="Close",
        bgcolor=ft.colors.WHITE24
        )
    # Button for solenoid on/off
    BotonSolenoidBT = ft.FloatingActionButton(
        #icon=ft.icons.SEND,
        text="S",
        on_click=Btn_SolenoidBT,
        bgcolor=ft.colors.WHITE24,
        tooltip="solenoid deactivated"
    )
    # Button for send text to bluetooth device
    BtnSendTextBT = ft.FloatingActionButton(
        icon=ft.icons.SEND,
        on_click=Btn_EnviarBT,
        bgcolor=ft.colors.WHITE24,
        tooltip="Send text"
    )
    # Text to send to bluetooth device
    TextToSendBT = ft.TextField(
        label="Ingrese texto a enviar..",
        multiline=True,
        value="...",
    )
    # Alert Dialog for Test Devices Bluetooth
    TestDeviceDialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Test Device"),
        content=ft.Column([BtnConectDevice, ft.Row([BtnLedDeviceBT, BotonSolenoidBT]), TextToSendBT, BtnSendTextBT, BtnCloseTestDevice])
    )
    
    c3 = ft.Container(  # Container de Conexion Bluetooth
        content=ft.Column([Devices, TableDevices, ft.Row([AddDeviceBluetooth, DeleteDeviceBT, TestDevice]) ]),
        margin=10,
        padding=10,
        alignment=ft.alignment.top_right,
        bgcolor=ft.colors.CYAN_200,
        expand=1,
        border_radius=10,
        ink=True,
        on_click=lambda e: print("Clickable with Ink clicked!")
    )

    # Name device WiFi
    NameDeviceWiFi = ft.TextField( 
        label="Name Device", hint_text="Name of the device")
    # Parameters for connect to server
    IPaddress = ft.TextField(label="Direccion IP")
    PortWiFi = ft.TextField(value="502", label="Puerto IP")
    
    # Add device WiFi
    AddDeviceWiFi = ft.FloatingActionButton(
        icon=ft.icons.ADD, text="Add WiFi Device", on_click=open_WiFiParameters)
    # Button for save device WiFi
    BtnSaveDeviceWiFi = ft.FloatingActionButton(
        icon=ft.icons.SAVE, tooltip="Save WiFi Device", on_click=save_WiFiDevice, expand=1)
    # Button for close dialog
    ButtonCloseDialogWiFi = ft.FloatingActionButton(
        icon=ft.icons.CLOSE, tooltip="Close", expand=1, on_click=close_dlgWiFi)
    # Delete device WiFi    
    DeleteDeviceWiFi = ft.FloatingActionButton(
        icon=ft.icons.DELETE, text="Delete WiFi Device", on_click=delete_WiFiDevice)
    # Show devices WiFi
    DevicesWiFi = ft.Dropdown(
        label="Devices", hint_text="choose device", on_change=ShowSelectedDeviceWiFi)
    # Table for show devices WiFi   
    TableDevicesWiFi = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Device name")),
                ft.DataColumn(ft.Text("IP")),
                ft.DataColumn(ft.Text("Port")),
            ]
        )
    # Alert Dialog for add device WiFi
    WiFiParametersDialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add WiFi Device"),
        content=ft.Column([Parametros,NameDeviceWiFi, IPaddress, PortWiFi, ft.Row(
            [BtnSaveDeviceWiFi, ButtonCloseDialogWiFi])])
    )
    ConectarServidor = ft.FloatingActionButton(
        on_click=conectaServidor,
        icon=ft.icons.SIGNAL_WIFI_CONNECTED_NO_INTERNET_4,
        bgcolor=ft.colors.BLUE_GREY,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=100,
        height=50,
        mini=True,
        tooltip="Desconectado"
    )
    BotonTCP = ft.FloatingActionButton(
        icon=ft.icons.LIGHT_MODE,
        tooltip="Encender LED",
        bgcolor=ft.colors.BLUE_GREY,
        on_click=BtnTCP,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=100,
        height=50,
        mini=True,

    )
    Barra = ft.Slider(min=0, max=65536, divisions=16,
                      label="{value}", on_change=slider_changed)
    BotonP = ft.FloatingActionButton(
        icon=ft.icons.SEND,
        on_click=EscribeMultiplesRegistros,
        bgcolor=ft.colors.GREEN_50,
        shape=ft.RoundedRectangleBorder(radius=5),
        
        mini=True,
        tooltip="Enviar"
    )
    Addres = ft.TextField(value="0", expand=1, tooltip="Address")
    Value = ft.TextField(value="0", expand=1, tooltip="Value")
    Tablas = ft.Column([
        ft.Row([ft.Text(value="ID", width=35), ft.Text(
            value="Address", expand=1), ft.Text(value="Value", expand=1)]),
        ft.Row([ft.Text(value="1", width=35), Addres, Value])
    ], width=350, height=100)

    c4 = ft.Container(  # Container de Conexion WiFi
        content=ft.Column(
            [DevicesWiFi, TableDevicesWiFi, ft.Row([AddDeviceWiFi, DeleteDeviceWiFi])]),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        border_radius=10,
        ink=True,
        expand=1,
        on_click=lambda e: print("Clickable transparent with Ink clicked!")
    )
    C4_1 = ft.Container(  # Container de Conexion WiFi
        content=ft.Column([ft.Row(
            [ConectarServidor, BotonTCP]), Barra, Tablas, BotonP]),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        border_radius=10,
        ink=True,
        expand=1,
        on_click=lambda e: print("Clickable transparent with Ink clicked!")
    )

    c5 = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.BLUE, ft.colors.BLACK]
        ),
        content=ft.Text("Clickable transparent with Ink"),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        expand=1,
        border_radius=10,
        ink=True,
        on_click=lambda e: print("Clickable transparent with Ink clicked!")
    )

    PaginaInicio = ft.View(
        "/",
        [
            ft.AppBar(title=ft.Text("Inicio"),
                      bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Row([rail, ft.VerticalDivider(width=1), ft.Column([ft.Row([c1], expand=True), TerminalConexion], expand=True)],
                   expand=True
                   )
        ],
        bgcolor=ft.colors.BLUE_50
    )
    PaginaUSB = ft.View(
        "/USB",
        [
            ft.AppBar(title=ft.Text("Conexion USB"),
                      bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Row(
                [rail, ft.VerticalDivider(width=1), ft.Column(
                    [c2, TerminalConexion], expand=True)],
                expand=True
            )
        ],
        bgcolor=ft.colors.BLUE_50
    )
    PaginaBluetooth = ft.View(
        "/Bluetooth",
        [
            ft.AppBar(title=ft.Text("Conexion Bluetooth"),
                      bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Row([rail, ft.VerticalDivider(width=1), ft.Column([c3, TerminalConexion], expand=True)],
                   expand=True
                   )
        ],
        bgcolor=ft.colors.BLUE_50
    )
    PaginaWiFi = ft.View(
        "/Wifi",
        [
            ft.AppBar(title=ft.Text("Conexion WiFi"),
                      bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Row([rail, ft.VerticalDivider(width=1), ft.Column([ft.Row([c4,C4_1], expand=True), TerminalConexion], expand=True)],
                   expand=True
                   )
        ],
        bgcolor=ft.colors.BLUE_50
    )
    PaginaConfiguracion = ft.View(
        "/Configuracion",
        [
            ft.AppBar(title=ft.Text("Configuracion"),
                      bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Row([rail, ft.VerticalDivider(width=1), ft.Column([c5, TerminalConexion], expand=True)],
                   expand=True
                   )
        ],
        bgcolor=ft.colors.BLUE_50
    )

    bs = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("!IMPRESORA NO CONECTADA¡", color="red",
                            size=20, font_family="Helvetica"),
                    ft.ElevatedButton("Cerrar", on_click=close_bs),
                ],
                tight=True,
            ),
            padding=10
        )
    )
   
    InitFunction(page)
    page.overlay.append(bs)
    page.scroll = "adaptive"
    
    page.on_route_change = route_change
    page.on_keyboard_event = on_keyboard
    page.go(page.route)
ft.app(target=main)  # , view=ft.WEB_BROWSER)