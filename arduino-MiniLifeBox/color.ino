/*
  Colorduino - Colorduino DEMO for Arduino.
 Copyright (c) 2010 zzy@IteadStudio.  All right reserved.
 Copyright (c) 2014 Dr. Mathias Wilhelm - adoption of code to run on UNO and Mega boards.

 This DEMO is free software; you can redistribute it and/or
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
/********************************************************
 * Name:DispShowChar
 * Function:Display a English latter in LED matrix
 * Parameter:chr :the latter want to show
 * R: the value of RED.   Range:RED 0~255
 * G: the value of GREEN. Range:RED 0~255
 * B: the value of BLUE.  Range:RED 0~255
 * bias: the bias of a letter in LED Matrix.Range -7~7
 ********************************************************/
void DispShowChar(char chr, unsigned char R, unsigned char G, unsigned char B, char bias)
{
  unsigned char i, j, Page_Write, temp;
  unsigned char Char;
  unsigned char chrtemp[24] = {0};
  if ((bias > 8) || (bias < -8))
    return;
  Char = chr - 32;
  if (Page_Index == 0)
    Page_Write = 1;
  if (Page_Index == 1)
    Page_Write = 0;
  j = 8 - bias;
  for (i = 0; i < 8; i++)
  {
    chrtemp[j] = pgm_read_byte(&(font8_8[Char][i]));
    j++;
  }
  for (i = 0; i < 8; i++)
  {
    temp = chrtemp[i + 8];
    for (j = 0; j < 8; j++)
    {
      if (temp & 0x80)
      {
        dots[Page_Write][j][i][0] = B;
        dots[Page_Write][j][i][1] = G;
        dots[Page_Write][j][i][2] = R;
      }
      else
      {
        dots[Page_Write][j][i][0] = 0;
        dots[Page_Write][j][i][1] = 0;
        dots[Page_Write][j][i][2] = 0;
      }
      temp = temp << 1;
    }
  }
  Page_Index = Page_Write;
}
/********************************************************
 * Name:DispShowColor
 * Function:Fill a color in LED matrix
 * Parameter:R: the value of RED.   Range:RED 0~255
 * G: the value of GREEN. Range:RED 0~255
 * B: the value of BLUE.  Range:RED 0~255
 ********************************************************/
void DispShowColor(unsigned char R, unsigned char G, unsigned char B)
{
  unsigned char Page_Write, i, j;

  if (Page_Index == 0)
    Page_Write = 1;
  if (Page_Index == 1)
    Page_Write = 0;
  for (i = 0; i < 8; i++)
    for (j = 0; j < 8; j++)
    {
      dots[Page_Write][i][j][2] = R;
      dots[Page_Write][i][j][1] = G;
      dots[Page_Write][i][j][0] = B;
    }
  Page_Index = Page_Write;
}
/********************************************************
 * Name:DispShowPic
 * Function:Fill a picture in LED matrix from FLASH
 * Parameter:Index:the index of picture in Flash.
 ********************************************************/
void DispShowPic(unsigned char Index)
{
  unsigned char Page_Write, i, j;

  if (Page_Index == 0)
    Page_Write = 1;
  if (Page_Index == 1)
    Page_Write = 0;
  for (i = 0; i < 8; i++)
  {
    for (j = 0; j < 8; j++)
    {
      dots[Page_Write][i][j][0] = pgm_read_byte(&(pic[Index][i][j][0]));
      dots[Page_Write][i][j][1] = pgm_read_byte(&(pic[Index][i][j][1]));
      dots[Page_Write][i][j][2] = pgm_read_byte(&(pic[Index][i][j][2]));
    }
  }
  Page_Index = Page_Write;
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
}

void loop()
{
  unsigned int i = 250;
  char j = 0;
  while (1)
  {
    i = 250;
    DispShowPic(0);
    delay(i);
    DispShowPic(1);
    delay(i);
    DispShowPic(2);
    delay(i);
    DispShowPic(3);
    delay(i);
    DispShowPic(4);
    delay(i);
    DispShowPic(5);
    delay(i);
    DispShowPic(6);
    delay(i);
    DispShowChar('A', 255, 0, 0, 0);
    delay(i);
    DispShowChar('B', 0, 255, 0, 0);
    delay(i);
    DispShowChar('C', 0, 0, 255, 0);
    delay(i);
    DispShowChar('D', 255, 255, 255, 0);
    delay(i);
    DispShowChar('E', 0, 255, 255, 0);
    delay(i);
    DispShowChar('F', 255, 255, 0, 0);
    delay(i);
    DispShowChar('G', 255, 0, 255, 0);
    delay(i);
    DispShowChar('H', 255, 127, 0, 0);
    delay(i);
    DispShowChar('I', 127, 255, 0, 0);
    delay(i);
    DispShowChar('J', 127, 0, 255, 0);
    delay(i);
    DispShowChar('K', 255, 127, 127, 0);
    delay(i);
    DispShowChar('L', 127, 127, 255, 0);
    delay(i);
    DispShowChar('M', 127, 255, 127, 0);
    delay(i);
    DispShowChar('N', 255, 127, 255, 0);
    delay(i);
    DispShowChar('O', 200, 120, 120, 0);
    delay(i);
    DispShowChar('P', 120, 200, 120, 0);
    delay(i);
    DispShowChar('Q', 200, 120, 120, 0);
    delay(i);
    DispShowChar('R', 120, 120, 200, 0);
    delay(i);
    DispShowChar('S', 120, 120, 120, 0);
    delay(i);
    DispShowChar('T', 127, 0, 100, 0);
    delay(i);
    DispShowChar('U', 255, 0, 200, 0);
    delay(i);
    DispShowChar('V', 200, 255, 120, 0);
    delay(i);
    DispShowChar('W', 120, 200, 200, 0);
    delay(i);
    DispShowChar('X', 200, 200, 120, 0);
    delay(i);
    DispShowChar('Y', 127, 0, 180, 0);
    delay(i);
    DispShowChar('Z', 0, 1800, 200, 0);
    delay(i);
    DispShowChar('a', 255, 0, 0, 0);
    delay(i);
    DispShowChar('b', 0, 255, 0, 0);
    delay(i);
    DispShowChar('c', 0, 0, 255, 0);
    delay(i);
    DispShowChar('d', 255, 255, 255, 0);
    delay(i);
    DispShowChar('e', 0, 255, 255, 0);
    delay(i);
    DispShowChar('f', 255, 255, 0, 0);
    delay(i);
    DispShowChar('g', 255, 0, 255, 0);
    delay(i);
    DispShowChar('h', 255, 127, 0, 0);
    delay(i);
    DispShowChar('i', 127, 255, 0, 0);
    delay(i);
    DispShowChar('j', 127, 0, 255, 0);
    delay(i);
    DispShowChar('k', 255, 127, 127, 0);
    delay(i);
    DispShowChar('l', 127, 127, 255, 0);
    delay(i);
    DispShowChar('m', 127, 255, 127, 0);
    delay(i);
    DispShowChar('n', 255, 127, 255, 0);
    delay(i);
    DispShowChar('0', 200, 120, 120, 0);
    delay(i);
    DispShowChar('p', 120, 200, 120, 0);
    delay(i);
    DispShowChar('q', 200, 120, 120, 0);
    delay(i);
    DispShowChar('r', 120, 120, 200, 0);
    delay(i);
    DispShowChar('s', 120, 120, 120, 0);
    delay(i);
    DispShowChar('t', 127, 0, 100, 0);
    delay(i);
    DispShowChar('u', 255, 0, 200, 0);
    delay(i);
    DispShowChar('v', 200, 255, 120, 0);
    delay(i);
    DispShowChar('w', 120, 200, 200, 0);
    delay(i);
    DispShowChar('x', 200, 200, 120, 0);
    delay(i);
    DispShowChar('y', 127, 0, 180, 0);
    delay(i);
    DispShowChar('z', 0, 1800, 200, 0);
    delay(i);
    DispShowChar('0', 200, 120, 120, 0);
    delay(i);
    DispShowChar('1', 120, 120, 200, 0);
    delay(i);
    DispShowChar('2', 120, 120, 120, 0);
    delay(i);
    DispShowChar('3', 127, 0, 100, 0);
    delay(i);
    DispShowChar('4', 255, 0, 200, 0);
    delay(i);
    DispShowChar('5', 200, 255, 120, 0);
    delay(i);
    DispShowChar('6', 120, 200, 200, 0);
    delay(i);
    DispShowChar('7', 200, 200, 120, 0);
    delay(i);
    DispShowChar('8', 127, 0, 180, 0);
    delay(i);
    DispShowChar('9', 0, 1800, 200, 0);
    delay(i);

    DispShowPic(0);
    delay(i);
    DispShowPic(1);
    delay(i);
    DispShowPic(2);
    delay(i);
    DispShowPic(3);
    delay(i);

    i = 50;
    for (j = -7; j < 7; j++)
    {
      DispShowChar('E', 255, 255, 0, j);
      delay(i);
    }
    for (j = -7; j < 7; j++)
    {
      DispShowChar('l', 0, 255, 255, j);
      delay(i);
    }
    for (j = -7; j < 7; j++)
    {
      DispShowChar('e', 255, 0, 255, j);
      delay(i);
    }
    for (j = -7; j < 7; j++)
    {
      DispShowChar('c', 255, 255, 255, j);
      delay(i);
    }
    for (j = -7; j < 7; j++)
    {
      DispShowChar('f', random(255), random(255), random(255), j);
      delay(i);
    }
    for (j = -7; j < 7; j++)
    {
      DispShowChar('r', random(255), random(255), random(255), j);
      delay(i);
    }
    for (j = -7; j < 7; j++)
    {
      DispShowChar('e', random(255), random(255), random(255), j);
      delay(i);
    }
    for (j = -7; j < 7; j++)
    {
      DispShowChar('a', random(255), random(255), random(255), j);
      delay(i);
    }
    for (j = -7; j < 7; j++)
    {
      DispShowChar('k', random(255), random(255), random(255), j);
      delay(i);
    }
    for (j = -7; j < 7; j++)
    {
      DispShowChar('s', random(255), random(255), random(255), j);
      delay(i);
    }
    for (j = -7; j < 7; j++)
    {
      DispShowChar('*', random(255), random(255), random(255), j);
      delay(i);
    }

    DispShowPic(0);
    delay(i);
    DispShowPic(1);
    delay(i);
    DispShowPic(2);
    delay(i);
    DispShowPic(3);
    delay(i);
    DispShowPic(4);
    delay(i);
    DispShowPic(5);
    delay(i);
  }
}
