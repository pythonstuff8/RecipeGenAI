from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHelperText, MDTextFieldHintText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import MainScreen
from screens.saved_recipes_screen import SavedRecipesScreen
from screens.extra_details_screen import ExtraDetailsScreen
from screens.recipe_display_screen import RecipeDisplayScreen
from screens.loading_screen import LoadingContainer
from kivy.properties import StringProperty
from screens.popular_dishes_screen import PopularDishesScreen
import subprocess

subprocess.PIPE = -1  # noqa
subprocess.STDOUT = -2  # noqa
subprocess.DEVNULL = -3  # noqa
class PantrifyApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main', md_bg_color=self.theme_cls.backgroundColor))
        self.sm.add_widget(SavedRecipesScreen(name='savedrecipes', md_bg_color=self.theme_cls.backgroundColor))
        self.sm.add_widget(ExtraDetailsScreen(name='extradetails', md_bg_color=self.theme_cls.backgroundColor))
        self.sm.add_widget(RecipeDisplayScreen(name='recipe_display', md_bg_color=self.theme_cls.backgroundColor))
        self.sm.add_widget(LoadingContainer(name='loading', md_bg_color=self.theme_cls.backgroundColor))
        self.sm.add_widget(PopularDishesScreen(name='popular_dishes', md_bg_color=self.theme_cls.backgroundColor))
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
    


if __name__ == '__main__':
    PantrifyApp().run()