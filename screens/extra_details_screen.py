from kivy.uix.scrollview import ScrollView
from kivymd.uix.slider import MDSlider
from widgets.custom_widgets import CustomFilterChip
from kivymd.uix.chip import MDChip
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.widget import MDWidget

class ExtraDetailsScreen(MDScreen):
    user_selections = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_chip=None
        self.active_chip2=None
        self.setup_layout()
        
    def setup_layout(self):
        scroll_view = ScrollView()
        
        layout = MDBoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20,
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))
        
        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1},
            size_hint_y=None,
            height="48dp",
            on_release=self.go_home
        )
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
        
        spacer = MDWidget(
            size_hint_y=None,
            height="20dp"
        )
        
        allergies_label = MDLabel(
            text="Dietary Restrictions/Allergies",
            halign='left',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="20dp"
        )
        
        self.allergies_grid = MDGridLayout(
            cols=2,
            spacing=10,
            size_hint=(None, None),
            width=500,
            height="200dp",
        )

        allergies = [
            "Dairy", "Eggs", "Peanuts", "Soy", "Wheat / Gluten",
            "Fish", "Shellfish", "Sesame", "Corn", "Sulfites", "Tree Nuts"
        ]
        
        for allergy in allergies:
            chip = CustomFilterChip(
                text=allergy
            )
            self.allergies_grid.add_widget(chip)
            
        # tree_nuts_chip = CustomFilterChip(
        #     text="Tree Nuts",c="#ffffff"
        # )
        # tree_nuts_chip.bind(active=self.toggle_tree_nuts_dropdown)
        # self.allergies_grid.add_widget(tree_nuts_chip)

        # self.tree_nuts_dropdown = MDGridLayout(
        #     cols=2,
        #     spacing=20,
        #     size_hint=(None, None),
        #     width=500,
        #     opacity=0,
        # )
        # self.tree_nuts_dropdown.bind(minimum_height=self.tree_nuts_dropdown.setter('height'))
        # spacer2 = MDWidget(
        #     size_hint_y=None,
        #     height="20dp"
        # )
        # self.tl=MDLabel(text="Tree Nuts", halign='center', size_hint_y=None, height="48dp",opacity=0,spacing=50, pos_hint={'center_x': 0.1})
        # tree_nuts = [
        #     "Almonds", "Walnuts", "Cashews", "Pecans", "Hazelnuts",
        #     "Pistachios", "Brazil Nuts", "Macadamia Nuts", "Pine Nuts"
        # ]
        
        # for nut in tree_nuts:
        #     chip = CustomFilterChip(
        #         text=nut,
        #     )
        #     chip.bind(on_release=self.toggle_chip)
        #     self.tree_nuts_dropdown.add_widget(chip)

        diet_label = MDLabel(
            text="Diet Preferences",
            halign='left',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="20dp"
        )
        self.diet_grid = MDGridLayout(
            cols=2,
            spacing=10,
            size_hint=(None, None),
            width=500,
            height="300dp",  
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
            halign='left',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="20dp"
        )
        self.meal_grid = MDGridLayout(
            cols=2,
            spacing=10,
            size_hint=(None, None),
            width=500,
            height="250dp",  
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
                text=meal, on_release=self.handle_chip_selection
            )
            self.meal_grid.add_widget(chip)

        cusine_label = MDLabel(
            text="Cuisine Type",
            halign='left',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="20dp"
        )
        self.cusine_grid = MDGridLayout(
            cols=2,
            spacing=10,
            size_hint=(None, None),
            width=500,
            height="250dp",
        )
        cusine_types = [
            "American",
            "Italian",
            "Mexican",
            "Chinese",
            "Indian",
            "Japanese",
            "Mediterranean",
            "French",
            "Spanish",
            "Thai",
            "Brazilian",
            "Vietnamese"]
        for cusine in cusine_types:
            chip = CustomFilterChip(
                text=cusine, on_release=self.handle_chip_selection2
            )
            self.cusine_grid.add_widget(chip)
        equipment_label = MDLabel(
            text="Equipment Available",
            halign='left',
            font_style="Title",
            role="large",
            size_hint_y=None,
            height="20dp"
        )
        self.equip_grid = MDGridLayout(
            cols=2,
            spacing=10,
            size_hint=(None, None),
            height="175dp",  
            width=500,
           
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
        # recipe_label = MDLabel(
        #     text="Number of Recipes",
        #     halign='center',
        #     font_style="Title",
        #     role="large",
        #     size_hint_y=None,
        #     height="48dp"
        # )
        # options2 = {
        #     0: "1",
        #     1: "2",
        #     2: "3",
        #     3: "4",
        #     4: "5",
        #     5: "6",
        #     6: "7",
        #     7: "8",
        #     8: "9",
        #     9: "10"
        # }

        # self.recipe_slider_label = MDLabel(
        #     text=options2[4],
        #     halign="center",
        #     size_hint_y=None,
        #     height="48dp"
        # )

        # slider2 = MDSlider(
        #     min=0,
        #     max=9,
        #     value=4,
        #     step=1,
        #     size_hint_y=None,
        #     height="48dp"
        # )
        # slider2.bind(value=lambda instance, val: self.recipe_slider_label.setter("text")(self.recipe_slider_label, options2.get(int(val), "")))
  
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
        layout.add_widget(MDLabel(text='', size_hint_y=None, height="40dp", opacity=0))  # Increased spacing

        # layout.add_widget(spacer2)
        # layout.add_widget(self.tl)
        # layout.add_widget(self.tree_nuts_dropdown)
        layout.add_widget(diet_label)
        layout.add_widget(self.diet_grid)
        layout.add_widget(MDLabel(text='', size_hint_y=None, height="25dp", opacity=0))  # Increased spacing

        layout.add_widget(meal_label)
        layout.add_widget(self.meal_grid)
        layout.add_widget(cusine_label)
        layout.add_widget(self.cusine_grid)
        layout.add_widget(equipment_label)
        layout.add_widget(self.equip_grid)
        layout.add_widget(serving_label)
        layout.add_widget(self.serving_size)
        layout.add_widget(time_label)
        layout.add_widget(self.time_slider_label)
        layout.add_widget(slider)
        # layout.add_widget(recipe_label)
        # layout.add_widget(self.recipe_slider_label)
        # layout.add_widget(slider2)
        layout.add_widget(notes_label)
        layout.add_widget(self.notes)
        layout.add_widget(MDButton(
            MDButtonText(text="Done"), pos_hint={'center_x': 0.5, 'y': 0},
            on_release=self.go_home
        ))
        layout.add_widget(MDLabel(text="",size_hint_y=None, height="200dp", opacity=0))
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)


    
    def toggle_tree_nuts_dropdown(self, instance, value):
        if value:
            self.tree_nuts_dropdown.opacity = 1
            self.tree_nuts_dropdown.height = self.tree_nuts_dropdown.minimum_height
            self.tl.opacity = 1
        else:
            self.tree_nuts_dropdown.opacity = 0
            self.tree_nuts_dropdown.height = 0
            self.tl.opacity = 0
            for child in self.tree_nuts_dropdown.children:
                if isinstance(child, MDChip):
                    child.active = False

    def go_home(self, instance):
        self.collect_selections()
        self.manager.current = 'main'
    def toggle_chip(self, chip):
        chip.active = not chip.active
    def handle_chip_selection(self, selected_chip):
        if self.active_chip and self.active_chip != selected_chip:
            self.active_chip.active = False
        
        self.active_chip = selected_chip if selected_chip.active else None
    def handle_chip_selection2(self, selected_chip):
        if self.active_chip2 and self.active_chip2 != selected_chip:
            self.active_chip2.active = False
        
        self.active_chip2 = selected_chip if selected_chip.active else None
    def collect_selections(self):
  
            selections = {
                "allergies": [],
                "tree_nuts": [],
                "diet_preferences": [],
                "meal_types": [],
                "equipment": [],
                "serving_size": self.serving_size.text,
                "notes": self.notes.text,
                "time_constraint": self.time_slider_label.text,
                #"recipe_count": self.recipe_slider_label.text,
                "cusine_types": [],
            }
            
            for child in self.cusine_grid.children:
                if isinstance(child, CustomFilterChip) and child.active:
                    selections["cusine_types"].append(child.text)
            for child in self.allergies_grid.children:
                if isinstance(child, CustomFilterChip) and child.active:
                        selections["allergies"].append(child.text)
            


            for child in self.diet_grid.children:
                if isinstance(child, CustomFilterChip) and child.active:
                    selections["diet_preferences"].append(child.text)
            
            for child in self.meal_grid.children:
                if isinstance(child, CustomFilterChip) and child.active:
                    selections["meal_types"].append(child.text)
            
            for child in self.equip_grid.children:
                if isinstance(child, CustomFilterChip) and child.active:
                    selections["equipment"].append(child.text)

            for child in self.children:
                if isinstance(child, ScrollView):
                    for widget in child.children[0].children:
                        if isinstance(widget, MDTextField):
                            if widget.hint_text == "Enter serving size, e.g 1-10, by default 4":
                                selections["serving_size"] = widget.text
                            elif widget.hint_text == "Enter any other notes or preferences":
                                selections["notes"] = widget.text
            
            ExtraDetailsScreen.user_selections = selections
            
            print("\n=== Selected Options ===")
            for category, items in selections.items():
                if items:
                    print(f"\n{category.replace('_', ' ').title()}:")
                    if isinstance(items, list):
                        for item in items:
                            print(f"- {item}")
                    else:
                        print(f"- {items}")
            print("\n=====================")
            return selections
