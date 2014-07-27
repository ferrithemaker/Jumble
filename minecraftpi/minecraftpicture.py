# Script By Ferran Fabregas (ferri.fc@gmail.com)
import Image, sys, math
sys.path.append("./mcpi/api/python/mcpi")
import minecraft

# COLOR MAPPING
def colormap(pixel):
    white=(221,221,221)
    orange=(219,125,62)
    magenta=(179,80,188)
    lightblue=(107,138,201)
    yellow=(177,166,39)
    lime=(65,174,56)
    pink=(208,132,153)
    gray=(64,64,64)
    lightgray=(154,161,161)
    cyan=(46,110,137)
    purple=(126,61,181)
    blue=(46,56,141)
    brown=(79,50,31)
    green=(53,70,27)
    red=(150,52,48)
    black=(25,22,22)

    colors=(white,orange,magenta,lightblue,yellow,lime,pink,gray,lightgray,cyan,purple,blue,brown,green,red,black)

    thecolor=0
    finalresult=256*256*256
    for idx,color in enumerate(colors):
        result=math.fabs(color[0]-pixel[0])+math.fabs(color[1]-pixel[1])+math.fabs(color[2]-pixel[2])
        if result<finalresult:
            finalresult=result
            thecolor=idx
    return thecolor
# LOAD IMAGE FILE
im= Image.open(sys.argv[1])
pixels=im.load()
print im.size

# INIT MINECRAFT WORLD
mc=minecraft.Minecraft.create()
mc.postToChat("Welcome to Minecraft Image Render")
for x in range (-(im.size[0]/2),(im.size[0]/2)):
    for y in range (-(im.size[1]/2),(im.size[1]/2)):
        mc.setBlock(x,29,y,35,colormap(pixels[x+(im.size[0]/2),y+(im.size[1]/2)]))
        print "Print position:(%i,%i)"%(x+(im.size[0]/2),y+(im.size[1]/2))
mc.player.setTilePos(0,30,0)
print "RENDER FINISHED!!"


