
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <DHT.h>
#include <DHT_U.h>
#include "Thing.CoAP.h"
#include "Thing.CoAP/Server.h"
#include "Thing.CoAP/ESP/UDPPacketProvider.h"

Thing::CoAP::Server server;
Thing::CoAP::ESP::UDPPacketProvider udpProvider;

const char *ssid = "Mery's A56";
const char *password = "merieme01012004";

#define LED_PIN 2
#define BUTTON_PIN 0
#define DHT_PIN 4 // DHT11 is connected to GPIO 4 (D2 on NodeMCU)

DHT dht(DHT_PIN, DHT11);
float temp = 0.0;

void setup()
{
  Serial.begin(9600);
  Serial.println("Initializing");

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  Serial.print("My IP: ");
  Serial.println(WiFi.localIP());

  dht.begin(); // Initialize the DHT sensor

  server.SetPacketProvider(udpProvider);

  // LED resource
  auto &ledEndpoint = server.CreateEndpoint("LED", Thing::CoAP::ContentFormat::TextPlain, true);
  ledEndpoint.OnGet([](Thing::CoAP::Request &request)
                    {
        Serial.println("GET Request received for endpoint 'LED'");
        std::string result;
        if (digitalRead(LED_PIN) == HIGH)
            result = "On";
        else
            result = "Off";
        return Thing::CoAP::Status::Ok(result); });

  ledEndpoint.OnPost([](Thing::CoAP::Request &request)
                     {
        Serial.println("POST Request received for endpoint 'LED'");
        auto payload = request.GetPayload();
        std::string message(payload.begin(), payload.end());
        Serial.print("The client sent the message: ");
        Serial.println(message.c_str());
        if (message == "On") {
            digitalWrite(LED_PIN, HIGH);
        } else if (message == "Off") {
            digitalWrite(LED_PIN, LOW);
        } else {
            return Thing::CoAP::Status::BadRequest();
        }
        return Thing::CoAP::Status::Created("ok merci"); });

  // Temperature sensor resource
  auto &tempEndpoint = server.CreateEndpoint("temp", Thing::CoAP::ContentFormat::TextPlain, false);
  tempEndpoint.OnGet([](Thing::CoAP::Request &request)
                     {
        Serial.println("GET Request received for endpoint 'temp'");
        float temperature = dht.readTemperature(); // Read temperature from DHT11
        std::string result = String(temperature).c_str();
        return Thing::CoAP::Status::Ok(result); });

  // Temp variable resource
  auto &tempVarEndpoint = server.CreateEndpoint("tempVar", Thing::CoAP::ContentFormat::TextPlain, false);
  tempVarEndpoint.OnGet([](Thing::CoAP::Request &request)
                        {
        Serial.println("GET Request received for endpoint 'tempVar'");
        std::string result = String(temp).c_str();
        return Thing::CoAP::Status::Ok(result); });

  server.Start();
}

void loop()
{
  temp += 1;
  Serial.println(temp);
  server.Process();
  delay(1000);
}