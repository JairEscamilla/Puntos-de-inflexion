# IMPORTANDO TODOS LOS COMPONENTES GRAFICOS PARA LA INTERFAZ
import kivy 
from decimal import Decimal
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config 
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

# IMPORTANDO SYMPY
from sympy import Derivative, diff, simplify, Symbol, Eq, solve, im, sympify, N
from sympy.interactive import printing
from sympy.plotting import plot   
# imprimir con notación matemática.
#printing.init_printing(use_latex='mathjax')
import matplotlib.pyplot as plt
from numpy import linspace, arange, zeros
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
    dx = ""
    ddx = ""
    soluciones = []
    pInflexiones = []
    coordenadas = []
    def recibirFuncion(self, funcion): # Recibimos la funcion ingresada por el usuario
        app = App.get_running_app()
        app.funcion = funcion # Obteniendo la funcion
        self.reescribirFuncion(app.funcion)
        print("Imprimiendo funcion: ")
        print(self.fx)
        print("Derivada de la función: ")
        self.derivarFuncion()
        print("Segunda derivada de la función: ")
        self.segundaDerivada()
        self.resolverEcuacion()
        self.evaluarIntervalos()
        self.coordenadasPInflexion()
        self.graficarFuncion()
    
    def reescribirFuncion(self, funcion): # Método para reescribir la funcion a manera de que sea entendible para Sympy
        self.fx = "" # Limpio la variable de clase
        auxiliar = [] 
        for i in range(len(funcion)-1): # Recorremos la funcion caracter a caracter
            auxiliar.append(funcion[i]) # Agregamos los caracteres a la variable auxiliar
            if((funcion[i] >= '0' and funcion[i] <= '9') and (funcion[i+1] == 'x')): # En caso de que encontremos un numero junto a una literal, se agrega el caracter *
                auxiliar.append('*')
        auxiliar.append(funcion[len(funcion)-1])
        
        for i in auxiliar: # Pasamos el valor de la variable auxiliar a la variable de instancia
            self.fx+= i

    def derivarFuncion(self): # Calculando la primer derivada de la función
        #printing.init_printing(use_latex='mathjax')
        x = Symbol('x')
        self.dx = Derivative(self.fx, x).doit()
        simplify(self.dx)
        print(self.dx)
    
    def segundaDerivada(self): # Calculando la segunda derivada de la función
        #printing.init_printing(use_latex='mathjax')
        x = Symbol('x')
        self.ddx = Derivative(self.dx, x).doit()
        simplify(self.ddx)
        print(self.ddx)

    def resolverEcuacion(self): # Resolviendo las ecuaciones de la segunda derivada
        self.soluciones = []
        ecuacion = Eq(self.ddx, 0)
        x = Symbol('x')
        self.soluciones = solve(ecuacion, x)
        print("Soluciones de las ecuaciones: ")
        for i in self.soluciones: # Imprimiendo las soluciones encontradas al resolver la ecuacion
            print(i)
    
    def evaluarIntervalos(self): # Evaluamos los intervalos para obtener los valores de x que cumplen con los requisitos de ser un punto de inflexión
        realSolutions = []
        self.pInflexiones = []
        type = 0
        type2 = 0
        x = Symbol('x')
        for i in self.soluciones: # Evaluamos que tampoco existan soluciones imaginarias
            imgPart = im(i)
            if imgPart == 0:
                realSolutions.append(i)
        if self.soluciones == [] or realSolutions == []: # Evaluamos que existan posibles soluciones
            print("No hay puntos de inflexión")
        else:
            for i in realSolutions:  # Evaluamos los resultados reales para obtener las concavidades de la funcion
                res = sympify(self.ddx).subs(x, i-0.05)
                res2 = sympify(self.ddx).subs(x, i+0.05)
                if res < 0 or res2 < 0: # En caso de que la evaluacion de la segunda derivada sea negativa, la funcion es concava en este punto
                    type = 1
                if res > 0 or res2 > 0:  # En caso de que la evaluacion de la segunda derivada sea negativa, la funcion es convexa en este punto
                    type2 = 2             
                if (type == 1 and type2 == 2) or (type == 2 and type2 == 1):
                    self.pInflexiones.append(i)
        print("Puntos de inflexión: ") # Imprimiendo los valores de x que son puntos de inflexión
        print(self.pInflexiones)
    
    def coordenadasPInflexion(self): # Obtenemos las coordenadas de los puntos de inflexión al evaluar las coordenas en x
        self.coordenadas = []
        if self.pInflexiones != []: # En caso de que no este vacia la lista, podemos calcular la coordenada en y
            x = Symbol('x')
            for i in self.pInflexiones: # Hacemos las evaluaciones en cada punto de x que se ha obtenido un punto de inflexión
                self.coordenadas.append(i.evalf())
                self.coordenadas.append(sympify(self.fx).subs(x, i).evalf())
        
        print("Las coordenadas de los puntos de inflexión son: ")
        print(self.coordenadas)

    def graficarFuncion(self):
        vt = arange(-2, 2, 0.1)
        x = Symbol('x')
        vx1 = zeros(len(vt))
        vx2 = zeros(len(vt))
        for i in range(0, len(vt)):
            vx1[i] = sympify(self.fx).subs(x, vt[i])
        plt.title("f(x)= "+self.fx+"\n")
        plt.plot(vt, vx1, "r")
        #plt.scatter(0, 0, marker = 'X', label = "Hola")
        k = 0
        for i in range(int((len(self.coordenadas))/2)):
            plt.scatter(self.coordenadas[k], self.coordenadas[k+1], marker= "X")
            k+= 2
        plt.show()


class Pinf(App):
    def build(self):
        return Interfaz()
    

if __name__ == "__main__":
    Pinf().run()
