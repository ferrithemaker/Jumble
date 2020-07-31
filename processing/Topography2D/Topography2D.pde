/**
 * Countour line example
 * for https://discourse.processing.org/t/topographical-map/13302/4
 * Press any key to toggle between viewing countour lines or hights (the lighter the higher)
 */
final static int W = 800;  // width of the hight map
final static int H = 600;  // height of the hight map
final static float k = 0.004;  //noise coefficient. play with it to get more or less «rough» land

final static int l = 50;  //show hight differense with this many contour lines

final static color c0 = #000000;  //color to draw background
final static color c1 = #008888;  //color to draw isolines

float[][] m;  // the hight map

boolean showHeightOrCountour = false;

void setup() {
  size(800, 600);
  m = new float[W][H];
  for (int j=0; j<H; j++) {
    for (int i=0; i<W; i++) {    
      m[i][j] = noise((i)*k,(j)*k);
    }
  }
}

void draw() {
  loadPixels();
  for (int j=0; j<H; j++) {
    for (int i=0; i<W; i++) {
      if (!showHeightOrCountour) {
        pixels[W*j+i] = color(round(m[i][j]*l)*(255/l));  //show hight with l resolution
      } else {
        if (i>0 && i<W-1 && j>0 && j<H-1) {
          int h0 = round(m[i][j]*l);    //get and adjust height at this point
          int hw = round(m[i-1][j]*l);  //get west neighbour's height
          int hn = round(m[i][j-1]*l);  //get nothern neighbour's height
          if (h0!=hw || h0!=hn) {  //if any neighbour's height on a different «step» of hight… 
            //pixels[W*j+i] = c1;    //…draw contour
            pixels[W*j+i] = color(m[i][j]*l, m[i][j]*l*20, m[i][j]*l*10); //…draw contour

          } else {
            pixels[W*j+i] = c0;    //…otherwise draw background
          }
        } else {
          pixels[W*j+i] = c0;
        }
      }
    }
  }
  updatePixels();
  surface.setTitle("Drawing contour lines @ "+round(frameRate));
}

void keyPressed() {
  showHeightOrCountour = !showHeightOrCountour;
}

void mousePressed() {
  println(m[mouseX][mouseY]);
}
