#!/usr/bin/env python3
"""
Contrôle simple de 3 LEDs via GPIO.

À COMPLÉTER : Ajoutez le code pour contrôler 3 LEDs
- LED rouge sur GPIO 17
- LED verte sur GPIO 27
- LED jaune sur GPIO 22

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

# TODO : Configurer le mode BCM
# GPIO.setmode(GPIO.???)

# TODO : Configurer les broches en sortie
# GPIO.setup(..., GPIO.OUT)

def allumer_toutes():
    """Allume toutes les LEDs."""
    # TODO : Implémenter
    pass

def eteindre_toutes():
    """Éteint toutes les LEDs."""
    # TODO : Implémenter
    pass

def main():
    """Fonction principale."""
    print("Contrôle de 3 LEDs")
    print("Rouge = GPIO 17, Verte = GPIO 27, Jaune = GPIO 22")
    print("Appuyez sur Ctrl+C pour quitter")

    try:
        while True:
            # TODO : Allumer chaque LED une par une
            # avec 1 seconde d'intervalle
            pass

    except KeyboardInterrupt:
        print("\nAu revoir!")
    finally:
        # TODO : Nettoyer les GPIO avant de quitter
        # GPIO.cleanup()
        pass

if __name__ == "__main__":
    main()
