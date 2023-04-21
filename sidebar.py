from flet import *

class Sidebar(UserControl):
    def __init__(self):
        super().__init__()
        self.top_nav_items = [
            
            NavigationRailDestination(
                label_content=Text("Home", color=colors.BLACK, size=15, weight=FontWeight.BOLD),
                label="Home",
                icon=icons.HOME_OUTLINED,
                selected_icon=icons.HOME_OUTLINED
                #icon=icons.FAVORITE_BORDER, selected_icon=icons.FAVORITE, label="First"
            ),
            NavigationRailDestination(
                label_content=Text("settings", color=colors.BLACK, size=15, weight=FontWeight.BOLD),
                label="Settings",
                icon=icons.SETTINGS_OUTLINED,
                selected_icon=icons.SETTINGS_OUTLINED
            ),
            NavigationRailDestination(
                label_content=Text("About", color=colors.BLACK, size=15, weight=FontWeight.BOLD),
                label="About",
                icon=icons.INFO_OUTLINED,
                selected_icon=icons.INFO_OUTLINED
            ),
            
        ]
        self.top_nav_rail = NavigationRail(
            selected_index=0,
            label_type=NavigationRailLabelType.ALL,
            height=500,
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.TRANSPARENT,
            group_alignment=-0.9,
        )
 
    def build(self):
        self.view = Row(
            [
                Container(
                    content=Column([self.top_nav_rail], expand=True),
                    width=100,
                    gradient=LinearGradient(
                        #begin=alignment.top_center,
                        #end=alignment.bottom_center,
                        begin=alignment.center_right,
                        end=alignment.center_left,
                        colors=[colors.WHITE, colors.BLUE_GREY_200]
                    ),
                  
                )
            ],
            expand=True
        )
        return self.view
 
    def top_nav_change(self, e):
        self.top_nav_rail.selected_index = e.control.selected_index
        self.view.update()
        index = e if (type(e) == int) else e.control.selected_index
        if index == 0:
            self.page.route = "/"
        elif index == 1:
            self.page.route = "/Settings"
        elif index == 2:
            self.page.route = "/About"
        self.page.update()