#!/usr/bin/env python3
"""
Lecture du capteur de température et d'humidité DHT22.

À COMPLÉTER : Lisez la température et l'humidité relative

Câblage DHT22 :
- Pin 1 (VCC)  → 3.3V ou 5V
- Pin 2 (DATA) → GPIO 4 (avec résistance 10K vers VCC)
- Pin 3 (NC)   → Non connecté
- Pin 4 (GND)  → GND

Note : Le DHT22 utilise un protocole one-wire (pas I²C).
"""

import time
import board
import adafruit_dht

# Configuration du capteur DHT22
# Le DHT22 et DHT11 utilisent le même pilote
DHT_PIN = board.D4  # GPIO 4 (Broche 7 sur le connecteur)
DHT_SENSOR = adafruit_dht.DHT22

def lire_temperature():
    """
    Lit la température en degrés Celsius.

    Returns:
        float: Température en °C, ou None si erreur
    """
    # TODO : Créer l'objet capteur DHT22
    # dht = DHT_SENSOR(DHT_PIN)

    try:
        # TODO : Lire et retourner la température
        # return dht.temperature
        pass
    except RuntimeError as e:
        print(f"Erreur de lecture: {e}")
        return None

def lire_humidite():
    """
    Lit l'humidité relative en pourcentage.

    Returns:
        float: Humidité relative en %RH, ou None si erreur
    """
    # TODO : Lire et retourner l'humidité
    pass

def afficher_mesures():
    """Affiche les mesures de température et d'humidité."""
    # Créer l'objet capteur
    dht = DHT_SENSOR(DHT_PIN)

    print("Capteur DHT22 - Température et Humidité")
    print("Appuyez sur Ctrl+C pour quitter")
    print("-" * 40)

    while True:
        try:
            # TODO : Lire la température et l'humidité
            temperature = dht.temperature
            humidite = dht.humidity

            # Vérifier que les valeurs sont valides
            if temperature is not None and humidite is not None:
                # Afficher les résultats
                print(f"Température: {temperature:.1f} °C")
                print(f"Humidité: {humidite:.1f} %RH")
                print("-" * 40)
            else:
                print("Échec de la lecture. Réessai...")

            time.sleep(2)  # Le DHT22 nécessite au moins 2 secondes entre les lectures

        except RuntimeError as error:
            # Les erreurs sont fréquentes avec le DHT22
            print(f"Erreur de lecture: {error.args[0]}")
            time.sleep(2.0)
            continue

        except KeyboardInterrupt:
            print("\nAu revoir!")
            break

        except Exception as e:
            print(f"Erreur: {e}")
            print("Vérifiez que:")
            print("  - Le capteur est correctement câblé")
            print("  - La broche DATA est sur GPIO 4")
            print("  - Une résistance 10K relie DATA à VCC")
            break

def main():
    """Fonction principale."""
    afficher_mesures()

if __name__ == "__main__":
    main()
