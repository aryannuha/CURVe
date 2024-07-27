void mix_detect_start2() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    lastData = data; // Store the received data

    if (data == 'H') { // Receive handshake signal from Raspberry Pi
      Serial.println("ACK"); // Send ACK as a response
    }
    digitalWrite(relay, HIGH);
    if (!start) {
      delay(3000);
      digitalWrite(relay, LOW);
      start = true;
    }

    if (start) {
      if (!state) {
        if ((distance1 < 450) && (distance1 > 10)) {
          naik();
          state = true;
        } else {
          turun();
        }
      }

      if (state) {
        if ((distance1 < 450) && (distance1 > 10)) {
          naik();
        } else {
          turun();
        }

        switch (data) {
          case 'w': maju(); break;
          case 'a': kiri(); break;
          case 's': stop(); break;
          case 'd': kanan(); break;
          case 'p':
            if (!belok_kanan) {
              kanan();
              delay(10000);
              belok_kanan = true;
            }
            if (belok_kanan) {
              maju();
            }
            break;
          case 'o':
            if (!belok_kiri) {
              digitalWrite(relay, HIGH);
              kiri();
              delay(10000);
              belok_kiri = true;
            }
            if (belok_kiri) {
              maju_biasa();
            }
            break;
          case 'b': maju_biasa(); break;
        }
      }
    }
  } else {
    if (lastData == '\0') {
      ESC1.writeMicroseconds(1100);
      ESC2.writeMicroseconds(1100);
      ESC3.writeMicroseconds(1100);
      ESC4.writeMicroseconds(1100);
      ESC5.writeMicroseconds(1460);
      ESC6.writeMicroseconds(1466);
    } else {
      if (start == 1) {
        if ((distance1 < 450) && (distance1 > 10)) {
          naik();
        } else {
          turun();
        }

        switch (lastData) {
          case 'w': maju(); break;
          case 'a': kiri(); break;
          case 's': stop(); break;
          case 'd': kanan(); break;
          case 'p':
            if (!belok_kanan) {
              kanan();
              delay(10000);
              belok_kanan = true;
            }
            if (belok_kanan) {
              maju();
            }
            break;
          case 'o':
            if (!belok_kiri) {
              digitalWrite(relay, HIGH);
              kiri();
              delay(10000);
              belok_kiri = true;
            }
            if (belok_kiri) {
              maju_biasa();
            }
            break;
          case 'b': maju_biasa(); break;
        }
      }
    }
  }
}

void mix_detect(){
  if(Serial.available() > 0){
    char data = Serial.read();

    if(start == 0){
      ESC1.writeMicroseconds(1100);
      ESC2.writeMicroseconds(1100);
      ESC3.writeMicroseconds(1100);
      ESC4.writeMicroseconds(1100);
      ESC5.writeMicroseconds(1460);
      ESC6.writeMicroseconds(1460);
    }

    if(start == 1){
      if(!state){
        if((distance1 < 800) && (distance1 > 10)){
          naik();
        }else{
          turun();
        }
      }

      if(state){
        if(distance1 < 600){
          naik();
        }else{
          turun();
        }

        if(data == 'w'){
          maju();
        }else if(data == 'a'){
          kiri();
        }else if(data == 's'){
          stop();
        }else if(data == 'd'){
          kanan();
        }else if(data == 'p'){
          if(!belok_kanan){
            kanan();
            delay(8000);
          }
          if(belok_kanan){
            maju();
          }
        }else if(data == 'o'){
          if(!belok_kiri){
            kiri();
            delay(8000);
          }
          if(belok_kiri){
            maju_biasa();
          }
        }else if(data == 'b'){
          maju_biasa();
        }
      }

    }
    
  }else{
    ESC1.writeMicroseconds(1100);
    ESC2.writeMicroseconds(1100);
    ESC3.writeMicroseconds(1100);
    ESC4.writeMicroseconds(1100);
    ESC5.writeMicroseconds(1460);
    ESC6.writeMicroseconds(1460);
  }

}

void mix_detect_baru(){
  if(Serial.available() > 0){
    char data = Serial.read();
    last_data = data;

    if(data == 'H'){ // Menerima sinyal handshake dari Raspberry Pi
      Serial.println("ACK"); // Mengirim ACK sebagai respons
    }

    digitalWrite(relay, HIGH);

    if(!start){
      ESC1.writeMicroseconds(1100);
      ESC2.writeMicroseconds(1100);
      ESC3.writeMicroseconds(1100);
      ESC4.writeMicroseconds(1100);
      ESC5.writeMicroseconds(1460);
      ESC6.writeMicroseconds(1460);

      delay(3000);
      digitalWrite(relay, LOW);
      start = true;
    }

    if(start){
      if(!state){
        if((distance1 < 800) && (distance1 > 10)){
          naik();
        }else{
          turun();
        }
      }

      if(state){
        if((distance1 < 600) && (distance1 > 10)){
          naik();
        }else{
          turun();
        }

        if(data == 'w'){
          maju();
        }else if(data == 'a'){
          kiri();
        }else if(data == 's'){
          stop();
        }else if(data == 'd'){
          kanan();
        }else if(data == 'p'){
          if(!belok_kanan){
            kanan();
            delay(8000);
          }
          if(belok_kanan){
            maju();
          }
        }else if(data == 'o'){
          if(!belok_kiri){
            kiri();
            delay(8000);
          }
          if(belok_kiri){
            maju_biasa();
          }
        }else if(data == 'b'){
          maju_biasa();
        }
      }

    }
    
  }else{
    if (lastData == '\0') {
      ESC1.writeMicroseconds(1100);
      ESC2.writeMicroseconds(1100);
      ESC3.writeMicroseconds(1100);
      ESC4.writeMicroseconds(1100);
      ESC5.writeMicroseconds(1460);
      ESC6.writeMicroseconds(1466);
    }else{
      if(state){
        if((distance1 < 600) && (distance1 > 10)){
          naik();
        }else{
          turun();
        }

        if(last_data == 'w'){
          maju();
        }else if(last_data == 'a'){
          kiri();
        }else if(last_data == 's'){
          stop();
        }else if(last_data == 'd'){
          kanan();
        }else if(last_data == 'p'){
          if(!belok_kanan){
            kanan();
            delay(8000);
          }
          if(belok_kanan){
            maju();
          }
        }else if(last_data == 'o'){
          if(!belok_kiri){
            kiri();
            delay(8000);
          }
          if(belok_kiri){
            maju_biasa();
          }
        }else if(last_data == 'b'){
          maju_biasa();
        }
      }
    }
    
  }

}

void mix_detect_ultra(){
  if(Serial.available() > 0){
    char data = Serial.read();

    if(data == 'H'){ // Received handshake signal from Raspberry Pi
      Serial.println("ACK"); // Send ACK as response
    }

    if(start == 0){
      ESC1.writeMicroseconds(1100);
      ESC2.writeMicroseconds(1100);
      ESC3.writeMicroseconds(1100);
      ESC4.writeMicroseconds(1100);
      ESC5.writeMicroseconds(1460);
      ESC6.writeMicroseconds(1460);
    }

    if(start == 1){
      if(!state){
        if((distance1 < 800) && (distance1 > 10)){
          naik();
        }else{
          turun();
        }
      }

      if(state){
        if(distance1 < 600){
          naik();
        }else{
          turun();
        }

        if(data == 'w'){
          maju();
        }else if(data == 'a'){
          kiri();
        }else if(data == 's'){
          stop();
        }else if(data == 'd'){
          kanan();
        }else if(data == 'p'){
          if(!belok_kanan){
            kanan();
            delay(8000);
          }
          if(belok_kanan){
            maju();
          }
        }else if(data == 'o'){
          if(!belok_kiri){
            kiri();
            delay(8000);
          }
          if(belok_kiri){
            maju_biasa();
          }
        }else if(data == 'b'){
          maju_biasa();
        }
      }
    }
  } else {
    ESC1.writeMicroseconds(1100);
    ESC2.writeMicroseconds(1100);
    ESC3.writeMicroseconds(1100);
    ESC4.writeMicroseconds(1100);
    ESC5.writeMicroseconds(1460);
    ESC6.writeMicroseconds(1460);
  }

}

void cek_motor(){
  ESC1.writeMicroseconds(1250);
  ESC2.writeMicroseconds(1250);
  ESC3.writeMicroseconds(1250);
  ESC4.writeMicroseconds(1250);
  ESC5.writeMicroseconds(1550);
  ESC6.writeMicroseconds(1550);
}

void tembak_bro(){
  if(!state){
    if((distance1 < 800) && (distance1 > 0)){
      naik();
      state = true;
        previousMillis = currentMillis;
        counter = 0;
    }else{
      turun();
    }
  }

  if(state){
    if(distance1 < 700){
      naik();
    }else{
      turun();
    }

    switch(counter){
      case 0:
        // maju pid
        if(currentMillis - previousMillis >= maju_interval){
          previousMillis = currentMillis;
          counter++;
        }else{
          maju();
        }
        break;

      case 1:
        // kanan menghindari obstacle
        if(currentMillis - previousMillis >= kanan_interval){
          previousMillis = currentMillis;
          counter++;
        }else{
          kanan();
        }
        break;

      case 2:
        // maju pid
        if(currentMillis - previousMillis >= maju2_interval){
          previousMillis = currentMillis;
          counter++;
        }else{
          maju();
        }
        break;

      case 3:
        // kiri
        if(currentMillis - previousMillis >= kiri_interval){
          previousMillis = currentMillis;
          counter++;
        }else{
          kiri();
        }
        break;

      case 4:
        // maju tanpa pid
        if(currentMillis - previousMillis >= maju3_interval){
          previousMillis = currentMillis;
          counter++;
        }else{
          maju_biasa();
        }
        break;

      case 5:
        // stop
        stop();
        break;
    }
  }
}

void tembak_bro_start(){
  if(start == 0){
    ESC1.writeMicroseconds(1100);
    ESC2.writeMicroseconds(1100);
    ESC3.writeMicroseconds(1100);
    ESC4.writeMicroseconds(1100);
    ESC5.writeMicroseconds(1460);
    ESC6.writeMicroseconds(1460);
  }

  if(start == 1){
    if(!state){
      if((distance1 < 800) && (distance1 > 0)){
        naik();
        state = true;
          previousMillis = currentMillis;
          counter = 0;
      }else{
        turun();
      }
    }

    if(state){
      if(distance1 < 700){
        naik();
      }else{
        turun();
      }

      switch(counter){
        case 0:
          // maju pid
          if(currentMillis - previousMillis >= maju_interval){
            previousMillis = currentMillis;
            counter++;
          }else{
            maju();
          }
          break;

        case 1:
          // kanan menghindari obstacle
          if(currentMillis - previousMillis >= kanan_interval){
            previousMillis = currentMillis;
            counter++;
          }else{
            kanan();
          }
          break;

        case 2:
          // maju pid
          if(currentMillis - previousMillis >= maju2_interval){
            previousMillis = currentMillis;
            counter++;
          }else{
            maju();
          }
          break;

        case 3:
          // kiri
          if(currentMillis - previousMillis >= kiri_interval){
            previousMillis = currentMillis;
            counter++;
          }else{
            kiri();
          }
          break;

        case 4:
          // maju tanpa pid
          if(currentMillis - previousMillis >= maju3_interval){
            previousMillis = currentMillis;
            counter++;
          }else{
            maju_biasa();
          }
          break;

        case 5:
          // stop
          stop();
          break;
      }
    }
  }
}

void tes_speed_motor(){
  if(Serial.available() > 0){
    String input = Serial.readStringUntil('\n');
    int y1 = input.toInt();

    // Validate the input range
    if (y1 >= 1000 && y1 <= 2000) {
      ESC1.writeMicroseconds(y1);
      ESC2.writeMicroseconds(y1);
      ESC3.writeMicroseconds(y1);
      ESC4.writeMicroseconds(y1);
      // ESC5.writeMicroseconds(y1);
      // ESC6.writeMicroseconds(y1);
    }else{
      Serial.println("invalid input");
    }
    delay(1000);
  }
}

void cek_ultra(){
  if (!state) {
    if ((distance1 < 1000) && (distance1 >= 0)) {
      naik();
      state = true;
    } else {
      turun();
    }
  }

  // Logika ketika state = true
  if (state) {
    if (distance1 < 800) {
      naik();
    } else {
      turun();
    }

    if ((distance2 < 600) && (distance2 > 10)) {
      atas_stop();
    } else{
      kiri_ultra();
    }
  }
}

void task(){
  unsigned long currentMillis = millis();

  if(Serial.available() > 0){
    String input = Serial.readStringUntil('\n');
    int y1 = input.toInt();

    switch(y1){
      case 0:
        if(currentMillis - previousMillis < interval){
          maju();
        }else{
          stop();
          previousMillis = currentMillis;
        }
        break;

      case 1:
        if(currentMillis - previousMillis < interval){
          kanan();
        }else{
          stop();
          previousMillis = currentMillis;
        }
        break;

      case 2:
        if(currentMillis - previousMillis < interval){
          kiri();
        }else{
          stop();
          previousMillis = currentMillis;
        }

        break;

      case 3:
        buka();
        break;
    }

    delay(1000);
  }
}

void task2(){
  unsigned long currentMillis2 = millis();

  if(start == 1){
    switch(counter){
      case 0:
        if(currentMillis2 - previousMillis < interval){
          ESC1.writeMicroseconds(1400);
          ESC2.writeMicroseconds(1400);
          ESC3.writeMicroseconds(1400);
          ESC4.writeMicroseconds(1400);
        }else{
          previousMillis = currentMillis2;
          counter = 1;
        }
        break;
      
      case 1:
        if(currentMillis2 - previousMillis < interval){
          ESC1.writeMicroseconds(1400);
          ESC2.writeMicroseconds(1400);
          ESC3.writeMicroseconds(1400);
          ESC4.writeMicroseconds(1400);
          maju();
        }else{
          previousMillis = currentMillis2;
          counter = 2;
        }
        break;

      case 2:
        if(currentMillis2 - previousMillis < interval){
          ESC1.writeMicroseconds(1400);
          ESC2.writeMicroseconds(1400);
          ESC3.writeMicroseconds(1400);
          ESC4.writeMicroseconds(1400);
          kanan();
        }else{
          previousMillis = currentMillis2;
          counter = 3;
        }
        break;

      case 3:
        if(currentMillis2 - previousMillis < interval){
          ESC1.writeMicroseconds(1400);
          ESC2.writeMicroseconds(1400);
          ESC3.writeMicroseconds(1400);
          ESC4.writeMicroseconds(1400);
          kiri();
        }else{
          previousMillis = currentMillis2;
          counter = 4;
        }
        break;

      case 4:
        stop();
        if(currentMillis2 - previousMillis < interval){
          buka();
        }else{
          previousMillis = currentMillis2;
          GRIPPER.write(50);
          counter = 5;
        }
        break;

      default:
        break;
    }
  }
}

void cek_semua_sensor(){
  Serial.print("jarak ultra1: ");
  Serial.print(distance1);
  Serial.print("   jarak ultra2: ");
  Serial.print(distance2);
  Serial.print("   bearing: ");
  Serial.print(getBearing());
  Serial.print("   pitch: ");
  Serial.print(getPitch());
  Serial.print("   roll: ");
  Serial.println(getRoll());

  if(digitalRead(rain) == 0){
    digitalWrite(relay, HIGH);
    delay(500);
    digitalWrite(relay, LOW);
    delay(500);
  }else{
    digitalWrite(relay, LOW);
  }
}

void misi_dengan_millis(){
  if(start == 0){
    ESC1.writeMicroseconds(1100);
    ESC2.writeMicroseconds(1100);
    ESC3.writeMicroseconds(1100);
    ESC4.writeMicroseconds(1100);
    ESC5.writeMicroseconds(1460);
    ESC6.writeMicroseconds(1460);
  }

  if(start == 1){
    if(!state){
      if((distance1 < 900) && (distance1 >= 0)){
        naik();
        state = true;
        previousMillis = currentMillis;
        counter = 0;
      }else{
        turun();
      }
    }

    if(state){
      if(distance1 > 800){
        turun();
      }else{
        naik();
      }

      switch(counter){
        case 0:
          if(currentMillis - previousMillis >= maju1_interval){
            previousMillis = currentMillis;
            counter++;
          }else{
            maju();
          }

          break;

        case 1:
          if(currentMillis - previousMillis >= kanan_interval){
            previousMillis = currentMillis;
            counter++;
          }else{
            kanan();
          }

          break;

        case 2:
          if(currentMillis - previousMillis >= kiri_interval){
            previousMillis = currentMillis;
            counter++;
          }else{
            kiri();
          }

          break;

        case 3:
          if(currentMillis - previousMillis >= maju2_interval){
            previousMillis = currentMillis;
            counter++;
          }else{
            maju();
          }
        
        case 4:
          if(Serial.available() > 0){
            char data = Serial.read();
            if(data == 'a'){
              kiri();
            }else if(data == 's'){
              stop();
            }else if(data == 'd'){
              kanan(); 
            }else if(data == 'b'){
              maju_biasa();
            }else{
              kiri();
              delay(5000);
              maju_biasa();
              delay(5000);
            }
          }else{
            ESC1.writeMicroseconds(1100);
            ESC2.writeMicroseconds(1100);
            ESC3.writeMicroseconds(1100);
            ESC4.writeMicroseconds(1100);
            ESC5.writeMicroseconds(1460);
            ESC6.writeMicroseconds(1460);
          }
      }
    }
  }
}