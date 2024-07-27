//Address of the CMPS12 compass on i2C
#define _i2cAddress 0x60

#define CONTROL_Register 0

#define BEARING_Register 2
#define PITCH_Register 4
#define ROLL_Register 5

#define MAGNET_X_Register 6
#define MAGNET_Y_Register 8
#define MAGNET_Z_Register 10

#define ACCELERO_X_Register 12
#define ACCELERO_Y_Register 14
#define ACCELERO_Z_Register 16

#define _Register_GYRO_X 18
#define _Register_GYRO_Y 20
#define _Register_GYRO_Z 22

#define ONE_BYTE 1
#define TWO_BYTES 2
//---------------------------------

int16_t getBearing() {
  // Begin communication with CMPS12
  Wire.beginTransmission(_i2cAddress);

  // Tell register you want some data
  Wire.write(BEARING_Register);

  // End the transmission
  int nackCatcher = Wire.endTransmission();

  // Return if we have a connection problem
  if (nackCatcher != 0) { return 0; }

  // Request 2 bytes from CMPS12
  int nReceived = Wire.requestFrom(_i2cAddress, TWO_BYTES);

  // Something has gone wrong
  if (nReceived != TWO_BYTES) return 0;

  // Read the values
  byte _byteHigh = Wire.read();
  byte _byteLow = Wire.read();

  // Calculate full bearing
  int _bearing = ((_byteHigh << 8) + _byteLow) / 10;

  return _bearing;
}

byte getPitch() {
  // Begin communication with CMPS12
  Wire.beginTransmission(_i2cAddress);

  // Tell register you want some data
  Wire.write(PITCH_Register);

  // End the transmission
  int nackCatcher = Wire.endTransmission();

  // Return if we have a connection problem
  if (nackCatcher != 0) { return 0; }

  // Request 1 byte from CMPS12
  int nReceived = Wire.requestFrom(_i2cAddress, ONE_BYTE);

  // Something has gone wrong
  if (nReceived != ONE_BYTE) return 0;

  // Read the values
  char _pitch = Wire.read();

  return _pitch;
}

byte getRoll() {
  // Begin communication with CMPS12
  Wire.beginTransmission(_i2cAddress);

  // Tell register you want some data
  Wire.write(ROLL_Register);

  // End the transmission
  int nackCatcher = Wire.endTransmission();

  // Return if we have a connection problem
  if (nackCatcher != 0) { return 0; }

  // Request 1 byte from CMPS12
  int nReceived = Wire.requestFrom(_i2cAddress, ONE_BYTE);

  // Something has gone wrong
  if (nReceived != ONE_BYTE) return 0;

  // Read the values
  char _roll = Wire.read();

  return _roll;
}