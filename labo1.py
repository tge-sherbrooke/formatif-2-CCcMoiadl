import RPi.GPIO as GPIO
import time

LED_ROUGE = 17
LED_VERTE = 27
LED_JAUNE = 22

# Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setup([LED_ROUGE, LED_VERTE, LED_JAUNE], GPIO.OUT)

# Allumer la LED rouge
GPIO.output(LED_ROUGE, GPIO.HIGH)
print("LED_ROUGE HIGH")
time.sleep(1)
GPIO.output(LED_ROUGE, GPIO.LOW)
print("LED_ROUGE LOW")
time.sleep(1)
GPIO.output(LED_VERTE, GPIO.HIGH)
print("LED_VERTE HIGH")
time.sleep(1)
GPIO.output(LED_VERTE, GPIO.LOW)
print("LED_VERTE LOW")
time.sleep(1)
GPIO.output(LED_JAUNE, GPIO.HIGH)
print("LED_JAUNE HIGH")
time.sleep(1)
GPIO.output(LED_JAUNE, GPIO.LOW)
print("LED_JAUNE LOW")
time.sleep(1)

GPIO.cleanup()