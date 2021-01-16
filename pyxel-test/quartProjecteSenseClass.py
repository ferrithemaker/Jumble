import pyxel

def update(): # ¿qué hace esta función?
    global x, y, speed, speedPre
    x = x + speed[0]
    y = y + speed[1]
    if x + 38 > pyxel.width or x < 0:
        speed[0] = -speed[0]
    if y + 16 > pyxel.height or y < 0:
        speed[1] = -speed[1]
    # control del teclado
    if pyxel.btnp(pyxel.KEY_SPACE):
        if speed[0] != 0:
            speedPre = speed # guardamos velocidad previa
            speed = [0,0] # paramos la imagen
        else:
            speed = speedPre

def draw():
    pyxel.cls(0) # borra la pantalla con el color del parametro (tenemos 16 colores 0-15)
    pyxel.blt(x, y, 0, 0, 0, 38, 16) # blt(x, y, img, u, v, w, h, [colkey])
    # Copia la región de tamaño (w, h) de (u, v) del banco de imágenes img(0-2) en (x, y).
    # Si se establece un valor negativo para w y/o h,
    # será invertido horizontal y/o verticalmente. Si colkey es especificado, ese color se trata como transparencia


pyxel.init(256, 256) # Tamaño maximo de 256x256
x = 200
y = 0
speed = [1,1] # definimos la velocidad en (x,y) en pixeles
speedPre = speed
pyxel.image(0).load(0, 0, "venv/assets/pyxel_logo_38x16.png") # Carga el logo de Pyxel en la posición (0,0) del banco de imagenes 0
pyxel.run(update, draw) # Los argumentos de la función run son la función update para actualizar cada cuadro,
# y la función draw para dibujar la escena cuando sea necesario.
