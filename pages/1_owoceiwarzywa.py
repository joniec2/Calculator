import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Kalkulator Kalorii", page_icon="🥗")

st.title("🥗 Kalkulator Kalorii")

# Ścieżka do pliku CSV w strukturze Twojego projektu
# Zmień "produkty.csv" na dokładną nazwę Twojego pliku!
NAZWA_PLIKU = "produkty.csv"


# Funkcja wczytująca plik ze sterowaniem cache (dzięki st.cache_data ładuje się błyskawicznie)
@st.cache_data
def naczytaj_dane(sciezka):
    if not os.path.exists(sciezka):
        return None

    # Obsługa błędu ze złym separatorem (np. średnik vs przecinek)
    try:
        # Automatyczne wykrycie separatora i pominięcie ewentualnych uszkodzonych wierszy
        return pd.read_csv(
            sciezka, sep=None, engine="python", on_bad_lines="skip"
        )
    except Exception:
        # Alternatywne wczytanie ze średnikiem (bardzo częste w polskich plikach z Excela)
        return pd.read_csv(sciezka, sep=";", on_bad_lines="skip")


# Automatyczne pobranie danych z pliku
df = naczytaj_dane(NAZWA_PLIKU)

if df is None:
    st.error(
        f"❌ Nie znaleziono pliku `{NAZWA_PLIKU}` w katalogu aplikacji! Upewnij się, że plik znajduje się w tym samym folderze co plik główny `app.py`."
    )
else:
    # Usunięcie zbędnych spacji z nazw kolumn
    df.columns = df.columns.str.strip()

    st.success(f"Wczytano bazę produktów z pliku `{NAZWA_PLIKU}`.")

    # Rozwijany podgląd całej bazy
    with st.expander("👀 Pokaż całą bazę produktów"):
        st.dataframe(df, use_container_width=True)

    st.subheader("🧮 Przelicz kalorie")

    # Wybór odpowiednich kolumn
    col1, col2 = st.columns(2)
    with col1:
        col_nazwa = st.selectbox("Kolumna z nazwą produktu:", df.columns, index=0)
    with col2:
        col_kalorie = st.selectbox(
            "Kolumna z kalorycznością (kcal/100g):",
            df.columns,
            index=min(1, len(df.columns) - 1),
        )

    # Wybór produktu z listy
    produkt_wybrany = st.selectbox(
        "Wybierz produkt:", df[col_nazwa].dropna().unique()
    )

    if produkt_wybrany:
        # Pobranie danych wybranego wiersza
        wiersz = df[df[col_nazwa] == produkt_wybrany].iloc[0]

        try:
            # Konwersja na liczbę (obsługuje też przecinki zamiast kropki)
            wartosc_kcal = str(wiersz[col_kalorie]).replace(",", ".")
            kcal_100g = float(wartosc_kcal)

            # Pobranie wagi od użytkownika
            waga_g = st.number_input(
                "Podaj wagę porcji (w gramach):",
                min_value=1.0,
                value=100.0,
                step=10.0,
            )

            # Kalkulacja
            kalorie_porcja = (kcal_100g * waga_g) / 100.0

            # Wyświetlenie wyniku w czytelnej karcie
            st.metric(
                label=f"Wartość energetyczna ({produkt_wybrany})",
                value=f"{kalorie_porcja:.1f} kcal",
                delta=f"Porcja: {waga_g:.0f}g ({kcal_100g} kcal / 100g)",
                delta_color="off",
            )
        except ValueError:
            st.error(
                f"Wartość kaloryczna dla '{produkt_wybrany}' w kolumnie '{col_kalorie}' nie jest poprawną liczbą."
            )