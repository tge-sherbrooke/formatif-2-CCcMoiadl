#!/usr/bin/env python3
"""
Effet chenillard sur 3 LEDs via GPIO.

À COMPLÉTER (BONUS) : Créez un effet chenillard

Câblage :
- LED rouge : GPIO 17 → résistance 330Ω → GND
- LED verte : GPIO 27 → résistance 330Ω → GND
- LED jaune : GPIO 22 → résistance 330Ω → GND
"""

import time
import RPi.GPIO as GPIO

# Configuration des broches GPIO
LED_ROUGE = 17
LED_VERTE = 27
LED_JAUNE = 22

LEDS = [LED_ROUGE, LED_VERTE, LED_JAUNE]

def chenillard(delai=0.3):
    """
    Effet chenillard : les LEDs s'allument successivement.

    Args:
        delai (float): Délai entre chaque LED en secondes
    """
    # TODO : Implémenter l'effet chenillard
    # Allumer LED 1, attendre, éteindre LED 1
    # Allumer LED 2, attendre, éteindre LED 2
    # Allumer LED 3, attendre, éteindre LED 3
    # Répéter

    for i in range(5) :
        # Allumer la LED rouge
        GPIO.output(LED_ROUGE, GPIO.HIGH)
        print("LED_ROUGE HIGH")
        time.sleep(delai)
        GPIO.output(LED_ROUGE, GPIO.LOW)
        print("LED_ROUGE LOW")
        GPIO.output(LED_VERTE, GPIO.HIGH)
        print("LED_VERTE HIGH")
        time.sleep(delai)
        GPIO.output(LED_VERTE, GPIO.LOW)
        print("LED_VERTE LOW")
        GPIO.output(LED_JAUNE, GPIO.HIGH)
        print("LED_JAUNE HIGH")
        time.sleep(delai)
        GPIO.output(LED_JAUNE, GPIO.LOW)
        print("LED_JAUNE LOW")

    pass

def chenillard_allume(delai=0.3):
    """
    Effet chenillard où les LEDs restent allumées.

    Args:
        delai (float): Délai entre chaque LED en secondes
    """
    # TODO : Implémenter l'effet chenillard "qui reste allumé"

    GPIO.output(LED_ROUGE, GPIO.HIGH)
    time.sleep(delai)
    GPIO.output(LED_VERTE, GPIO.HIGH)
    time.sleep(delai)
    GPIO.output(LED_JAUNE, GPIO.HIGH)
    time.sleep(delai)
    pass

def main():
    """Fonction principale."""
    # Configuration
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDS, GPIO.OUT)

    # Éteindre toutes les LEDs au départ
    for led in LEDS:
        GPIO.output(led, GPIO.LOW)

    print("Effet chenillator sur 3 LEDs")
    print("Appuyez sur Ctrl+C pour quitter")

    try:
        while True:
            # TODO : Appeler votre fonction chenillard
            chenillard(0.1)
            chenillard_allume(0.3)
            pass

    except KeyboardInterrupt:
        print("\nAu revoir!")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
