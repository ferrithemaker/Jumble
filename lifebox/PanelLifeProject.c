// Code to drive the 32x32 LED arrays available from SKPANG 
// http://skpang.co.uk/catalog/rgb-led-panel-32x32-p-1329.html
// Based on code from https://github.com/hzeller/rpi-rgb-led-matrix
// Which contains the following copyright notice:
// Code is (c) Henner Zeller h.zeller@acm.org, and I grant you the
// permission to do whatever you want with it :)

// This code is (c) Peter Onion (Peter.Onion@btinternet.com), and I too grant you the
// permission to do whatever you want with it, as long as this header block
// is retained in any code you may distribute that uses or is based on this code.
// Life Simulator game is (c) of Ferran Fabregas (ferri.fc@gmail.com) 
// gcc -o PanelLifeProject PanelLifeProject.c -lm -lpthread


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

#define PLANTS_LIFE_EXPECTANCY 255
#define PLANTS_RANDOM_BORN_CHANCES 1000 // high is less chances
#define PLANTS_RANDOM_NEARBORN_CHANCES 100
#define PLANTS_RANDOM_DIE_CHANCES 2
#define PLANTS_ENERGY_BASE_PER_CYCLE 10

#define SPECIE1_LIFE_EXPECTANCY 200
#define SPECIE1_RANDOM_BORN_CHANCES 10000
#define SPECIE1_RANDOM_NEARBORN_CHANCES 100
#define SPECIE1_RANDOM_DIE_CHANCES 2
#define SPECIE1_ENERGY_BASE 10
#define SPECIE1_ENERGY_NEEDED_PER_CYCLE 2
#define SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE 10
#define SPECIE1_ENERGY_TO_REPLICATE 15

#define SPECIE2_LIFE_EXPECTANCY 180
#define SPECIE2_RANDOM_BORN_CHANCES 10000
#define SPECIE2_RANDOM_NEARBORN_CHANCES 100
#define SPECIE2_RANDOM_DIE_CHANCES 2
#define SPECIE2_ENERGY_BASE 10
#define SPECIE2_ENERGY_NEEDED_PER_CYCLE 2
#define SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE 20
#define SPECIE2_ENERGY_TO_REPLICATE 11



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

void *startLifeSimulatorThread(void *args)
{
	typedef struct plants
	{
   		int age;
   		int energy;
	} PLANT;

	typedef struct species
	{
   		int age;
   		int energy;
	} SPECIE;

	PLANT plantes[32][32];
	SPECIE specie1[32][32];
	SPECIE specie2[32][32];
	
	int x,y,xp,xm,yp,ym;
	int plants_neighbours,specie1_neighbours,specie2_neighbours;
	int i;
	int available[8];
	memset(available,0,sizeof(available));
	int pos;
	int random_number;
	int rand_pos;
	int loopcount=0;
	int total_energy;

	// Clear the board
	memset(plantes,0,sizeof(plantes));
	memset(specie1,0,sizeof(specie1));
	memset(specie2,0,sizeof(specie2));
	
	srandom(time(NULL));
	while (1) { // bucle principal
		for(x=0;x<32;x++) {
			// Calculate adjacent coordinates with correct wrap at edges
			xp = (x + 1) & 31;
			xm = (x - 1) & 31;

			for(y=0;y<32;y++) {
				yp = (y + 1) & 31;
				ym = (y - 1) & 31;
				//printf("%i\n",loopcount);
				loopcount++;	
				// Count the number of currently live neighbouring cells
				plants_neighbours=0;
				specie1_neighbours=0;
				specie2_neighbours=0;
				// [Plants]
				if (plantes[x][y].age==0 && plantes[xm][y].age>0) { plants_neighbours++; }
				if (plantes[x][y].age==0 && plantes[xp][y].age>0) { plants_neighbours++; }
				if (plantes[x][y].age==0 && plantes[xm][ym].age>0) { plants_neighbours++; }
				if (plantes[x][y].age==0 && plantes[x][ym].age>0) { plants_neighbours++; }
				if (plantes[x][y].age==0 && plantes[xp][ym].age>0) { plants_neighbours++; }
				if (plantes[x][y].age==0 && plantes[xm][yp].age>0) { plants_neighbours++; }
				if (plantes[x][y].age==0 && plantes[x][yp].age>0) { plants_neighbours++; }
				if (plantes[x][y].age==0 && plantes[xp][yp].age>0) { plants_neighbours++; }
				// [Specie1]
				if (specie1[x][y].age==0 && specie1[xm][y].age>0) { specie1_neighbours++; }
				if (specie1[x][y].age==0 && specie1[xp][y].age>0) { specie1_neighbours++; }
				if (specie1[x][y].age==0 && specie1[xm][ym].age>0) { specie1_neighbours++; }
				if (specie1[x][y].age==0 && specie1[x][ym].age>0) { specie1_neighbours++; }
				if (specie1[x][y].age==0 && specie1[xp][ym].age>0) { specie1_neighbours++; }
				if (specie1[x][y].age==0 && specie1[xm][yp].age>0) { specie1_neighbours++; }
				if (specie1[x][y].age==0 && specie1[x][yp].age>0) { specie1_neighbours++; }
				if (specie1[x][y].age==0 && specie1[xp][yp].age>0) { specie1_neighbours++; }
				// [Specie2]
				if (specie2[x][y].age==0 && specie2[xm][y].age>0) { specie2_neighbours++; }
				if (specie2[x][y].age==0 && specie2[xp][y].age>0) { specie2_neighbours++; }
				if (specie2[x][y].age==0 && specie2[xm][ym].age>0) { specie2_neighbours++; }
				if (specie2[x][y].age==0 && specie2[x][ym].age>0) { specie2_neighbours++; }
				if (specie2[x][y].age==0 && specie2[xp][ym].age>0) { specie2_neighbours++; }
				if (specie2[x][y].age==0 && specie2[xm][yp].age>0) { specie2_neighbours++; }
				if (specie2[x][y].age==0 && specie2[x][yp].age>0) { specie2_neighbours++; }
				if (specie2[x][y].age==0 && specie2[xp][yp].age>0) { specie2_neighbours++; }	
				
				// Plants logic
				if (plantes[x][y].age>=PLANTS_LIFE_EXPECTANCY) { plantes[x][y].age=0; plantes[x][y].energy=0;  } // plant dies
				if (plantes[x][y].age>0 && plantes[x][y].age<PLANTS_LIFE_EXPECTANCY && plantes[x][y].energy<=0) { plantes[x][y].age=0; plantes[x][y].energy=0; } // plant dies
				if (plantes[x][y].age>0 && plantes[x][y].age<PLANTS_LIFE_EXPECTANCY ) { plantes[x][y].age++; plantes[x][y].energy=plantes[x][y].energy+PLANTS_ENERGY_BASE_PER_CYCLE; } // plant grows
				if (plantes[x][y].age==0 && plants_neighbours==0) { // no neighbours plant born
					//srand(time(NULL));
					random_number = random() % PLANTS_RANDOM_BORN_CHANCES;
					//printf("%i\n",random_number);
					if (random_number==1) { plantes[x][y].age=1; plantes[x][y].energy=1;}
				} 
				if (plantes[x][y].age==0 && plants_neighbours>0) {  // neighbours plant born
					//srand(time(NULL));
					random_number = random() % PLANTS_RANDOM_NEARBORN_CHANCES;
					if (random_number==1) { plantes[x][y].age=1; plantes[x][y].energy=1; }
				}
				
				// Specie1 logic
				if (specie1[x][y].age>0) { // if there are an individual alive
					// try to eat
					if (plantes[x][y].energy>0) { 
						total_energy=0;
						if (plantes[x][y].energy>SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE) { total_energy=SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE; plantes[x][y].energy=plantes[x][y].energy-SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE; }
					else { total_energy=plantes[x][y].energy; plantes[x][y].energy=0;}
					specie1[x][y].energy=specie1[x][y].energy+total_energy;
					}
					// grow and decrease energy
					specie1[x][y].age++;
					specie1[x][y].energy=specie1[x][y].energy-SPECIE1_ENERGY_NEEDED_PER_CYCLE;
					if (specie1[x][y].energy<0) { specie1[x][y].energy=0; specie1[x][y].age=0;} // die
					// try to replicate
					if (specie1[x][y].energy>SPECIE1_ENERGY_TO_REPLICATE) {
						for (i=0;i<8;i++) { available[i]=0; }
						pos=0;
						//srand(time(NULL));
						random_number = random() % SPECIE1_RANDOM_NEARBORN_CHANCES;
						if (specie1[xm][y].age==0) { available[pos]=1; pos++; }
						if (specie1[xp][y].age==0) { available[pos]=2; pos++; }
						if (specie1[xm][ym].age==0) { available[pos]=3; pos++; }
						if (specie1[x][ym].age==0) { available[pos]=4; pos++; }
						if (specie1[xp][ym].age==0) { available[pos]=5; pos++; }
						if (specie1[xm][yp].age==0) { available[pos]=6; pos++; }
						if (specie1[x][yp].age==0) { available[pos]=7; pos++; }
						if (specie1[xp][yp].age==0) { available[pos]=8; pos++; }
						//srand(time(NULL));
						if (pos>0) {
							rand_pos=random() % pos;
							switch (available[rand_pos]) { // one individual born radomly
								case 1: if (random_number==1) { specie1[xm][y].age=1; specie1[xm][y].energy=SPECIE1_ENERGY_BASE; } break;
								case 2: if (random_number==1) { specie1[xp][y].age=1; specie1[xp][y].energy=SPECIE1_ENERGY_BASE; } break;
								case 3: if (random_number==1) { specie1[xm][ym].age=1; specie1[xm][ym].energy=SPECIE1_ENERGY_BASE; } break;
								case 4: if (random_number==1) { specie1[x][ym].age=1; specie1[x][ym].energy=SPECIE1_ENERGY_BASE; } break;
								case 5: if (random_number==1) { specie1[xp][ym].age=1; specie1[xp][ym].energy=SPECIE1_ENERGY_BASE; } break;
								case 6: if (random_number==1) { specie1[xm][yp].age=1; specie1[xm][yp].energy=SPECIE1_ENERGY_BASE; } break;
								case 7: if (random_number==1) { specie1[x][yp].age=1; specie1[x][yp].energy=SPECIE1_ENERGY_BASE; } break;
								case 8: if (random_number==1) { specie1[xp][yp].age=1; specie1[xp][yp].energy=SPECIE1_ENERGY_BASE; } break;
								default: printf("ERROR\n"); break; // all full
							}
						}
					}
					// die if too old
					if (specie1[x][y].age>SPECIE1_LIFE_EXPECTANCY) { specie1[x][y].energy=0; specie1[x][y].age=0;}
				}
				if (specie1[x][y].age==0) { // if theres no individual, new individual will born? (to avoid extintion)
					if (specie1_neighbours==0) {
						//srand(time(NULL));
						random_number = random() % SPECIE1_RANDOM_BORN_CHANCES;
						if (random_number==1) { specie1[x][y].age=1; specie1[x][y].energy=SPECIE1_ENERGY_BASE; }
					}
				}
				
				// Specie2 logic
				
				if (specie2[x][y].age>0) { // if there are an individual alive
					// try to eat
					if (plantes[x][y].energy>0) { 
						total_energy=0;
						if (plantes[x][y].energy>SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE) { total_energy=SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE; plantes[x][y].energy=plantes[x][y].energy-SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE; }
						else { total_energy=plantes[x][y].energy; plantes[x][y].energy=0;}
						specie2[x][y].energy=specie2[x][y].energy+total_energy;
					}
					// grow and decrease energy
					specie2[x][y].age++;
					specie2[x][y].energy=specie2[x][y].energy-SPECIE2_ENERGY_NEEDED_PER_CYCLE;
					if (specie2[x][y].energy<0) { specie2[x][y].energy=0; specie2[x][y].age=0;} // die
					// try to replicate
					if (specie2[x][y].energy>SPECIE2_ENERGY_TO_REPLICATE) {
						for (i=0;i<8;i++) { available[i]=0; }
						pos=0;
						//srand(time(NULL));
						random_number = random() % SPECIE2_RANDOM_NEARBORN_CHANCES;
						if (specie2[xm][y].age==0) { available[pos]=1; pos++; }
						if (specie2[xp][y].age==0) { available[pos]=2; pos++; }
						if (specie2[xm][ym].age==0) { available[pos]=3; pos++; }
						if (specie2[x][ym].age==0) { available[pos]=4; pos++; }
						if (specie2[xp][ym].age==0) { available[pos]=5; pos++; }
						if (specie2[xm][yp].age==0) { available[pos]=6; pos++; }
						if (specie2[x][yp].age==0) { available[pos]=7; pos++; }
						if (specie2[xp][yp].age==0) { available[pos]=8; pos++; }
						//srand(time(NULL));
						if (pos>0) {
							rand_pos=random() % pos;
							switch (available[rand_pos]) { // one individual born radomly
								case 1: if (random_number==1) { specie2[xm][y].age=1; specie2[xm][y].energy=SPECIE2_ENERGY_BASE; } break;
								case 2: if (random_number==1) { specie2[xp][y].age=1; specie2[xp][y].energy=SPECIE2_ENERGY_BASE; } break;
								case 3: if (random_number==1) { specie2[xm][ym].age=1; specie2[xm][ym].energy=SPECIE2_ENERGY_BASE; }break;
								case 4: if (random_number==1) { specie2[x][ym].age=1; specie2[x][ym].energy=SPECIE2_ENERGY_BASE; } break;
								case 5: if (random_number==1) { specie2[xp][ym].age=1; specie2[xp][ym].energy=SPECIE2_ENERGY_BASE; } break;
								case 6: if (random_number==1) { specie2[xm][yp].age=1; specie2[xm][yp].energy=SPECIE2_ENERGY_BASE; } break;
								case 7: if (random_number==1) { specie2[x][yp].age=1; specie2[x][yp].energy=SPECIE2_ENERGY_BASE; } break;
								case 8: if (random_number==1) { specie2[xp][yp].age=1; specie2[xp][yp].energy=SPECIE2_ENERGY_BASE; } break;
								// default: break; // all full
							}
						}
					}
				// die if too old
				if (specie2[x][y].age>SPECIE2_LIFE_EXPECTANCY) { specie2[x][y].energy=0; specie2[x][y].age=0;}
				}
				if (specie2[x][y].age==0) { // if theres no individual, new individual will born? (to avoid extintion)
					if (specie2_neighbours==0) {
						//srand(time(NULL));
						random_number = random() % SPECIE2_RANDOM_BORN_CHANCES;
						if (random_number==1) { specie2[x][y].age=1; specie2[x][y].energy=SPECIE2_ENERGY_BASE; }
					}
				}
				
				// draw
				if (specie1[x][y].age>0 && specie2[x][y].age>0) { setPixelColour(x,y,1,1,0); } // yellow if species comp
				if (specie1[x][y].age>0 && specie2[x][y].age==0) { setPixelColour(x,y,1,0,0); } // red only specie1
				if (specie1[x][y].age==0 && specie2[x][y].age>0) { setPixelColour(x,y,0,0,1); } // blue only specie2
				if (specie1[x][y].age==0 && specie2[x][y].age==0 && plantes[x][y].age>0) { setPixelColour(x,y,0,1,0); } // green only plants
				if (specie1[x][y].age==0 && specie2[x][y].age==0 && plantes[x][y].age==0) { setPixelColour(x,y,0,0,0); } // black nothing
			}
		}
				
		swapBuffers();
		//memset(PixelsB,0,sizeof(Pixels1));
		// Sleep to set game rate
		usleep(1000 *50);
	}
printf("Surt del bucle\n");
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

    displayRunning = true;
    gameRunning = false;
    
    // Start the display
    pthread_create(&displayThread, NULL, &startDisplayThread,NULL);
  
    // Up the priority of the display thread
    p.sched_priority = 10;
    pthread_setschedparam(displayThread, SCHED_FIFO, &p);


    // Start life
    gameRunning = true;
    gameStop = false;
    pthread_create(&gameThread, NULL, &startLifeSimulatorThread,NULL);
	    


    // Tidy up threads
    pthread_join(displayThread, NULL);
    if(gameRunning) pthread_join(gameThread, NULL);

    printf("\nThanks for watching!\n");

    // Restore keyboard mode.
    tcsetattr(STDIN_FILENO,TCSANOW,&oldt);

}

