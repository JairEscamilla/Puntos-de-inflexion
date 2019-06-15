# IMPORTANDO TODOS LOS COMPONENTES GRAFICOS PARA LA INTERFAZ
import kivy 
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config 
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

# CONFIGURANDO EL TAMAÑO DE LA VENTANA
Config.set('graphics', 'width', '400') # Configurando el ancho
Config.set('graphics', 'height', '400') # Configurando el ancho
Config.write()

# AGREGANDO LOS COMPONENTES GRAFICOS A LA INTERFAZ
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

# CLASE PARA LA LOGICA DE LA APLICACION
class Interfaz(FloatLayout):
    # Variables de clase
    fx = ""
    def recibirFuncion(self, funcion): # Recibimos la funcion ingresada por el usuario
        app = App.get_running_app()
        app.funcion = funcion # Obteniendo la funcion
        self.reescribirFuncion(app.funcion)
        print("Entrando en sistema, imprimiendo funcion: ")
        print(app.funcion)
        print(self.fx)
    
    def reescribirFuncion(self, funcion):
        self.fx = ""
        auxiliar = []
        for i in range(len(funcion)-1):
            auxiliar.append(funcion[i])
            if((funcion[i] >= '1' and funcion[i] <= '9') and (funcion[i+1] == 'x')):
                auxiliar.append('*')
        auxiliar.append(funcion[len(funcion)-1])
        for i in auxiliar:
            self.fx+= i


class Pinf(App):
    def build(self):
        return Interfaz()
    

if __name__ == "__main__":
    Pinf().run()
