import streamlit as st

st.set_page_config(
    page_title="Camper Share Finanzmodell",
    layout="wide"
)

st.title("Camper Share Finanzmodell")
st.caption("Interaktiver Rechner für Kapitalbedarf, Umsatz, Kosten, Gewinn und Break-even")

# Standardwerte
standard_camper = 4
standard_mitglieder = 30
standard_preis = 200

# Layout
col_links, col_rechts = st.columns([1, 1])

with col_links:
    st.subheader("1. Grundannahmen")

    anzahl_camper = st.number_input(
        "Anzahl Camper",
        min_value=1,
        value=standard_camper,
        step=1
    )

    mitglieder_pro_camper = st.number_input(
        "Mitglieder pro Camper",
        min_value=1,
        value=standard_mitglieder,
        step=1
    )

    preis_pro_mitglied = st.number_input(
        "Durchschnittlicher Monatsbeitrag pro Mitglied (€)",
        min_value=0,
        value=standard_preis,
        step=10
    )

    st.subheader("2. Einmalkosten")

    plattform_entwicklung = st.number_input(
        "Plattformentwicklung (€)",
        min_value=0,
        value=30000,
        step=1000
    )

    schluesselbox_hardware = st.number_input(
        "Schlüsselbox Hardware (€)",
        min_value=0,
        value=2500,
        step=100
    )

    branding_recht_website = st.number_input(
        "Branding / Recht / Website (€)",
        min_value=0,
        value=5000,
        step=500
    )

    setup_infrastruktur = st.number_input(
        "Standort- / Infrastruktur-Setup (€)",
        min_value=0,
        value=5000,
        step=500
    )

    reserve_puffer = st.number_input(
        "Reserve / Puffer (€)",
        min_value=0,
        value=10000,
        step=500
    )

    st.subheader("3. Monatliche Kosten pro Camper")

    leasing = st.number_input(
        "Leasing pro Camper (€)",
        min_value=0,
        value=1100,
        step=50
    )

    versicherung = st.number_input(
        "Versicherung pro Camper (€)",
        min_value=0,
        value=250,
        step=10
    )

    wartung = st.number_input(
        "Wartung pro Camper (€)",
        min_value=0,
        value=200,
        step=10
    )

    standort = st.number_input(
        "Standort / Infrastruktur pro Camper (€)",
        min_value=0,
        value=200,
        step=10
    )

    software_camper = st.number_input(
        "Software pro Camper (€)",
        min_value=0,
        value=150,
        step=10
    )

    variable_kosten = st.number_input(
        "Variable Kosten pro Camper (€)",
        min_value=0,
        value=400,
        step=10
    )

    st.subheader("4. Monatliche Fixkosten gesamt")

    plattform_fixkosten = st.number_input(
        "Plattform-Fixkosten gesamt (€)",
        min_value=0,
        value=2000,
        step=50
    )

    buchhaltung = st.number_input(
        "Buchhaltung / Steuerberater (€)",
        min_value=0,
        value=300,
        step=50
    )

    marketing = st.number_input(
        "Marketing gesamt (€)",
        min_value=0,
        value=800,
        step=50
    )

    sonstige_fixkosten = st.number_input(
        "Sonstige Fixkosten gesamt (€)",
        min_value=0,
        value=200,
        step=50
    )

# Berechnungen
einmalkosten_gesamt = (
    plattform_entwicklung
    + schluesselbox_hardware
    + branding_recht_website
    + setup_infrastruktur
    + reserve_puffer
)

umsatz_pro_camper = mitglieder_pro_camper * preis_pro_mitglied
gesamtumsatz_monat = anzahl_camper * umsatz_pro_camper
gesamtumsatz_jahr = gesamtumsatz_monat * 12

fixkosten_pro_camper = (
    leasing
    + versicherung
    + wartung
    + standort
    + software_camper
)

gesamtkosten_pro_camper = fixkosten_pro_camper + variable_kosten
monatliche_camperkosten_gesamt = anzahl_camper * gesamtkosten_pro_camper

monatliche_fixkosten_gesamt = (
    plattform_fixkosten
    + buchhaltung
    + marketing
    + sonstige_fixkosten
)

gesamtkosten_monat = monatliche_camperkosten_gesamt + monatliche_fixkosten_gesamt
gesamtkosten_jahr = gesamtkosten_monat * 12

gewinn_monat = gesamtumsatz_monat - gesamtkosten_monat
gewinn_jahr = gewinn_monat * 12

gesamtmitglieder = anzahl_camper * mitglieder_pro_camper

if preis_pro_mitglied > 0:
    break_even_mitglieder = (
        gesamtkosten_pro_camper + (monatliche_fixkosten_gesamt / anzahl_camper)
    ) / preis_pro_mitglied
else:
    break_even_mitglieder = 0

# Status
if gewinn_monat > 0:
    status_text = "Profitabel"
    status_typ = "success"
elif gewinn_monat == 0:
    status_text = "Break-even"
    status_typ = "warning"
else:
    status_text = "Nicht profitabel"
    status_typ = "error"

with col_rechts:
    st.subheader("5. Schlüsselkennzahlen")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Kapitalbedarf Start", f"€{einmalkosten_gesamt:,.0f}")
        st.metric("Gesamtumsatz / Monat", f"€{gesamtumsatz_monat:,.0f}")
        st.metric("Gesamtkosten / Monat", f"€{gesamtkosten_monat:,.0f}")

    with col2:
        st.metric("Gewinn / Monat", f"€{gewinn_monat:,.0f}")
        st.metric("Gewinn / Jahr", f"€{gewinn_jahr:,.0f}")
        st.metric("Break-even Mitglieder / Camper", f"{break_even_mitglieder:.1f}")

    st.subheader("6. Kostenstruktur")

    st.write(f"Einmalkosten gesamt: €{einmalkosten_gesamt:,.0f}")
    st.write(f"Fixkosten pro Camper / Monat: €{fixkosten_pro_camper:,.0f}")
    st.write(f"Gesamtkosten pro Camper / Monat: €{gesamtkosten_pro_camper:,.0f}")
    st.write(f"Monatliche Camperkosten gesamt: €{monatliche_camperkosten_gesamt:,.0f}")
    st.write(f"Monatliche Fixkosten gesamt: €{monatliche_fixkosten_gesamt:,.0f}")

    st.subheader("7. Überblick")

    st.write(f"Anzahl Camper: {anzahl_camper}")
    st.write(f"Mitglieder pro Camper: {mitglieder_pro_camper}")
    st.write(f"Gesamtmitglieder: {gesamtmitglieder}")
    st.write(f"Umsatz pro Camper / Monat: €{umsatz_pro_camper:,.0f}")
    st.write(f"Gesamtumsatz / Jahr: €{gesamtumsatz_jahr:,.0f}")
    st.write(f"Gesamtkosten / Jahr: €{gesamtkosten_jahr:,.0f}")

    st.subheader("8. Bewertung")

    if status_typ == "success":
        st.success(
            f"Status: {status_text}. "
            "Das Modell ist mit den aktuellen Annahmen profitabel."
        )
    elif status_typ == "warning":
        st.warning(
            f"Status: {status_text}. "
            "Das Modell liegt genau an der Schwelle."
        )
    else:
        st.error(
            f"Status: {status_text}. "
            "Mit den aktuellen Annahmen ist das Modell nicht tragfähig."
        )

st.markdown("---")
st.caption("Hinweis: Für ein Bankgespräch als Nächstes noch Liquiditätsverlauf, Mitglieder-Ramp-up und 3-Jahres-Plan ergänzen.")
