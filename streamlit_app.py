import streamlit as st

st.set_page_config(page_title="Camper Share Rechner", layout="centered")

st.title("Camper Share Finanzmodell")

st.subheader("Eingaben")

camper = st.number_input("Anzahl Camper", min_value=1, value=4)
mitglieder = st.number_input("Mitglieder pro Camper", min_value=1, value=30)
preis = st.number_input("Durchschnittlicher Preis pro Mitglied (€)", min_value=0, value=200)

leasing = st.number_input("Leasing pro Camper (€)", min_value=0, value=1100)
versicherung = st.number_input("Versicherung pro Camper (€)", min_value=0, value=250)
wartung = st.number_input("Wartung pro Camper (€)", min_value=0, value=200)
standort = st.number_input("Standort / Infrastruktur (€)", min_value=0, value=200)
software = st.number_input("Software pro Camper (€)", min_value=0, value=150)
variable = st.number_input("Variable Kosten pro Camper (€)", min_value=0, value=400)
plattform = st.number_input("Fixkosten Plattform (€)", min_value=0, value=2000)

st.subheader("Ergebnisse")

umsatz_pro_camper = mitglieder * preis
gesamtumsatz = camper * umsatz_pro_camper

fixkosten_pro_camper = leasing + versicherung + wartung + standort + software
gesamtkosten = camper * (fixkosten_pro_camper + variable) + plattform

gewinn_monat = gesamtumsatz - gesamtkosten
gewinn_jahr = gewinn_monat * 12

break_even = (fixkosten_pro_camper + variable + (plattform / camper)) / preis if preis > 0 else 0

st.metric("Umsatz pro Camper", f"€{umsatz_pro_camper:,.0f}")
st.metric("Gesamtumsatz", f"€{gesamtumsatz:,.0f}")
st.metric("Gesamtkosten / Monat", f"€{gesamtkosten:,.0f}")
st.metric("Gewinn / Monat", f"€{gewinn_monat:,.0f}")
st.metric("Gewinn / Jahr", f"€{gewinn_jahr:,.0f}")
st.metric("Break-even Mitglieder pro Camper", f"{break_even:.1f}")

st.subheader("Zusammenfassung")

st.write(f"Fixkosten pro Camper: €{fixkosten_pro_camper:,.0f}")
st.write(f"Gesamtmitglieder: {camper * mitglieder}")
