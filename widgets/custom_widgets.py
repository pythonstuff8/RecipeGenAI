from kivymd.uix.chip import MDChip, MDChipText
from kivy.properties import BooleanProperty
from kivy.clock import Clock

class CustomFilterChip(MDChip):
    """Custom chip that toggles on short press only"""
    
    def __init__(self, text="", active=False, c="#ffffff",**kwargs):
        super().__init__(**kwargs)
        self.type = "filter"
        self.selected_color = c
        self.theme_bg_color = "Custom"
        self.md_bg_color = "#ffffff"
        self.active = active
        self.add_widget(MDChipText(text=text))
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Toggle active state on touch
            self.active = not self.active
            return True
        return super().on_touch_down(touch)