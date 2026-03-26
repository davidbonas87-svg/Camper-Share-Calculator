import streamlit as st

st.set_page_config(page_title="Camper Share Rechner", layout="wide")

st.title("Camper Share Finanzmodell")

# Layout
col_input, col_output = st.columns([1, 1])

# INPUTS (links)
with col_input:
    st.subheader("Eingaben")

    camper = st.number_input("Anzahl Camper", value=4)
    mitglieder = st.number_input("Mitglieder pro Camper", value=30)
    preis = st.number_input("Preis pro Mitglied (€)", value=200)

    leasing = st.number_input("Leasing (€)", value=1100)
    versicherung = st.number_input("Versicherung (€)", value=250)
    wartung = st.number_input("Wartung (€)", value=200)
    standort = st.number_input("Standort (€)", value=200)
    software = st.number_input("Software (€)", value=150)
    variable = st.number_input("Variable Kosten (€)", value=400)

    plattform = st.number_input("Plattform Fixkosten (€)", value=2000)

# BERECHNUNG
umsatz_pro_camper = mitglieder * preis
gesamtumsatz = camper * umsatz_pro_camper

fixkosten = leasing + versicherung + wartung + standort + software
gesamtkosten = camper * (fixkosten + variable) + plattform

gewinn = gesamtumsatz - gesamtkosten
break_even = (fixkosten + variable + (plattform / camper)) / preis

# OUTPUT (rechts)
with col_output:
    st.subheader("Ergebnis")

    st.metric("Monatlicher Gewinn", f"€{gewinn:,.0f}")
    st.metric("Gesamtumsatz", f"€{gesamtumsatz:,.0f}")
    st.metric("Gesamtkosten", f"€{gesamtkosten:,.0f}")
    st.metric("Break-even Mitglieder", f"{break_even:.1f}")

    # einfache Ampel
    if gewinn > 0:
        st.success("Profitabel")
    else:
        st.error("Nicht profitabel")
