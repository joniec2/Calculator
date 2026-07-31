import streamlit as st

# Tytuł aplikacji
st.title("🥗 Kalkulator Kalorii i Makro")

# Sekcja danych wejściowych (suwaki lub pola do wpisywania)
col1, col2 = st.columns(2)

with col1:
    cal_100 = st.number_input("Kcal na 100g", min_value=0.0, value=300.0, step=10.0)
    protein_100 = st.number_input("Białko na 100g (g)", min_value=0.0, value=20.0, step=1.0)

with col2:
    grams = st.number_input("Waga porcji (g)", min_value=0.0, value=150.0, step=10.0)
    carbs_100 = st.number_input("Węglowodany na 100g (g)", min_value=0.0, value=30.0, step=1.0)
    fat_100 = st.number_input("Tłuszcz na 100g (g)", min_value=0.0, value=10.0, step=1.0)

# Obliczenia
if grams > 0:
    factor = grams / 100.0
    total_kcal = cal_100 * factor
    protein = protein_100 * factor
    carbs = carbs_100 * factor
    fat = fat_100 * factor
    
    st.divider()
    st.subheader(f"Wynik dla {grams:.0f}g porcji:")
    
    # Wyświetlenie wyników w zgrabnych kafelkach (metrics)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Kalorie", f"{total_kcal:.1f} kcal")
    m2.metric("Białko", f"{protein:.1f} g")
    m3.metric("Węglowodany", f"{carbs:.1f} g")
    m4.metric("Tłuszcz", f"{fat:.1f} g")