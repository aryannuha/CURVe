void readSensor1() {
  SoftwareSerial mySerial1(53,51); // Fils blanc Ã  gauche (sur connecteur 8)
  mySerial1.begin(115200);
  mySerial1.write(COM1);
  delay(50);
  if (mySerial1.available() > 0) {
    delay(10);
    if (mySerial1.read() == 0xff) {
      buffer_RTT[0] = 0xff;
      for (int i = 1; i < 4; i++) {
        buffer_RTT[i] = mySerial1.read();
      }
      CS = buffer_RTT[0] + buffer_RTT[1] + buffer_RTT[2];
      if (buffer_RTT[3] == CS) {
        distance1 = (buffer_RTT[1] << 8) + buffer_RTT[2];
      }
    }
  }
}

void readSensor2() {
  SoftwareSerial mySerial2(A10,A11); // fils blanc sur 10
  mySerial2.begin(115200);
  mySerial2.write(COM2);
  delay(50);
  if (mySerial2.available() > 0) {
    delay(10);
    if (mySerial2.read() == 0xff) {
      buffer_RTT[0] = 0xff;
      for (int i = 1; i < 4; i++) {
        buffer_RTT[i] = mySerial2.read();
      }
      CS = buffer_RTT[0] + buffer_RTT[1] + buffer_RTT[2];
      if (buffer_RTT[3] == CS) {
        distance2 = (buffer_RTT[1] << 8) + buffer_RTT[2];
      }
    }
  }
}