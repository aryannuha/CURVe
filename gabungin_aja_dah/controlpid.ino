void PID_control() {
  // ReadErrorYPR(); // Read the current yaw error
  // Use the corrected yaw error
  error = ErrorYawCal;
  P = error;
  I = I + error;
  D = error - lastError;

  lastError = error;
  float thrustCorrection = P * Kp + I * Ki + D * Kd; // Calculate the correction

  int thrustLeft = neutralThrust + thrustCorrection;
  int thrustRight = neutralThrust - thrustCorrection;

  if (thrustLeft > maxThrust) {
    thrustLeft = maxThrust;
  }
  if (thrustRight > maxThrust) {
    thrustRight = maxThrust;
  }

  if (thrustLeft < minThrust) {
    thrustLeft = minThrust;
  }
  if (thrustRight < minThrust) {
    thrustRight = minThrust;
  }

  // Serial.print("correction: ");
  // Serial.print(thrustCorrection);
  // Serial.print("   error: ");
  // Serial.print(error);
  // Serial.print("   left: ");
  // Serial.print(thrustLeft);
  // Serial.print("   right: ");
  // Serial.println(thrustRight);

  ESC5.writeMicroseconds(thrustRight); // Apply the thrust correction
  ESC6.writeMicroseconds(thrustLeft);
}