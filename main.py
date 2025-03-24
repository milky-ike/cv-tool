#main.py

import os
import cv2
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from dotenv import load_dotenv
from utils.cv import ImageManager
from typing import List, Dict, Callable, Optional

INITIAL_INDEX = 0  # Set the initial index for file navigation

class NumberInput(TextInput):
    def insert_text(self, substring: str, from_undo: bool = False) -> None:
        if all(char.isdigit() or char == "." for char in substring):
            super().insert_text(substring, from_undo=from_undo)

class CvApp(App):
    def build(self) -> BoxLayout:
        self.set_window_size_from_env()
        return MyBoxLayout()

    def set_window_size_from_env(self) -> None:
        try:
            Window.size = tuple(map(int, os.getenv('WINDOW_SIZE').strip('[]').split(',')))
        except Exception as e:
            print(f"Error setting the window size: {e}")

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(**kwargs)
        self.bind(on_parent=self.on_parent)

    def on_parent(self, instance: BoxLayout, value: bool) -> None:
        if value:
            self.bind_left_box_size()

    def bind_left_box_size(self) -> None:
        left_box = self.ids.left_box
        if left_box:
            left_box.bind(on_size=self.update_left_box_size_hint_x)

    def update_left_box_size_hint_x(self, instance: BoxLayout, value: float) -> None:
        left_box = self.ids.left_box
        if left_box:
            left_box.size_hint_x = instance.width / self.width

class TopNavBar(BoxLayout):
    pass

class LeftBox(BoxLayout):
    pass

class CenterBox(BoxLayout):
    pass

class RightBox(BoxLayout):
    def update_label_text(self, button_text: str) -> None:
        self.ids.right_label.text = f"{button_text}"

class MyAppButton(Button):
    supported_files: List[str] = []
    current_index: int = INITIAL_INDEX
    image_manager: ImageManager = ImageManager()

    def __init__(self, **kwargs: dict) -> None:
        super(MyAppButton, self).__init__(**kwargs)
        self.bind(on_release=self.on_button_release)
        self.filters: List[str] = os.getenv('IMAGE_EXT', '').split()

    def on_button_release(self, instance: Button) -> None:
        actions: Dict[str, Callable[[], None]] = {
            'Open': self.show_file_chooser,
            'Open Dir': self.show_directory_chooser,
            'Next': self.next_action,
            'Prev': self.prev_action,
            'Save': self.save_action,
            'Info': self.Info_action,
            'Crop': self.crop_action,
            'Resize': self.resize_action,
            'Brt': self.brightness_action,
            'Sat': self.saturation_action,
            'Rot 90°': self.rotate_90_action,
            'FV/FH': self.flip_action,
        }
        action = actions.get(self.text, self.update_right_label)
        action()

    def show_file_chooser(self) -> None:
        self.file_chooser_popup(is_dir=False)

    def show_directory_chooser(self) -> None:
        self.file_chooser_popup(is_dir=True)

    def next_action(self) -> None:
        supported_list = MyAppButton.supported_files[1:]
        if MyAppButton.current_index < len(supported_list):
            file_path = supported_list[MyAppButton.current_index]
            self.load_image(file_path)
            MyAppButton.current_index += 1
        else:
            self.load_none_image()

    def prev_action(self) -> None:
        if MyAppButton.current_index > 0:
            MyAppButton.current_index -= 1
            file_path = MyAppButton.supported_files[MyAppButton.current_index]
            self.load_image(file_path)
        else:
            self.load_none_image()

    def save_action(self) -> None:
        self.image_manager.save_image(MyAppButton.supported_files, MyAppButton.current_index)

    def Info_action(self) -> None:
        pass

    def crop_action(self) -> None:
        self.create_ui(items=['Top', 'Left', 'Bottom', 'Right'], is_input_ui=True, callback=self.crop_button_callback)

    def resize_action(self) -> None:
        self.create_ui(items=['Width', 'Height'], is_input_ui=True, callback=self.resize_button_callback)

    def brightness_action(self) -> None:
        self.create_ui(items=['brt'], is_input_ui=True, callback=self.brightness_button_callback)

    def saturation_action(self) -> None:
        self.create_ui(items=['sat'], is_input_ui=True, callback=self.saturation_button_callback)

    def rotate_90_action(self) -> None:
        self.create_ui(items={'90°': 1, '180°': 2, '270°': 3}, is_input_ui=False, callback=self.rotate_90_button_callback)

    def flip_action(self) -> None:
        self.create_ui(items={'vertically': "vertically", 'horizontally': "horizontally"}, is_input_ui=False, callback=self.flip_button_callback)

    def create_ui(self, items: List[str], is_input_ui: bool, callback: Optional[Callable[[List[TextInput]], None]]) -> None:
        right_box = App.get_running_app().root.ids.right_box
        right_box.clear_widgets()

        float_layout = FloatLayout()
        LABEL_WIDTH_RATIO = 0.2
        INPUT_WIDTH_RATIO = 0.6
        BUTTON_WIDTH_RATIO = 0.8
        input_center_y = 0.9

        if is_input_ui:
            labels: List[Label] = []
            text_inputs: List[TextInput] = []

            label_width = right_box.width * LABEL_WIDTH_RATIO  
            text_input_width = right_box.width * INPUT_WIDTH_RATIO

            for i, label_name in enumerate(items):
                label = Label(text=f"{label_name} : ", size_hint=(None, None), size=(label_width, 60), padding=(10, 10))
                text_input = TextInput(text="", size_hint=(None, None), width=text_input_width, height=60, padding=(10, 10))

                labels.append(label)
                text_inputs.append(text_input)

            button = Button(text="Submit", size_hint=(None, None), size=(label_width + text_input_width, 60))
            button.background_color = (250/255, 219/255, 216/255, 1)

            for i in range(len(items)):
                float_layout.add_widget(labels[i])
                float_layout.add_widget(text_inputs[i])
                text_inputs[i].pos_hint = {'center_x': 0.6, 'center_y': input_center_y}
                labels[i].pos_hint = {'center_x': 0.2, 'center_y': input_center_y}
                input_center_y -= 0.0525
            
            button.pos_hint = {'center_x': 0.5, 'center_y': input_center_y}
            button.bind(on_press=lambda instance: callback(text_inputs))

            float_layout.add_widget(button)

        else:
            for label, value in items.items():
                text_button = Button(
                    text=label,
                    size_hint=(None, None),
                    size=(right_box.width * BUTTON_WIDTH_RATIO, 60),
                    padding=(10, 10),
                    background_color=(250/255, 219/255, 216/255, 1)
                )
                text_button.pos_hint = {'center_x': 0.5, 'center_y': input_center_y}
                text_button.bind(on_press=lambda instance, v=value: callback(v))

                float_layout.add_widget(text_button)
                input_center_y -= 0.0525

        right_box.add_widget(float_layout)

    def update_right_label(self) -> None:
        right_box = App.get_running_app().root.ids
        right_box.update_label_text(self.text)

    def file_chooser_popup(self, is_dir: bool) -> None:
        file_chooser = FileChooserListView(on_submit=self.on_directory_chosen if is_dir else self.on_file_chosen, dirselect=is_dir)
        popup = Popup(title="Select Directory" if is_dir else "Select File", content=file_chooser, size_hint=(0.8, 0.8))
        popup.open()
    
    def dismiss_popup(self, instance: Button) -> None:
        parent = instance.parent
        while parent and not isinstance(parent, Popup):
            parent = parent.parent
        if parent:
            parent.dismiss()

    def on_file_chosen(self, instance: FileChooserListView, value: List[str], touch: Optional[object]) -> None:
        if value:
            MyAppButton.supported_files.clear()
            MyAppButton.current_index = INITIAL_INDEX
            base_path = value[0]
            MyAppButton.supported_files.append(base_path)
            self.load_image(MyAppButton.supported_files[0])
            self.dismiss_popup(instance)

    def on_directory_chosen(self, instance: FileChooserListView, value: List[str], touch: Optional[object]) -> None:
        extensions = [filter_.replace('*', '') for filter_ in self.filters]
        if value:
            MyAppButton.supported_files.clear()
            MyAppButton.current_index = INITIAL_INDEX
            base_path = value[0]
            for root_directory, _, filenames in os.walk(base_path):
                for filename in filenames:
                    file_path = os.path.join(root_directory, filename)
                    if os.path.isfile(file_path) and os.path.splitext(file_path)[1].lower() in extensions:
                        MyAppButton.supported_files.append(file_path)
            if MyAppButton.supported_files:
                self.load_image(MyAppButton.supported_files[0])
            self.dismiss_popup(instance)

    def load_image(self, file_path: str) -> None:
        center_box = App.get_running_app().root.ids.center_box
        center_box.clear_widgets()
        try:
            center_box.add_widget(Image(source=file_path))
        except Exception as e:
            center_box.add_widget(Label(text=f"Error: {str(e)}"))

    def load_none_image(self) -> None:
        center_box = App.get_running_app().root.ids.center_box
        center_box.clear_widgets()
        center_box.add_widget(Label(text="No more images available"))

    def crop_button_callback(self, text: List[TextInput]) -> None:
        items = []
        for item in text:
            if not item.text.isdigit():
                print("Please enter numeric values.")
                return
            items.append(int(item.text))
        
        self.image_manager.set_cropped(MyAppButton.supported_files, MyAppButton.current_index, items, self.load_image)

    def resize_button_callback(self, text: List[TextInput]) -> None:
        items = []
        for item in text:
            if not item.text.isdigit():
                print("Please enter numeric values.")
                return
            items.append(int(item.text))
        
        self.image_manager.set_resize(MyAppButton.supported_files, MyAppButton.current_index, items, self.load_image)
    
    def brightness_button_callback(self, text: List[TextInput]) -> None:
        items = []
        for item in text:
            value = float(item.text)
            if value < 0 or value > 2.5:
                print("Please enter numeric value between 0 and 2.5.")
                return
            items.append(value)

            self.image_manager.set_brightness(MyAppButton.supported_files, MyAppButton.current_index, items, self.load_image)

    def saturation_button_callback(self, text: List[TextInput]) -> None:
        items = []
        for item in text:
            value = float(item.text)
            if value < 0 or value > 2.5:
                print("Please enter numeric value between 0 and 2.5.")
                return
            items.append(value)

            self.image_manager.set_saturation(MyAppButton.supported_files, MyAppButton.current_index, items, self.load_image)

    def rotate_90_button_callback(self, text: int) -> None:
        item = int(text)

        self.image_manager.set_rotate_90(MyAppButton.supported_files, MyAppButton.current_index, item, self.load_image)

    def flip_button_callback(self, text: str) -> None:
        item = text
        if text not in {'vertically', 'horizontally'}:
            print("Please enter a valid flip option: 'vertically' or 'horizontally'.")
            return

        self.image_manager.set_flip(MyAppButton.supported_files, MyAppButton.current_index, item, self.load_image)

if __name__ == '__main__':
    try:
        load_dotenv()
    except FileNotFoundError:
        print("Could not find the `.env` file. Environment variables are not loaded.")
    
    CvApp().run()