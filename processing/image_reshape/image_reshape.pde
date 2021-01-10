
int x = 640;
int y = 360;
int threshold=500;

PImage img;
PImage originalImg;
color[] reshape = new color[x*y]; 

void setup() {
  size(640, 360);
  // The image file must be in the data folder of the current sketch 
  // to load successfully
  img = loadImage("moonwalk.jpg");  // Load the image into the program
  img.loadPixels();
  originalImg = img.get();
}

void draw() {
  
  if (keyPressed) {
    if (key == 'q' || key == 'Q') {
      threshold=threshold+100;
    }
    if (key == 'a' || key == 'A') {
      threshold=threshold-100;
    }
    if (key == CODED) {
      if (keyCode == UP) {
        threshold++;
      }
      if (keyCode == DOWN) {
        threshold--;
      }
    }
  }
  transformation();      
  image(img, 0, 0);
}


void transformation() {
  //println(threshold);
  for (int i=0; i<x*y; i++) {
    float difference = 0.0;
    if (i-1>=0) {
      difference = difference + abs(red(originalImg.pixels[i])-red(originalImg.pixels[i-1]))+
        abs(green(originalImg.pixels[i])-green(originalImg.pixels[i-1]))+
        abs(blue(originalImg.pixels[i])-blue(originalImg.pixels[i-1]));
    }
    if (i-x-1>=0) {
      difference = difference + abs(red(originalImg.pixels[i])-red(originalImg.pixels[i-1-x]))+
        abs(green(originalImg.pixels[i])-green(originalImg.pixels[i-1-x]))+
        abs(blue(originalImg.pixels[i])-blue(originalImg.pixels[i-1-x]));
    }
    if (i-x+1>=0) {
      difference = difference + abs(red(originalImg.pixels[i])-red(originalImg.pixels[i+1-x]))+
        abs(green(originalImg.pixels[i])-green(originalImg.pixels[i+1-x]))+
        abs(blue(originalImg.pixels[i])-blue(originalImg.pixels[i+1-x]));
    }
    if (i-x>=0) {
      difference = difference + abs(red(originalImg.pixels[i])-red(originalImg.pixels[i-1]))+
        abs(green(originalImg.pixels[i])-green(originalImg.pixels[i-1]))+
        abs(blue(originalImg.pixels[i])-blue(originalImg.pixels[i-1]));
    }
    if (i+1<x*y) {
      difference = difference + abs(red(originalImg.pixels[i])-red(originalImg.pixels[i+1]))+
        abs(green(originalImg.pixels[i])-green(originalImg.pixels[i+1]))+
        abs(blue(originalImg.pixels[i])-blue(originalImg.pixels[i+1]));
    }
    if (i+1+x<x*y) {
      difference = difference + abs(red(originalImg.pixels[i])-red(originalImg.pixels[i+1+x]))+
        abs(green(originalImg.pixels[i])-green(originalImg.pixels[i+1+x]))+
        abs(blue(originalImg.pixels[i])-blue(originalImg.pixels[i+1+x]));
    }
    if (i-1+x<x*y) {
      difference = difference + abs(red(originalImg.pixels[i])-red(originalImg.pixels[i-1+x]))+
        abs(green(originalImg.pixels[i])-green(originalImg.pixels[i-1+x]))+
        abs(blue(originalImg.pixels[i])-blue(originalImg.pixels[i-1+x]));
    }
    if (i+x<x*y) {
      difference = difference + abs(red(originalImg.pixels[i])-red(originalImg.pixels[i+x]))+
        abs(green(originalImg.pixels[i])-green(originalImg.pixels[i+x]))+
        abs(blue(originalImg.pixels[i])-blue(originalImg.pixels[i+x]));
    }
    // differece range (0-6144) 0 > same color around 6144 > different color around
    float greyRemap = map(difference,0,6144-threshold,0,255);
    //if (difference > threshold) {
    //  reshape[i]=color(255);
    //}
    reshape[i]=color(greyRemap);
    //reshape[i]= color(red(img.pixels[i])/2, green(img.pixels[i])/2, blue(img.pixels[i])/2);   
    //println(red(img.pixels[i])+","+green(img.pixels[i])+","+blue(img.pixels[i]));
  }
  for (int i=0; i<x*y; i++) {
    img.pixels[i]= reshape[i];
  }
 img.updatePixels();
}
