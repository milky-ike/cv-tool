from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class TopNavBar(BoxLayout):
    pass

class LeftBox(BoxLayout):
    pass

class CenterBox(BoxLayout):
    pass

class RightBox(BoxLayout):
    """
    Right side panel where additional image options and actions are displayed.
    """
    def update_label_text(self, button_text: str) -> None:
        self.ids.right_label.text = f"{button_text}"