from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

class MainScreen(MDScreen):
    Builder.load_string('''
#:import MDActionBottomAppBarButton kivymd.uix.appbar.MDActionBottomAppBarButton


<MainScreen>:


    ScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 20
            size_hint_y: None
            height: self.minimum_height  # Enable scrolling
            Widget:
                spacing: 20
                size_hint_y: None
                height: "100dp"  # Add fixed height for top spacing
                        
            MDLabel:
                text: "MealMakerAI"
                font_style: "Display"
                role: "medium"
                halign: 'center'
                size_hint_y: None
                height: self.texture_size[1] 
            
            MDLabel:
                text: "Add your ingredients"
                halign: 'center'
                spacing: 20
                size_hint_y: None
                height: self.texture_size[1] + 10
                
            Widget:

            MDBoxLayout:
                id: input_fields_container
                orientation: 'vertical'
                spacing: 30
                size_hint_y: None
                height: self.minimum_height
            
            MDIconButton:
                icon: "plus"
                pos_hint: {"center_x": .5}
                on_release: app.add_input_field()

            Widget:

            MDExtendedFabButton:
                id: extra_notes_btn
                fab_state: "expand"
                on_release: app.get_running_app().root.current = "extradetails"  # Updated navigation

                MDExtendedFabButtonIcon:
                    icon: "note-plus"

                    MDExtendedFabButtonText:
                        text: "Extra Details"
            Widget:
                        
            MDButton:
                style: "filled"
                pos_hint: {"center_x": .5, "center_y": .5}

                MDButtonIcon:
                    icon: "chef-hat"

                MDButtonText:
                    text: "Generate your recipes"
            Widget:
                height: "1000dp"  # Add fixed height for bottom spacing
            

    MDBottomAppBar:
        id: bottom_appbar
        action_items:
            [
            MDActionBottomAppBarButton(icon="home"),
            ]

        MDFabBottomAppBarButton:
            icon: "book-open-variant-outline"
            on_release: app.get_running_app().root.current = "savedrecipes"




    



        
       
'''
)