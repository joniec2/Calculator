#!/usr/bin/env python3
"""
Prosty kalkulator kalorii.
Podajesz wartość na 100g, a program oblicza dla dowolnej ilości gramów.
"""
import sys


def calc(cal_per_100g, grams):
    """Zwraca kalorie dla podanej ilości gramów."""
    return cal_per_100g * grams / 100.0


def main():
    try:
        cal = float(input("Podaj kcal na 100g: ").strip().replace(',', '.'))
        grams = float(input("Podaj ile gramów potrzebujesz: ").strip().replace(',', '.'))
        # Pobierz zawartość makroskładników na 100g
        protein_per_100 = float(input("Podaj białko na 100g (g): ").strip().replace(',', '.'))
        carbs_per_100 = float(input("Podaj węglowodany na 100g (g): ").strip().replace(',', '.'))
        fat_per_100 = float(input("Podaj tłuszcz na 100g (g): ").strip().replace(',', '.'))
    except (ValueError, EOFError):
        print("Błędne dane wejściowe.")
        sys.exit(1)
    # Obliczenia
    result = calc(cal, grams)
    # ilości makr w porcji
    protein = protein_per_100 * grams / 100.0
    carbs = carbs_per_100 * grams / 100.0
    fat = fat_per_100 * grams / 100.0
    # kalorie z makr
    kcal_from_protein = protein * 4.0
    kcal_from_carbs = carbs * 4.0
    kcal_from_fat = fat * 9.0
    kcal_macros_total = kcal_from_protein + kcal_from_carbs + kcal_from_fat

    print(f"Dla {grams:.2f} g: {result:.2f} kcal")
    print("Makroskładniki:")
    print(f"  Białko: {protein:.2f} g -> {kcal_from_protein:.2f} kcal")
    print(f"  Węglowodany: {carbs:.2f} g -> {kcal_from_carbs:.2f} kcal")
    print(f"  Tłuszcz: {fat:.2f} g -> {kcal_from_fat:.2f} kcal")
    print(f"  Razem z makr: {kcal_macros_total:.2f} kcal")
    # jeżeli suma kcal z makr różni się od deklarowanej energii, poinformuj
    diff = result - kcal_macros_total
    if abs(diff) > 1.0:
        print(f"Uwaga: różnica między podanymi kcal a sumą kcal z makr: {diff:.2f} kcal")


if __name__ == '__main__':
    main()
