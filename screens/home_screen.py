from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from screens.extra_details_screen import ExtraDetailsScreen
from utils.api import gen_recipe, safe_extract_json
from screens.recipe_display_screen import RecipeDisplayScreen
from kivy.app import App
from kivy.clock import Clock
import threading
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.widget import MDWidget


class MainScreen(MDScreen):
    reciped = None
    ip = None
    allow_other_ingredients = True

    def show_alert_dialog(self, icon, title="", subtext=""):
        self.dialog = MDDialog(
            MDDialogHeadlineText(text=title),
            MDDialogSupportingText(text=subtext),
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

    def go_extra_details(self, *args):
        ExtraDetailsScreen.display_recipe("main")
        App.get_running_app().root.current = "extradetails"

    def toggle_ingredients(self):
        MainScreen.allow_other_ingredients = not MainScreen.allow_other_ingredients
        btn_text = self.ids.toggle_text
        if MainScreen.allow_other_ingredients:
            btn_text.text = "Yes"
            btn_text.text_color = "green"
        else:
            btn_text.text = "No"
            btn_text.text_color = "red"

    def show_popular_dishes(self, *args):
        App.get_running_app().root.current = "popular_dishes"

    def generate_recipe(self, *args):
        App.get_running_app().root.current = "loading"
        threading.Thread(target=self._do_generate_recipe, daemon=True).start()

    def _do_generate_recipe(self):
        recipe_data, ip = self.get_recipe_prompt()
        Clock.schedule_once(lambda dt: self._update_recipe_screen(recipe_data, ip), 0)

    def _update_recipe_screen(self, recipe_data, ip):
        MainScreen.reciped = recipe_data
        MainScreen.ip = ip
        RecipeDisplayScreen.display_recipe(recipe_data, ip)
        App.get_running_app().root.current = "recipe_display"

    def get_recipe_prompt(self):
        """Collect all ingredients and extra details to generate recipe prompt"""
        ingredients = []
        container = self.ids.input_fields_container
        for field_container in container.children:
            text_field = field_container.children[1]
            if text_field.text.strip():
                ingredients.append(text_field.text.strip())
        extra_details = ExtraDetailsScreen.user_selections

        prompt = "Create a recipe using these ingredients:\n"
        prompt += "- " + "\n- ".join(ingredients) + "\n\n"
        if not MainScreen.allow_other_ingredients:
            prompt += (
                "Only use the ingredients listed above, do not add any other ingredients.\n\n"
            )

        if extra_details:
            prompt += "Additional requirements:\n"
            if extra_details.get("fat_min"):
                prompt += f"Minimum Fat Per Serving Of The Dish Will Be: {extra_details['fat_min']}\n"
            if extra_details.get("fat_max"):
                prompt += f"Maximum Fat Per Serving Of The Dish Will Be: {extra_details['fat_max']}\n"
            if extra_details.get("protein_min"):
                prompt += f"Minimum Protein Per Serving Of The Dish Will Be: {extra_details['protein_min']}\n"
            if extra_details.get("protein_max"):
                prompt += f"Maximum Protein Per Serving Of The Dish Will Be: {extra_details['protein_max']}\n"
            if extra_details.get("carbs_min"):
                prompt += f"Minimum Carbohydrates Per Serving Of The Dish Will Be: {extra_details['carbs_min']}\n"
            if extra_details.get("carbs_max"):
                prompt += f"Maximum Carbohydrates Per Serving Of The Dish Will Be: {extra_details['carbs_max']}\n"
            if extra_details.get("calories_min"):
                prompt += f"Minimum Calories Per Serving Of The Dish Will Be: {extra_details['calories_min']}\n"
            if extra_details.get("calories_max"):
                prompt += f"Maximum Calories Per Serving Of The Dish Will Be: {extra_details['calories_max']}\n"
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
                prompt += "\n\nThe Meal Type Will Be:\n"
                prompt += "- " + "\n- ".join(extra_details["meal_types"])
            if extra_details.get("cuisine_types"):
                prompt += "\n\nThe Dish Cuisine Type Will Be:\n"
                prompt += "- " + "\n- ".join(extra_details["cuisine_types"])
            if extra_details.get("equipment"):
                prompt += "\n\nAvailable Equipment:\n"
                prompt += "- " + "\n- ".join(extra_details["equipment"])
            if extra_details.get("serving_size"):
                prompt += f"\n\nServing Size: {extra_details['serving_size']}"
            if extra_details.get("time_constraint"):
                prompt += f"\n\nTime Constraint: {extra_details['time_constraint']}"
            if extra_details.get("notes"):
                prompt += f"\n\nAdditional Notes:\n{extra_details['notes']}"

        prompt += """
Return the recipe strictly as a JSON object — no ```json, no explanations, no markdown, no formatting. Do not include comments or placeholders. Generate a detailed recipe. If no ingredeints given then make your own recipe following this format

Format:
{
  "cuisine": "The chosen cuisine type",
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
  "calorie_count": "CALORIES PER SERVING; example: 500, DO NOT include the word ,calories, in ur response",
  "macros": {
    "protein": "Amount of protein PER SERVING; example: 10g",
    "carbohydrates": "Amount of carbohydrates PER SERVING; example: 15g",
    "fat": "Amount of fat PER SERVING; example: 5g"
  },
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
            response = gen_recipe(
                prompt, api_key="AIzaSyBySkCG5yLgtz4IANJySl5Y59Xxt9pdVWI"
            )
            print(response)
        except Exception:
            App.get_running_app().root.current = "main"
            self.show_alert_dialog(
                title="Error",
                subtext="Failed to generate recipe. Please Try Again",
                icon="close",
            )
        return response


Builder.load_string('''
<MainScreen>:
    ScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 20
            size_hint_y: None
            height: self.minimum_height
            Widget:
                spacing: 20
                size_hint_y: None
                height: "100dp"
            MDLabel:
                text: "RecipeGen AI"
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
            MDLabel:
                text: "More Ingredients for flavor?"
                halign: 'center'
                spacing: 20
                size_hint_y: None
                height: self.texture_size[1] + 10
            MDButton:
                id: toggle_ingredients_btn
                pos_hint: {"center_x": .5}
                on_release: root.toggle_ingredients()
                MDButtonText:
                    id: toggle_text
                    text: "Yes"
                    theme_text_color: "Custom"
                    text_color: "green"
            MDExtendedFabButton:
                id: extra_notes_btn
                fab_state: "expand"
                on_release: root.go_extra_details()
                pos_hint: {"center_x": .25}
                MDExtendedFabButtonIcon:
                    icon: "pencil-plus"
                MDExtendedFabButtonText:
                    text: "   Customize    "
                    opacity: 1
            Widget:
                size_hint_y: None
                height: "10dp"
            MDExtendedFabButton:
                id: popular_dishes_btn
                fab_state: "expand"
                on_release: root.show_popular_dishes()
                pos_hint: {"center_x": .25}
                MDExtendedFabButtonIcon:
                    icon: "star"
                MDExtendedFabButtonText:
                    text: "Popular Dishes"
                    opacity: 1
            MDButton:
                id: generate_button
                style: "filled"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.generate_recipe()
                MDButtonIcon:
                    icon: "chef-hat"
                MDButtonText:
                    text: "Generate your recipe"
            Widget:
                height: "1000dp"
''')