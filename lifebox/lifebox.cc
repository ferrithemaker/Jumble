// -*- mode: c++; c-basic-offset: 2; indent-tabs-mode: nil; -*-
//
// This code is public domain
// (but note, once linked against the led-matrix library, this is
// covered by the GPL v2)
//
// This is a grab-bag of various demos and not very readable.
#include "led-matrix.h"
#include "threaded-canvas-manipulator.h"
#include "transformer.h"
#include "graphics.h"

#include <assert.h>
#include <getopt.h>
#include <limits.h>
#include <math.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <thread>

#include <algorithm>

#include <iostream>
#include <stdexcept>
#include <string>
#include <cstring>
#include <vector>

using std::min;
using std::max;
std::string potValues;
int controldata[21] = { 0 };

#define TERM_ERR  "\033[1;31m"
#define TERM_NORM "\033[0m"

using namespace rgb_matrix;

volatile bool interrupt_received = false;
static void InterruptHandler(int signo) {
  interrupt_received = true;
}

std::string exec(const char* cmd) {
    char buffer[128];
    std::string result = "";
    FILE* pipe = popen(cmd, "r");
    if (!pipe) throw std::runtime_error("popen() failed!");
    try {
        while (!feof(pipe)) {
            if (fgets(buffer, 128, pipe) != NULL)
                result += buffer;
        }
    } catch (...) {
        pclose(pipe);
        throw;
    }
    pclose(pipe);
    return result;
}

std::vector<std::string> split(std::string str,std::string sep){
    char* cstr=const_cast<char*>(str.c_str());
    char* current;
    std::vector<std::string> arr;
    current=strtok(cstr,sep.c_str());
    while(current!=NULL){
        arr.push_back(current);
        current=strtok(NULL,sep.c_str());
    }
    return arr;
}

void getPotValues() {
  int lastdata[21];
	while (!interrupt_received) {
		potValues = exec("cat /var/www/html/lifeboxdata");
		std::vector<std::string> arr;
		arr=split(potValues,"|");
		for(size_t i=0;i<arr.size();i++) {
			//printf("%s\n",arr[i].c_str());
			lastdata[i]=atoi((arr[i].c_str()));
      if (lastdata[i]<controldata[i]) { controldata[i]--; }
      if (lastdata[i]>controldata[i]) { controldata[i]++; }
			//printf("%i - %i\n",i,controldata[i]);
		}
		//std::cout << potValues;
		//printf("%s\n",arr[7].c_str());
		//printf("%i\n",controldata[7]);
		usleep(1000000);
	}
  }


// lifebox
class LifeBox : public ThreadedCanvasManipulator {
public:
  LifeBox(Canvas *m) : ThreadedCanvasManipulator(m) {
    width_ = canvas()->width();
    height_ = canvas()->height();

    // Clear the board
  	memset(theplants,0,sizeof(theplants));
  	memset(specie1,0,sizeof(specie1));
  	memset(specie2,0,sizeof(specie2));
    memset(available,0,sizeof(available));

    // Init values randomly
    srandom(time(NULL));
    // srand(time(NULL));

  }
  // destrueix la classe, allibera la memoria
  ~LifeBox() {

  }

  void Run() {
	  // TODO Random die
    while (running() && !interrupt_received) {
      plants_last_individuals = plants_individuals;
      specie2_last_individuals = specie2_individuals;
      specie1_last_individuals = specie1_individuals;
      specie2_individuals = 0;
      specie1_individuals = 0;
      plants_individuals = 0;
		for(x=0;x<32;x++) {
  			// Calculate adjacent coordinates with correct wrap at edges
  			xp = (x + 1);
			if (xp >= 32) { xp = 31; }
  			xm = (x - 1);
			if (xm < 0) { xm = 0; }

  			for(y=0;y<32;y++) {
  				yp = (y + 1);
				if (yp >= 32) { yp = 31; }
  				ym = (y - 1);
				if (ym < 0) { ym = 0; }

  				// Count the number of currently live neighbouring cells
  				plants_neighbours=0;
  				specie1_neighbours=0;
  				specie2_neighbours=0;
  				// [Plants]
  				if (theplants[x][y].age==0 && theplants[xm][y].age>0) { plants_neighbours++; }
  				if (theplants[x][y].age==0 && theplants[xp][y].age>0) { plants_neighbours++; }
  				if (theplants[x][y].age==0 && theplants[xm][ym].age>0) { plants_neighbours++; }
  				if (theplants[x][y].age==0 && theplants[x][ym].age>0) { plants_neighbours++; }
  				if (theplants[x][y].age==0 && theplants[xp][ym].age>0) { plants_neighbours++; }
  				if (theplants[x][y].age==0 && theplants[xm][yp].age>0) { plants_neighbours++; }
  				if (theplants[x][y].age==0 && theplants[x][yp].age>0) { plants_neighbours++; }
  				if (theplants[x][y].age==0 && theplants[xp][yp].age>0) { plants_neighbours++; }
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


  				if (theplants[x][y].age>=(int)((PLANTS_LIFE_EXPECTANCY+controldata[16]))) { theplants[x][y].age=0; theplants[x][y].energy=0;  } // plant dies
  				if (theplants[x][y].age>0 && theplants[x][y].age<(int)((PLANTS_LIFE_EXPECTANCY+controldata[16])) && theplants[x][y].energy<=0) { theplants[x][y].age=0; theplants[x][y].energy=0; } // plant dies
  				if (theplants[x][y].age>0 && theplants[x][y].age<(int)((PLANTS_LIFE_EXPECTANCY+controldata[16]))) { theplants[x][y].age++; theplants[x][y].energy=theplants[x][y].energy+(int)(PLANTS_ENERGY_BASE_PER_CYCLE+controldata[20]); plants_individuals = plants_individuals + 1; } // plant grows
  				if (theplants[x][y].age==0 && plants_neighbours==0) { // no neighbours plant born
  					//srand(time(NULL));
  					if (controldata[18]>0 && plants_neighbours == 0 && ((plants_last_individuals == 0 && plants_individuals == 0 && realistic_mode == 1) || realistic_mode == 0)) {
						int randomborn;
						if (PLANTS_RANDOM_BORN_CHANCES-controldata[18] < 2) { randomborn = 2; } else { randomborn = PLANTS_RANDOM_BORN_CHANCES-controldata[18]; }
						random_number = random() % (int)(randomborn);
						if (random_number==1) { theplants[x][y].age=1; theplants[x][y].energy=1; plants_individuals = plants_individuals + 1;}
					}
  				}
  				if (theplants[x][y].age==0 && plants_neighbours>0) {  // neighbours plant born
  					//srand(time(NULL));
  					if (controldata[17]>0) {
						int randomborn;
						if (PLANTS_NEARBORN_CHANCES-controldata[17] < 2) { randomborn = 2; } else { randomborn = PLANTS_NEARBORN_CHANCES-controldata[17]; }
						random_number = random() % (int)(randomborn);
						if (random_number==1) { theplants[x][y].age=1; theplants[x][y].energy=1; 	plants_individuals = plants_individuals + 1;}
					}
  				}

  				// Specie1 logic
  				if (specie1[x][y].age>0) { // if there are an individual alive
            specie1_individuals = specie1_individuals + 1;
  					// try to eat
  					if (theplants[x][y].energy>0) {
  						total_energy=0;
  						if (theplants[x][y].energy>SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE+controldata[6]) { total_energy=SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE+controldata[6]; theplants[x][y].energy=theplants[x][y].energy-SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE+controldata[6]; } // ERROR, FALTA PARENTESIS RESTA
  					else { total_energy=theplants[x][y].energy; theplants[x][y].energy=0;}
  					specie1[x][y].energy=specie1[x][y].energy+total_energy;
  					}
  					// grow and decrease energy
  					specie1[x][y].age++;
  					specie1[x][y].energy=specie1[x][y].energy-(int)(SPECIE1_ENERGY_NEEDED_PER_CYCLE+controldata[5]);
  					if (specie1[x][y].energy<0) { specie1[x][y].energy=0; specie1[x][y].age=0;} // die
  					// try to replicate
  					if (specie1[x][y].energy>(int)(SPECIE1_ENERGY_TO_REPLICATE+controldata[7])) {
  						for (i=0;i<8;i++) { available[i]=0; }
  						pos=0;
  						//srand(time(NULL));
  						if (controldata[1]>0) {
							int randomborn;
							if (SPECIE1_NEARBORN_CHANCES-controldata[1] < 2) { randomborn = 2; } else { randomborn = SPECIE1_NEARBORN_CHANCES-controldata[1]; }
							random_number = random() % (int)(randomborn);
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
									case 1: if (random_number==1) { specie1[xm][y].age=1; specie1[xm][y].energy=(int)(SPECIE1_ENERGY_BASE+controldata[4]); specie1_individuals = specie1_individuals + 1;} break;
									case 2: if (random_number==1) { specie1[xp][y].age=1; specie1[xp][y].energy=(int)(SPECIE1_ENERGY_BASE+controldata[4]); specie1_individuals = specie1_individuals + 1; } break;
									case 3: if (random_number==1) { specie1[xm][ym].age=1; specie1[xm][ym].energy=(int)(SPECIE1_ENERGY_BASE+controldata[4]); specie1_individuals = specie1_individuals + 1;} break;
									case 4: if (random_number==1) { specie1[x][ym].age=1; specie1[x][ym].energy=(int)(SPECIE1_ENERGY_BASE+controldata[4]); specie1_individuals = specie1_individuals + 1;} break;
									case 5: if (random_number==1) { specie1[xp][ym].age=1; specie1[xp][ym].energy=(int)(SPECIE1_ENERGY_BASE+controldata[4]); specie1_individuals = specie1_individuals + 1;} break;
									case 6: if (random_number==1) { specie1[xm][yp].age=1; specie1[xm][yp].energy=(int)(SPECIE1_ENERGY_BASE+controldata[4]); specie1_individuals = specie1_individuals + 1;} break;
									case 7: if (random_number==1) { specie1[x][yp].age=1; specie1[x][yp].energy=(int)(SPECIE1_ENERGY_BASE+controldata[4]); specie1_individuals = specie1_individuals + 1;} break;
									case 8: if (random_number==1) { specie1[xp][yp].age=1; specie1[xp][yp].energy=(int)(SPECIE1_ENERGY_BASE+controldata[4]); specie1_individuals = specie1_individuals + 1;} break;
									default: printf("ERROR\n"); break; // all full
								}
							}
						}
  					}
  					// die if too old
  					if (specie1[x][y].age>(int)((SPECIE1_LIFE_EXPECTANCY+controldata[0]))) { specie1[x][y].energy=0; specie1[x][y].age=0;}
  				}
  				if (specie1[x][y].age==0) { // if theres no individual, new individual will born? (to avoid extintion)
  					if (specie1_neighbours==0 && ((specie1_last_individuals == 0 && specie1_individuals == 0 && realistic_mode == 1) || realistic_mode == 0)) {
  						//srand(time(NULL));
  						if (controldata[2]>0) {
							int randomborn;
							if (SPECIE1_RANDOM_BORN_CHANCES-controldata[2] < 2) { randomborn = 2; } else { randomborn = SPECIE1_RANDOM_BORN_CHANCES-controldata[2]; }
							random_number = random() % (int)(randomborn);
							if (random_number==1) { specie1[x][y].age=1; specie1[x][y].energy=(int)(SPECIE1_ENERGY_BASE+controldata[4]); specie1_individuals = specie1_individuals + 1;}
						}
  					}
  				}


  				// Specie2 logic

  				if (specie2[x][y].age>0) { // if there are an individual alive
  					// try to eat
            specie2_individuals = specie2_individuals + 1;
  					if (theplants[x][y].energy>0) {
  						total_energy=0;
  						if (theplants[x][y].energy>SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE+controldata[14]) { total_energy=SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE+controldata[14]; theplants[x][y].energy=theplants[x][y].energy-SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE+controldata[14]; }
  						else { total_energy=theplants[x][y].energy; theplants[x][y].energy=0;}
  						specie2[x][y].energy=specie2[x][y].energy+total_energy;
  					}
  					// grow and decrease energy
  					specie2[x][y].age++;
  					specie2[x][y].energy=specie2[x][y].energy-(int)(SPECIE2_ENERGY_NEEDED_PER_CYCLE+controldata[13]);
  					if (specie2[x][y].energy<0) { specie2[x][y].energy=0; specie2[x][y].age=0;} // die
  					// try to replicate
  					if (specie2[x][y].energy>(int)(SPECIE2_ENERGY_TO_REPLICATE+controldata[15])) {
  						for (i=0;i<8;i++) { available[i]=0; }
  						pos=0;
  						//srand(time(NULL));
  						if (controldata[9] >0) {
							int randomborn;
							if (SPECIE2_NEARBORN_CHANCES-controldata[9] < 2) { randomborn = 2; } else { randomborn = SPECIE2_NEARBORN_CHANCES-controldata[9]; }
							random_number = random() % (int)(randomborn);
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
									case 1: if (random_number==1) { specie2[xm][y].age=1; specie2[xm][y].energy=(int)(SPECIE2_ENERGY_BASE+controldata[12]); specie2_individuals = specie2_individuals + 1;} break;
									case 2: if (random_number==1) { specie2[xp][y].age=1; specie2[xp][y].energy=(int)(SPECIE2_ENERGY_BASE+controldata[12]); specie2_individuals = specie2_individuals + 1;} break;
									case 3: if (random_number==1) { specie2[xm][ym].age=1; specie2[xm][ym].energy=(int)(SPECIE2_ENERGY_BASE+controldata[12]); specie2_individuals = specie2_individuals + 1;}break;
									case 4: if (random_number==1) { specie2[x][ym].age=1; specie2[x][ym].energy=(int)(SPECIE2_ENERGY_BASE+controldata[12]); specie2_individuals = specie2_individuals + 1;} break;
									case 5: if (random_number==1) { specie2[xp][ym].age=1; specie2[xp][ym].energy=(int)(SPECIE2_ENERGY_BASE+controldata[12]); specie2_individuals = specie2_individuals + 1;} break;
									case 6: if (random_number==1) { specie2[xm][yp].age=1; specie2[xm][yp].energy=(int)(SPECIE2_ENERGY_BASE+controldata[12]); specie2_individuals = specie2_individuals + 1;} break;
									case 7: if (random_number==1) { specie2[x][yp].age=1; specie2[x][yp].energy=(int)(SPECIE2_ENERGY_BASE+controldata[12]); specie2_individuals = specie2_individuals + 1;} break;
									case 8: if (random_number==1) { specie2[xp][yp].age=1; specie2[xp][yp].energy=(int)(SPECIE2_ENERGY_BASE+controldata[12]); specie2_individuals = specie2_individuals + 1;} break;
									// default: break; // all full
								}
							}
						}
  					}
  				// die if too old
  				if (specie2[x][y].age>(int)((SPECIE2_LIFE_EXPECTANCY+controldata[8]))) { specie2[x][y].energy=0; specie2[x][y].age=0;}
  				}
  				if (specie2[x][y].age==0) { // if theres no individual, new individual will born? (to avoid extintion)
  					if (specie2_neighbours==0 && ((specie2_last_individuals == 0 && specie2_individuals == 0 && realistic_mode == 1) || realistic_mode == 0)) {
  						//srand(time(NULL));
  						if (controldata[10] > 0) {
							int randomborn;
							if (SPECIE2_RANDOM_BORN_CHANCES-controldata[10] < 2) { randomborn = 2; } else { randomborn = SPECIE2_RANDOM_BORN_CHANCES-controldata[10]; }
							random_number = random() % (int)(randomborn);
							if (random_number==1) { specie2[x][y].age=1; specie2[x][y].energy=(int)(SPECIE2_ENERGY_BASE+controldata[12]); specie2_individuals = specie2_individuals + 1; }
						}
  					}
  				}

          // draw
          if (gradient_mode == 1) {
            if (specie1[x][y].age==0 && specie2[x][y].age==0 && theplants[x][y].age>0) {
              if (theplants[x][y].energy>255) {
				red = 255; green = 255; blue = 255;
				}
			  else {
				red = theplants[x][y].energy; green = theplants[x][y].energy; blue = theplants[x][y].energy;
			  }
			}
            if (specie1[x][y].age>0 && specie2[x][y].age==0) {
				if (specie1[x][y].energy>255) {
					red = 255; green = 255; blue = 0;
				}
				else {
					red = specie1[x][y].energy; green = specie1[x][y].energy; blue = 0;
				}
			}
            if (specie1[x][y].age==0 && specie2[x][y].age>0) {
              if (specie2[x][y].energy>255) {
				red = 0; green = 0; blue = 255;
			  }
			  else {
                red = 0; green= 0; blue = specie2[x][y].energy;
              }
            }
            if (specie1[x][y].age>0 && specie2[x][y].age>0) {
              if (specie1[x][y].energy+specie2[x][y].energy>255) {
				red = 255; green = 0; blue = 255;
			  }
              else {
    			red = specie1[x][y].energy+specie2[x][y].energy; green = 0; blue = specie1[x][y].energy+specie2[x][y].energy;
              }
		    }
          }

          if (gradient_mode == 0) {
  				      if (specie1[x][y].age>0 && specie2[x][y].age>0) { canvas()->SetPixel(x, y, 255, 0, 255); } // species comp
  				      if (specie1[x][y].age>0 && specie2[x][y].age==0) { canvas()->SetPixel(x, y, 255, 255, 0);} // only specie1
  				      if (specie1[x][y].age==0 && specie2[x][y].age>0) { canvas()->SetPixel(x, y, 0, 255, 255); } // only specie2
  				      if (specie1[x][y].age==0 && specie2[x][y].age==0 && theplants[x][y].age>0) { canvas()->SetPixel(x, y, 255, 255, 255); } // only plants
  				      if (specie1[x][y].age==0 && specie2[x][y].age==0 && theplants[x][y].age==0) {   canvas()->SetPixel(x, y, 0, 0, 0); } // black nothing
          } else {
                if (specie1[x][y].age>0 && specie2[x][y].age>0) { canvas()->SetPixel(x, y, red, green, blue); } // species comp
                if (specie1[x][y].energy>species_draw_threshold && specie2[x][y].energy<=species_draw_threshold) { canvas()->SetPixel(x, y, red, green, blue);} // only specie1
                if (specie1[x][y].energy<=species_draw_threshold && specie2[x][y].energy>species_draw_threshold) { canvas()->SetPixel(x, y, red, green, blue); } // only specie2
                if (specie1[x][y].energy<=species_draw_threshold && specie2[x][y].energy<species_draw_threshold && theplants[x][y].energy>plants_draw_threshold) { canvas()->SetPixel(x, y, red, green, blue); } // only plants
                if (specie1[x][y].energy<species_draw_threshold && specie2[x][y].energy<species_draw_threshold && theplants[x][y].energy<plants_draw_threshold) {   canvas()->SetPixel(x, y, 0, 0, 0); } // black nothing
          }
  			}
  		}


  		usleep(TIME_TO_DRAW);


      // END
    }
  }

private:

  int width_;
  int height_;

  int realistic_mode = 1;
  int gradient_mode = 1;

  int red,green,blue;

  int specie2_individuals = 0;
  int specie1_individuals = 0;
  int plants_individuals = 0;
  int plants_last_individuals;
  int specie2_last_individuals;
  int specie1_last_individuals;

  int species_draw_threshold = 50;
  int plants_draw_threshold = 50;

  const int PLANTS_LIFE_EXPECTANCY = 100;
  const int PLANTS_RANDOM_BORN_CHANCES = 1000;
  const int PLANTS_NEARBORN_CHANCES = 100;
  const int PLANTS_RANDOM_DIE_CHANCES = 2; // not used now
  const int PLANTS_ENERGY_BASE_PER_CYCLE = 5;

  const int SPECIE1_LIFE_EXPECTANCY = 200;
  const int SPECIE1_RANDOM_BORN_CHANCES = 5000;
  const int SPECIE1_NEARBORN_CHANCES = 12;
  const int SPECIE1_RANDOM_DIE_CHANCES = 2; // not used now
  const int SPECIE1_ENERGY_BASE = 20;
  const int SPECIE1_ENERGY_NEEDED_PER_CYCLE = 5;
  const int SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE = 7;
  const int SPECIE1_ENERGY_TO_REPLICATE = 5;

  const int SPECIE2_LIFE_EXPECTANCY = 200;
  const int SPECIE2_RANDOM_BORN_CHANCES = 5000;
  const int SPECIE2_NEARBORN_CHANCES = 12;
  const int SPECIE2_RANDOM_DIE_CHANCES = 2; // not used now
  const int SPECIE2_ENERGY_BASE = 20;
  const int SPECIE2_ENERGY_NEEDED_PER_CYCLE = 5;
  const int SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE = 7;
  const int SPECIE2_ENERGY_TO_REPLICATE = 5;

  const int TIME_TO_DRAW = 20000;

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

	PLANT theplants[32][32];
	SPECIE specie1[32][32];
	SPECIE specie2[32][32];

  int x,y,xp,xm,yp,ym;
	int plants_neighbours,specie1_neighbours,specie2_neighbours;
	int i;
	int available[8];
	int pos;
	int random_number;
	int rand_pos;
	int total_energy;
	int cycles=0;
};



static int usage(const char *progname) {
  fprintf(stderr, "usage: %s <options> -D <demo-nr> [optional parameter]\n",
          progname);
  fprintf(stderr, "Options:\n");
  fprintf(stderr,
          "\t-D <demo-nr>              : Always needs to be set\n"
          "\t-L                        : Large display, in which each chain is 'folded down'\n"
          "\t                            in the middle in an U-arrangement to get more vertical space.\n"
          "\t-R <rotation>             : Sets the rotation of matrix. "
          "Allowed: 0, 90, 180, 270. Default: 0.\n"
          "\t-t <seconds>              : Run for these number of seconds, then exit.\n");


  rgb_matrix::PrintMatrixFlags(stderr);


  return 1;
}

int main(int argc, char *argv[]) {
  int runtime_seconds = -1;
  int rotation = 0;
  bool large_display = false;

  RGBMatrix::Options matrix_options;
  rgb_matrix::RuntimeOptions runtime_opt;

  // These are the defaults when no command-line flags are given.
  matrix_options.rows = 32;
  matrix_options.chain_length = 1;
  matrix_options.parallel = 1;

  // First things first: extract the command line flags that contain
  // relevant matrix options.
  if (!ParseOptionsFromFlags(&argc, &argv, &matrix_options, &runtime_opt)) {
    return usage(argv[0]);
  }

  int opt;
  while ((opt = getopt(argc, argv, "t:r:P:c:p:b:LR:hH")) != -1) {
    switch (opt) {

   case 't':
      runtime_seconds = atoi(optarg);
      break;

    case 'R':
      rotation = atoi(optarg);
      break;

    case 'L':
      if (matrix_options.chain_length == 1) {
        // If this is still default, force the 64x64 arrangement.
        matrix_options.chain_length = 4;
      }
      large_display = true;
      break;

      // These used to be options we understood, but deprecated now. Accept
      // but don't mention in usage()
    case 'd':
      runtime_opt.daemon = 1;
      break;

    case 'r':
      matrix_options.rows = atoi(optarg);
      break;

    case 'P':
      matrix_options.parallel = atoi(optarg);
      break;

    case 'c':
      matrix_options.chain_length = atoi(optarg);
      break;

    case 'p':
      matrix_options.pwm_bits = atoi(optarg);
      break;

    case 'b':
      matrix_options.brightness = atoi(optarg);
      break;

	case 'h':
		return usage(argv[0]);

    default: /* '?' */
      return usage(argv[0]);
    }
  }


  if (rotation % 90 != 0) {
    fprintf(stderr, TERM_ERR "Rotation %d not allowed! "
            "Only 0, 90, 180 and 270 are possible.\n" TERM_NORM, rotation);
    return 1;
  }

  RGBMatrix *matrix = CreateMatrixFromOptions(matrix_options, runtime_opt);
  if (matrix == NULL)
    return 1;

  if (large_display) {
    // Mapping the coordinates of a 32x128 display mapped to a square of 64x64.
    // Or any other U-arrangement.
    matrix->ApplyStaticTransformer(UArrangementTransformer(
                                     matrix_options.parallel));
  }

  if (rotation > 0) {
    matrix->ApplyStaticTransformer(RotateTransformer(rotation));
  }

  printf("Size: %dx%d. Hardware gpio mapping: %s\n",
         matrix->width(), matrix->height(), matrix_options.hardware_mapping);

  Canvas *canvas = matrix;

  // The ThreadedCanvasManipulator objects are filling
  // the matrix continuously.
  ThreadedCanvasManipulator *image_gen = NULL;

  image_gen = new LifeBox(canvas);

  std::thread pv(getPotValues);

  if (image_gen == NULL)
    return usage(argv[0]);

  // Set up an interrupt handler to be able to stop animations while they go
  // on. Note, each demo tests for while (running() && !interrupt_received) {},
  // so they exit as soon as they get a signal.
  signal(SIGTERM, InterruptHandler);
  signal(SIGINT, InterruptHandler);

  // Image generating demo is crated. Now start the thread.
  image_gen->Start();

  // Now, the image generation runs in the background. We can do arbitrary
  // things here in parallel. In this demo, we're essentially just
  // waiting for one of the conditions to exit.
  if (runtime_seconds > 0) {
    sleep(runtime_seconds);
  } else {
    // The
    printf("Press <CTRL-C> to exit and reset LEDs\n");
    while (!interrupt_received) {
      sleep(1); // Time doesn't really matter. The syscall will be interrupted.
    }
  }

  // Stop image generating thread. The delete triggers
  delete image_gen;
  delete canvas;

  printf("\%s. Exiting.\n",
         interrupt_received ? "Received CTRL-C" : "Timeout reached");
  return 0;
}
