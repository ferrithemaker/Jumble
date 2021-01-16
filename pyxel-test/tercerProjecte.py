import pyxel

class App:
    def __init__(self):
        pyxel.init(256, 256) # Tamaño maximo de 256x256
        self.x = 200
        self.y = 0
        self.speed = [1,1] # definimos la velocidad en (x,y) en pixeles
        pyxel.image(0).load(0, 0, "venv/assets/pyxel_logo_38x16.png") # Carga el logo de Pyxel en la posición (0,0) del banco de imagenes 0
        pyxel.run(self.update, self.draw) # Los argumentos de la función run son la función update para actualizar cada cuadro,
        # y la función draw para dibujar la escena cuando sea necesario.

    def update(self): # ¿qué hace esta función?
        self.x = self.x + self.speed[0]
        self.y = self.y + self.speed[1]
        if self.x + 38 > pyxel.width or self.x < 0:
            self.speed[0] = -self.speed[0]
        if self.y + 16 > pyxel.height or self.y < 0:
            self.speed[1] = -self.speed[1]

    def draw(self):
        pyxel.cls(0) # borra la pantalla con el color del parametro (tenemos 16 colores 0-15)
        pyxel.blt(self.x, self.y, 0, 0, 0, 38, 16) # blt(x, y, img, u, v, w, h, [colkey])
        # Copia la región de tamaño (w, h) de (u, v) del banco de imágenes img(0-2) en (x, y).
        # Si se establece un valor negativo para w y/o h,
        # será invertido horizontal y/o verticalmente. Si colkey es especificado, ese color se trata como transparencia

App()