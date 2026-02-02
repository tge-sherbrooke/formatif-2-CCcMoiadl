# Formatif F2 — GPIO, Git et capteur DHT22

**Cours** : 243-413-SH — Introduction aux objets connectes
**Semaine** : 2
**Type** : Formative (non notee)
**Retries** : Illimites - poussez autant de fois que necessaire!

---

## Progressive Milestones

Ce formatif utilise des **jalons progressifs** avec retroaction detaillee:

| Jalon | Points | Verification |
|-------|--------|-------------|
| **Milestone 1** | 25 pts | Scripts LED avec RPi.GPIO |
| **Milestone 2** | 35 pts | DHT22 avec LOGIQUE DE RETRY (critique!) |
| **Milestone 3** | 40 pts | Git workflow de base (clone/add/commit/push) |

**Chaque test echoue vous dit**: ce qui etait attendu, ce qui a ete trouve, une suggestion pour corriger.

---

## IMPORTANT: Erreurs DHT22 sont NORMALES!

Le protocole one-wire du DHT22 echoue 10-20% du temps. **C'est normal!**
Votre code **DOIT** implementer une logique de retry:

```python
for attempt in range(5):
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        break  # Succes!
    except RuntimeError as e:
        print(f"Retry {attempt + 1}/5: {e}")
        time.sleep(2)
```

---

## Objectif

Ce formatif vise a verifier que vous etes capable de :
1. Controler des actionneurs (LEDs) via les broches GPIO
2. Utiliser les commandes Git de base (clone, add, commit, push)
3. Lire un capteur DHT22 (temperature + humidite) avec gestion des erreurs

---

## Workflow de soumission

⚠️ **IMPORTANT** : Vous devez **exécuter les tests localement sur le Raspberry Pi AVANT de pousser**.

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKLOAD FORMATIF F2                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Créer une branche feature/led                               │
│     └─ Compléter led_simple.py et led_rgb.py                   │
│     └─ Tester sur le matériel                                   │
│     └─ Commiter et fusionner dans main                         │
│                                                                  │
│  2. Créer une branche feature/dht22                            │
│     └─ Compléter dht22.py                                        │
│     └─ Tester sur le matériel                                   │
│     └─ Commiter et fusionner dans main                         │
│                                                                  │
│  3. Exécuter les tests locaux                                   │
│     └─ python3 run_tests.py                                    │
│     └─ Corriger les erreurs                                    │
│                                                                  │
│  4. Pousser votre travail                                      │
│     └─ git push origin main                                    │
│                                                                  │
│  5. GitHub Actions valide automatiquement                      │
│     └─ Vérifie la syntaxe Python                              │
│     └─ Vérifie les branches Git                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tâche 1 : Contrôle de LEDs via GPIO

### Câblage

| LED | GPIO | Résistance | Vers |
|-----|------|-----------|------|
| Rouge | 17 | 330Ω | GND |
| Verte | 27 | 330Ω | GND |
| Jaune | 22 | 330Ω | GND |

⚠️ **Important** : La patte la plus longue de la LED (anode) va vers le GPIO. La patte courte (cathode) va vers la résistance, puis vers GND.

### Script à compléter : `led_simple.py`

Complétez le script pour :
1. Configurer le mode BCM
2. Configurer les 3 broches en sortie
3. Allumer et éteindre chaque LED successivement

```python
import RPi.GPIO as GPIO

LED_ROUGE = 17
LED_VERTE = 27
LED_JAUNE = 22

# Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setup([LED_ROUGE, LED_VERTE, LED_JAUNE], GPIO.OUT)

# Allumer la LED rouge
GPIO.output(LED_ROUGE, GPIO.HIGH)
time.sleep(1)
GPIO.output(LED_ROUGE, GPIO.LOW)

# ... faire de même pour verte et jaune

GPIO.cleanup()
```

### Bonus : `led_rgb.py`

Créez un effet chenillard où les LEDs s'allument successivement.

---

## Tâche 2 : Utilisation des branches Git

### Format des messages de commit

Utilisez le format : `<type>(<portée>): <description>`

| Type | Description |
|------|-------------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Documentation |
| `test` | Tests |

**Exemples** :
- `feat(led): ajout contrôle LED rouge`
- `feat(dht22): lecture température et humidité`
- `fix(gpio): correction numéro de broche`
- `docs: mise à jour README`

### Workflow avec branches

```bash
# Créer la branche pour les LEDs
git checkout -b feature/led

# Compléter et tester led_simple.py
git add led_simple.py
git commit -m "feat(led): ajout contrôle simple des LEDs"

# Compléter et tester led_rgb.py (bonus)
git add led_rgb.py
git commit -m "feat(led): ajout effet chenillator"

# Fusionner dans main
git checkout main
git merge feature/led --no-ff -m "Merge feature/led - Contrôle LEDs complété"

# Créer la branche pour le DHT22
git checkout -b feature/dht22

# Compléter et tester dht22.py
git add dht22.py
git commit -m "feat(dht22): lecture température et humidité"

# Fusionner dans main
git checkout main
git merge feature/dht22 --no-ff -m "Merge feature/dht22 - Capteur DHT22 complété"

# Pousser vers GitHub
git push origin main
```

### Voir l'historique avec graph

```bash
git log --graph --oneline --all
```

---

## Tâche 3 : Lecture du capteur DHT22

### Câblage DHT22

Le DHT22 a 4 broches (ou 3 broches sur certains modules) :

| Broche | Description | Connexion |
|--------|-------------|-----------|
| Pin 1 | VCC | 3.3V ou 5V |
| Pin 2 | DATA | GPIO 4 (Broche 7) + résistance 10K vers VCC |
| Pin 3 | NC | Non connecté |
| Pin 4 | GND | GND |

⚠️ **Important** : Une résistance de 10KΩ doit relier DATA à VCC (pull-up).
Certains modules incluent déjà cette résistance sur le PCB.

### Schéma de connexion

```
DHT22
│
├─ VCC (Pin 1) ──────────── 3.3V ou 5V
│
├─ DATA (Pin 2) ───┬──────── GPIO 4 (Broche 7)
│                  │
│                  └──────── résistance 10KΩ ──── VCC
│
├─ NC (Pin 3) ───────────── (non connecté)
│
└─ GND (Pin 4) ──────────── GND
```

### Script à compléter : `dht22.py`

Complétez le script pour lire la température et l'humidité :

```python
import board
import adafruit_dht
import time

# Configuration du capteur
DHT_PIN = board.D4
dht = adafruit_dht.DHT22(DHT_PIN)

while True:
    try:
        temperature = dht.temperature
        humidite = dht.humidity

        print(f"Température: {temperature:.1f} °C")
        print(f"Humidité: {humidite:.1f} %RH")

        time.sleep(2)  # Minimum 2 secondes entre les lectures
    except RuntimeError as e:
        print(f"Erreur de lecture: {e}")
        time.sleep(2)
```

### Tester le script

```bash
# Installer les dépendances
uv pip install adafruit-circuitpython-dht adafruit-blinka RPi.GPIO

# Exécuter le script
uv run dht22.py
```

---

## Exécuter les tests locaux

⚠️ **Ceci est l'étape obligatoire avant de pousser!**

```bash
python3 run_tests.py
```

Le script `run_tests.py` va :
1. ✅ Vérifier la syntaxe Python de tous les scripts
2. ✅ Vérifier que les imports sont corrects
3. ✅ Vérifier que les branches Git ont été créées
4. ✅ Vérifier le format des messages de commit
5. ✅ Valider le script DHT22 (protocole one-wire, pas de détection I²C)
6. ✅ Créer des fichiers marqueurs dans `.test_markers/`

Si tous les tests passent, vous verrez :
```
🎉 TOUS LES TESTS SONT PASSÉS!
```

---

## Pousser votre travail

Une fois les tests passés :

```bash
git add .
git commit -m "feat: formatif F2 complété"
git push origin main
```

GitHub Actions validera automatiquement que vous avez exécuté les tests.

---

## Livrables

Dans ce dépôt, vous devez avoir :

- [ ] `led_simple.py` — Script de contrôle des LEDs complété
- [ ] `led_rgb.py` — Script chenillator (bonus)
- [ ] `dht22.py` — Script de lecture du DHT22 complété
- [ ] Historique Git avec branches `feature/led` et `feature/dht22`
- [ ] Messages de commit au format conventionné
- [ ] `.test_markers/` — Dossier créé par `run_tests.py`

---

## Comprendre la validation

### Pourquoi exécuter `run_tests.py` AVANT de pousser ?

Le formatif F2 utilise une validation en deux temps :

| Étape | Où | Ce qui est validé |
|-------|----|-------------------|
| **run_tests.py** | Sur Raspberry Pi | - Syntaxe Python<br>- Imports corrects<br>- Branches Git créées<br>- Format des commits<br>- Scripts DHT22 vérifiés |
| **GitHub Actions** | Automatique après push | - Les marqueurs existent<br>- Syntaxe Python valide<br>- Structure des fichiers |

Cette approche garantit que vous avez **réellement** travaillé sur le matériel tout en bénéficiant de l'automatisation GitHub.

---

## Résumé des commandes

```bash
# ===== INSTALLER LES DÉPENDANCES =====
uv pip install adafruit-circuitpython-dht adafruit-blinka RPi.GPIO

# ===== ACTIVER GPIO (si nécessaire) =====
sudo raspi-config nonint do_gpio 0

# ===== BRANCHE ET COMPLÉTER LED =====
git checkout -b feature/led
# ... compléter led_simple.py ...
uv run led_simple.py
git add led_simple.py
git commit -m "feat(led): ajout contrôle simple des LEDs"

# ===== FUSIONNER DANS MAIN =====
git checkout main
git merge feature/led --no-ff

# ===== BRANCHE ET COMPLÉTER DHT22 =====
git checkout -b feature/dht22
# ... compléter dht22.py ...
uv run dht22.py
git add dht22.py
git commit -m "feat(dht22): lecture température et humidité"

# ===== FUSIONNER DANS MAIN =====
git checkout main
git merge feature/dht22 --no-ff

# ===== EXÉCUTER LES TESTS =====
python3 run_tests.py

# ===== POUSSER =====
git push origin main
```

---

## Ressources

- [Guide de l'étudiant](../../deliverables/activites/semaine-2/labo/guide-étudiant.md)
- [Guide de dépannage](../../deliverables/activites/semaine-2/labo/guide-depannage.md)
- [Documentation RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/)
- [Documentation Adafruit DHT](https://learn.adafruit.com/dht)

---

Bonne chance ! 🚀
