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
    while (running() && !interrupt_received) {

      for(x=0;x<32;x++) {
  			// Calculate adjacent coordinates with correct wrap at edges
  			xp = (x + 1) & 31;
  			xm = (x - 1) & 31;

  			for(y=0;y<32;y++) {
  				yp = (y + 1) & 31;
  				ym = (y - 1) & 31;

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

  				//printf("%d\n",(int)((PLANTS_LIFE_EXPECTANCY*controldata[4]*2)));
  				if (theplants[x][y].age>=(int)((PLANTS_LIFE_EXPECTANCY*(controldata[4]*2)))) { theplants[x][y].age=0; theplants[x][y].energy=0;  } // plant dies
  				if (theplants[x][y].age>0 && theplants[x][y].age<(int)((PLANTS_LIFE_EXPECTANCY*(controldata[4]*2))) && theplants[x][y].energy<=0) { theplants[x][y].age=0; theplants[x][y].energy=0; } // plant dies
  				if (theplants[x][y].age>0 && theplants[x][y].age<(int)((PLANTS_LIFE_EXPECTANCY*(controldata[4]*2)))) { theplants[x][y].age++; theplants[x][y].energy=theplants[x][y].energy+(int)(PLANTS_ENERGY_BASE_PER_CYCLE*(controldata[4]*2)); } // plant grows
  				if (theplants[x][y].age==0 && plants_neighbours==0) { // no neighbours plant born
  					//srand(time(NULL));
  					random_number = random() % (int)(PLANTS_RANDOM_BORN_CHANCES*(controldata[4]*2));
  					if (random_number==1) { theplants[x][y].age=1; theplants[x][y].energy=1;}
  				}
  				if (theplants[x][y].age==0 && plants_neighbours>0) {  // neighbours plant born
  					//srand(time(NULL));
  					random_number = random() % (int)(PLANTS_RANDOM_NEARBORN_CHANCES*(controldata[4]*2));
  					if (random_number==1) { theplants[x][y].age=1; theplants[x][y].energy=1; }
  				}

  				// Specie1 logic
  				if (specie1[x][y].age>0) { // if there are an individual alive
  					// try to eat
  					if (theplants[x][y].energy>0) {
  						total_energy=0;
  						if (theplants[x][y].energy>SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE) { total_energy=SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE; theplants[x][y].energy=theplants[x][y].energy-SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE; }
  					else { total_energy=theplants[x][y].energy; theplants[x][y].energy=0;}
  					specie1[x][y].energy=specie1[x][y].energy+total_energy;
  					}
  					// grow and decrease energy
  					specie1[x][y].age++;
  					specie1[x][y].energy=specie1[x][y].energy-(int)(SPECIE1_ENERGY_NEEDED_PER_CYCLE/(controldata[0]*2));
  					if (specie1[x][y].energy<0) { specie1[x][y].energy=0; specie1[x][y].age=0;} // die
  					// try to replicate
  					if (specie1[x][y].energy>(int)(SPECIE1_ENERGY_TO_REPLICATE/(controldata[0]*2))) {
  						for (i=0;i<8;i++) { available[i]=0; }
  						pos=0;
  						//srand(time(NULL));
  						random_number = random() % (int)(SPECIE1_NEARBORN_CHANCES/(controldata[0]/2));
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
  								case 1: if (random_number==1) { specie1[xm][y].age=1; specie1[xm][y].energy=(int)(SPECIE1_ENERGY_BASE*(controldata[1]*2)); } break;
  								case 2: if (random_number==1) { specie1[xp][y].age=1; specie1[xp][y].energy=(int)(SPECIE1_ENERGY_BASE*(controldata[1]*2)); } break;
  								case 3: if (random_number==1) { specie1[xm][ym].age=1; specie1[xm][ym].energy=(int)(SPECIE1_ENERGY_BASE*(controldata[1]*2)); } break;
  								case 4: if (random_number==1) { specie1[x][ym].age=1; specie1[x][ym].energy=(int)(SPECIE1_ENERGY_BASE*(controldata[1]*2)); } break;
  								case 5: if (random_number==1) { specie1[xp][ym].age=1; specie1[xp][ym].energy=(int)(SPECIE1_ENERGY_BASE*(controldata[1]*2)); } break;
  								case 6: if (random_number==1) { specie1[xm][yp].age=1; specie1[xm][yp].energy=(int)(SPECIE1_ENERGY_BASE*(controldata[1]*2)); } break;
  								case 7: if (random_number==1) { specie1[x][yp].age=1; specie1[x][yp].energy=(int)(SPECIE1_ENERGY_BASE*(controldata[1]*2)); } break;
  								case 8: if (random_number==1) { specie1[xp][yp].age=1; specie1[xp][yp].energy=(int)(SPECIE1_ENERGY_BASE*(controldata[1]*2)); } break;
  								default: printf("ERROR\n"); break; // all full
  							}
  						}
  					}
  					// die if too old
  					if (specie1[x][y].age>(int)((SPECIE1_LIFE_EXPECTANCY)*controldata[1]*2)) { specie1[x][y].energy=0; specie1[x][y].age=0;}
  				}
  				if (specie1[x][y].age==0) { // if theres no individual, new individual will born? (to avoid extintion)
  					if (specie1_neighbours==0) {
  						//srand(time(NULL));
  						random_number = random() % (int)(SPECIE1_RANDOM_BORN_CHANCES/(controldata[0]*2));
  						if (random_number==1) { specie1[x][y].age=1; specie1[x][y].energy=(int)(SPECIE1_ENERGY_BASE*(controldata[1]*2)); }
  					}
  				}

  				// Specie2 logic

  				if (specie2[x][y].age>0) { // if there are an individual alive
  					// try to eat
  					if (theplants[x][y].energy>0) {
  						total_energy=0;
  						if (theplants[x][y].energy>SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE) { total_energy=SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE; theplants[x][y].energy=theplants[x][y].energy-SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE; }
  						else { total_energy=theplants[x][y].energy; theplants[x][y].energy=0;}
  						specie2[x][y].energy=specie2[x][y].energy+total_energy;
  					}
  					// grow and decrease energy
  					specie2[x][y].age++;
  					specie2[x][y].energy=specie2[x][y].energy-(int)(SPECIE2_ENERGY_NEEDED_PER_CYCLE/(controldata[2]*2));
  					if (specie2[x][y].energy<0) { specie2[x][y].energy=0; specie2[x][y].age=0;} // die
  					// try to replicate
  					if (specie2[x][y].energy>(int)(SPECIE2_ENERGY_TO_REPLICATE/(controldata[2]*2))) {
  						for (i=0;i<8;i++) { available[i]=0; }
  						pos=0;
  						//srand(time(NULL));
  						random_number = random() % (int)(SPECIE2_NEARBORN_CHANCES/(controldata[2]/2));
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
  								case 1: if (random_number==1) { specie2[xm][y].age=1; specie2[xm][y].energy=(int)(SPECIE2_ENERGY_BASE*(controldata[3]*2)); } break;
  								case 2: if (random_number==1) { specie2[xp][y].age=1; specie2[xp][y].energy=(int)(SPECIE2_ENERGY_BASE*(controldata[3]*2)); } break;
  								case 3: if (random_number==1) { specie2[xm][ym].age=1; specie2[xm][ym].energy=(int)(SPECIE2_ENERGY_BASE*(controldata[3]*2)); }break;
  								case 4: if (random_number==1) { specie2[x][ym].age=1; specie2[x][ym].energy=(int)(SPECIE2_ENERGY_BASE*(controldata[3]*2)); } break;
  								case 5: if (random_number==1) { specie2[xp][ym].age=1; specie2[xp][ym].energy=(int)(SPECIE2_ENERGY_BASE*(controldata[3]*2)); } break;
  								case 6: if (random_number==1) { specie2[xm][yp].age=1; specie2[xm][yp].energy=(int)(SPECIE2_ENERGY_BASE*(controldata[3]*2)); } break;
  								case 7: if (random_number==1) { specie2[x][yp].age=1; specie2[x][yp].energy=(int)(SPECIE2_ENERGY_BASE*(controldata[3]*2)); } break;
  								case 8: if (random_number==1) { specie2[xp][yp].age=1; specie2[xp][yp].energy=(int)(SPECIE2_ENERGY_BASE*(controldata[3]*2)); } break;
  								// default: break; // all full
  							}
  						}
  					}
  				// die if too old
  				if (specie2[x][y].age>(int)((SPECIE2_LIFE_EXPECTANCY)*controldata[3]*2)) { specie2[x][y].energy=0; specie2[x][y].age=0;}
  				}
  				if (specie2[x][y].age==0) { // if theres no individual, new individual will born? (to avoid extintion)
  					if (specie2_neighbours==0) {
  						//srand(time(NULL));
  						random_number = random() % (int)(SPECIE2_RANDOM_BORN_CHANCES/(controldata[2]*2));
  						if (random_number==1) { specie2[x][y].age=1; specie2[x][y].energy=(int)(SPECIE2_ENERGY_BASE*(controldata[3]*2)); }
  					}
  				}

  				// draw
  				if (specie1[x][y].age>0 && specie2[x][y].age>0) { canvas()->SetPixel(x, y, 255, 0, 255); } // species comp
  				if (specie1[x][y].age>0 && specie2[x][y].age==0) { canvas()->SetPixel(x, y, 255, 255, 0);} // only specie1
  				if (specie1[x][y].age==0 && specie2[x][y].age>0) { canvas()->SetPixel(x, y, 0, 255, 255); } // only specie2
  				if (specie1[x][y].age==0 && specie2[x][y].age==0 && theplants[x][y].age>0) { canvas()->SetPixel(x, y, 255, 255, 255); } // only plants
  				if (specie1[x][y].age==0 && specie2[x][y].age==0 && theplants[x][y].age==0) {   canvas()->SetPixel(x, y, 0, 0, 0); } // black nothing
  			}
  		}

  		swapBuffers();
  		usleep(TIME_TO_DRAW);

      // END
    }
  }

private:

  int width_;
  int height_;

  const int PLANTS_LIFE_EXPECTANCY = 100;
  const int PLANTS_RANDOM_BORN_CHANCES = 1000;
  const int PLANTS_NEARBORN_CHANCES = 100;
  const int PLANTS_RANDOM_DIE_CHANCES = 2;
  const int PLANTS_ENERGY_BASE_PER_CYCLE = 5;

  const int SPECIE1_LIFE_EXPECTANCY = 200;
  const int SPECIE1_RANDOM_BORN_CHANCES = 5000;
  const int SPECIE1_NEARBORN_CHANCES = 50;
  const int SPECIE1_RANDOM_DIE_CHANCES = 2;
  const int SPECIE1_ENERGY_BASE = 20;
  const int SPECIE1_ENERGY_NEEDED_PER_CYCLE = 2;
  const int SPECIE1_MAX_ENERGY_RECOLECTED_PER_CYCLE = 20;
  const int SPECIE1_ENERGY_TO_REPLICATE = 5;

  const int SPECIE2_LIFE_EXPECTANCY = 170;
  const int SPECIE2_RANDOM_BORN_CHANCES = 4000;
  const int SPECIE2_NEARBORN_CHANCES = 40;
  const int SPECIE2_RANDOM_DIE_CHANCES = 2;
  const int SPECIE2_ENERGY_BASE = 20;
  const int SPECIE2_ENERGY_NEEDED_PER_CYCLE = 2;
  const int SPECIE2_MAX_ENERGY_RECOLECTED_PER_CYCLE = 20;
  const int SPECIE2_ENERGY_TO_REPLICATE = 6;

  const int TIME_TO_DRAW = 5000;

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
