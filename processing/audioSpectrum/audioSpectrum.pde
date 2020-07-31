import processing.sound.*;

FFT fft;
AudioIn in;
int bands = 512;
float sum;
int fade = 100;
float[] spectrum = new float[bands];

void setup() {
  fullScreen(P3D);
  colorMode(HSB);
    
  // Create an Input stream which is routed into the Amplitude analyzer
  fft = new FFT(this, bands);
  in = new AudioIn(this, 0);
  
  // start the Audio Input
  in.start();
  
  // patch the AudioIn
  fft.input(in);
}      

void draw() { 
  background(0);
  fft.analyze(spectrum);

  for(int x = 0; x < 5; x++){
    sum = 0;
    for(int i = 0; i < 20; i ++) {
      sum = sum + spectrum[(x*20)+i];
    }
    strokeWeight(5);
    stroke(100);
    fill(fade+map(sum,0,1,0,200),map(x,0,4,100,255),map(noise(x),0,1,00,255));
    fade += 1;
    if (fade == 255) fade = 100;
    ellipse(360+(x*180*2),height/2,sum*600,sum*600);
  } 
}
