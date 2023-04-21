from flet import *
from app_layout import AppLayout
from FilesUploaded import FilesGoogleDrive
from SettingsPrinter import TabSettings
from BrailleG1 import Translate_To_Braiile
import ManageGoogleDrive
import time

class Printer_Braille_2023(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.fonts = {"Pacifico": "/Pacifico-Regular.ttf"}
        self.page.title = "Printer Braille 2023"
        self.page.scroll="adaptive"
        self.page.window_width = 1500
        self.page.window_height = 610
        self.page.window_min_width = 400
        self.page.window_min_height = 400
        self.page.on_resize = self.page_resize
        self.ListOfFiles = FilesGoogleDrive()
        self.File_Properties = ManageGoogleDrive.Get_ListFiles()
        self.SettingPrinterBraille = TabSettings(page)
        self.page.on_route_change = self.route_change
        self.appbar_items = [
            PopupMenuItem(text="Login"),
            PopupMenuItem(),  # divider
            PopupMenuItem(text="Settings")
        ]
        self.appbar = AppBar(
            #leading=Icon(icons.HOME),
            leading_width=100,
            center_title=False,
            toolbar_height=75,
            bgcolor=colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                Container(
                    content=PopupMenuButton(
                        items=self.appbar_items
                    ),
                    margin=margin.only(left=50, right=25)
                )
            ],
        )
        self.page.appbar = self.appbar
        self.TextToTranslate = TextField( # Add a textfield to the container
            # set the label
            label = "Translated", 
            # set number of lines
            multiline = True, 
            # set the initial value
            value="...",
            expand=True,
            border_width=0,
            text_style=TextStyle(weight=FontWeight.BOLD, color=colors.BLACK, size=24),
            on_change = lambda e: print("Change the text to translate")
        )
        self.ShowCoordinates = Text(
            value="X: 0, Y: 0, Bin: 000",
            size=20,
            color=colors.BLUE_GREY_500,
            weight=FontWeight.BOLD,
            width=400
        )
        self.Braille_Translator = Translate_To_Braiile(page, self.TextToTranslate, self.ShowCoordinates)
        self.TextInput = TextField( # Enter the text to be translated
            # set the label
            label = "Text to be translated", 
            # set number of lines
            multiline = True, 
            # set the initial value
            value="...",
            expand=True,
            border_width=0
        )
        self.TerminalConexion = TextField(
            label="Terminal", 
            multiline=True, 
            tooltip="Terminal",
            max_lines=2,
            min_lines=1
        )
        self.ContLeft = Container( #  
            # Add a textfield to the container
            content=Column(
                [
                    self.TextInput
                ]),
            gradient=LinearGradient(
                            begin=alignment.top_center,
                            end=alignment.bottom_center,
                            colors=[colors.WHITE, colors.BLUE_GREY_200]
                        ),
            margin=10,
            padding=10,
            alignment=alignment.center,
            expand=1,
            ink=True,
            border_radius=10,
            on_click=lambda e: print("Clickable transparent with Ink clicked!")
        )
        self.ContRight = Container(# 
            content = Column(# Add a textfield to the container
                [
                    self.TextToTranslate
                ]),
            margin=10,
            padding=10,
            alignment = alignment.center,
            gradient=LinearGradient(
                            begin=alignment.top_center,
                            end=alignment.bottom_center,
                            colors=[colors.WHITE, colors.BLUE_GREY_200]
                        ),
            expand = 1,
            ink = True,
            border_radius=10,
            on_click=lambda e: print("Clickable transparent with Ink clicked!")
        )
        self.SearchWordGD=TextField(# Textfield to search word 
            hint_text="Search files", 
            on_change=self.SearchWord, expand=True
        )
        self.BtnClose_dlgFilesGoogleDrive = FloatingActionButton(# Button to close the alert dialog
            icon=icons.CLOSE,
            on_click=self.close_dlgFilesGoogleDrive
        )
        self.BtnSelectFile = FloatingActionButton(# Button to select the file to be translated, this file is uploaded in Google Drive
            icon=icons.FILE_OPEN_SHARP,
            on_click=self.Fun_SelectFile
        )
        self.BtnOpenAlertFilesGD = FloatingActionButton(
            icon=icons.ADD_TO_DRIVE_ROUNDED,
            on_click=self.open_FilesGoogleDrive
        )
        self.FilesGoogleDriveDialog = AlertDialog(
            modal=True,
            title=Text("Files in Google Drive"),
            content = Column(
                [
                    Text("Select the file to be translated"),
                    Row([
                            self.SearchWordGD
                            ]),
                    self.ListOfFiles,
                    Row([self.BtnClose_dlgFilesGoogleDrive, self.BtnSelectFile])
                ]
            )
        )
        
        self.ProgresPrint = ProgressBar(
            value=0,
            color=colors.BLUE_GREY_500,
            expand=True
        )
        self.ProgresBar_DialogtoPrint = AlertDialog( # Alert dialog to show the progress of the printing process
            modal=True,
            title=Text("Printing..."),
            content = Column(
                [
                    Text("Please wait while the file is printed", size=20, color=colors.BLUE_GREY_500),
                    self.ProgresPrint,
                    self.ShowCoordinates,
                    FloatingActionButton(
                        icon=icons.CLOSE,
                        on_click=self.Fun_Close_ProgresBar_DialogtoPrint
                    )
                ]
            )
        )
        self.BtnTranslate = FloatingActionButton(
            icon=icons.TRANSLATE, 
            on_click=self.TranslateText
        )
        self.BtnPrint = FloatingActionButton(  # Button to print the text translated
            icon=icons.PRINT,
            on_click=self.Fun_Open_PrintTextTranslatedDialog
        )
        self.BtnClear = FloatingActionButton( # Button to clear the text
            icon=icons.CLEAR,
            on_click=self.ClearText
        )
        self.c1 = Container(  # Container for initial page 
            content=Row( # Add a textfield to the container
                [
                    self.ContLeft, Column([self.BtnOpenAlertFilesGD, self.BtnTranslate, self.BtnPrint ,self.BtnClear]), self.ContRight
                ]),
            margin=10,
            padding=10,
            alignment=alignment.center,
            bgcolor=colors.BLUE_GREY_200,
            expand=True,
            ink=True,
            border_radius=10,
            on_click=lambda e: print("Clickable transparent with Ink clicked!")
        )
        self.Page_Init = Column(
            [
                self.c1,
                self.SettingPrinterBraille.TerminalConnection
            ], 
            expand=True
        )
        self.Page_Settings = Column(
            [
                Container(content = self.SettingPrinterBraille, expand=True), 
                self.SettingPrinterBraille.TerminalConnection
            ],
            expand=True
        )
        self.page.update()
    def build(self):
        self.layout = AppLayout()
        return self.layout
    def initialize(self):
        self.page.go("/")
    def route_change(self, e):
        troute = TemplateRoute(self.page.route)
        self.page.views.clear()
        if troute.match("/"):
            self.SetTitleAppBar(e, "HOME")
            self.appbar.leading = Icon(icons.HOME)
            self.page.views.append(
            View(
                "/",
                [
                    self.appbar, Row([self.layout,  self.Page_Init], expand=True) 
                ],
                padding=padding.all(0),
                bgcolor=colors.WHITE,
                auto_scroll=True
            )
        )
        elif troute.match("/Settings"):
            #self.SettingPrinterBraille.tab_change(e)
            self.SetTitleAppBar(e, "Settings")
            self.appbar.leading = Icon(icons.SETTINGS)
            self.page.views.append(
            View(
                "/Settings",
                [
                    self.appbar, Row([self.layout, self.Page_Settings], expand=True)
                ],
                padding=padding.all(0),
                bgcolor=colors.WHITE,
                auto_scroll=True
            )
        )
        elif troute.match("/About"):
            self.SetTitleAppBar(e, "About")
            self.appbar.leading = Icon(icons.INFO)
            self.page.views.append(
            View(
                "/About",
                [
                    self.appbar, Row([self.layout,  Text("Here is all content of About")], expand=True)
                ],
                padding=padding.all(0),
                bgcolor=colors.GREEN,
                auto_scroll=True
            )
        )
        self.page.update()
    def ShowListFilesGoogleDrive(self, e): # function to open the file explorer 
        self.File_Properties = ManageGoogleDrive.Get_ListFiles()
        self.ListOfFiles.AddListOfTasks(e, [File[1] for File in self.File_Properties]) # Add the list of files in Google Drive
        self.page.update()
    def open_FilesGoogleDrive(self, e):
        self.page.dialog = self.FilesGoogleDriveDialog
        self.FilesGoogleDriveDialog.open = True
        self.page.update()
        try:
            self.ShowListFilesGoogleDrive(e)
        except Exception as ex:
            print("Error al actualizar la pagina: ", ex)
    def TranslateText(self, e):
        self.TextToTranslate.value = "" # Clear the text to translate
        TextBlock = "" # Block of text t0 translate (hello world)
        try:
            for Content in self.TextInput.value: # Loop to translate the text
                TextBlock += Content  # Add the content to the block of text
                if Content =='\n': # If the content is a new line, translate the block of text
                    self.Braille_Translator.TranslateGradeOne(TextBlock) # Translate the block of text
                    TextBlock = "" # Clear the block of text
            self.SettingPrinterBraille.TerminalConnection.value = self.SettingPrinterBraille.TerminalConnection.value + '\n' + "text translated successfully"
        except Exception as ex:
            self.SettingPrinterBraille.TerminalConnection.value = self.SettingPrinterBraille.TerminalConnection.value + '\n' + str(ex)
        self.update()
        self.page.update()
    def ClearText(self, e):# function to clear the text
        self.TextInput.value = ""
        self.TextToTranslate.value = ""
        self.page.update()
    def SearchWord(self, e):
        self.ListOfFiles.SearchExternal(e, self.SearchWordGD.value.lower())
        self.page.update()
    def AddFileGD(self, e):
        self.ListOfFiles.add_clickedExternal(self.TextfieldAddFileGD.value)
    def close_dlgFilesGoogleDrive(self, e): # function to close the dialog FilesGoogleDriveDialog
        self.FilesGoogleDriveDialog.open = False
        self.page.update()
    def page_resize(self, e):
        print("New page size:", self.page.window_width, self.page.window_height)
    def SetTitleAppBar(self, e, Title):
        self.appbar.title = Text(Title, size=32, text_align="start")
    def Fun_SelectFile(self, e):
        self.SettingPrinterBraille.TerminalConnection.value = self.SettingPrinterBraille.TerminalConnection.value + '\n' + self.ListOfFiles.Selected_File(e)[0]
        for File in self.File_Properties:
            if File[1] == self.ListOfFiles.Selected_File(e)[0]:
                ID_File = File[0]
        self.close_dlgFilesGoogleDrive(e)
        self.TextInput.value = ManageGoogleDrive.get_text(ID_File)
        self.update()
        self.page.update()
    def Fun_Open_PrintTextTranslatedDialog(self, e):
        self.SettingPrinterBraille.TerminalConnection.value = self.SettingPrinterBraille.TerminalConnection.value + '\n' + 'Printing the text translated to Braille'
        self.page.dialog = self.ProgresBar_DialogtoPrint
        self.ProgresBar_DialogtoPrint.open = True
        try:
            self.page.update()
            self.Fun_PrintTextTranslated(e)
        except Exception as ex:
            print("Error al actualizar la pagina: ", ex)
    def Fun_Close_ProgresBar_DialogtoPrint(self, e):
        self.ProgresBar_DialogtoPrint.open = False
        self.page.update()
    def Fun_PrintTextTranslated(self, e):
        self.TextToTranslate.value
        _Range = len(self.TextToTranslate.value) # Get the length of the text to translate -> this is the 100% of the progress bar
        self.ShowCoordinates.value = "0%" # Set the initial value of the progress bar
        i = 0
        _Row = 0
        String_Character_Braille = "" # String to store the character in Braille
        for Character_Braille in self.TextToTranslate.value: # Loop to print the text translated to Braille
            String_Character_Braille += Character_Braille # Add the character to the string
            if Character_Braille == '\n': # If the character is a new line, print a new line
                self.Braille_Translator.GetCoordinates(String_Character_Braille, _Row) # Get the coordinates of the character in Braille
                _Row += self.Braille_Translator.d
                String_Character_Braille = "" # Clear the string
            self.ProgresPrint.value = int((i * 100) / _Range) * 0.01 # Set the value of the progress bar
            i += 1
            self.page.update()
        time.sleep(2)
        self.Fun_Close_ProgresBar_DialogtoPrint(e)
        self.SettingPrinterBraille.TerminalConnection.value = self.SettingPrinterBraille.TerminalConnection.value + '\n' + 'Text translated to Braille printed successfully'
        self.update()
        self.page.update()
    
if __name__ == "__main__":
    def main(page: Page):
        Printer = Printer_Braille_2023(page)
        page.add(Printer)
        page.update()
        Printer.initialize()
    app(target=main) # , view=WEB_BROWSER)