from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.widget import Widget

class DataShare(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "A200"
        
        self.screen = Screen()
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path
        )
        
        self.dialog = None
        self.selected_file_path = None
        
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        toolbar = MDTopAppBar(
            title="DataShare",
        )
        register_button = MDIconButton(
            icon="account-plus", on_release=self.send_message, theme_text_color="ContrastParentBackground"
        )
        toolbar.add_widget(register_button)
        toolbar.pos_hint = {'top': 1}
        layout.add_widget(toolbar)

        
        self.received_label = MDLabel(
            text="Received messages will be shown here.",
            halign='center',
            theme_text_color="Hint"

        )
        layout.add_widget(self.received_label)
        
        self.text_field = MDTextField(
            hint_text="Enter your message",
            size_hint_x=0.9,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.text_field)
        
        self.file_button = MDIconButton(
            icon="attachment",
            pos_hint={'center_x': 0.5},
            on_release=self.open_file_manager
        )
        layout.add_widget(self.file_button)
        
        self.send_button = MDRaisedButton(
            text="Send",
            pos_hint={'center_x': 0.5},
            on_release=self.send_message
        )
        layout.add_widget(self.send_button)


        # Add a space below the send button
        layout.add_widget(Widget(size_hint_y=None, height=self.send_button.height))
        
        self.screen.add_widget(layout)
        
        return self.screen
    
    def open_file_manager(self, *args):
        self.file_manager.show('/')
    
    def select_path(self, path):
        self.exit_manager()
        self.selected_file_path = path
        self.show_confirmation_dialog()
    
    def exit_manager(self, *args):
        self.file_manager.close()
    
    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="File Selected",
                text=f"Selected file: {self.selected_file_path}",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_dialog
                    )
                ]
            )
        self.dialog.text = f"Selected file: {self.selected_file_path}" 
        self.dialog.open()
    
    def close_dialog(self, *args):
        self.dialog.dismiss()
    
    def send_message(self, *args):
        message = self.text_field.text
        if self.selected_file_path:
            message += f"\nAttached file: {self.selected_file_path}"
        
        self.received_label.text = f"Sent message: {message}"
        self.text_field.text = ""
        self.selected_file_path = None

if __name__ == '__main__':
    DataShare().run()
