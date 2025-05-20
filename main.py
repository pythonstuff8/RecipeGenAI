from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHelperText, MDTextFieldHintText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.chip import MDChip, MDChipText
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.widget import MDWidget
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.uix.slider import MDSlider
from custom_widgets import CustomFilterChip
from kivymd.uix.menu import MDDropdownMenu



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
class SavedRecipesScreen(MDScreen):
    pass
class ExtraDetailsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_layout()
        
    def setup_layout(self):
        # Create scroll view
        scroll_view = ScrollView()
        
        # Create main vertical box layout
        layout = MDBoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20,
            size_hint_y=None  # Add this
        )
        # Bind the height to minimum_height
        layout.bind(minimum_height=layout.setter('height'))  # Add this
        
        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1},
            size_hint_y=None,
            height="48dp",
            on_release=self.go_home
        )
        # Add header labels
        header = MDLabel(
            text="Extra Details",
            halign='center',
            font_style="Headline",
            role="large",
            size_hint_y=None,
            height="60dp"
        )
        
        subheader = MDLabel(
            text="Add your extra details, if there is something that you want to add but is not available then put it in the other notes section",
            halign='center',
            size_hint_y=None,
            height=self.texture_size[1] if hasattr(self, 'texture_size') else "60dp"
        )
        subheader.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        
        # Spacer
        spacer = MDWidget(
            size_hint_y=None,
            height="20dp"
        )
        
        allergies_label = MDLabel(
            text="Dietary Restrictions/Allergies",
            halign='center',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="48dp"
        )
        
        # Create grid for allergy chips
        self.allergies_grid = MDGridLayout(
            cols=2,
            spacing=10,
            size_hint=(None, None),
            width=500,
            height="200dp",  # Fixed height for grid
        )
        
        # Define allergies
        allergies = [
            "Dairy", "Eggs", "Peanuts", "Soy", "Wheat / Gluten",
            "Fish", "Shellfish", "Sesame", "Corn", "Sulfites"
        ]
        
        # Create and add allergy chips
        for allergy in allergies:
            chip = CustomFilterChip(
                text=allergy
            )
            self.allergies_grid.add_widget(chip)
            
        # Add tree nuts chip with dropdown functionality
        tree_nuts_chip = CustomFilterChip(
            text="Tree Nuts",c="#ffffff"
        )
        tree_nuts_chip.bind(active=self.toggle_tree_nuts_dropdown)
        self.allergies_grid.add_widget(tree_nuts_chip)

        self.tree_nuts_dropdown = MDGridLayout(
            cols=2,
            spacing=20,
            size_hint=(None, None),
            width=500,
            opacity=0,
        )
        self.tree_nuts_dropdown.bind(minimum_height=self.tree_nuts_dropdown.setter('height'))
        spacer2 = MDWidget(
            size_hint_y=None,
            height="20dp"
        )
        self.tl=MDLabel(text="Tree Nuts", halign='center', size_hint_y=None, height="48dp",opacity=0,spacing=50, pos_hint={'center_x': 0.1})
        # Define tree nuts
        tree_nuts = [
            "Almonds", "Walnuts", "Cashews", "Pecans", "Hazelnuts",
            "Pistachios", "Brazil Nuts", "Macadamia Nuts", "Pine Nuts"
        ]
        
        for nut in tree_nuts:
            chip = CustomFilterChip(
                text=nut,
            )
            chip.bind(on_release=self.toggle_chip)
            self.tree_nuts_dropdown.add_widget(chip)

        diet_label = MDLabel(
            text="Diet Preferences",
            halign='center',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="48dp"
        )
        self.diet_grid = MDGridLayout(
            cols=2,
            spacing=10,
            size_hint=(None, None),
            width=500,
            height="200dp",  
        )

        prefs = [
            "Vegetarian",
            "Vegan",
            "Pescatarian",
            "Gluten-Free",
            "Lactose-Free",
            "Dairy-Free",
            "Nut-Free",
            "Soy-Free",
            "Low-Carb / Keto",
            "Low-FODMAP",
            "Diabetic-Friendly",
            "Paleo",
            "Halal",
            "Kosher",
            "Low-Sodium",
            "High-Protein"
        ]
        
        for pref in prefs:
            chip = CustomFilterChip(
                text=pref,
            )
            self.diet_grid.add_widget(chip)
        time_label = MDLabel(
            text="Time Constraints",
            halign='center',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="48dp"
        )
        options = {
            0: "Under 10 min",
            1: "Under 20 min",
            2: "Under 30 min",
            3: "Under 1hr",
            4: "No Time Limit"
        }

        self.time_slider_label = MDLabel(
            text=options[4],
            halign="center",
            size_hint_y=None,
            height="48dp"
        )

        slider = MDSlider(
            min=0,
            max=4,
            value=4,
            step=1,
            size_hint_y=None,
            height="48dp"
        )
        slider.bind(value=lambda instance, val: self.time_slider_label.setter("text")(self.time_slider_label, options.get(int(val), "")))

        
        meal_label = MDLabel(
            text="Meal Type",
            halign='center',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="48dp"
        )
        self.meal_grid = MDGridLayout(
            cols=2,
            spacing=10,
            size_hint=(None, None),
            width=500,
            height="200dp",  
        )
        meal_types = [
            "Breakfast",
            "Lunch",
            "Dinner",
            "Snack",
            "Dessert",
            "Appetizer",
            "Side Dish",
            "Salad",
            "Soup",
            "Beverage",
            "Condiment",
            "Smoothie",
        ]

        for meal in meal_types:
            chip = CustomFilterChip(
                text=meal, active=True
            )
            self.meal_grid.add_widget(chip)



        equipment_label = MDLabel(
            text="Equipment Available",
            halign='center',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="48dp"
        )
        self.equip_grid = MDGridLayout(
            cols=2,
            spacing=10,
            size_hint=(None, None),
            height="200dp",  
           
        )
        equipment = [
            "Stove top",
            "Oven",
            "Microwave",
            "Blender",
            "Air Fryer",
            "Instant Pot",
            "Toaster",
            "No-Cook",
            "Grill",
            "Food Processor"
        ]

        for equip in equipment:
            chip = CustomFilterChip(
                text=equip, active=True
            )
            self.equip_grid.add_widget(chip)

        serving_label = MDLabel(
            text="Serving Size",
            halign='center',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="48dp"
        )
        self.serving_size = MDTextField(MDTextFieldHintText(
            text="Enter serving size, e.g 1-10, by default 4",))
        self.serving_size.text = "4"
        notes_label = MDLabel(
            text="Other Notes",
            halign='center',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="48dp"
        )
        self.notes = MDTextField(
            MDTextFieldHintText(text="Enter any other notes or preferences"),
            multiline=True,
            size_hint_y=None,
            height="200dp"
        )
        layout.add_widget(back_button)
        layout.add_widget(header)
        layout.add_widget(subheader)
        layout.add_widget(spacer)
        layout.add_widget(allergies_label)
        layout.add_widget(self.allergies_grid)
        layout.add_widget(spacer2)
        layout.add_widget(self.tl)
        layout.add_widget(self.tree_nuts_dropdown)  # Add dropdown after grid
        layout.add_widget(diet_label)
        layout.add_widget(self.diet_grid)


        layout.add_widget(time_label)
        layout.add_widget(self.time_slider_label)
        layout.add_widget(slider)
        layout.add_widget(meal_label)
        layout.add_widget(self.meal_grid)

        layout.add_widget(equipment_label)
        layout.add_widget(self.equip_grid)
        layout.add_widget(serving_label)
        layout.add_widget(self.serving_size)
        layout.add_widget(notes_label)
        layout.add_widget(self.notes)
        layout.add_widget(MDButton(
            MDButtonText(text="Done"), pos_hint={'center_x': 0.5, 'y': 0},
            on_release=self.go_home
        ))
        # Add main layout to screen
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)
    
    
    def toggle_tree_nuts_dropdown(self, instance, value):
        """Toggle the visibility of tree nuts dropdown and label opacity when chip is clicked"""
        if value:  # When chip is active
            self.tree_nuts_dropdown.opacity = 1
            self.tree_nuts_dropdown.height = self.tree_nuts_dropdown.minimum_height
            self.tl.opacity = 1  # Set label opacity to 1
        else:  # When chip is inactive
            self.tree_nuts_dropdown.opacity = 0
            self.tree_nuts_dropdown.height = 0
            self.tl.opacity = 0  # Set label opacity to 0
            # Deselect all tree nut chips when parent is deactivated
            for child in self.tree_nuts_dropdown.children:
                if isinstance(child, MDChip):
                    child.active = False

    def go_home(self, instance):
        """Collect selections and return to main screen"""
        self.collect_selections()  # Call the new method
        self.manager.current = 'main'
    def toggle_chip(self, chip):
        """Toggle chip state with short press"""
        chip.active = not chip.active  # Toggle between True and False on each press


    def collect_selections(self):
        """Collect all selected options and text input from Extra Details screen"""
        selections = {
            "allergies": [],
            "tree_nuts": [],
            "diet_preferences": [],
            "meal_types": [],
            "equipment": [],
            "serving_size": self.serving_size.text,
            "notes": self.notes.text,
            "time_constraint": self.time_slider_label.text
        }
        
        # Collect allergies
        for child in self.allergies_grid.children:
            if isinstance(child, CustomFilterChip) and child.active:
                if child.text != "Tree Nuts":
                    selections["allergies"].append(child.text)
        
        # Collect tree nuts if tree nuts chip is active
        if any(child for child in self.allergies_grid.children 
               if isinstance(child, CustomFilterChip) and 
               child.text == "Tree Nuts" and child.active):
            for child in self.tree_nuts_dropdown.children:
                if isinstance(child, CustomFilterChip) and child.active:
                    selections["tree_nuts"].append(child.text)
        # Get time constraint from slider

        # Collect diet preferences
        for child in self.diet_grid.children:
            if isinstance(child, CustomFilterChip) and child.active:
                selections["diet_preferences"].append(child.text)
        
        # Collect meal types
        for child in self.meal_grid.children:
            if isinstance(child, CustomFilterChip) and child.active:
                selections["meal_types"].append(child.text)
        
        # Collect equipment
        for child in self.equip_grid.children:
            if isinstance(child, CustomFilterChip) and child.active:
                selections["equipment"].append(child.text)

        # Get serving size and notes
        for child in self.children:
            if isinstance(child, ScrollView):
                for widget in child.children[0].children:
                    if isinstance(widget, MDTextField):
                        if widget.hint_text == "Enter serving size, e.g 1-10, by default 4":
                            selections["serving_size"] = widget.text
                        elif widget.hint_text == "Enter any other notes or preferences":
                            selections["notes"] = widget.text
        
        print("\n=== Selected Options ===")
        for category, items in selections.items():
            if items:  # Only print non-empty selections
                print(f"\n{category.replace('_', ' ').title()}:")
                if isinstance(items, list):
                    for item in items:
                        print(f"- {item}")
                else:
                    print(f"- {items}")
        print("\n=====================")
        return selections


class PantrifyApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main',md_bg_color=self.theme_cls.backgroundColor))
        self.sm.add_widget(SavedRecipesScreen(name='savedrecipes',md_bg_color=self.theme_cls.backgroundColor))
        self.sm.add_widget(ExtraDetailsScreen(name='extradetails',md_bg_color=self.theme_cls.backgroundColor))
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return self.sm
    
    def on_start(self):

            self.add_input_field()
            self.add_input_field()
            self.add_input_field()

    def add_input_field(self):
        container = self.root.get_screen('main').ids.input_fields_container
        index = len(container.children)

        # Create a BoxLayout to hold the text field and remove button horizontally
        field_container = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height="48dp",
            spacing="10dp",
        )

        text_field = MDTextField(
            size_hint_y=None,
            height="50dp",
            size_hint_x=0.8
        )

        remove_button = MDIconButton(
            icon="minus",
            size_hint_x=None,
            width="48dp",
            pos_hint={"center_y": 0.5}
        )

        # Modified remove function to remove both the button and text field
        def remove_widgets(instance):
            container.remove_widget(field_container)

        remove_button.bind(on_release=remove_widgets)
        
        # Add widgets to the horizontal container
        field_container.add_widget(text_field)
        field_container.add_widget(remove_button)
        
        # Add the container to the main container
        container.add_widget(field_container)
    
    def toggle_tree_nuts_dropdown(self):
        dropdown = self.root.ids.tree_nuts_dropdown
        chip = self.root.ids.tree_nuts_chip

        if chip.active:
            dropdown.opacity = 1
            dropdown.height = dropdown.minimum_height
        else:
            dropdown.opacity = 0
            dropdown.height = 0


if __name__ == '__main__':
    PantrifyApp().run()