import pyxel

class App:
    def __init__(self):
        pyxel.init(256, 256) # Tamaño maximo de 256x256
        self.x = 0
        pyxel.image(0).load(0, 0, "venv/assets/pyxel_logo_38x16.png") # Carga el logo de Pyxel en la posición (0,0) del banco de imagenes 0
        pyxel.run(self.update, self.draw) # Los argumentos de la función run son la función update para actualizar cada cuadro,
        # y la función draw para dibujar la escena cuando es necesario.

    def update(self): # ¿qué hace esta función?
        self.x = self.x + 1
        if self.x > pyxel.width:
            self.x = 0

    def draw(self):
        pyxel.cls(0) # borra la pantalla con el color del parametro (tenemos 16 colores 0-15)
        pyxel.rect(self.x, 0, 8, 8, 9) # crea un cuadro en la posicion (x,0), de tamaño (8,8) y código de color 9.
        pyxel.blt(self.x, 66, 0, 0, 0, 38, 16) # blt(x, y, img, u, v, w, h, [colkey])
        # Copia la región de tamaño (w, h) de (u, v) del banco de imágenes img(0-2) en (x, y).
        # Si se establece un valor negativo para w y/o h,
        # será invertido horizontal y/o verticalmente. Si colkey es especificado, ese color se trata como transparencia

App()