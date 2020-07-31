// based on https://www.youtube.com/watch?v=IKB1hWWedMk
import processing.sound.*;

int scl = 20;
int w = 2000;
int h = 2000;
int cols,rows;

float flying = 0;
float rotate = 0;

float[][] terrain;
float[][] colorofvertex;

FFT fft;
AudioIn in;
int bands = 512;
int indexbands = 0;
float[] spectrum = new float[bands];
  


void generateTerrain(float distance) {
float yoff = 0 + distance;
fft.analyze(spectrum);
  for (int y = 0; y < rows; y++) {
    float xoff = 0;
    indexbands = 0;
    for (int x = 0; x < cols-1; x++) {
      terrain[x][y] = spectrum[indexbands]*1000;
      indexbands = indexbands * 5;
      colorofvertex[x][y] = map(noise(xoff,yoff),0,1,0,200);
      xoff = xoff + 0.2;
    }
    yoff = yoff + 0.2;
  }
  
}

void setup() {
 size (1000,1000,P3D);
 cols = w / scl;
 rows = h / scl;
 terrain = new float[cols][rows];
 colorofvertex = new float[cols][rows];
 // Create an Input stream which is routed into the Amplitude analyzer
  fft = new FFT(this, bands);
  in = new AudioIn(this, 0);
  
  // start the Audio Input
  in.start();
  
  // patch the AudioIn
  fft.input(in); 
 generateTerrain(0.0);
    
}

void draw() {
  
  //flying = flying - 0.2;
  generateTerrain(flying);
  background(0);
  stroke(255);
  noFill();
  translate(width/2,height/2);
  rotateX(PI/4);
  rotateZ(PI+rotate);
  translate(-w/2,-h/2);
  for (int y = 0; y < rows-1; y++) {
    beginShape(TRIANGLE_STRIP);
    for (int x = 0; x < cols-1; x++) {
      //stroke(100);
      //fill(int(colorofvertex[x][y]));
      vertex(x*scl,y*scl,terrain[x][y]);
      vertex(x*scl,(y+1)*scl,terrain[x][y+1]);
    }
    endShape();
  }
  if (keyPressed == true) {
    if (key=='w') flying = flying + 0.12;
    if (key=='s') flying = flying - 0.12;
    if (key=='a') rotate = rotate + 0.2;
    if (key=='d') rotate = rotate - 0.2;
  }
}
