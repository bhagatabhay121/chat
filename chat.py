from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import OneLineAvatarIconListItem, MDList
import requests

SERVER_URL = "http://192.168.250.50:5000"  # Replace with your local server IP

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        title: "Chat App"
        pos_hint: {"top": 1}

    ScrollView:
        MDList:
            id: chat_list

    MDBoxLayout:
        padding: 10
        spacing: 10
        size_hint_y: None
        height: "50dp"

        MDTextField:
            id: message_input
            hint_text: "Type a message..."
            size_hint_x: 0.8

        MDRaisedButton:
            text: "Clear Chat"
            on_release: app.clear_chat()


        MDRaisedButton:
            text: "Send"
            on_release: app.send_message()
'''

class ChatApp(MDApp):
    username = "Abhay"

    def build(self):
        return Builder.load_string(KV)

    def send_message(self):
        message = self.root.ids.message_input.text
        if message:
            requests.post(f"{SERVER_URL}/send", json={"user": self.username, "message": message})
            self.root.ids.message_input.text = ""
            self.update_chat()

    def update_chat(self, *args):
        response = requests.get(f"{SERVER_URL}/messages").json()
        chat_list = self.root.ids.chat_list
        chat_list.clear_widgets()

        for msg in response:
            chat_list.add_widget(OneLineAvatarIconListItem(text=f"{msg['user']}: {msg['message']}"))

    def on_start(self):
        Clock.schedule_interval(self.update_chat, .1)  # Auto-refresh chat every 2 seconds


    def clear_chat(self):
        requests.delete(f"{SERVER_URL}/clear")
        self.update_chat()  # Refresh chat display


if __name__ == "__main__":
    ChatApp().run()
