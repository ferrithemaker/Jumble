class Blob {
  PVector pos;
  float r;
  PVector vel;
  
  Blob(float x, float y) {
    pos = new PVector(x,y);
    vel = PVector.random2D();
    vel.mult(random(2,5));
    r = 40;
  }
  
  void update() {
    pos.add(vel);
    
    if (pos.x > width || pos.x < 0) {
      vel.x *= -1;
    }
    
    if (pos.y > height || pos.y < 0) {
      vel.y *= -1;
    }
  }
  
  
  void show() { // show the blob itself, only to check the positions of the blobs
    noFill();
    stroke(0);
    strokeWeight(4);
    ellipse(pos.x,pos.y,r*2,r*2);
  }
}
