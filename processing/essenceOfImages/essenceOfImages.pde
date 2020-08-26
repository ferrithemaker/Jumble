PImage theImage;
int h=250;
int w=366;
color[] essence = new color[h*w];
void setup() {
  size(250,366);
  theImage = loadImage("london.jpeg");
  image(theImage, 0, 0);
  loadPixels();
  float colorsum;
  float maxcs = 0.0; 
  for (int ydest = 0; ydest < w; ydest++) {
    for (int xdest = 0; xdest < h; xdest++) {
      colorsum = 0.0;
      for (int y = 0; y < w; y++) {
        for (int x = 0; x < h; x++) {
          color oldcolor = get(x,y);
          if (ydest != y & xdest != x) {
            colorsum =  colorsum + ((red(oldcolor)+green(oldcolor)+blue(oldcolor))*(1/(log(dist(ydest,xdest,y,x))))/(w*h));
          }
          if (colorsum > maxcs) {
            println(x,y,colorsum);
            maxcs = colorsum;
          }
          //delay(1);
        }
      }
      println(ydest,xdest);
     color agcolor = color(map(colorsum,0,100,0,255));
     essence[xdest+(ydest*h)]=agcolor;
    }
  }
  for  (int i=0;i<w*h;i++) {
    //println(i,essence[i]);
    //delay(1);
    pixels[i]=essence[i];
  }
  updatePixels(); 
}

void draw() {
  
}
