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

    # color matching calculations
    result=math.fabs(white[0]-pixel[0])+math.fabs(white[1]-pixel[1])+math.fabs(white[2]-pixel[2])
    finalresult=result
    color=0
    result=math.fabs(orange[0]-pixel[0])+math.fabs(orange[1]-pixel[1])+math.fabs(orange[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=1
    result=math.fabs(magenta[0]-pixel[0])+math.fabs(magenta[1]-pixel[1])+math.fabs(magenta[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=2
    result=math.fabs(lightblue[0]-pixel[0])+math.fabs(lightblue[1]-pixel[1])+math.fabs(lightblue[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=3
    result=math.fabs(yellow[0]-pixel[0])+math.fabs(yellow[1]-pixel[1])+math.fabs(yellow[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=4
    result=math.fabs(lime[0]-pixel[0])+math.fabs(lime[1]-pixel[1])+math.fabs(lime[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=5
    result=math.fabs(pink[0]-pixel[0])+math.fabs(pink[1]-pixel[1])+math.fabs(pink[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=6
    result=math.fabs(gray[0]-pixel[0])+math.fabs(gray[1]-pixel[1])+math.fabs(gray[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=7
    result=math.fabs(lightgray[0]-pixel[0])+math.fabs(lightgray[1]-pixel[1])+math.fabs(lightgray[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=8
    result=math.fabs(cyan[0]-pixel[0])+math.fabs(cyan[1]-pixel[1])+math.fabs(cyan[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=9
    result=math.fabs(purple[0]-pixel[0])+math.fabs(purple[1]-pixel[1])+math.fabs(purple[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=10
    result=math.fabs(blue[0]-pixel[0])+math.fabs(blue[1]-pixel[1])+math.fabs(blue[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=11
        result=math.fabs(brown[0]-pixel[0])+math.fabs(brown[1]-pixel[1])+math.fabs(brown[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=12
    result=math.fabs(green[0]-pixel[0])+math.fabs(green[1]-pixel[1])+math.fabs(green[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=13
    result=math.fabs(red[0]-pixel[0])+math.fabs(red[1]-pixel[1])+math.fabs(red[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=14
    result=math.fabs(black[0]-pixel[0])+math.fabs(black[1]-pixel[1])+math.fabs(black[2]-pixel[2])
    if result < finalresult:
        finalresult=result
        color=15
    return color

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


