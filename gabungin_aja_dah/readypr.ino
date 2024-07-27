void ReadErrorYPR() {
  
  if (!testonce2) {
    YawA = getBearing();
    PitchA = getPitch();
    RollA = getRoll();
    Yaw = getBearing() - 180;
    Pitch = getPitch() - 128;
    Roll = getRoll() - 128;
    testonce2 = 1;
  }
  // Bearing Max 360
  // Pitch Max 255
  // Roll Max 255

  ErrorYaw = YawA - getBearing();
  ErrorPitch = PitchA - getPitch();
  ErrorRoll = RollA - getRoll();

  // Yaw

  // Kalibrasi Yaw
  if (YawA < 180) {
    if ((ErrorYaw < -180) && (getBearing() != YawA)) {
      ErrorYawCal = ErrorYaw + 360;
    } else {
      ErrorYawCal = ErrorYaw;
    }
  } else if (YawA > 180) {
    if ((ErrorYaw > 180) && (getBearing() != YawA)) {
      ErrorYawCal = ErrorYaw - 360;
    } else {
      ErrorYawCal = ErrorYaw;
    }
  } else {
    ErrorYawCal = ErrorYaw;
  }

  // Pitch

  // Pitch
  if (PitchA < 128) {
    if ((ErrorPitch < -128) && (getPitch() != PitchA)) {
      ErrorPitchCal = ErrorPitch + 256;
    } else {
      ErrorPitchCal = ErrorPitch;
    }
  } else if (PitchA > 128) {
    if ((ErrorPitch > 128) && (getPitch() != PitchA)) {
      ErrorPitchCal = ErrorPitch - 256;
    } else {
      ErrorPitchCal = ErrorPitch;
    }
  } else {
    ErrorPitchCal = ErrorPitch;
  }

  // Roll

  // Roll
  if (RollA < 128) {
      if ((ErrorRoll < -128) && (getRoll() != RollA)) {
        ErrorRollCal = ErrorRoll + 255;
      } else {
        ErrorRollCal = ErrorRoll;
      }
    } else if (RollA > 128) {
      if ((ErrorRoll > 128) && (getRoll() != RollA)) {
        ErrorRollCal = ErrorRoll - 255;
      } else {
        ErrorRollCal = ErrorRoll;
      }
    } else {
      ErrorRollCal = ErrorRoll;
    }
}