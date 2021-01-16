import pyxel

class App:
    def __init__(self):
        pyxel.init(256, 256) # Tamaño maximo de 256x256
        self.x = 0
        pyxel.run(self.update, self.draw) # Los argumentos de la función run son la función update para actualizar cada cuadro,
        # y la función draw para dibujar la escena cuando es necesario.

    def update(self): # ¿qué hace esta función?
        self.x = self.x + 1
        if self.x > pyxel.width:
            self.x = 0

    def draw(self):
        pyxel.cls(0) # borra la pantalla con el color del parametro (tenemos 16 colores 0-15)
        pyxel.rect(self.x, 0, 8, 8, 9) # crea un cuadro en la posicion (x,0), de tamaño (8,8) y código de color 9.

App()