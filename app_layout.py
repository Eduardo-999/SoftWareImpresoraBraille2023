from flet import *
from sidebar import Sidebar 
 
class AppLayout(Row):
    def __init__(self):
        super().__init__()
        self.toggle_nav_rail_button = IconButton(
            icon=icons.APPS, 
            icon_color=colors.BLUE_GREY_400, 
            selected=False,
            selected_icon=icons.APPS, 
            on_click=self.toggle_nav_rail,
            
        )
        self.sidebar = Sidebar()
        self._active_view: Control = Column(
            alignment="center", 
            horizontal_alignment="center"
        )
        self.controls = [
            self.sidebar,
            self.toggle_nav_rail_button, 
            Row([self.active_view])
        ]

    @property
    def active_view(self):
        return self._active_view
 
    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()
 
    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.update()
