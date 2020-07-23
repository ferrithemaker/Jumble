// based on https://www.youtube.com/watch?v=IKB1hWWedMk

int scl = 20;
int w = 2000;
int h = 2000;
int cols,rows;

float flying = 0;
float rotate = 0;

float[][] terrain;
float[][] colorofvertex;

void generateTerrain(float distance) {
float yoff = 0 + distance;
  for (int y = 0; y < rows; y++) {
    float xoff = 0;
    for (int x = 0; x < cols-1; x++) {
      terrain[x][y] = map(noise(xoff,yoff),0,1,-100,10);
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
 
 generateTerrain(0.0);
    
}

void draw() {
  
  //flying = flying - 0.2;
  generateTerrain(flying);
  background(0);
  stroke(255);
  noFill();
  translate(width/2,height/2);
  rotateX(PI/2.2);
  rotateZ(PI+rotate);
  translate(-w/2,-h/2);
  for (int y = 0; y < rows-1; y++) {
    beginShape(TRIANGLE_STRIP);
    for (int x = 0; x < cols-1; x++) {
      stroke(100);
      fill(int(colorofvertex[x][y]));
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

  
