PImage bg;

int scl = 20;
int w = 3000;
int h = 2000;
int cols,rows;

float flying = 0;
float wave = 0;
float rotate = 0;

float[][] terrain;
float[][] colorofvertex;

void generateTerrain(float distance,float wave) {
float yoff = 0 + distance;
  for (int y = 0; y < rows; y++) {
    float xoff = 0;
    for (int x = 0; x < cols-1; x++) {
      terrain[x][y] = map(noise(xoff,yoff),0,1,-80,10)+map(noise(xoff+wave+sin(xoff),yoff+wave+cos(yoff)),0,1,-10,10)*2;
      colorofvertex[x][y] = map(noise(xoff,yoff),0,1,0,80)+map(noise(xoff+wave+sin(xoff),yoff+wave+cos(yoff)),0,1,-0,170)*2;
      xoff = xoff + 0.2;
    }
    yoff = yoff + 0.2;
  }
}

void setup() {
 bg = loadImage("/home/ferran/c.jpg");
 //size (1920,1080,P3D);
 fullScreen(P3D);
 cols = w / scl;
 rows = h / scl;
 terrain = new float[cols][rows];
 colorofvertex = new float[cols][rows];
 
 generateTerrain(0.0,0.0);
    
}

void draw() {
  background(bg);
  wave = wave + 0.02;
  generateTerrain(flying,wave);
  stroke(255);
  noFill();
  translate(width/2,height/2);
  rotateX(PI/2.2);
  rotateZ(PI+rotate);
  translate(-w/2,-h/2);
  for (int y = 0; y < rows-1; y++) {
    beginShape(TRIANGLE_STRIP);
    for (int x = 0; x < cols-1; x++) {
      stroke(0,0,colorofvertex[x][y]-50);
      fill(0,0,colorofvertex[x][y]);
      vertex(x*scl,y*scl,terrain[x][y]);
      vertex(x*scl,(y+1)*scl,terrain[x][y+1]);
    }
    endShape();
  }
}

  
