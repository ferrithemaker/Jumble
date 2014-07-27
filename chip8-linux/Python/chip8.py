import pygame, math, random, sys, types

def memoryDump():
        global memory
        global romLen
        for i in range (0,4096):
                if type(memory[i]) is types.IntType:
                        print i, "Integer:",memory[i]                   
                else:                   
                        print i,hex(ord(memory[i]))

def chip8Cycle():
        global pc
        global delay_timer
        global gfx
        global opcode
        global Ir
        global sound_timer
        global memory
        global V
        global keys
        global stack
        global sp
        global drawFlag
        opcode = ord(memory[pc]) << 8 | ord(memory[pc + 1])
        #print hex(pc),hex(opcode)
        if type(memory[pc]) is types.IntType:
                print "Current PC: ",pc,hex(pc), "The memory[pc] is an integer:",memory[pc]                  
        else:                   
                print "Current PC: ", pc,hex(pc), "memory[pc]:",hex(ord(memory[pc]))
        t=V[0]+2 # break with error if v[0] is not int. DEBUG line
        if (opcode & 0xF000) == 0x0000:
                if (opcode & 0x000F) == 0x0000:
                        print "Clears the screen"
                        for i in range(0,gfxSize):
                                gfx[i]=0
                        drawFlag = 1
                        pc=pc+2
                if (opcode & 0x000F) == 0x000E:
                        print "Returns from subrutine"
                        sp=sp-1
                        pc=stack[sp]
        if (opcode & 0xF000) == 0x1000:
                print "Jumps to address NNN"
                pc=opcode & 0x0FFF
        if (opcode & 0xF000) == 0x2000:
                print "Calls subroutine at NNN"
                stack[sp] = pc
                sp=sp+1
                pc = opcode & 0x0FFF
        if (opcode & 0xF000) == 0x3000:
                print "Skips the next instruction if VX equals NN"
                if V[(opcode & 0x0F00) >> 8] == (opcode & 0x00FF):
                        pc=pc+4
                else:
                        pc=pc+2
        if (opcode & 0xF000) == 0x4000:
                print "Skips the next instruction if VX doesn't equal NN"
                if V[(opcode & 0x0F00) >> 8] != (opcode & 0x00FF):
                        pc=pc+4
                else:
                        pc=pc+2
        if (opcode & 0xF000) == 0x5000:
                print "Skips the next instruction if VX equals VY"
                if V[(opcode & 0x0F00) >> 8] != V[(opcode & 0x00F0) >> 4]:
                        pc=pc+4
                else:
                        pc=pc+2
        if (opcode & 0xF000) == 0x6000:
                print "Sets VX to NN"
                V[(opcode & 0x0F00) >> 8] = opcode & 0x00FF
                pc=pc+2
        if (opcode & 0xF000) == 0x7000:
                print "Adds NN to VX"
                V[(opcode & 0x0F00) >> 8] =  V[(opcode & 0x0F00) >> 8] + (opcode & 0x00FF)
                pc=pc+2
        if (opcode & 0xF000) == 0x8000:
                if (opcode & 0x000F) == 0x0000:
                        print "Sets VX to the value of VY"
                        V[(opcode & 0x0F00) >> 8] = V[(opcode & 0x00F0) >> 4]
                        pc=pc+2
                if (opcode & 0x000F) == 0x0001:
                        print "Sets VX to VX OR VY"
                        V[(opcode & 0x0F00) >> 8] = V[(opcode & 0x0F00) >> 8] | V[(opcode & 0x00F0) >> 4]
                        pc=pc+2
                if (opcode & 0x000F) == 0x0002:
                        print "Sets VX to VX AND VY"
                        V[(opcode & 0x0F00) >> 8] = (V[(opcode & 0x0F00) >> 8] & V[(opcode & 0x00F0) >> 4])
                        pc=pc+2
                if (opcode & 0x000F) == 0x0003:
                        print "Sets VX to VX XOR VY"
                        V[(opcode & 0x0F00) >> 8] =  (V[(opcode & 0x0F00) >> 8] ^ V[(opcode & 0x00F0) >> 4])
                        pc=pc+2
                if (opcode & 0x000F) == 0x0004:
                        print "Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there"
                        if V[(opcode & 0x00F0) >> 4] > (0xFF - V[(opcode & 0x0F00) >> 8]):
                                V[0xF] = 1 #carry
                        else:
                                V[0xF] = 0                              
                        V[(opcode & 0x0F00) >> 8] = V[(opcode & 0x0F00) >> 8] + V[(opcode & 0x00F0) >> 4]
                        pc = pc +2
                if (opcode & 0x000F) == 0x0005:
                        print "VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't"
                        if V[(opcode & 0x00F0) >> 4] > V[(opcode & 0x0F00) >> 8]:
                                V[0xF] = 0
                        else:
                                V[0xF] = 1
                        V[(opcode & 0x0F00) >> 8] = V[(opcode & 0x0F00) >> 8] - V[(opcode & 0x00F0) >> 4]
                        pc=pc+2
                if (opcode & 0x000F) == 0x0006:
                        print "Shifts VX right by one. VF is set to the value of the least significant bit of VX before the shift"
                        V[0xF] = V[(opcode & 0x0F00) >> 8] & 0x1
                        V[(opcode & 0x0F00) >> 8] = V[(opcode & 0x0F00) >> 8] >> 1
                        pc=pc+2
                if (opcode & 0x000F) == 0x0007:
                        print "Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't"
                        if V[(opcode & 0x0F00) >> 8] > V[(opcode & 0x00F0) >> 4]:
                                V[0xF] = 0
                        else:
                                V[0xF] = 1
                        V[(opcode & 0x0F00) >> 8] = V[(opcode & 0x00F0) >> 4] - V[(opcode & 0x0F00) >> 8]
                        pc = pc + 2
                if (opcode & 0x000F) == 0x000E:
                        print "Shifts VX left by one. VF is set to the value of the most significant bit of VX before the shift"
                        V[0xF] = V[(opcode & 0x0F00) >> 8] >> 7
                        V[(opcode & 0x0F00) >> 8] = V[(opcode & 0x0F00) >> 8] << 1
                        pc=pc+2

        if (opcode & 0xF000) == 0x9000:
                print "Skips the next instruction if VX doesn't equal VY"
                if V[(opcode & 0x0F00) >> 8] != V[(opcode & 0x00F0) >> 4]:
                        pc = pc + 4
                else:
                        pc = pc + 2
        if (opcode & 0xF000) == 0xA000:
                print "Sets I to the address NNN"
                Ir = opcode & 0x0FFF
                pc = pc + 2
        if (opcode & 0xF000) == 0xB000:
                print "Jumps to the address NNN plus V0"
                pc = (opcode & 0x0FFF) + V[0]
        if (opcode & 0xF000) == 0xC000:
                print "sets VX to a random number and NN"
                V[(opcode & 0x0F00) >> 8] = (random.randint(0,32767) % 0xFF) & (opcode & 0x00FF)
                pc=pc+2
        if (opcode & 0xF000) == 0xD000:
                print "Draws a sprite at coordinate (VX, VY) that has a width of 8 pixels and a height of N pixels"
                xPos = V[(opcode & 0x0F00) >> 8]
                yPos = V[(opcode & 0x00F0) >> 4]
                height = opcode & 0x000F
                V[0xF] = 0
                for yline in range (0,height):
                        pixel=memory[Ir+yline]
                        for xline in range (0,8):
                                if (ord(pixel) & (0x80 >> xline)) != 0:
                                        if gfx[(xPos + xline + ((yPos + yline) * 64))] == 1:
                                                V[0xF] = 1
                                        gfx[xPos + xline + ((yPos + yline) * 64)] = gfx[xPos + xline + ((yPos + yline) * 64)] ^ 1
                drawFlag = 1                    
                pc=pc+2      
        if (opcode & 0xF000) == 0xE000:
                if (opcode & 0x00FF) == 0x009E:
                        print "Skips the next instruction if the key stored in VX is pressed"
                        if keys[V[(opcode & 0x0F00) >> 8]] != 0:
                                pc=pc+4
                        else:
                                pc=pc+2
                if (opcode & 0x00FF) == 0x00A1:
                        print "Skips the next instruction if the key stored in VX isn't pressed"
                        if keys[V[(opcode & 0x0F00) >> 8]] == 0:
                                pc=pc+4
                        else:
                                pc=pc+2
        if (opcode & 0xF000) == 0xF000:
                if (opcode & 0x00FF) == 0x0007:
                        print "Sets VX to the value of the delay timer"
                        V[(opcode & 0x0F00) >> 8] = delay_timer
                        pc=pc+2
                if (opcode & 0x00FF) == 0x000A:
                        print "A key press is awaited, and then stored in VX"
                        keyPress = 0
                        for i in range (0,16):
                                if keys[i] != 0:
                                        V[(opcode & 0x0F00) >> 8] = i
                                        keyPress=1
                        if keyPress==0:
                                return
                        pc = pc + 2     
                if (opcode & 0x00FF) == 0x0015:
                        print "Sets the delay timer to VX"
                        delay_timer = V[(opcode & 0x0F00) >> 8]
                        pc=pc+2
                if (opcode & 0x00FF) == 0x0018:
                        print "Sets the sound timer to VX"
                        sound_timer = V[(opcode & 0x0F00) >> 8]
                        pc=pc+2
                if (opcode & 0x00FF) == 0x001E:
                        print "Adds VX to I"
                        if type(V[(opcode & 0x0F00) >> 8]) is types.IntType:
                                Vcontent=V[(opcode & 0x0F00) >> 8]
                        else:
                                Vcontent=ord(V[(opcode & 0x0F00) >> 8])
                        if (Ir + V[(opcode & 0x0F00) >> 8]) > 0xFFF:
                                V[0xF] = 1
                        else:
                                V[0xF] = 0
                        #print type(Ir)
                        #print type((opcode & 0x0F00) >> 8)
                        #print type(ord(V[(opcode & 0x0F00) >> 8]))
                        #print type(V[1])
                        #print V[1]
                        #print (opcode & 0x0F00) >> 8
                        Ir = Vcontent + Ir
                        pc=pc+2
                if (opcode & 0x00FF) == 0x0029:
                        print "Sets Ir to the location of the sprite for the character in VX. Characters 0-F (in hexadecimal) are represented by a 4x5 font"
                        Ir = V[(opcode & 0x0F00) >> 8] * 0x5
                        pc=pc+2
                if (opcode & 0x00FF) == 0x0033:
                        print "Stores the Binary-coded decimal representation of VX at the addresses I, I plus 1, and I plus 2"
                        memory[Ir] = V[(opcode & 0x0F00) >> 8] / 100
                        memory[Ir + 1] = (V[(opcode & 0x0F00) >> 8] / 10) % 10
                        memory[Ir + 2] = (V[(opcode & 0x0F00) >> 8] % 100) % 10
                        pc=pc+2
                if (opcode & 0x00FF) == 0x0055:
                        print "Stores V0 to VX in memory starting at address I"
                        for i in range (0,((opcode & 0x0F00) >> 8) ): # +1 or not????
                                memory[Ir + i] = V[i]
                        Ir = Ir + ((opcode & 0x0F00) >> 8) + 1
                        pc=pc+2
                if (opcode & 0x00FF) == 0x0065:
                        print "Fills V0 to VX with values from memory starting at address Ir"
                        print "Base IR: ", Ir, hex(Ir)
                        for i in range (0,((opcode & 0x0F00) >> 8) ): # +1 or not????
                                print i, Ir+i                           
                                if type(memory[Ir+i]) is types.IntType:
                                        print "Memory dump of Ir+",i,": (integer)",memory[Ir+i], hex(memory[Ir+i])
                                        V[i]=memory[Ir + i]
                                else:                   
                                        print "Memory dump of Ir+",i,": (not integer)",memory[Ir+i], ord(memory[Ir+i])
                                        V[i] = ord(memory[Ir + i])
                                #V[i] = memory[Ir + i]                   
                        Ir = Ir + ((opcode & 0x0F00) >> 8) + 1
                        pc=pc+2 

        # timers
        if delay_timer>0:
                delay_timer=delay_timer-1
        if sound_timer>0:
                if sound_timer==1:
                       print "BEEP"
                sound_timer=sound_timer-1

#debugmode
debugmode=0

# define scale modifier
modifier=10
# define chip8 screen size
gfxSizeX=64
gfxSizeY=32
gfxSize=gfxSizeX*gfxSizeY # chip8 pixel screen size

gfx = [] # gdx array, range (0-255) 1 byte
# PC (Program Counter)

pc=0x200 # 0x200 hex = 512 dec range 0x000 to 0xFFF, 2 bytes
# Ir (index register) range 0x000 to 0xFFF, 2 bytes
Ir=0x000

# opcode
opcode = 0x000 # to store the current opcode, range 2 bytes (unsigned short)

# memory size
maxMemorySize = 4096
memory = [] # memory array, range 1 byte
# memory map:   0x000 to 0x1FF Chip 8 interpreter (contains font set in emu)
#               0x050 to 0x0A0 Used for the built in 4x5 pixel font set (0-F)
#               0x200 to 0xFFF Program ROM and work RAM

# CPU registers
V = [] # range 1 byte
maxV=16 # Max registers

# Key stats
maxKeyStats=16
keys = [] # range 1 byte per key

# Stack
stackSize=16
stack = [] # range 2 bytes per stack position
sp=0 # current stack index

# timers
delay_timer = 0 # 1 byte
sound_timer = 0 # 1 byte

# fontset 
chip8_fontset = [
    0xF0, 0x90, 0x90, 0x90, 0xF0,
    0x20, 0x60, 0x20, 0x20, 0x70,
    0xF0, 0x10, 0xF0, 0x80, 0xF0,
    0xF0, 0x10, 0xF0, 0x10, 0xF0,
    0x90, 0x90, 0xF0, 0x10, 0x10,
    0xF0, 0x80, 0xF0, 0x10, 0xF0,
    0xF0, 0x80, 0xF0, 0x90, 0xF0,
    0xF0, 0x10, 0x20, 0x40, 0x40,
    0xF0, 0x90, 0xF0, 0x90, 0xF0,
    0xF0, 0x90, 0xF0, 0x10, 0xF0,
    0xF0, 0x90, 0xF0, 0x90, 0x90,
    0xE0, 0x90, 0xE0, 0x90, 0xE0,
    0xF0, 0x80, 0x80, 0x80, 0xF0,
    0xE0, 0x90, 0x90, 0x90, 0xE0,
    0xF0, 0x80, 0xF0, 0x80, 0xF0,
    0xF0, 0x80, 0xF0, 0x80, 0x80]

# init memory
for i in range (0,maxMemorySize):
        memory.append(0)
for (i, value) in enumerate(chip8_fontset): # copy fontset to memory array
        memory[i]=chr(value)
        #print i,hex(value)

# init keys
for i in range (0,maxKeyStats):
        keys.append(0)

# init gfx
for i in range(0,gfxSize):
        gfx.append(0)

# init stack
for i in range(0,stackSize):
        stack.append(0)

# init V (CPU registers)
for i in range(0,maxV):
        V.append(0)

# ***************** TESTED OK

# Clear screen once
drawFlag = 1 # 1 true 0 false

        
i=0
with open('invaders.c8','rb') as rom:
        while 1: # copy ROM to memory
                byte_read=rom.read(1)
                if not byte_read:
                        rom.close() # close file
                        break
                memory[i+512]=byte_read # 512 = 0x200 (PC start index)
                i=i+1
romLen=i # store the lenght of the loaded ROM

# pygame init
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()
window = pygame.display.set_mode((gfxSizeX*modifier, gfxSizeY*modifier))
pygame.display.set_caption("Chip-8 emulator")
screen = pygame.display.get_surface()

#print hex(pc)
#i=0
#while i<romLen-1:
#       print hex(ord(memory[i+512]))
#       i=i+1
#i=romLen
#while pc<512+romLen-1:
        #chip8Cycle()
        #print  hex(i+512), opcode # dump all rom stored in memory
        #pc=pc+2
#for i in xrange (512,4093,2): # memory dump
        #print i,hex(memory[i])
        #print  ord(memory[i]) << 8
        #print opcode
#print hex(memory[0x001])
#Fetch opcode
#opcode = memory[pc] << 8 | memory[pc + 1];

if debugmode==1:
        memoryDump()

# pygame loop
ev = pygame.event.poll()
while ev.type!=pygame.QUIT: 
        ev = pygame.event.poll()
        # run program
        if debugmode==0:
                chip8Cycle()
        # Keyboard control
        if ev.type == pygame.KEYDOWN: # seems to work ok
                if ev.key == pygame.K_1:
                        keys[0x1] = 1
                        #print "press 1"
                elif ev.key == pygame.K_2:
                        keys[0x2] = 1
                elif ev.key == pygame.K_3:
                        keys[0x3] = 1
                elif ev.key == pygame.K_4:
                        keys[0xC] = 1
                elif ev.key == pygame.K_q:
                        keys[0x4] = 1
                elif ev.key == pygame.K_w:
                        keys[0x5] = 1
                elif ev.key == pygame.K_e:
                        keys[0x6] = 1
                elif ev.key == pygame.K_r:
                        keys[0xD] = 1
                elif ev.key == pygame.K_a:
                        keys[0x7] = 1
                elif ev.key == pygame.K_s:
                        keys[0x8] = 1
                elif ev.key == pygame.K_d:
                        keys[0x9] = 1
                elif ev.key == pygame.K_f:
                        keys[0xE] = 1
                elif ev.key == pygame.K_z:
                        keys[0xA] = 1
                elif ev.key == pygame.K_x:
                        keys[0x0] = 1
                elif ev.key == pygame.K_c:
                        keys[0xB] = 1
                elif ev.key == pygame.K_v:
                        keys[0xF] = 1
        if ev.type == pygame.KEYUP:
                if ev.key == pygame.K_1:
                        keys[0x1] = 0
                        #print "release 1"
                elif ev.key == pygame.K_2:
                        keys[0x2] = 0
                elif ev.key == pygame.K_3:
                        keys[0x3] = 0
                elif ev.key == pygame.K_4:
                        keys[0xC] = 0
                elif ev.key == pygame.K_q:
                        keys[0x4] = 0
                elif ev.key == pygame.K_w:
                        keys[0x5] = 0
                elif ev.key == pygame.K_e:
                        keys[0x6] = 0
                elif ev.key == pygame.K_r:
                        keys[0xD] = 0
                elif ev.key == pygame.K_a:
                        keys[0x7] = 0
                elif ev.key == pygame.K_s:
                        keys[0x8] = 0
                elif ev.key == pygame.K_d:
                        keys[0x9] = 0
                elif ev.key == pygame.K_f:
                        keys[0xE] = 0
                elif ev.key == pygame.K_z:
                        keys[0xA] = 0
                elif ev.key == pygame.K_x:
                        keys[0x0] = 0
                elif ev.key == pygame.K_c:
                        keys[0xB] = 0
                elif ev.key == pygame.K_v:
                        keys[0xF] = 0     
        
        # draw gfx matrix
        if drawFlag == 1: # if we must paint the screen
                for x in range(0,64):
                        for y in range(0,32):
                                if (gfx[x+(y*64)]!=0): 
                                        pygame.draw.rect(screen, WHITE, (x*modifier, y*modifier, modifier,modifier))
                                if (gfx[x+(y*64)]==0):
                                        pygame.draw.rect(screen, BLACK, (x*modifier, y*modifier, modifier,modifier))
                pygame.display.flip() # draw screen
                drawFlag=0
pygame.quit() # finish
        



