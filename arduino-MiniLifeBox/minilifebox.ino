/*
 MiniLifeBox
 Copyright (c) 2014 Ferran Fàbregas
 Based on:
 Colorduino - Colorduino DEMO for Arduino.
 Copyright (c) 2010 zzy@IteadStudio.  All right reserved.
 Copyright (c) 2014 Dr. Mathias Wilhelm - adoption of code to run on UNO and Mega boards.

 This is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.

 This DEMO is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */
 
#include <avr/pgmspace.h>
#include <MsTimer2.h>

/***************************************************
 * define pins used and fast manipulation routines
 ***************************************************/
#define cbi(reg, bitmask) *reg &= ~bitmask
#define sbi(reg, bitmask) *reg |= bitmask
#define RST_PIN A2
#define LAT_PIN A1
#define SLB_PIN A0
#define SCL_PIN 6
#define SDA_PIN 7
#define L0_PIN 8
#define L1_PIN 9
#define L2_PIN 10
#define L3_PIN 11
#define L4_PIN 12
#define L5_PIN 13
#define L6_PIN 3
#define L7_PIN 4

volatile uint8_t *P_RST, *P_LAT, *P_SLB, *P_SDA, *P_SCL;
uint8_t           B_RST,  B_LAT,  B_SLB,  B_SDA,  B_SCL;
volatile uint8_t *P_L0, *P_L1, *P_L2, *P_L3, *P_L4, *P_L5, *P_L6, *P_L7;
uint8_t           B_L0,  B_L1,  B_L2,  B_L3,  B_L4,  B_L5,  B_L6,  B_L7;

#define open_line0    {sbi(P_L0,B_L0);}
#define open_line1    {sbi(P_L1,B_L1);}
#define open_line2    {sbi(P_L2,B_L2);}
#define open_line3    {sbi(P_L3,B_L3);}
#define open_line4    {sbi(P_L4,B_L4);}
#define open_line5    {sbi(P_L5,B_L5);}
#define open_line6    {sbi(P_L6,B_L6);}
#define open_line7    {sbi(P_L7,B_L7);}

// Define LifeBox parameters
#define PLANTS_LIFE_EXPECTANCY 255
#define PLANTS_RANDOM_BORN_CHANCES 100 // high is less chances
#define PLANTS_RANDOM_NEARBORN_CHANCES 10
#define PLANTS_RANDOM_DIE_CHANCES 2
#define PLANTS_ENERGY_BASE_PER_CYCLE 10

#define SPECIE1_LIFE_EXPECTANCY 200
#define SPECIE1_RANDOM_BORN_CHANCES 1000
#define SPECIE1_RANDOM_NEARBORN_CHANCES 100
#define SPECIE1_RANDOM_DIE_CHANCES 2
#define SPECIE1_ENERGY_BASE 10
#define SPECIE1_ENERGY_NEEDED_PER_CYCLE 2
#define SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE 10
#define SPECIE1_ENERGY_TO_REPLICATE 15

#define SPECIE2_LIFE_EXPECTANCY 180
#define SPECIE2_RANDOM_BORN_CHANCES 1000
#define SPECIE2_RANDOM_NEARBORN_CHANCES 100
#define SPECIE2_RANDOM_DIE_CHANCES 2
#define SPECIE2_ENERGY_BASE 10
#define SPECIE2_ENERGY_NEEDED_PER_CYCLE 2
#define SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE 20
#define SPECIE2_ENERGY_TO_REPLICATE 11

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

PLANT plantes[8][8];
SPECIE specie1[8][8];
SPECIE specie2[8][8];

void close_all_line()
{
  cbi(P_L0, B_L0);
  cbi(P_L1, B_L1);
  cbi(P_L2, B_L2);
  cbi(P_L3, B_L3);
  cbi(P_L4, B_L4);
  cbi(P_L5, B_L5);
  cbi(P_L6, B_L6);
  cbi(P_L7, B_L7);
  cbi(P_SDA, B_SDA);
  cbi(P_SCL, B_SCL);
}

/*******************************************
 * define the data zone
 *******************************************/

unsigned char dots[2][8][8][3] = {0};
//dots matrix
//[2]:Page:one for display, one for receive data
//[8]:Row:8 row in LED plane
//[8]:Column:8 column in one row
//[3]:Color:RGB data: 0 for Red; 1 for green, 2 for Blue
unsigned char Gamma_Value[3] = { 10, 63, 63 };
//Gamma correctly value, every LED plane is different.value range is 0~63
//[3]:RGB data, 0 for Red; 1 for green, 2 for Blue
unsigned char Page_Index = 0; // the index of buffer
unsigned char row = 0;        //the value of row in LED plane, from 0~7
unsigned char column = 0;     //the value of every row, from 0~7
unsigned char color = 0;      //the value of every dots, 0 is Red, 1 is Green, 2 is Blue

volatile unsigned char line = 0;

/**************************************************
 * define the extern data zone
 **************************************************/
extern unsigned char font8_8[92][8];
extern unsigned char pic[4][8][8][3];

/***************************************************
 * all parts inition functions zone
 ***************************************************/
void _IO_Init()
{
  P_RST = portOutputRegister(digitalPinToPort(RST_PIN));
  B_RST = digitalPinToBitMask(RST_PIN);
  P_LAT = portOutputRegister(digitalPinToPort(LAT_PIN));
  B_LAT = digitalPinToBitMask(LAT_PIN);
  P_SLB = portOutputRegister(digitalPinToPort(SLB_PIN));
  B_SLB = digitalPinToBitMask(SLB_PIN);
  P_SDA = portOutputRegister(digitalPinToPort(SDA_PIN));
  B_SDA = digitalPinToBitMask(SDA_PIN);
  P_SCL = portOutputRegister(digitalPinToPort(SCL_PIN));
  B_SCL = digitalPinToBitMask(SCL_PIN);
  P_L0 = portOutputRegister(digitalPinToPort(L0_PIN));
  B_L0 = digitalPinToBitMask(L0_PIN);
  P_L1 = portOutputRegister(digitalPinToPort(L1_PIN));
  B_L1 = digitalPinToBitMask(L1_PIN);
  P_L2 = portOutputRegister(digitalPinToPort(L2_PIN));
  B_L2 = digitalPinToBitMask(L2_PIN);
  P_L3 = portOutputRegister(digitalPinToPort(L3_PIN));
  B_L3 = digitalPinToBitMask(L3_PIN);
  P_L4 = portOutputRegister(digitalPinToPort(L4_PIN));
  B_L4 = digitalPinToBitMask(L4_PIN);
  P_L5 = portOutputRegister(digitalPinToPort(L5_PIN));
  B_L5 = digitalPinToBitMask(L5_PIN);
  P_L6 = portOutputRegister(digitalPinToPort(L6_PIN));
  B_L6 = digitalPinToBitMask(L6_PIN);
  P_L7 = portOutputRegister(digitalPinToPort(L7_PIN));
  B_L7 = digitalPinToBitMask(L7_PIN);
  for (int i = 0; i < 14; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  digitalWrite(A0, LOW);
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
}

void _LED_Init()
{
  LED_RST(1);
  LED_Delay(1);
  LED_RST(0);
  LED_Delay(1);
  LED_RST(1);
  LED_Delay(1);
  SetGamma();
  line = 0;
}

void timer()          //Timer2  Service
{
  cli();
  if(line > 7) line = 0;    
  close_all_line();  
  run(line);
  open_line(line);
  line++;
  sei();
}

/****************************************************
 * the LED Hardware operate functions zone
 ****************************************************/
void LED_rgbSDA(unsigned char temp)
{
  if (temp)
    sbi(P_SDA, B_SDA);
  else
    cbi(P_SDA, B_SDA);
}

void LED_rgbSCL(unsigned char temp)
{
  if (temp)
    sbi(P_SCL, B_SCL);
  else
    cbi(P_SCL, B_SCL);
}

void LED_RST(unsigned char temp)
{
  if (temp)
    sbi(P_RST, B_RST);
  else
    cbi(P_RST, B_RST);
}

void LED_LAT(unsigned char temp)
{
  if (temp)
    sbi(P_LAT, B_LAT);
  else
    cbi(P_LAT, B_LAT);
}

void LED_SLB(unsigned char temp)
{
  if (temp)
    sbi(P_SLB, B_SLB);
  else
    cbi(P_SLB, B_SLB);
}
/***************************************************
 * the LED datas operate functions zone
 ***************************************************/
void SetGamma()
{
  unsigned char i = 0;
  unsigned char j = 0;
  unsigned char k = 0;
  unsigned char temp = 0;
  LED_LAT(0);
  LED_SLB(0);
  for (k = 0; k < 8; k++)
    for (i = 3; i > 0 ; i--)
    {
      temp = Gamma_Value[i - 1] << 2;
      for (j = 0; j < 6; j++)
      {
        if (temp & 0x80)
          LED_rgbSDA(1);
        else
          LED_rgbSDA(0);
        temp = temp << 1;
        LED_rgbSCL(0);
        LED_rgbSCL(1);
      }
    }
  LED_SLB(1);
}

void run(unsigned char k)
{
  unsigned char i = 0;
  unsigned char j = 0;
  unsigned char p = 0;
  unsigned char temp = 0;
  LED_SLB(1);
  LED_LAT(0);
  for (i = 0; i < 8; i++)
  {
    for (j = 0; j < 3; j++)
    {
      temp = dots[Page_Index][k][i][2 - j];
      for (p = 0; p < 8; p++)
      {
        if (temp & 0x80)
          LED_rgbSDA(1);
        else
          LED_rgbSDA(0);
        temp = temp << 1;
        LED_rgbSCL(0);
        LED_rgbSCL(1);
      }
    }
  }
  LED_LAT(1);
  LED_LAT(0);
}

void open_line(unsigned char x)
{
  switch (x)
  {
    case 0 :
      open_line0;
      break;
    case 1 :
      open_line1;
      break;
    case 2 :
      open_line2;
      break;
    case 3 :
      open_line3;
      break;
    case 4 :
      open_line4;
      break;
    case 5 :
      open_line5;
      break;
    case 6 :
      open_line6;
      break;
    case 7 :
      open_line7;
      break;
    default:
      close_all_line;
      break;
  }
}


void DispShowDot(unsigned char R, unsigned char G, unsigned char B, unsigned char x,unsigned char y)
{
    dots[0][x][y][2] = R;
    dots[0][x][y][1] = G;
    dots[0][x][y][0] = B;
}



/******************************************
 * the other operate functions zone
 ******************************************/
void LED_Delay(unsigned char i)
{
  unsigned int y;
  y = i * 10;
  while (y--);
}

/****************************************************
 * Main Functions zone
 ****************************************************/
void setup()
{
  _IO_Init();           //Init IO
  _LED_Init();          //Init LED Hardware
  MsTimer2::set(2, timer); // 500ms period
  MsTimer2::start();
  randomSeed(analogRead(0));
}

void loop()
{
  unsigned int dly = 150;
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
  //srandom(time(NULL));
  while (1) {
	// Screen test
	/*
        for (x = 0; x < 8; x++) {
		for (y = 0; y < 8; y++) {
			DispShowDot(50,50,50,x,y);
			delay(dly);
		}
	}
        */
	
	for(x=0;x<8;x++) {
			// Calculate adjacent coordinates with correct wrap at edges
			xp = (x + 1) & 7;
			xm = (x - 1) & 7;
			for(y=0;y<8;y++) {
				yp = (y + 1) & 7;
				ym = (y - 1) & 7;
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
				if (specie1[x][y].age>0 && specie2[x][y].age>0) { DispShowDot(255,0,255,x,y); } // magenta if species comp
				if (specie1[x][y].age>0 && specie2[x][y].age==0) { DispShowDot(20,100,50,x,y); } // yellow-like only specie1
				if (specie1[x][y].age==0 && specie2[x][y].age>0) { DispShowDot(0,0,255,x,y); } // blue only specie2
				if (specie1[x][y].age==0 && specie2[x][y].age==0 && plantes[x][y].age>0) { DispShowDot(100,255,100,x,y); } // green-like only plants
				if (specie1[x][y].age==0 && specie2[x][y].age==0 && plantes[x][y].age==0) { DispShowDot(0,0,0,x,y); } // black nothing
			}
		}
		// Sleep to set game rate
		delay(dly);
      
	}

}