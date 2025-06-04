from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen 
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock

class LoadingContainer(MDScreen):
    progress = NumericProperty(0)
    status_text = StringProperty("Starting recipe generation...")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progress = 0
    
    def on_enter(self):
        # Reset progress when screen is entered
        self.progress = 0
        # Schedule progress updates
        self.event = Clock.schedule_interval(self.update_progress, 0.1)
    
    def on_leave(self):
        # Cancel scheduling when leaving screen
        if hasattr(self, 'event'):
            self.event.cancel()
    
    def update_progress(self, dt):
        # Increment progress over 19 seconds
        if self.progress < 100:
            self.progress += 0.526  # (100 / 19) / 10 (since we update every 0.1 seconds)
            
            # Update status text based on progress
            if self.progress < 20:
                self.status_text = "Preparing recipe request..."
            elif self.progress < 40:
                self.status_text = "Generating recipe..."
            elif self.progress < 60:
                self.status_text = "Creating recipe image..."
            elif self.progress < 80:
                self.status_text = "Processing image..."
            elif self.progress < 90:
                self.status_text = "Finalizing recipe..."
            else:
                self.status_text = "Almost done..."
            
            return True
        return False

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
            text: root.status_text
            halign: 'center'
            theme_text_color: "Custom"
            size_hint_y: None
            height: dp(50)
            
        MDLinearProgressIndicator:
            value: root.progress
            size_hint_x: 0.8
            pos_hint: {'center_x': 0.5}
            
        MDLabel:
            text: f"{int(root.progress)}%"
            halign: 'center'
            theme_text_color: "Custom"
            size_hint_y: None
            height: dp(30)
    ''')

