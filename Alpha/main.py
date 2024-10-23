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
import socket
import threading
import os


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
        self.device_name = None
        self.security_level = None
        self.recipient = None
        
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="DataShare",
        )
        register_button = MDIconButton(
            icon="account-plus", on_release=self.show_register_popup, theme_text_color="ContrastParentBackground"
        )
        toolbar.add_widget(register_button)
        toolbar.pos_hint = {'top': 1}
        layout.add_widget(toolbar)
        
        # Label to display received messages
        self.received_label = MDLabel(
            text="Received messages will be shown here.",
            halign='center',
            theme_text_color="Hint"
        )
        layout.add_widget(self.received_label)
        
        # Text field for entering messages
        self.text_field = MDTextField(
            hint_text="Enter your message",
            size_hint_x=0.9,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.text_field)
        
        # File attachment button
        self.file_button = MDIconButton(
            icon="attachment",
            pos_hint={'center_x': 0.5},
            on_release=self.open_file_manager
        )
        layout.add_widget(self.file_button)
        
        # Send button
        self.send_button = MDRaisedButton(
            text="Send",
            pos_hint={'center_x': 0.5},
            on_release=self.send_message
        )
        layout.add_widget(self.send_button)
        
        # Add a space below the send button
        layout.add_widget(Widget(size_hint_y=None, height=self.send_button.height))
        
        self.screen.add_widget(layout)

        # Start receiving data on app start
        self.start_receiving()
        
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
                title="Success",
                text="",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_dialog
                    )
                ]
            )
        self.dialog.text = "Action completed successfully"
        self.dialog.open()
    
    def close_dialog(self, *args):
        self.dialog.dismiss()
    
    # Local network logic for sending a message or file
    def send_message(self, *args):
        message = self.text_field.text
        if self.selected_file_path:
            self.send_file_over_network(self.selected_file_path)
            self.selected_file_path = None  # Reset after sending file
        elif message:
            self.send_over_network(message)
        self.text_field.text = ""
    
    # Local network send function for message
    def send_over_network(self, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Replace with the recipient's local IP and port
                s.connect(("127.0.0.1", 5000))  # Localhost and port 5000
                s.sendall(f"MSG:{message}".encode('utf-8'))
                self.show_confirmation_dialog()
        except Exception as e:
            print(f"Error sending message: {e}")
    
    # Local network send function for file
    def send_file_over_network(self, file_path):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("127.0.0.1", 5000))
                
                # Send file metadata (header)
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                s.sendall(f"FILE:{file_name}:{file_size}".encode('utf-8'))
                
                # Send file content in chunks
                with open(file_path, "rb") as file:
                    chunk = file.read(1024)
                    while chunk:
                        s.sendall(chunk)
                        chunk = file.read(1024)
                self.show_confirmation_dialog()
        except Exception as e:
            print(f"Error sending file: {e}")
    
    # Local network receive logic (should run on a separate thread)
    def start_receiving(self):
        receive_thread = threading.Thread(target=self.receive_from_network)
        receive_thread.daemon = True  # Daemonize the thread so it stops when the main thread stops
        receive_thread.start()
    
    # Local network receive function
    def receive_from_network(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("0.0.0.0", 5000))  # Listen on all interfaces, port 5000
                s.listen()
                while True:
                    conn, addr = s.accept()
                    with conn:
                        header = conn.recv(1024).decode('utf-8')
                        
                        if header.startswith("MSG:"):
                            message = header[4:]
                            self.update_received_label(f"Message: {message}")
                        elif header.startswith("FILE:"):
                            _, file_name, file_size = header.split(":")
                            self.receive_file(conn, file_name, int(file_size))
        except Exception as e:
            print(f"Error receiving data: {e}")
    
    # Function to receive a file
    def receive_file(self, conn, file_name, file_size):
        try:
            received_size = 0
            with open(f"received_{file_name}", "wb") as file:
                while received_size < file_size:
                    data = conn.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    received_size += len(data)
            self.update_received_label(f"Received file: {file_name}")
        except Exception as e:
            print(f"Error receiving file: {e}")
    
    def update_received_label(self, message):
        # Schedule this to update on the main thread
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.received_label_update(message))
    
    def received_label_update(self, message):
        self.received_label.text = message
    
    def show_register_popup(self, *args):
        self.device_name_field = MDTextField(
            hint_text="Enter device name",
            size_hint_x=0.9,
            pos_hint={'center_x': 0.5}
        )
        
        self.security_level_field = MDTextField(
            hint_text="Enter security level",
            size_hint_x=0.9,
            pos_hint={'center_x': 0.5}
        )
        
        content = MDBoxLayout(orientation='vertical', spacing=10)
        content.add_widget(self.device_name_field)
        content.add_widget(self.security_level_field)
        
        self.register_dialog = MDDialog(
            title="",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="Confirm",
                    on_release=self.save_register_info
                ),
                MDRaisedButton(
                    text="Cancel",
                    on_release=self.close_register_dialog
                )
            ],
            size_hint=(0.8, 0.4)  # Adjust the size_hint to make the dialog larger
        )
        self.register_dialog.open()
    
    def save_register_info(self, *args):
        # Displaying a success message instead of writing to a database
        self.device_name = self.device_name_field.text
        self.security_level = self.security_level_field.text
        self.register_dialog.dismiss()
        self.show_confirmation_dialog()  # Show a success message saying it was "saved to the database"
    
    def close_register_dialog(self, *args):
        self.register_dialog.dismiss()

if __name__ == '__main__':
    DataShare().run()
