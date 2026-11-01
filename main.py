import json
import threading
import urllib.request
import urllib.error

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

API_URL = "https://api.apinex.bond/v1/chat/completions"
MODEL = "free/gemini-3.8-flash"

KV = """
<Root>:
    orientation: "vertical"
    padding: 12
    spacing: 10

    canvas.before:
        Color:
            hex: "#07150D"
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "[b][color=#43F58B]🌿 VERDIN AI[/color][/b]"
        markup: True
        font_size: "28sp"
        size_hint_y: None
        height: "65dp"

    Label:
        text: root.status
        color: "#A8DCB8"
        size_hint_y: None
        height: "25dp"

    ScrollView:
        id: scroll

        GridLayout:
            id: messages
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: 10

    TextInput:
        id: api_key
        hint_text: "Chave APInex"
        password: True
        multiline: False
        size_hint_y: None
        height: "45dp"

    TextInput:
        id: message
        hint_text: "Digite sua mensagem..."
        multiline: False
        size_hint_y: None
        height: "50dp"
        on_text_validate: root.send_message()

    BoxLayout:
        size_hint_y: None
        height: "48dp"
        spacing: 8

        Button:
            text: "Enviar"
            background_color: "#20BD5D"
            on_release: root.send_message()

        Button:
            text: "🎤 Falar"
            background_color: "#167E48"
            on_release: root.voice_command()
"""

class Root(BoxLayout):
    status = StringProperty("Seu assistente está pronto.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = [{
            "role": "system",
            "content": "Seu nome é VERDIN. Responda em português."
        }]
        Clock.schedule_once(self.welcome, 0.5)

    def welcome(self, *args):
        self.add_message("Olá! Eu sou o VERDIN.", "VERDIN")

    def add_message(self, text, author):
        from kivy.uix.label import Label

        label = Label(
            text=f"[b]{author}[/b]\n{text}",
            markup=True,
            size_hint_y=None,
            halign="left",
            valign="middle",
            color=(1, 1, 1, 1)
        )

        label.bind(
            width=lambda obj, width:
            setattr(obj, "text_size", (width - 20, None))
        )

        label.bind(
            texture_size=lambda obj, size:
            setattr(obj, "height", size[1] + 20)
        )

        self.ids.messages.add_widget(label)
        Clock.schedule_once(
            lambda dt: setattr(self.ids.scroll, "scroll_y", 0),
            0.2
        )

    def send_message(self):
        message = self.ids.message.text.strip()
        key = self.ids.api_key.text.strip()

        if not message:
            return

        if not key:
            self.status = "Digite sua chave APInex."
            return

        self.ids.message.text = ""
        self.add_message(message, "VOCÊ")

        self.history.append({
            "role": "user",
            "content": message
        })

        self.status = "VERDIN está pensando..."

        threading.Thread(
            target=self.ask_api,
            args=(key,),
            daemon=True
        ).start()

    def ask_api(self, key):
        payload = json.dumps({
            "model": MODEL,
            "messages": self.history
        }).encode("utf-8")

        request = urllib.request.Request(
            API_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + key
            }
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))

            answer = result["choices"][0]["message"]["content"]

            self.history.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as error:
            answer = "Erro: " + str(error)

        Clock.schedule_once(
            lambda dt: self.show_answer(answer)
        )

    def show_answer(self, answer):
        self.add_message(answer, "VERDIN")
        self.status = "Pronto."

    def voice_command(self):
        self.status = (
            "O reconhecimento de voz será integrado "
            "na próxima etapa do projeto Android."
        )


class VerdinApp(App):
    def build(self):
        Builder.load_string(KV)
        return Root()


if __name__ == "__main__":
    VerdinApp().run()
