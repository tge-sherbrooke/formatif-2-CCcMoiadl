#!/usr/bin/env python3
"""
Test runner local pour le Formatif F2 - Semaine 2

Ce script exécute les tests localement sur le Raspberry Pi et crée
des fichiers marqueurs qui seront vérifiés par GitHub Actions.

Usage: python3 run_tests.py
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Couleurs ANSI pour le terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def check_python_syntax(script_path):
    """Vérifie la syntaxe Python d'un script."""
    try:
        with open(script_path) as f:
            compile(f.read(), script_path, 'exec')
        return True, None
    except SyntaxError as e:
        return False, f"Erreur de syntaxe ligne {e.lineno}: {e.msg}"


def check_python_imports(script_path, required_imports):
    """Vérifie que les imports requis sont présents."""
    content = script_path.read_text()
    missing = []
    for imp in required_imports:
        if imp not in content:
            missing.append(imp)
    return len(missing) == 0, missing


def check_led_scripts():
    """Vérifie les scripts LED."""
    print_header("VÉRIFICATION SCRIPTS LED")

    results = {}

    # Vérifier led_simple.py
    led_simple = Path(__file__).parent / "led_simple.py"
    if led_simple.exists():
        print_success("Fichier led_simple.py trouvé")

        # Syntaxe
        valid, error = check_python_syntax(led_simple)
        if valid:
            print_success("Syntaxe Python valide")
        else:
            print_error(f"Erreur de syntaxe: {error}")

        # Imports
        required = ['RPi.GPIO', 'GPIO']
        valid, missing = check_python_imports(led_simple, required)
        if valid:
            print_success("Imports RPi.GPIO présents")
        else:
            print_warning(f"Imports manquants: {missing}")

        results['led_simple'] = valid
    else:
        print_error("Fichier led_simple.py introuvable")
        results['led_simple'] = False

    # Vérifier led_rgb.py (optionnel)
    led_rgb = Path(__file__).parent / "led_rgb.py"
    if led_rgb.exists():
        print_success("Fichier led_rgb.py trouvé (bonus)")

        valid, error = check_python_syntax(led_rgb)
        if valid:
            print_success("Syntaxe Python valide")
        else:
            print_error(f"Erreur de syntaxe: {error}")

        results['led_rgb'] = valid
    else:
        print_warning("Fichier led_rgb.py introuvable (optionnel)")
        results['led_rgb'] = True  # Non obligatoire

    # Créer le marqueur
    marker = Path(__file__).parent / ".test_markers" / "led_scripts_verified.txt"
    marker.parent.mkdir(exist_ok=True)
    marker.write_text(f"LED scripts verified: {datetime.now().isoformat()}\n")
    print_success(f"Marqueur LED créé: {marker}")

    return all(results.values())


def check_dht22_script():
    """Vérifie le script DHT22."""
    print_header("VÉRIFICATION SCRIPT DHT22")

    dht22 = Path(__file__).parent / "dht22.py"

    if not dht22.exists():
        print_error("Fichier dht22.py introuvable")
        return False

    print_success("Fichier dht22.py trouvé")

    # Syntaxe
    valid, error = check_python_syntax(dht22)
    if valid:
        print_success("Syntaxe Python valide")
    else:
        print_error(f"Erreur de syntaxe: {error}")
        return False

    # Imports
    required = ['board', 'adafruit_dht']
    valid, missing = check_python_imports(dht22, required)
    if valid:
        print_success("Imports requis présents")
    else:
        print_warning(f"Imports manquants: {missing}")

    # Créer le marqueur
    marker = Path(__file__).parent / ".test_markers" / "dht22_script_verified.txt"
    marker.write_text(f"DHT22 script verified: {datetime.now().isoformat()}\n")
    print_success(f"Marqueur DHT22 créé: {marker}")

    return True


def check_git_branches():
    """Vérifie que les branches Git requises existent."""
    print_header("VÉRIFICATION BRANCHES GIT")

    # Vérifier si on est dans un dépôt Git
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            print_warning("Pas dans un dépôt Git")
            return False
    except FileNotFoundError:
        print_warning("Git non trouvé")
        return False

    print_success("Dépôt Git détecté")

    # Lister toutes les branches (locales et distantes)
    try:
        result = subprocess.run(
            ['git', 'branch', '-a'],
            capture_output=True, text=True, timeout=5
        )
        branches = result.stdout

        required_branches = ['feature/led', 'feature/dht22']
        found = []

        for branch in required_branches:
            if branch in branches:
                print_success(f"Branche trouvée: {branch}")
                found.append(branch)
            else:
                print_warning(f"Branche non trouvée: {branch}")

        # Vérifier l'historique pour les branches fusionnées
        result = subprocess.run(
            ['git', 'log', '--all', '--oneline', '--grep', 'Merge'],
            capture_output=True, text=True, timeout=5
        )
        merge_history = result.stdout

        for branch in required_branches:
            if branch in merge_history:
                print_success(f"Branche fusionnée détectée: {branch}")
                if branch not in found:
                    found.append(branch)

        success = len(found) >= 2

        # Créer le marqueur
        marker = Path(__file__).parent / ".test_markers" / "git_branches_verified.txt"
        marker.write_text(f"Git branches verified: {datetime.now().isoformat()}\n")
        marker.write_text(f"Branches trouvées: {', '.join(found)}\n")
        print_success(f"Marqueur branches créé: {marker}")

        return success

    except Exception as e:
        print_warning(f"Erreur lors de la vérification des branches: {e}")
        return False


def check_git_commits():
    """Vérifie le format des messages de commit."""
    print_header("VÉRIFICATION MESSAGES DE COMMIT")

    try:
        # Récupérer les derniers commits
        result = subprocess.run(
            ['git', 'log', '--oneline', '-10'],
            capture_output=True, text=True, timeout=5
        )

        if result.returncode != 0:
            print_warning("Impossible de lire l'historique Git")
            return False

        commits = result.stdout.strip().split('\n')

        # Pattern pour les commits conventionnés
        # Format: type(scope): description
        pattern = re.compile(r'^(feat|fix|docs|test|refactor|style|chore)\(.+\):')

        valid_count = 0
        total_count = 0

        for commit in commits:
            if not commit.strip():
                continue
            total_count += 1
            if pattern.match(commit):
                valid_count += 1

        if total_count > 0:
            ratio = valid_count / total_count
            print(f"Commits conventionnés: {valid_count}/{total_count} ({ratio*100:.0f}%)")

            if ratio >= 0.5:
                print_success("Format des commits généralement conforme")
                success = True
            else:
                print_warning("Moins de 50% des commits suivent le format conventionné")
                success = True  # Avertissement, pas une erreur
        else:
            print_warning("Aucun commit trouvé")
            success = True  # Pas d'erreur si pas de commits

        # Créer le marqueur
        marker = Path(__file__).parent / ".test_markers" / "git_commits_verified.txt"
        marker.write_text(f"Git commits verified: {datetime.now().isoformat()}\n")
        marker.write_text(f"Commits conventionnés: {valid_count}/{total_count}\n")
        print_success(f"Marqueur commits créé: {marker}")

        return success

    except Exception as e:
        print_warning(f"Erreur lors de la vérification des commits: {e}")
        return True  # Pas bloquant


def check_hardware():
    """Vérifie le matériel (Raspberry Pi)."""
    print_header("VÉRIFICATION MATÉRIEL (Raspberry Pi)")

    # Vérifier si on est sur un Raspberry Pi
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            is_rpi = 'Raspberry Pi' in cpuinfo or 'Broadcom' in cpuinfo
    except:
        is_rpi = False

    if not is_rpi:
        print_warning("Pas sur Raspberry Pi - tests matériels skipés")
        print("   Exécutez ce script sur le Raspberry Pi pour les tests matériels")
        return True

    print_success("Raspberry Pi détecté")

    # Pour le DHT22, on ne peut pas le détecter automatiquement via i2cdetect
    # Le DHT22 utilise un protocole one-wire propriétaire
    print_info("DHT22 utilise un protocole one-wire (pas I²C)")
    print_info("Vérification manuelle requise:")
    print("   - Le capteur est-il connecté sur GPIO 4?")
    print("   - La résistance 10KΩ est-elle en place?")
    print("   - VCC est-il connecté (3.3V ou 5V)?")

    # Créer le marqueur matériel
    marker = Path(__file__).parent / ".test_markers" / "hardware_detected.txt"
    marker.write_text(f"Hardware scan: {datetime.now().isoformat()}\n")
    marker.write_text("DHT22: Vérification manuelle requise (GPIO 4)\n")
    print_success(f"Marqueur matériel créé: {marker}")

    return True


def update_gitignore():
    """Met à jour .gitignore pour permettre de commettre les marqueurs."""
    gitignore_path = Path(__file__).parent / ".gitignore"
    marker_dir = Path(__file__).parent / ".test_markers"

    if not marker_dir.exists():
        return

    if not gitignore_path.exists():
        return

    # Lire le .gitignore actuel
    lines = gitignore_path.read_text().splitlines()

    # Filtrer les lignes qui excluent .test_markers
    new_lines = []
    modified = False
    for line in lines:
        if '.test_markers' in line and not line.strip().startswith('#'):
            if not modified:
                new_lines.append('# .test_markers/ is now allowed (created by run_tests.py)')
                modified = True
        else:
            new_lines.append(line)

    if modified:
        gitignore_path.write_text('\n'.join(new_lines) + '\n')
        print_success(".gitignore mis à jour - les marqueurs peuvent être commités")


def create_test_summary():
    """Crée un résumé des tests."""
    marker_dir = Path(__file__).parent / ".test_markers"
    summary_file = marker_dir / "test_summary.txt"

    markers = list(marker_dir.glob("*_verified.txt")) + list(marker_dir.glob("*_detected.txt"))

    summary = f"""Test Summary for Formatif F2
Generated: {datetime.now().isoformat()}
Tests Run: {len(markers)}

Markers:
"""
    for marker in sorted(markers):
        summary += f"  - {marker.stem}: {marker.read_text().strip()}\n"

    summary_file.write_text(summary)
    print_success(f"Résumé des tests créé: {summary_file}")


def main():
    """Fonction principale."""
    print(f"\n{Colors.BOLD}Formatif F2 - Test Runner Local{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    results = {
        "LED": check_led_scripts(),
        "DHT22": check_dht22_script(),
        "Branches": check_git_branches(),
        "Commits": check_git_commits(),
        "Hardware": check_hardware(),
    }

    # Créer le résumé
    create_test_summary()

    # Afficher le résultat final
    print_header("RÉSULTAT FINAL")

    all_passed = all(results.values())

    for test, passed in results.items():
        if passed:
            print_success(f"{test}: OK")
        else:
            print_error(f"{test}: ÉCHEC")

    print()

    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 TOUS LES TESTS SONT PASSÉS!{Colors.END}")

        # Met à jour .gitignore pour permettre de commettre les marqueurs
        update_gitignore()

        print("\n📤 Vous pouvez maintenant pousser vos modifications:")
        print("   git add .")
        print("   git commit -m \"feat: tests F2 complétés\"")
        print("   git push")

        # Créer le marqueur final de succès
        marker = Path(__file__).parent / ".test_markers" / "all_tests_passed.txt"
        marker.write_text(f"All tests passed: {datetime.now().isoformat()}\n")

        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}⚠️  CERTAINS TESTS ONT ÉCHOUÉ{Colors.END}")
        print("\nCorrigez les erreurs ci-dessus et relancez:")
        print("   python3 run_tests.py")

        return 1


if __name__ == "__main__":
    sys.exit(main())
