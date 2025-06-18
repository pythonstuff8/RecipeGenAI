from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.widget import MDWidget
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivy.app import App
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.widget import Widget
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from utils.api import delete_recipe_image


class RecipeDisplayScreen(MDScreen):
    recipe_data = None
    ip = None

    @classmethod
    def display_recipe(cls, recipe_data, ip):
        cls.recipe_data = recipe_data
        cls.ip = ip

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.setup_layout()

    def setup_layout(self):
        self.clear_widgets()

        if not RecipeDisplayScreen.recipe_data:
            self.add_widget(
                MDLabel(text="No recipe data available", halign="center")
            )
            return

        recipe = RecipeDisplayScreen.recipe_data
        path = RecipeDisplayScreen.ip
        scroll_view = ScrollView()

        layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing="20dp",
            size_hint_y=None,
        )
        layout.bind(minimum_height=layout.setter("height"))

        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1},
            size_hint_y=None,
            height="48dp",
            on_release=self.back_button_callback,
        )
        layout.add_widget(back_button)

        image = AsyncImage(
            source=path,
            size_hint=(None, None),
            width="800dp",
            height="400dp",
            pos_hint={"center_x": 0.5},
            allow_stretch=True,
            keep_ratio=True,
        )
        layout.add_widget(image)

        title_label = MDLabel(
            text=recipe["title"],
            font_style="Display",
            role="small",
            halign="center",
            size_hint_y=None,
        )
        title_label.bind(
            texture_size=lambda instance, size: setattr(instance, "height", size[1])
        )
        layout.add_widget(title_label)

        desc_label = MDLabel(
            text=recipe["description"],
            halign="left",
            font_style="Title",
            role="large",
            size_hint_y=None,
        )
        desc_label.bind(
            texture_size=lambda instance, size: setattr(instance, "height", size[1])
        )
        layout.add_widget(desc_label)

        details_grid = MDGridLayout(
            cols=3,
            spacing="10dp",
            size_hint_y=None,
            adaptive_height=True,
        )

        prep_time = recipe.get("prep_time", "N/A")
        cook_time = recipe.get("cook_time", "N/A")
        total_time = recipe.get("total_time", "N/A")
        cuisine = recipe.get("cuisine", "N/A")
        servings = recipe.get("servings", "N/A")
        meal_type = recipe.get("meal_type", "N/A")
        calorie_count = recipe.get("calorie_count", "N/A")
        macros = recipe.get("macros", {})
        protein = macros.get("protein", "N/A")
        carbohydrates = macros.get("carbohydrates", "N/A")
        fat = macros.get("fat", "N/A")

        details = [
            ("Prep Time", prep_time),
            ("Cook Time", cook_time),
            ("Total Time", total_time),
            ("Cuisine", cuisine),
            ("Servings", servings),
            ("Course", meal_type),
            ("Calories", f"{calorie_count} calories per serving"),
            ("Protein", f"{protein} protein per serving"),
            ("Carbs", f"{carbohydrates} carbs per serving"),
            ("Fat", f"{fat} fat per serving"),
        ]

        for label, value in details:
            detail_label = MDLabel(
                text=f"{label}: {value}",
                halign="left",
                size_hint_y=None,
                bold=True,
            )
            detail_label.bind(
                texture_size=lambda instance, size: setattr(instance, "height", size[1])
            )
            details_grid.add_widget(detail_label)

        layout.add_widget(details_grid)


        dl_title = MDLabel(
            text="Diet Labels:",
            halign="left",
            size_hint_y=None,
            bold=True,
        )
        layout.add_widget(dl_title)

        if "diet_labels" in recipe and recipe["diet_labels"]:
            diet_label = MDLabel(
                text="\n".join([f"• {label}" for label in recipe["diet_labels"]]),
                halign="left",
                size_hint_y=None,
            )
            diet_label.bind(
                texture_size=lambda instance, size: setattr(instance, "height", size[1])
            )
            layout.add_widget(diet_label)

        eu_title = MDLabel(
            text="Equipment Used:",
            halign="left",
            size_hint_y=None,
            bold=True,
        )
        layout.add_widget(eu_title)

        if "equipment_used" in recipe and recipe["equipment_used"]:
            equip_label = MDLabel(
                text="\n".join([f"• {item}" for item in recipe["equipment_used"]]),
                halign="left",
                size_hint_y=None,
            )
            equip_label.bind(
                texture_size=lambda instance, size: setattr(instance, "height", size[1])
            )
            layout.add_widget(equip_label)

        ingredients_title = MDLabel(
            text="Ingredients:",
            halign="left",
            size_hint_y=None,
            bold=True,
        )
        layout.add_widget(ingredients_title)

        ingredients_label = MDLabel(
            text="\n".join([f"• {item}" for item in recipe["ingredients"]]),
            halign="left",
            size_hint_y=None,
        )
        ingredients_label.bind(
            texture_size=lambda instance, size: setattr(instance, "height", size[1])
        )
        layout.add_widget(ingredients_label)

        instructions_title = MDLabel(
            text="Instructions:",
            halign="left",
            size_hint_y=None,
            bold=True,
        )
        layout.add_widget(instructions_title)

        instructions = recipe["instructions"]
        if isinstance(instructions, list):
            instructions_text = "\n".join(
                [f"{i+1}. {step}" for i, step in enumerate(instructions)]
            )
        else:
            instructions_text = f"Instructions:\n{instructions}"

        instructions_label = MDLabel(
            text=instructions_text,
            halign="left",
            size_hint_y=None,
        )
        instructions_label.bind(
            texture_size=lambda instance, size: setattr(instance, "height", size[1])
        )
        layout.add_widget(instructions_label)

        layout.add_widget(Widget(size_hint_y=None, height="20dp"))

        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def icon_callback(self, instance):
        if instance.icon == "content-save-plus-outline":
            instance.icon = "content-save-plus"

    def back_button_callback(self, title="", icon="close", subtext=""):
        self.dialog = MDDialog(
            MDDialogIcon(icon="alert-circle", pos_hint={"center_x": 0.9}),
            MDDialogHeadlineText(text="Go Back"),
            MDDialogSupportingText(
                text="Are you sure you want to go back? Your recipe will be lost."
            ),
            MDDialogButtonContainer(
                MDWidget(),
                MDButton(
                    MDButtonText(text="No"),
                    style="text",
                    on_release=lambda x: self.dialog.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="Yes"),
                    style="text",
                    on_release=self.go_back_home,
                ),
                spacing="8dp",
            ),
        )
        self.dialog.open()

    def go_back_home(self, instance):
        if hasattr(self, "dialog") and self.dialog:
            self.dialog.dismiss()
            self.dialog = None
        try:
            delete_recipe_image(file_name=RecipeDisplayScreen.recipe_data["image_name"])
        except Exception as e:
            pass
        App.get_running_app().root.current = "main"
