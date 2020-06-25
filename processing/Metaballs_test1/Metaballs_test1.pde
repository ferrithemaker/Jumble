Blob[] blobs = new Blob[10];

Boolean is_color = false;

void setup() {
  size(800, 600);
  colorMode(HSB);
  for (int i = 0; i < blobs.length; i++) {
    blobs[i] = new Blob(random(width), random(height));
  }
}

void draw() {
  //background(51);
  loadPixels();
  for (int x = 0; x < width; x++) {
    for (int y = 0; y < height; y++) {
      int index = x + y * width;
      float sum = 0;
      for (Blob b : blobs) {
        float d = dist(x, y, b.pos.x, b.pos.y);
        sum += 100 * b.r / d;
      }
      if (is_color) {
        pixels[index] = color(sum, 255, 255);
      }
      else {
        pixels[index] = color(sum);
      }
    }
  }

  updatePixels();

  for (Blob b: blobs) {
    b.update();
  }
}
