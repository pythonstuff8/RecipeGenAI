from kivy.uix.scrollview import ScrollView
from kivymd.uix.slider import MDSlider
from widgets.custom_widgets import CustomFilterChip
from kivymd.uix.chip import MDChip
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.widget import MDWidget
from screens.extra_details_screen import ExtraDetailsScreen
from kivy.clock import Clock
from kivy.app import App
from screens.recipe_display_screen import RecipeDisplayScreen
from utils.api import gen_recipe, safe_extract_json
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDExtendedFabButton, MDExtendedFabButtonIcon, MDExtendedFabButtonText
from kivymd.uix.dialog import MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer

class PopularDishesScreen(MDScreen):
    pd_selections = {}
    reciped=None
    ip = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_chip=None
        self.setup_layout()
        
    def show_alert_dialog(self, icon, title="", subtext=""):
        self.dialog=MDDialog(

            MDDialogHeadlineText(
                text=title,
            ),
            MDDialogSupportingText(
                text=subtext,
            ),
            MDDialogButtonContainer(
                MDWidget(),
                MDButton(
                    MDButtonText(text="Done"),
                    style="text",
                    on_release=lambda x: self.dialog.dismiss()
                ),
          
               ),
        )
        self.dialog.open()

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
            text="Popular Dishes",
            halign='center',
            font_style="Headline",
            role="large",
            size_hint_y=None,
            height="60dp"
        )
        
        subheader = MDLabel(
            text="Here you can choose a popular kind of dish that you want the recipe to be",
            halign='center',
            size_hint_y=None,
            height=self.texture_size[1] if hasattr(self, 'texture_size') else "60dp"
        )
        subheader.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        
        spacer = MDWidget(
            size_hint_y=None,
            height="20dp"
        )
        
        
        
        self.pd_grid = MDGridLayout(
            cols=2,
            spacing=10,
            size_hint=(None, None),
            width=500,
            height="400dp",
        )
        
        pd = [
    "Pizza",
    "Sushi",
    "Tacos",
    "Pasta",
    "Burger",
    "Pad Thai",
    "Paella",
    "Curry",
    "Shawarma",
    "Pho",
    "Biryani",
    "Ramen",
    "Dumplings",
    "BBQ Ribs",
    "Fish and Chips",
    "Thanksgiving dishes",
    "Eid dishes",
    "Christmas dishes",
    "Diwali dishes",
    "Lunar New Year dishes",
    "Other(type in Notes)"
]

        
        for d in pd:
            chip = CustomFilterChip(
                text=d,
                on_release=self.handle_chip_selection  # Add callback for selection
            )
            self.pd_grid.add_widget(chip)
        fab_button = MDExtendedFabButton(
            MDExtendedFabButtonIcon(icon="pencil-plus"),
            MDExtendedFabButtonText(text="   Customize    ", opacity=1),
            fab_state="expand",
            on_release=self.go_extra_details
        )
        self.notes = MDTextField(
            MDTextFieldHintText(text="Enter any other stuff that you want to add"),
            multiline=True,
            size_hint_y=None,
            height="200dp"
        )
        layout.add_widget(back_button)
        layout.add_widget(header)
        layout.add_widget(subheader)
        layout.add_widget(spacer)
        layout.add_widget(self.pd_grid)
        layout.add_widget(MDLabel(text="",size_hint_y=None, height="50dp", opacity=0))
        layout.add_widget(fab_button)
        layout.add_widget(MDLabel(text="",size_hint_y=None, height="50dp", opacity=0))
        layout.add_widget(self.notes)
        layout.add_widget(MDButton(
            MDButtonText(text="Generate Your Recipe"), MDButtonIcon(icon="chef-hat"), pos_hint={'center_x': 0.5, 'y': 0},
           style="filled", on_release=self.generate_recipe
        ))
        layout.add_widget(MDLabel(text="",size_hint_y=None, height="1000dp", opacity=0))
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)



    def generate_recipe(self, *args):
        PopularDishesScreen.pd_selections = self.collect_pd_selections()
        if not PopularDishesScreen.pd_selections:
            # if not hasattr(self, 'dialog') or self.dialog is None:
            #     self.dialog = MDDialog(
            #         title="No Recipe Selected",
            #         text="Please select a popular dish before generating a recipe.",
            #         buttons=[],
            #     )
            # self.dialog.open()
            self.show_alert_dialog(title="No Recipe Selected", subtext="Please select a popular dish before generating a recipe.", icon="close")
        
            return None
        App.get_running_app().root.current = 'loading'
        Clock.schedule_once(self.do_generate_recipe, 1)

    def do_generate_recipe(self, *args):
       
            recipe_data,ip = self.get_recipe_prompt()
            PopularDishesScreen.reciped = recipe_data
            PopularDishesScreen.ip = ip
            RecipeDisplayScreen.display_recipe(recipe_data,ip) 
            App.get_running_app().root.current = 'recipe_display'
    



    def get_recipe_prompt(self):
        """Collect all ingredients and extra details to generate recipe prompt"""
        

        extra_details = ExtraDetailsScreen.user_selections
        popular_dishes= PopularDishesScreen.pd_selections
    
        if not popular_dishes or "popular_dishes" not in popular_dishes:
            return None
        print(popular_dishes)
        prompt = f"Create a {popular_dishes['popular_dishes']} recipe"
        if extra_details:
            prompt += "Additional requirements:\n"
            
            if extra_details.get("allergies"):
                prompt += "\nAllergies/Restrictions to avoid:\n"
                prompt += "- " + "\n- ".join(extra_details["allergies"])
            

        
            if extra_details.get("tree_nuts"):
                if not prompt.endswith("\n"):
                    prompt += "\n"
                prompt += "- " + "\n- ".join(extra_details["tree_nuts"]) 

            if extra_details.get("diet_preferences"):
                prompt += "\n\nDietary Preferences:\n"
                prompt += "- " + "\n- ".join(extra_details["diet_preferences"])
                
            if extra_details.get("meal_types"):
                prompt += "\n\nPreferred Meal Type:\n"
                prompt += "- " + "\n- ".join(extra_details["meal_types"])
            if extra_details.get("cuisine_types"):
                prompt += "\n\nPreferred Cuisine Type:\n"
                prompt += "- " + "\n- ".join(extra_details["cuisine_types"])
            if extra_details.get("equipment"):
                prompt += "\n\nAvailable Equipment:\n"
                prompt += "- " + "\n- ".join(extra_details["equipment"])

            if extra_details.get("serving_size"):
                prompt += f"\n\nServing Size: {extra_details['serving_size']}"
                
            if extra_details.get("time_constraint"):
                prompt += f"\n\nTime Constraint: {extra_details['time_constraint']}"
            # if extra_details.get("recipe_count"):
            #     prompt += f"\n\nRecipe Count: {extra_details['recipe_count']}"
            if extra_details.get("notes"):
                prompt += f"\n\nAdditional Notes:\n{extra_details['notes']}"
            if popular_dishes.get("more_notes"):
                prompt += f"\n\n More Additional Notes:\n{popular_dishes['more_notes']}"


        print(prompt)  
        prompt += """
Return the recipe strictly as a JSON object — no ```json, no explanations, no markdown, no formatting. Do not include comments or placeholders. Generate a detailed recipe.

Format:
{
  "cuisine": "The chosen or inferred cuisine type",
  "title": "Recipe Title",
  "description": "A detailed description or introduction to the recipe.",
  "image_description": "A very detailed description to generate the image for the recipe.",
  "servings": "Number of servings",
  "prep_time": "Time to prepare",
  "cook_time": "Time to cook",
  "total_time": "Total time",
  "ingredients": [
    "Ingredient 1",
    "Ingredient 2"
  ],
  "instructions": [
    "Step 1",
    "Step 2"
  ],
  "meal_type": "e.g. Lunch, Dinner, etc.",
  "equipment_used": [
    "Equipment 1",
    "Equipment 2"
  ],
  "diet_labels": [
    "Label 1",
    "Label 2"
  ]
}
"""
        try:
            response = gen_recipe(prompt, api_key="AIzaSyBySkCG5yLgtz4IANJySl5Y59Xxt9pdVWI")
        except:
            App.get_running_app().root.current = 'main'
            self.show_alert_dialog(title="Error", subtext="Failed to generate recipe. Please Try Again")

      

        return response
    def go_home(self, instance):
        self.collect_pd_selections()
        self.manager.current = 'main'
    def toggle_chip(self, chip):
        chip.active = not chip.active
    def handle_chip_selection(self, selected_chip):
        if self.active_chip and self.active_chip != selected_chip:
            self.active_chip.active = False
        
        self.active_chip = selected_chip if selected_chip.active else None

    def collect_pd_selections(self):
        if not self.active_chip:
            return None
            
        pd_selections = {
            "popular_dishes": self.active_chip.text,
            "more_notes": self.notes.text if self.notes.text else ""
        }

        print("\n=== Selected Options ===")
        for category, items in pd_selections.items():
            if items:
                print(f"\n{category.replace('_', ' ').title()}:")
                print(f"- {items}")
        print("\n=====================")
        
        return pd_selections
    def go_extra_details(self, *args):
        App.get_running_app().root.current = 'extradetails'
