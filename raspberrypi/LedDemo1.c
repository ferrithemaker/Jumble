// Code to drive the 32x32 LED arrays available from SKPANG 
// http://skpang.co.uk/catalog/rgb-led-panel-32x32-p-1329.html
// Based on code from https://github.com/hzeller/rpi-rgb-led-matrix
// Which contains the following copyright notice:
// Code is (c) Henner Zeller h.zeller@acm.org, and I grant you the
// permission to do whatever you want with it :)

// This code is (c) Peter Onion (Peter.Onion@btinternet.com), and I too grant you the
// permission to do whatever you want with it, as long as this header block
// is retained in any code you may distribute that uses or is based on this code.
// How to compile: gcc -o LedDemo1 LedDemo1.c -lm -lpthread

#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

#include <pthread.h>
#include <time.h>
#include <stdbool.h>
#include <stdint.h>

#include <sys/mman.h>

#include <termios.h>
#include <unistd.h>

#include <signal.h>
#include <math.h>
#include <time.h>

// Names for the GPIO pin numbers
enum bitNames {OE=2,CLK=3,STB=4,ROWA=7,ROWB=8,ROWC=9,ROWD=10,
	       R1=17,G1=18,B1=22,
	       R2=23,G2=24,B2=25};

// Array of GPIO bit numbers to be set for output.
int outputBits[] = {OE,CLK,STB,ROWA,ROWB,ROWC,ROWD,
		    R1,G1,B1,
		    R2,G2,B2,-1};

// GPIO hardware memory addresses
#define BCM2708_PERI_BASE 0x20000000
#define GPIO_BASE (BCM2708_PERI_BASE + 0x200000) /* GPIO controller */
#define BLOCK_SIZE (4*1024)

// GPIO setup macros. Always use INP_GPIO(x) before using OUT_GPIO(x) or SET_GPIO_ALT(x,y)
#define INP_GPIO(g) *(gpio_port+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g) *(gpio_port+((g)/10)) |=  (1<<(((g)%10)*3))


volatile uint32_t *gpio_port;
uint32_t portMask;    // Bit set for each used GPIO bits
uint32_t pixelMask = (1<<R1|1<<R2|1<<G1|1<<G2|1<<B1|1<<B2);
uint32_t pixelClkMask = (1<<R1|1<<R2|1<<G1|1<<G2|1<<B1|1<<B2|1<<CLK);


int greyCode[16] = {0,1,3,2,6,7,5,4,12,13,15,14,10,11,9,8};
int greyCodeChange[16];
bool greyCodeSet[16];

// Global thread control variables
bool displayRunning;
bool gameRunning;
bool gameStop;

// In an attempt to reduce ghosting between lines I use a grey code 
// order for the scanning.

void buildGreyCode(void)
{
    int row,prevRow,diff;
    for(row=0;row < 16; row++)
    {
	prevRow = (row - 1) & 15;
	diff = greyCode[row] ^ greyCode[prevRow];
	greyCodeChange[row] = diff;
	greyCodeSet[row] = (diff &  greyCode[row]) ? true : false;

    }
//  for(row = 0;row < 16; row++)
//	printf("%d %x %d\n",row,greyCodeChange[row],greyCodeSet[row]);
}


// Set the bits that are '1' in the output. Leave the rest untouched.
inline void SetBits(uint32_t value) 
{
    gpio_port[0x1C / sizeof(uint32_t)] = value & portMask;
}

// Clear the bits that are '1' in the output. Leave the rest untouched.
inline void ClearBits(uint32_t value) 
{
    gpio_port[0x28 / sizeof(uint32_t)] = value & portMask;
}


// Set up the mempry mapped access to the GPIO registers
bool initGPIO(void)
{
    
    int mem_fd,n,bitNumber;
    if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) 
    {
	perror("can't open /dev/mem: ");
	return false;
    }

    char *gpio_map = (char*) mmap(NULL,             //Any adddress in our space will do
				  BLOCK_SIZE,       //Map length
				  PROT_READ|PROT_WRITE,// Enable reading & writting to mapped memory
				  MAP_SHARED,       //Shared with other processes
				  mem_fd,           //File to map
				  GPIO_BASE);         //Offset to GPIO peripheral
	

    close(mem_fd); //No need to keep mem_fd open after mmap

    if (gpio_map == MAP_FAILED) 
    {
	fprintf(stderr, "mmap error %ld\n", (long)gpio_map);
	return false;
    }

    // set global pointer to the GPIO registers
    gpio_port = (volatile uint32_t *)gpio_map;

    // Build the bit mask for the used pins
    portMask = 0;
    n = 0;
    while((bitNumber = outputBits[n++]) != -1)
    {
	INP_GPIO(bitNumber);
	OUT_GPIO(bitNumber);
	portMask |= 1 << bitNumber;
    }
    
    ClearBits(portMask);

    return true;
}




// Short delays for bit banging signals.

void settleTime(time)
{
    int i;
    for (i = time; i != 0; --i) {
	asm("");   // force GCC not to optimize this away.
    }
}



uint32_t Pixels1[32*16];
uint32_t Pixels2[32*16];

// Pointers to Front and Back buffer
uint32_t *PixelsF,*PixelsB;

// This thread continuously cycles through the Pixels array sending the 
// pixel data to the display row by row.

void *startDisplayThread(void *args)
{
    int n,col,row;
    struct timespec sleepTime = { 0, 5000000 };
    struct timespec onTime =    { 0,  200000 };
    uint32_t *pixelData; 

    initGPIO();

    buildGreyCode();

    // Set up buffer pointers.
    PixelsF = Pixels1;
    PixelsB = Pixels2;

    // Set row bits to zero to start with.
    ClearBits( 15 << ROWA);
    row = 0;

    while(displayRunning)
    {

	// Cycle through the rows in a grey code order to minimise changes on address lines.
	// Changing the address lines seems to a part of the cause of the ghosting problems.
	if(greyCodeSet[row])
	{
	    SetBits(greyCodeChange[row] << ROWA);   // Set a bit for the current row 
	}
	else
	{
	    ClearBits(greyCodeChange[row] << ROWA);   // Clear a bit for the current row 
	}

	settleTime(5);
	// Clock one rows worth of pixels into the display
	pixelData = &PixelsF[32*greyCode[row]];
	for(col=0;col<32;col++)
	{
	    ClearBits(pixelClkMask);  // Clk low
	    settleTime(5);
	    SetBits(*pixelData++ & pixelMask);
	    settleTime(5);
	    SetBits(1<<CLK);          // Clk high
	    settleTime(5);
	}

	SetBits(1<<STB);   // Strobe
	//settleTime(5);
	ClearBits(1<<STB);
	settleTime(50);
	ClearBits(1<<OE);  // turn display on	
	nanosleep(&onTime, NULL);   // Fixed on time 
	SetBits(1<<OE);     // turn off the display
	settleTime(5);

	row += 1;
	row &= 15;
#if 1
	// Pause at the end of the frame
	if(row == 0)
	{
	    SetBits(1<<OE);
	    nanosleep(&sleepTime, NULL);
	}
#endif
    }
    // Make sure display is off when we exit the thread
    SetBits(1<<OE);


}

void setPixelColour(int x,int y, int r,int g,int b)
{
    int address;
    uint32_t bits,bitmask;

    // Sanities parameters
    x &= 31;
    y &= 31;
    r &= 1;
    g &= 1;
    b &= 1;

    address = x;
    // Set bits & mask depending on which half of the display the pixel is in. 
    if(y < 16)
    {
	bits = (r<<R1|g<<G1|b<<B1);
	bitmask = (1<<R1|1<<G1|1<<B1);
    }
    else
    {
	bits = (r<<R2|g<<G2|b<<B2);
	bitmask = (1<<R2|1<<G2|1<<B2);
    }
    address += (y & 15) * 32;
    // Clear and set the appropriate bits in the Pixel data
    PixelsB[address] &= ~bitmask;  
    PixelsB[address] |= bits;
    
    
}

// Integer maths version of Bresenham's line drawing algorithm
void drawLine(int x1, int y1, int x2, int y2,int r, int g, int b)
{
    int dx,dy,D,x,y,xstep,ystep,steps,E1,E2;

    dx=x2-x1;
    x = x1;

    if(dx >= 0)
    {
	xstep = 1;
    }
    else
    {
	xstep = -1;
	dx = -dx;
    }

    dy=y2-y1;
    y = y1;
    if(dy >= 0)
    {
	ystep = 1;
    }
    else
    {
	ystep = -1;
	dy = -dy;
    }
    
    if(dx >= dy)
    { // Shallow
	D = 2*dy - dx;
	E1 = 2*dy-2*dx;
	E2 =  2*dy;
	setPixelColour(x,y,r,g,b);
	steps = dx;
	while(steps--)
	{
	    x += xstep;
	    if(D > 0)
	    {
		y = y+ystep;
		D = D + E1;
	    }
	    else
	    {
		D = D + E2;
	    }
	    setPixelColour(x,y,r,g,b);
	}
    }
    else
    { // Steep
	D = 2*dx - dy;
	E1 = 2*dx-2*dy;
	E2 = 2*dx;
	setPixelColour(x,y,r,g,b);
	steps = dy;
	while(steps--)
	{
	    y += ystep;
	    if(D > 0)
	    {
		x = x+xstep;
		D = D + E1;
	    }
	    else
	    {
		D = D + E2;
	    }
	    setPixelColour(x,y,r,g,b);
	}
    }
}


// This is not syncronised to the display thread starting the next redraw,
// but for the current demos this doesn't matter.
void swapBuffers(void)
{
    uint32_t *PixelsT;
// Swap front and back buffers.
    PixelsT = PixelsF;
    PixelsF = PixelsB;
    PixelsB = PixelsT;

}


// Structure for a tetris block.
// The blocks array hold the bit patterns in a 4x4 grid for the four rotations of the shape.

typedef struct block 
{
    int size;
    int r,g,b;
    uint16_t blocks[4];
} BLOCK;

BLOCK L = { 4, 0,0,1,
	    {0x0740,0x0622,0x02E0,0x4460} };
BLOCK J = { 4, 1,1,1,
	    {0x0470,0x0644,0x0E20,0x2260} };

BLOCK O = { 4, 1,0,0,
	    {0x0660,0x0660,0x0660,0x0660} };
BLOCK T = { 4, 0,1,0,
	    {0x08C8,0x004E,0x04C4,0x00E4} };
BLOCK I = { 4, 1,0,1,
	    {0x2222,0x00F0,0x4444,0x0F00} };

BLOCK S = { 4, 0,1,1,
	    {0x0360,0x2310,0x0360,0x2310} };
BLOCK Z = { 4, 1,1,0,
	    {0x0630,0x1320,0x0630,0x1320} };




BLOCK *blocks[] = {&L,&J,&O,&T,&S,&I,&S,&Z};
#define SHAPES 8


// Bit patterns for score digits on a 4x5 grid
uint32_t D0 = {0x69996};
uint32_t D1 = {0x26222};
uint32_t D2 = {0xE1687};
uint32_t D3 = {0xE161E};
uint32_t D4 = {0x99611};
uint32_t D5 = {0xF861E};
uint32_t D6 = {0x78696};
uint32_t D7 = {0xF1248};
uint32_t D8 = {0x69696};
uint32_t D9 = {0x69612};
uint32_t DS = {0x00000};

uint32_t *digits[] = {&D0,&D1,&D2,&D3,&D4,&D5,&D6,&D7,&D8,&D9,&DS};

int score;



uint8_t board[32][32];

// Circular buffer for passing key presses from the main thread to the tetris thread.
char keys[100];
int keyw = 0;
int keyr = 0;


// Draw a tetris block at xo,yo 
// Does not put the block into the board array

void drawBlock(BLOCK *bp,int xo,int yo,int or,bool on)
{
    int x,y,rr,gg,bb;
    uint16_t bits;
// Get bits in correct orientation
    bits = bp->blocks[or];
    if(on)
    {
	rr = bp->r;
	gg = bp->g;
	bb = bp->b;
    }
    else
    {
	rr = gg = bb = 0;
    }

    
    for(x=0;x<4;x++)
    {
	for(y=0;y<4;y++)
	{
	    if(bits & 1) setPixelColour(x+xo,y+yo,rr,gg,bb);
	    bits >>= 1;
	}
    }
} 

// Test if a block can be drawn at a particular location
bool testBlock(BLOCK *bp,int xo,int yo,int or)
{
    int x,y;
    uint16_t bits;
    
    bits = bp->blocks[or];

    for(x=0;x<4;x++)
    {
	for(y=0;y<4;y++)
	{
	    if((bits & 1) && (board[x+xo][y+yo] != 0)) return(false) ;
	    bits >>= 1;
	}
    }
    return(true);
} 

// Put a block into the board arry 
void dropBlock(BLOCK *bp,int xo,int yo,int or)
{
    int x,y;
    uint16_t bits;
    uint8_t colour;
    
    bits = bp->blocks[or];
    colour = ((bp->r & 1) << 2) | ((bp->g & 1) << 1) | ((bp->b & 1));
    for(x=0;x<4;x++)
    {
	for(y=0;y<4;y++)
	{
	    if(bits & 1) board[x+xo][y+yo] = colour ;
	    bits >>= 1;
	}
    }
} 

// Draw a digit
void dropDigit(uint32_t *dp,int xo,int yo)
{
    int x,y;
    uint32_t bits;
    
    bits = *dp;

    for(y=5;y>=0;y--)
    {
	for(x=4;x>0;x--)
    	{
	    if(bits & 1) setPixelColour(x+xo,y+yo,1,1,1);
	    else setPixelColour(x+xo,y+yo,0,0,0);
	    bits >>= 1;
	}
    }
    return;
} 

// Draw the score
void showScore(void)
{
    char text[10],*cp;
    int x,y,number;

    // Convert score to string.
    sprintf(text,"%3d",score);

    cp = &text[0];
    y = 1;
    for(x = 0; x<=8; x += 4)
    {
	number = *cp++ - '0';
	if((number<0)||(number>9))  number = 10;
	dropDigit(digits[number],x,y);
    }
}

// Check for full rows and delete them
void checkRows(void)
{
    int full,rowsCleared;
    int x,y,ylower,yupper,r,g,b;
    uint8_t  pixel;

    rowsCleared = 0; 

    // Start checking at the bottom and move upwards
    for(y=30; y > 2; y--)
    {
   
	full = 0;
	// Scan a row
	for(x = 20; x < 31; x+=1)
	{
	    if(board[x][y] != 0) 
	    {
		full +=1;
	    }
	}
    
	if(full == 11)
	{
	    // Move all higher rows down one row
	    for(ylower = y,yupper = y - 1; yupper > 1; yupper--,ylower--)
	    {
		for(x = 20; x < 31; x+=1)
		{
		    pixel = board[x][ylower] = board[x][yupper];
		    setPixelColour(x,ylower,(pixel >> 2) & 1,(pixel >> 1) & 1,pixel & 1);
		}

	    }
	    rowsCleared += 1;
	    y += 1;   // Check same line again after the fall
	}
    }
    // Update the score
    score += rowsCleared;
    showScore();

}


void *startTetrisThread(void *args)
{
    int x,y,rotation,xold,yold,rotationold,t,n;
    char ch;
    BLOCK *blockInPlay;
    int speed;
    bool fast = false;

    // No swapping so make front and back the same
    PixelsF = PixelsB = Pixels1;
    memset(Pixels1,0,sizeof(Pixels1));
   
    memset(board,0,sizeof(board));


    // Draw edges 
    drawLine(19,31,31,31,1,1,1);
    for(x=19;x<32;x++) board[x][31] = 1;

    drawLine(19,0,19,31,1,1,1);
    for(y=0;y<32;y++) board[19][y] = 1;

    drawLine(31,0,31,31,1,1,1);
    for(y=0;y<32;y++) board[31][y] = 1;

    score = 0;
    speed = 20000;

    x = 24; y = 0;
    rotation = 0; t = 0;

    blockInPlay = blocks[t];

    while(!gameStop)
    {
	// Save current position
	xold = x; yold = y; rotationold = rotation;
	

	for(n=0;n<10;n++)
	{
	while(keyw != keyr)
	{
	    //printf("got %c\n",keys[keyr]);
	    ch = keys[keyr];

	    switch(ch)
	    {
	    case '1':
		x -= 1;
		break;
	    case '2':
		// Drop block quickly
		fast = true;
		break;
	    case '3':
		x += 1;
		break;
	    case '5':
		rotation += 1;
		rotation &= 3;
		break;
	    default:
		break;
		
	    }
	    if(testBlock(blockInPlay,x,y,rotation))
	    {
		// Remove from old position, redraw in new position
		drawBlock(blockInPlay,xold,yold,rotationold,false);
		drawBlock(blockInPlay,x,y,rotation,true);
		// Update old position to new position
		xold = x; yold = y; rotationold = rotation;
	    }
	    else
	    {
		// Cant move to new position so restore old position
		x = xold; y = yold; rotation = rotationold;
	    }
	    keyr += 1;
	    keyr %= 100;
	
	}	
	if(fast) usleep(1000); 
	else usleep(speed - (score * 500));
	}

	// Move block down one row
	y += 1;

	if(testBlock(blockInPlay,x,y,rotation))
	{
	    // Update block on the display
	    drawBlock(blockInPlay,xold,yold,rotationold,false);
	    drawBlock(blockInPlay,x,y,rotation,true);
	}
	else
	{
	    // Can't make the move so drop the block
	    dropBlock(blockInPlay,xold,yold,rotationold);
	    // Delete full rows
	    checkRows();
	    // Start new block
	    y = 0;
	    x = 24;
	    rotation = random() & 3;
	    t = random() %  SHAPES;
	    blockInPlay = blocks[t];
	    fast = false;
	}

	showScore();

    }

}


void *startClockThread(void *args)
{
    double seconds,hours,mins,ps,ph,pm;
    int x,y;

    struct tm *now;
    time_t secs;
    
  
    ps = ph = pm = 0;
    memset(PixelsB,0,sizeof(Pixels1));
    while (!gameStop) 
    {
	for(seconds = 0; seconds < 60; seconds += 5)
	{
	    x = 16.5 + 15.0 * sin(2.0 * M_PI * seconds / 60.0);
	    y = 16.5 + 15.0 * -cos(2.0 * M_PI * seconds / 60.0);
	
	    setPixelColour(x,y,1,1,1);
	}

	secs = time(NULL);
	now = localtime(&secs);
	
	seconds = now->tm_sec;
	mins = now->tm_min;
	hours = now->tm_hour % 12;

	hours += mins / 60.0;

	x = 16.5 + 15.0 * sin(2.0 * M_PI * hours / 12.0);
	y = 16.5 + 15.0 * -cos(2.0 * M_PI * hours / 12.0);
	drawLine(x,y,16,16,1,0,0);

	x = 16.5 + 15.0 * sin(2.0 * M_PI * mins / 60.0);
	y = 16.5 + 15.0 * -cos(2.0 * M_PI * mins / 60.0);
	drawLine(x,y,16,16,0,1,0);

	x = 16.5 + 15.0 * sin(2.0 * M_PI * seconds / 60.0);
	y = 16.5 + 15.0 * -cos(2.0 * M_PI * seconds / 60.0);
	drawLine(x,y,16,16,1,1,1);

	ps = seconds;
	pm = mins;
	ph = hours;


	swapBuffers();

	memset(PixelsB,0,sizeof(Pixels1));

	// No point in updating more than once a second !
	sleep(1);
    }
}



void *startKelidescopeThread(void *args)
{
    uint8_t pixels[256],value,colour;
    
    int counter,step,xy,yx,x,y;
    int r, g, b;

    // No swapping so make front and back the same
    PixelsF = PixelsB = Pixels1;
    memset(Pixels1,0,sizeof(Pixels1));

    memset(pixels,0,sizeof(pixels));
    step = 1;
    counter = 0;
    
    xy = 0;
    while (!gameStop) {

      
	if(counter == 256*4)
	{
	    counter = 1;
	    step += 1;
	    xy = 0;
	}
	else
	{
	    counter += 1;
	}
	usleep(5 * 1000);
      
     
	xy &= 255;
	x = xy & 15;
	y = (xy >> 4) & 15;

	yx = ((xy & 15) << 4) | ((xy >> 4) & 15);

	colour = pixels[xy];
	colour += 1;
	colour &= 7;
	pixels[xy] = colour;

    
	colour = pixels[yx];
	colour += 1;
	colour &= 7;
	pixels[yx] = colour;
  
	xy += step; 
      
	value = 0xFF;
	switch (colour) 
	{
	case 0: r = g = b = 0; break;
	case 1: 
	case 4:r = value; g = b = 0; break;

	case 2: 
	case 5: g = value; r = b = 0; break;

	case 3: 
	case 6: b = value; r = g = 0; break;
 
	case 7: r = g = b = value; break;
      
	default: r = g = b = 0; break;
	}

      
	setPixelColour(x+16, 16-y, r, g, b);
	setPixelColour(y+16, 16-x, r, g, b);    
 
	setPixelColour(-x+16, 16-y, r, g, b);
	setPixelColour(-y+16, 16-x, r, g, b);    

	setPixelColour(x+16, 16+y, r, g, b);
	setPixelColour(y+16, 16+x, r, g, b);    
 
	setPixelColour(-x+16, 16+y, r, g, b);
	setPixelColour(-y+16, 16+x, r, g, b);    
    }
    // Restore the buffer pointers
    PixelsF = Pixels1;
    PixelsB = Pixels2;
}








void *startSquaresThread(void *args)
{
    int x,y,xleft,xright,ytop,ybottom,temp;
    int r,g,b;

    // No swapping so make front and back the same
    PixelsF = PixelsB = Pixels1;

    while(!gameStop)
    {
	xleft = random();
	xright = (xleft >> 5) & 31;
	xleft &= 31;

	ytop = random();
	ybottom = (ytop >> 5) & 31;
	ytop &= 31;

	if(xleft > xright)
	{
	    temp = xleft; xleft = xright; xright = temp;
	}
	if(ytop > ybottom)
	{
	    temp = ytop; ytop = ybottom; ybottom = temp;
	}

	switch (random() % 8) 
	{
	case 0: r = 1; g = b = 0; break;
	case 1: g = 1; r = b = 0; break;
	case 2: b = 1; r = g = 0; break;
	case 3: g = b = 1; r = 0; break;
	case 4: g = r = 1; b = 0; break;
	case 5: b = r = 1; g = 0; break;
	case 6: r = g = b = 1; break;
	case 7: r = g = b = 0; break;
	default: r = g = b = 0; break;
	}

	for(x = xleft; x <= xright; x += 1)
	{
	    for(y = ytop; y <= ybottom; y += 1)
	    {
		setPixelColour(x,y,r,g,b);
	    }
	}



	usleep(100 * 1000);

    }
    // Restore the buffer pointers.
    PixelsF = Pixels1;
    PixelsB = Pixels2;

}

void *startLifeThread(void *args) 
{

    uint8_t Cells[32][32],thisgen,nextgen,temp8,r,g,b;

    int generations = 0;
    int x,y,n,xp,xm,yp,ym;
    int neighbours,population,previousPopulation,change,stable;
    // Clear the board
    memset(Cells,0,sizeof(Cells));
  
    // Set bits for generation flags in Cells.
    thisgen = 0x80;
    nextgen = 0x40;

    // Drop an initial Glider
    // Cells[16][16] = Cells[15][16] = Cells[17][16] = thisgen;
    // Cells[15][17] = Cells[16][18] = thisgen;

    population = previousPopulation = stable = 0;

    while (!gameStop) {
      
	// Drop a block if pattern is stable
	// for too long
	if(stable > 16)
	{
	    stable = 0;
	    x = random();
	    y = (x >> 5) & 31;
	    x &= 31;
	    xp = (x + 1) & 31;
	    yp = (y + 1) & 31;
	    Cells[x][y] = Cells[xp][y] = Cells[xp][yp] = Cells[x][yp] = thisgen;
	    printf("Dropped a block %d\a\n",generations);
	}

	previousPopulation = population;
	population = 0;

	for(x=0;x<32;x++)
	{
	    // Calculate adjacent coordinates with correct wrap at edges
	    xp = (x + 1) & 31;
	    xm = (x - 1) & 31;

	    for(y=0;y<32;y++)
	    {
		yp = (y + 1) & 31;
		ym = (y - 1) & 31;

		
		// Count the number of currently live neighbouring cells 
		neighbours  = Cells[x ][y] & thisgen ? 10 : 0;
		neighbours += Cells[xm][y] & thisgen ? 1 : 0;
		neighbours += Cells[xp][y] & thisgen ? 1 : 0;
		neighbours += Cells[xm][ym] & thisgen ? 1 : 0;
		neighbours += Cells[x ][ym] & thisgen ? 1 : 0;
		neighbours += Cells[xp][ym] & thisgen ? 1 : 0;
		neighbours += Cells[xm][yp] & thisgen ? 1 : 0;
		neighbours += Cells[x ][yp] & thisgen ? 1 : 0;
		neighbours += Cells[xp][yp] & thisgen ? 1 : 0;

		
		temp8 = Cells[x][y];
		temp8 &= ~nextgen;

		// Conway's life rules....
		switch(neighbours)
		{
		case 0:
		case 1:
		case 2:
		    // Dead and staying dead
		    r = g = b = 0x0;
		    break;
		case 3:
		    // Birth
		    temp8 |= nextgen;
		    g = 0xFF;
		    r = b = 0x0;
		    population += 1;
		    break;
		case 4:
		case 5:
		case 6:
		case 7:
		case 8:
		case 9:
		    // Dead and staying dead
		    r = g = b = 0x0;
		    break;
		case 10:
		case 11:
		    // Alive but dying
		    r = 0xFF;
		    g = b = 0x0;
		    population += 1;
		    break;
		case 12:
		case 13:
		    // Alive and staying alive
		    temp8 |= nextgen;
		    b = 0xFF;
		    g = r = 0x0;
		    population += 1;
		    break;
		case 14:
		case 15:
		case 16:
		case 17:
		case 18:
		case 19:
		default:      
		    // Alive but dying
		    r = 0xFF;
		    g = b = 0x0;
		    population += 1;
		    break;
		}
            
		// Update cell state
		Cells[x][y] = temp8;
		// Update pixel colour
		setPixelColour(x, y, r, g, b);
	    }
	}

	// swap meaning of thisgen and nextgen flags 
	temp8 = nextgen;
	nextgen = thisgen;
	thisgen = temp8;

	// Swap front and back buffers.
	swapBuffers();

	// Not needed as every pixel is drawn every time
	//memset(PixelsB,0,sizeof(Pixels1));

	// Sleep to set game rate
	usleep(1000 * 50);
	generations += 1;
	
	change = population-previousPopulation;
	if((change < 4) && (change > -4))
	{
	    stable += 1;
	}
	else
	{
	    stable = 0;
	}
    }
}

// Thread states
pthread_t displayThread;
pthread_t gameThread;


// Ctrl-C handler
void stop(int sig)
{
    displayRunning = false;
    gameStop = true;
}


int main(int argc, char **argv)
{
    struct sched_param p;
    static struct termios oldt, newt;
    int ch;

    int x,y,z,n;

    struct sigaction new_sa;
    struct sigaction old_sa;
    sigfillset(&new_sa.sa_mask);
    new_sa.sa_handler = SIG_IGN;
    new_sa.sa_flags = 0;


    // Set up handler for ctrl-c to shut down properly
    if (sigaction(SIGINT, &new_sa, &old_sa) == 0 && old_sa.sa_handler != SIG_IGN)
    {
	new_sa.sa_handler = stop;
	sigaction(SIGINT, &new_sa, 0);
    }


    printf("Press 'k' to start Kelidescope\nPress 'K' to stop Kelidescope\n"
	   "Press 'l' to start Life\nPress 'L' to stop Life\n"
	   "Press 's' tp start Squares\nPress 'S' to stop Squares\n"
	   "Press 'c' to start Clock\nPress 'C' to stop Clock\n"
	   "Press 't' to start Tetris\nPress 'T' to stop Tetris\n"
	   "Press 'q' to quit.");

    displayRunning = true;
    gameRunning = false;
    
    // Start the display
    pthread_create(&displayThread, NULL, &startDisplayThread,NULL);
  
    // Up the priority of the display thread
    p.sched_priority = 10;
    pthread_setschedparam(displayThread, SCHED_FIFO, &p);


    // Set keyboard to get characters as they are pressed.
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON| ECHO);
    tcsetattr(STDIN_FILENO,TCSANOW,&newt);

    do
    {
	ch = getchar();
	switch(ch)
	{
	case 'q':
	    displayRunning = false;
	    gameStop = true;
	    break;

	case 'k':
	    // Start kelidescope
	    if(gameRunning) break;
	    gameRunning = true;
	    gameStop = false;
	    
	    pthread_create(&gameThread, NULL, &startKelidescopeThread,NULL);
	    break;

	case 'l':
	    // Start life
	    if(gameRunning) break;
	    gameRunning = true;
	    gameStop = false;
	    
	    pthread_create(&gameThread, NULL, &startLifeThread,NULL);
	    break;

	case 's':
	    // Start squares
	    if(gameRunning) break;
	    gameRunning = true;
	    gameStop = false;
	    
	    pthread_create(&gameThread, NULL, &startSquaresThread,NULL);
	    break;

	case 'c':
	    // Start clock
	    if(gameRunning) break;
	    gameRunning = true;
	    gameStop = false;
	    
	    pthread_create(&gameThread, NULL, &startClockThread,NULL);
	    break;

	    // Put digits into buffer 
	case '1':
	case '2':
	case '3':
	case '5':
	    keys[keyw] = ch;
	    n = keyw + 1;
	    n %= 100;
	    keyw = n;
	    break;

	case 't':
	    // Start Tetris
	    if(gameRunning) break;
	    gameRunning = true;
	    gameStop = false;
	    printf("Controls are 1 2 3 5 on key pad\n"); 
	    pthread_create(&gameThread, NULL, &startTetrisThread,NULL);
	    break;

	case 'L':
	case 'K':
	case 'S':
	case 'C':
	case 'T':

	    // Stop game
	    if(!gameRunning) break;
	    gameStop = true;
	    pthread_join(gameThread, NULL);	
	    gameRunning = false;
	    break;

	default:
	    break;
	}
    } while(displayRunning);


    // Tidy up threads
    pthread_join(displayThread, NULL);
    if(gameRunning) pthread_join(gameThread, NULL);

    printf("\nThanks for watching!\n");

    // Restore keyboard mode.
    tcsetattr(STDIN_FILENO,TCSANOW,&oldt);

}

