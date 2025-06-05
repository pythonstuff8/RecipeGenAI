from kivymd.uix.chip import MDChip, MDChipText
from kivy.properties import StringProperty, ObjectProperty


class CustomFilterChip(MDChip):
    text = StringProperty("")
    on_release = ObjectProperty(None)

    def __init__(self, text="", active=False, c="#ffffff", on_release=None, **kwargs):
        super().__init__(**kwargs)
        self.type = "filter"
        self.selected_color = c
        self.theme_bg_color = "Custom"
        self.md_bg_color = "#ffffff"
        self.active = active
        self.text = text
        self.on_release = on_release
        self.add_widget(MDChipText(text=text))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            if self.on_release:
                self.on_release(self)
            return True
        return super().on_touch_down(touch)