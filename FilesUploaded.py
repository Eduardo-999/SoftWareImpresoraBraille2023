import flet as ft

class FilesGoogleDrive(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.tasks = ft.ListView(auto_scroll=True)  # assign Column object to self.tasks attribute
        self.new_task = ft.TextField(
            hint_text="What needs to be done?", 
            #expand=True
        )
        self.search_box = ft.TextField(
            hint_text="Search file", 
            on_change=self.search,
            # expand=True
        )
    def build(self):
        # application's root control (i.e. "view") containing all other controls
        return ft.ListView(
            width=600,
            height=200,
            spacing=10,
            auto_scroll=True,
            controls=[
            # Work only this file ##################
                #ft.Row(
                 #   controls=[
                  #      self.new_task,
                   #     ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    #    self.search_box,
                    #],
                #),
            #########################################
                self.tasks,
            ]
        )
    def print_selected_tasks(self, e):
        selected_tasks = []
        for control in self.tasks.controls:
            if isinstance(control.content, ft.Row): # if control.content is a Row
                for subcontrol in control.content.controls: # iterate over Row's controls
                    if isinstance(subcontrol, ft.Checkbox) and subcontrol.value:
                        selected_tasks.append(subcontrol.label)

    def Selected_File(self, e):
        selected_tasks = []
        for control in self.tasks.controls:
            if isinstance(control.content, ft.Row): # if control.content is a Row
                for subcontrol in control.content.controls: # iterate over Row's controls
                    if isinstance(subcontrol, ft.Checkbox) and subcontrol.value:
                        selected_tasks.append(subcontrol.label)
        return selected_tasks
    def buildContainer(e, ContentContainer):
        return ft.Container(
            content=ContentContainer, 
            #bgcolor=ft.colors.BLUE_200,
            border_radius=10,
            ink=True,
            on_click=lambda e: print("Clickable transparent with Ink clicked!")
        )
    def add_clicked(self, e):
        self.tasks.controls.append(
            self.buildContainer(
                ft.Column([
                    ft.Row([
                        ft.Icon(name=ft.icons.AUDIOTRACK, color="green"), 
                        ft.Checkbox(label=self.new_task.value)
                    ]),
                    ft.Row([
                        ft.Text(value="Description", color=ft.colors.BLACK, size=8, font_family="Roboto", weight=ft.FontWeight.BOLD)
                    ]),
                    ft.Row([
                        ft.Text(value="Date", color=ft.colors.BLACK, size=8, font_family="Roboto", weight=ft.FontWeight.BOLD)
                    ]),
                    ft.Row([
                        ft.Text(value="Time", color=ft.colors.BLACK, size=8, font_family="Roboto", weight=ft.FontWeight.BOLD)
                    ]),
                ])
            )
        )
        self.new_task.value = ""
        self.update()
    def AddListOfTasks(self, e, ListOfTasks):
        for task_name in ListOfTasks:
            if task_name:
                self.tasks.controls.append(
                    self.buildContainer(
                        ft.Row([ft.Icon(name=ft.icons.AUDIOTRACK, color="green"),ft.Checkbox(label=task_name)])
                    )
                )
        self.update()
    def search(self, e):
        query = self.search_box.value.lower()
        print(query)
        for task in self.tasks.controls:
            checkbox = task.content.controls
            for check in checkbox:
                if isinstance(check, ft.Checkbox):
                    label = check.label.lower()
                    if query in label:
                        task.visible = True
                    else:
                        task.visible = False
        self.update()

    def SearchExternal(self, e, search_WordExternal):
        query = search_WordExternal
        print(query)
        for task in self.tasks.controls:
            checkbox = task.content.controls
            for check in checkbox:
                if isinstance(check, ft.Checkbox):
                    label = check.label.lower()
                    if query in label:
                        task.visible = True
                    else:
                        task.visible = False
        self.update()
    def add_clickedExternal(self, external_Task):
        self.tasks.controls.append(
            self.buildContainer(
                ft.Column([ft.Row([
                    ft.Icon(name=ft.icons.AUDIOTRACK, color="green"), 
                    ft.Checkbox(label=external_Task)
                    ]),
                    ft.Text("Description")
                ])
            )
        )
        self.update()
