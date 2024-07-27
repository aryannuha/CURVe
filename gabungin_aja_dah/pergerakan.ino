void maju(){
  PID_control();
}

void maju_biasa(){
  ESC5.writeMicroseconds(1700);
  ESC6.writeMicroseconds(1700);
}

void turun(){
  ControlPitch();
}

void naik(){
  ESC1.writeMicroseconds(1100);
  ESC2.writeMicroseconds(1100);
  ESC3.writeMicroseconds(1100);
  ESC4.writeMicroseconds(1100);
}

void stop(){
  buka();
  ESC1.writeMicroseconds(1100);
  ESC2.writeMicroseconds(1100);
  ESC3.writeMicroseconds(1100);
  ESC4.writeMicroseconds(1100);
  ESC5.writeMicroseconds(1460);
  ESC6.writeMicroseconds(1460);
}

void kanan(){
  ESC5.writeMicroseconds(1750);
  ESC6.writeMicroseconds(1900);
}

void kiri(){
  ESC5.writeMicroseconds(1900);
  ESC6.writeMicroseconds(1750);
}

void kanan_ultra(){
  ESC5.writeMicroseconds(1600);
  ESC6.writeMicroseconds(1900);
}

void kiri_ultra(){
  ESC5.writeMicroseconds(1900);
  ESC6.writeMicroseconds(1600);
}

void buka(){
  GRIPPER.write(0);
}

void atas_stop(){
  ESC5.writeMicroseconds(1460);
  ESC6.writeMicroseconds(1460);
}