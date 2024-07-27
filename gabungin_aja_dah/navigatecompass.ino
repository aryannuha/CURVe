void MajuControlYaw() {
  // Mengatur kecepatan motor kanan berdasarkan error yaw
  ErrorKanan = ErrorYawCal;
  if (ErrorYawCal < -90) ErrorKanan = -90;
  if (ErrorYawCal > 0) ErrorKanan = 0;
  pwmSignal2 = map(ErrorKanan, -90, 0, 1585, 1485); // Menggunakan map untuk mendapatkan nilai pwm yang sesuai
  
  // Mengatur kecepatan motor kiri berdasarkan error yaw
  ErrorKiri = ErrorYawCal;
  if (ErrorYawCal > 90) ErrorKiri = 90;
  if (ErrorYawCal < 0) ErrorKiri = 0;
  pwmSignal3 = map(ErrorKiri, 0, 90, 1490, 1590); // Menggunakan map untuk mendapatkan nilai pwm yang sesuai
  
  // Mengirim sinyal ke ESC motor kanan dan kiri
  ESC5.writeMicroseconds(pwmSignal2);
  ESC6.writeMicroseconds(pwmSignal3);

  // Serial.print("kiri: ");
  // Serial.print(ErrorKiri);
  // Serial.print("   kanan: ");
  // Serial.print(ErrorKanan);
  // Serial.print("   pwm2: ");
  // Serial.print(pwmSignal2);
  // Serial.print("   pwm3: ");
  // Serial.println(pwmSignal3);
}

void ControlPitch() {
  // Mengatur kecepatan motor depan berdasarkan error pitch
  ErrorDepan = ErrorPitchCal;
  if (ErrorPitchCal < -64) ErrorDepan = -64;
  if (ErrorPitchCal > 0) ErrorDepan = 0;
  int pwmSignalDepanKanan = map(ErrorDepan, -64, 0, 1630, 1430); // Motor kanan depan
  int pwmSignalDepanKiri = map(ErrorDepan, -64, 0, 1520, 1420);  // Motor kiri depan
  
  // Mengatur kecepatan motor belakang berdasarkan error pitch
  ErrorBelakang = ErrorPitchCal;
  if (ErrorPitchCal > 64) ErrorBelakang = 64;
  if (ErrorPitchCal < 0) ErrorBelakang = 0;
  int pwmSignalBelakangKanan = map(ErrorBelakang, 0, 64, 1430, 1530); // Motor kanan belakang
  int pwmSignalBelakangKiri = map(ErrorBelakang, 0, 64, 1430, 1530);  // Motor kiri belakang
  
  // Mengirim sinyal ke ESC motor depan dan belakang
  ESC1.writeMicroseconds(pwmSignalBelakangKanan);
  ESC2.writeMicroseconds(pwmSignalBelakangKiri);
  ESC3.writeMicroseconds(pwmSignalDepanKanan);
  ESC4.writeMicroseconds(pwmSignalDepanKiri);

  // Serial.print("Depan: ");
  // Serial.print(ErrorDepan);
  // Serial.print("   Belakang: ");
  // Serial.print(ErrorBelakang);
  // Serial.print("   pwmDepanKanan: ");
  // Serial.print(pwmSignalDepanKanan);
  // Serial.print("   pwmDepanKiri: ");
  // Serial.print(pwmSignalDepanKiri);
  // Serial.print("   pwmBelakangKanan: ");
  // Serial.print(pwmSignalBelakangKanan);
  // Serial.print("   pwmBelakangKiri: ");
  // Serial.println(pwmSignalBelakangKiri);
}

void ControlRoll() {
  // Mengatur kecepatan motor kiri berdasarkan error roll
  ErrorSaKiri = ErrorRollCal;
  if (ErrorRollCal < -64) ErrorSaKiri = -64;
  if (ErrorRollCal > 0) ErrorSaKiri = 0;
  int pwmSignalKiriDepan = map(ErrorSaKiri, -64, 0, 1320, 1220);  // Motor kiri depan
  int pwmSignalKiriBelakang = map(ErrorSaKiri, -64, 0, 1330, 1230); // Motor kiri belakang

  // Mengatur kecepatan motor kanan berdasarkan error roll
  ErrorSaKanan = ErrorRollCal;
  if (ErrorRollCal > 64) ErrorSaKanan = 64;
  if (ErrorRollCal < 0) ErrorSaKanan = 0;
  int pwmSignalKananDepan = map(ErrorSaKanan, 0, 64, 1230, 1330);  // Motor kanan depan
  int pwmSignalKananBelakang = map(ErrorSaKanan, 0, 64, 1230, 1330); // Motor kanan belakang

  // Mengirim sinyal ke ESC motor kiri dan kanan
  ESC1.writeMicroseconds(pwmSignalKiriBelakang);
  ESC2.writeMicroseconds(pwmSignalKananBelakang);
  ESC3.writeMicroseconds(pwmSignalKiriDepan);
  ESC4.writeMicroseconds(pwmSignalKananDepan);

  // Serial.print("SampingKa: ");
  // Serial.print(ErrorSaKanan);
  // Serial.print("   SampingKi: ");
  // Serial.print(ErrorSaKiri);
  // Serial.print("   pwmKiriDepan: ");
  // Serial.print(pwmSignalKiriDepan);
  // Serial.print("   pwmKiriBelakang: ");
  // Serial.print(pwmSignalKiriBelakang);
  // Serial.print("   pwmKananDepan: ");
  // Serial.print(pwmSignalKananDepan);
  // Serial.print("   pwmKananBelakang: ");
  // Serial.println(pwmSignalKananBelakang);
}