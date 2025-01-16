#include <Arduino_HS300x.h> // Temperatur + Luftfeuchtigkeit
#include <ArduinoBLE.h>

// Definition von Service und Charakteristik
BLEService serialService("180C"); // Benutzerdefinierter Service
BLECharacteristic serialCharacteristic("2A56", BLERead | BLENotify, 512);

void setup() {
  // Status-LED zum Testen hinzufügen
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // LED einschalten, um zu zeigen, dass der Arduino läuft
  
  // Serielle Kommunikation starten (falls nötig)
  Serial.begin(9600);
  while (!Serial); // Warten, bis der serielle Monitor bereit ist
  
  // Kleine Verzögerung, um sicherzustellen, dass das BLE-Modul genügend Zeit zum Starten hat
  delay(2000);  // Warte 2 Sekunden

  // BLE-Initialisierung
  if (!BLE.begin()) {
    Serial.println("BLE konnte nicht gestartet werden");
    while (1); // Endlosschleife bei Fehler
  }

  // BLE-Konfiguration
  BLE.setLocalName("Nano33BLE");         // Anzeigename im BLE-Scanner

  // Charakteristik dem Service hinzufügen
  serialService.addCharacteristic(serialCharacteristic);

  // Service zum BLE hinzufügen
  BLE.addService(serialService);

  // Charakteristik initialisieren
  serialCharacteristic.writeValue("Initial Value");

  // Service der Werbung hinzufügen und Werbung starten
  BLE.setAdvertisedService(serialService);
  if (!BLE.advertise()) {
    Serial.println("BLE-Werbung konnte nicht gestartet werden");
    while (1);
  }

  Serial.println("BLE ist bereit und bewirbt den Service 180C");

  // Initialisierung des Temperatursensors
  if (!HS300x.begin()) {
    Serial.println("Temperatursensor konnte nicht initialisiert werden");
    while (1); // Endlosschleife bei Fehler
  }

  digitalWrite(LED_BUILTIN, LOW);  // LED ausschalten, wenn der Arduino bereit ist
}

void loop() {
  // BLE-Zentrale (Central Device) verwalten
  BLEDevice central = BLE.central();
  if (central) {
    Serial.println("Verbindung hergestellt mit: " + central.address());
    int a = -20;
    while (central.connected()) {
      // Temperatur auslesen und senden
      float temperature = HS300x.readTemperature();
      String tempString = "Zeit:" + String(a) + " Temperatur:" + String(temperature);

      // Temperaturänderungen nur bei Bedarf senden
      serialCharacteristic.writeValue(tempString.c_str());
      Serial.println("Daten gesendet: " + tempString);

      delay(1000);
      a = a + 1;
    }
    Serial.println("Verbindung getrennt");
  }

  delay(500); // Vermeidung übermäßiger CPU-Auslastung
}
