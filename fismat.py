import kivy 
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config 
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')
Config.write()


Builder.load_string("""
<Interfaz>:
    BoxLayout:
        id: index
        orientation: 'vertical'
        padding: [30, 20, 30, 50]
        spacing: 30
        Label:
            text: "Puntos de inflexión"
            font_size: 30
        BoxLayout:
            orientation: "vertical"
            Label:
                text: "Ingresar función: "
                font_size: 22
                
                text_size: root.width-30, 30
            TextInput:
                id: funcion
                multiline: True
                halign: "left"
                font_size: 15
        Button:
            text: "Calcular puntos de inflexión"
            font_size: 22
            on_press: root.recibirFuncion(funcion.text)
""")

class Interfaz(FloatLayout):
    def recibirFuncion(self, funcion):
        app = App.get_running_app()
        app.funcion = funcion 
        print("Entrando en sistema, imprimiendo funcion: ")
        print(app.funcion)


class Fismat(App):
    def build(self):
        return Interfaz()
    

if __name__ == "__main__":
    Fismat().run()
