/**
 * Additive Wave
 * by Daniel Shiffman. 
 * 
 * Create a more complex wave by adding two waves together. 
 */
 
int xspacing = 1;   // How far apart should each horizontal location be spaced
int w;              // Width of entire wave
int maxwaves = 10;   // total # of waves to add together

int angle = 0;
int count = 0;
float sv = 1.0;
int svdir = 1;
int wait = 0;
float theta = 0.0;
float[] amplitude = new float[maxwaves];   // Height of wave
float[] dx = new float[maxwaves];          // Value for incrementing X, to be calculated as a function of period and xspacing
float[] yvalues;                           // Using an array to store height values for the wave (not entirely necessary)

void setup() {
  size(640, 360);
  //fullScreen();
  frameRate(30);
  colorMode(HSB, 255, 255, 255, 100);
  w = width + 6;

  for (int i = 0; i < maxwaves; i++) {
    amplitude[i] = random(10,20);
    float period = random(100,1800); // How many pixels before the wave repeats
    dx[i] = (TWO_PI / period) * xspacing;
  }

  yvalues = new float[w/xspacing];
}

void draw() {
  
   /*if (count == 10) {
    if (angle==360) { angle = 0; }
    rotate(1);
    translate(0,-width);
    angle++;
    count = 0;
  }
  count++;*/
  background(0);
  calcWave();
  renderWave();
}

void calcWave() {
  // Increment theta (try different values for 'angular velocity' here
  theta += 0.01;

  // Set all height values to zero
  for (int i = 0; i < yvalues.length; i++) {
    yvalues[i] = 0;
  }
 
  // Accumulate wave height values
  for (int j = 0; j < maxwaves; j++) {
    float x = theta;
    for (int i = 0; i < yvalues.length; i++) {
      // Every other wave is cosine instead of sine
      if (j % 2 == 0)  yvalues[i] += sin(x)*amplitude[j];
      else yvalues[i] += cos(x)*amplitude[j];
      x+=dx[j];
    }
  }
}

void renderWave() {
  // A simple way to draw the wave with an ellipse at each location
  noStroke();
  fill(255,50);
  ellipseMode(CENTER);
  for (int x = 0; x < yvalues.length; x++) {
    for (int lines = 0; lines < 25; lines ++) {
      fill(0+lines*15,0+lines*15,255-lines*15);
      scale(1);
      ellipse(x*xspacing,height+yvalues[x]-(lines*40),0.5,40);
    }
  }
  if (sv < 1.001) {
    wait++;
    sv=1.001;
    //println("zero");
  }
  if (wait > 10) { wait=0; }
  if (svdir == 1 && wait==0) { sv=sv+0.00001; } else { sv=sv-0.00001; }
  if (sv>1.001 || sv<1) {
    //println("Cambi direccio");
    svdir = -svdir; 
}
}
