from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen 
from kivy.lang import Builder
class LoadingContainer(MDScreen):
    Builder.load_string('''
<LoadingContainer>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: (None, None)
        size: (dp(300), dp(200))
        MDLabel:
            text: "Generating Recipe ... Can Take Up to 30 Seconds"
            halign: 'center'
            theme_text_color: "Custom"
        MDCircularProgressIndicator:
            size_hint: (None, None)
            size: (dp(48), dp(48))
            pos_hint: {'center_x': 0.5}
    ''')

