import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Camper Share Finanzmodell",
    layout="wide"
)

st.title("Camper Share Finanzmodell")
st.caption("Interaktive Planung für interne Steuerung sowie Bank- und Investorengespräche")

tab1, tab2 = st.tabs(["Interne Planung", "Bank / Investoren"])

# =========================
# GEMEINSAME EINGABEN
# =========================

with tab1:
    st.header("Interne Planung")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Grundannahmen")

        anzahl_camper = st.number_input("Anzahl Camper", min_value=1, value=4, step=1)
        ziel_mitglieder_pro_camper = st.number_input("Ziel-Mitglieder pro Camper", min_value=1, value=30, step=1)
        beitrag_pro_mitglied = st.number_input("Durchschnittlicher Monatsbeitrag pro Mitglied (€)", min_value=0, value=200, step=10)

        st.subheader("2. Mitglieder-Ramp-up")

        start_mitglieder_pro_camper = st.number_input("Start-Mitglieder pro Camper im Monat 1", min_value=0, value=8, step=1)
        ramp_up_monate = st.number_input("Monate bis Ziel-Mitglieder erreicht werden", min_value=1, value=8, step=1)

        st.subheader("3. Einmalkosten")

        plattform_entwicklung = st.number_input("Plattformentwicklung (€)", min_value=0, value=30000, step=1000)
        schluesselbox_hardware = st.number_input("Schlüsselbox Hardware (€)", min_value=0, value=2500, step=100)
        branding_recht_website = st.number_input("Branding / Recht / Website (€)", min_value=0, value=5000, step=500)
        setup_infrastruktur = st.number_input("Standort- / Infrastruktur-Setup (€)", min_value=0, value=5000, step=500)
        reserve_puffer = st.number_input("Reserve / Puffer (€)", min_value=0, value=10000, step=500)

    with col2:
        st.subheader("4. Monatliche Kosten pro Camper")

        leasing = st.number_input("Leasing pro Camper (€)", min_value=0, value=1100, step=50)
        versicherung = st.number_input("Versicherung pro Camper (€)", min_value=0, value=250, step=10)
        wartung = st.number_input("Wartung pro Camper (€)", min_value=0, value=200, step=10)
        standort = st.number_input("Standort / Infrastruktur pro Camper (€)", min_value=0, value=200, step=10)
        software_camper = st.number_input("Software pro Camper (€)", min_value=0, value=150, step=10)
        variable_kosten = st.number_input("Variable Kosten pro Camper (€)", min_value=0, value=400, step=10)

        st.subheader("5. Monatliche Fixkosten gesamt")

        plattform_fixkosten = st.number_input("Plattform-Fixkosten gesamt (€)", min_value=0, value=2000, step=50)
        buchhaltung = st.number_input("Buchhaltung / Steuerberater (€)", min_value=0, value=300, step=50)
        marketing = st.number_input("Marketing gesamt (€)", min_value=0, value=800, step=50)
        sonstige_fixkosten = st.number_input("Sonstige Fixkosten gesamt (€)", min_value=0, value=200, step=50)

        st.subheader("6. Liquidität")

        start_liquiditaet = st.number_input("Verfügbare Startliquidität (€)", min_value=0, value=70000, step=1000)

# =========================
# BERECHNUNGEN
# =========================

einmalkosten_gesamt = (
    plattform_entwicklung
    + schluesselbox_hardware
    + branding_recht_website
    + setup_infrastruktur
    + reserve_puffer
)

fixkosten_pro_camper = (
    leasing
    + versicherung
    + wartung
    + standort
    + software_camper
)

gesamtkosten_pro_camper = fixkosten_pro_camper + variable_kosten

monatliche_fixkosten_gesamt = (
    plattform_fixkosten
    + buchhaltung
    + marketing
    + sonstige_fixkosten
)

def mitglieder_im_monat(monat, start, ziel, ramp_monate):
    if ramp_monate <= 1:
        return ziel
    if monat >= ramp_monate:
        return ziel
    steigung = (ziel - start) / (ramp_monate - 1)
    return round(start + steigung * (monat - 1), 2)

daten = []
liquiditaet = start_liquiditaet - einmalkosten_gesamt

for monat in range(1, 13):
    mitglieder_pc = mitglieder_im_monat(
        monat,
        start_mitglieder_pro_camper,
        ziel_mitglieder_pro_camper,
        ramp_up_monate
    )
    gesamtmitglieder = mitglieder_pc * anzahl_camper
    umsatz_pro_camper = mitglieder_pc * beitrag_pro_mitglied
    gesamtumsatz = umsatz_pro_camper * anzahl_camper
    camperkosten_gesamt = gesamtkosten_pro_camper * anzahl_camper
    gesamtkosten = camperkosten_gesamt + monatliche_fixkosten_gesamt
    gewinn = gesamtumsatz - gesamtkosten
    liquiditaet += gewinn

    daten.append({
        "Monat": f"M{monat}",
        "Mitglieder_pro_Camper": mitglieder_pc,
        "Gesamtmitglieder": gesamtmitglieder,
        "Umsatz": gesamtumsatz,
        "Kosten": gesamtkosten,
        "Gewinn": gewinn,
        "Liquidität": liquiditaet
    })

df_12m = pd.DataFrame(daten)

umsatz_jahr_1 = df_12m["Umsatz"].sum()
kosten_jahr_1 = df_12m["Kosten"].sum()
gewinn_jahr_1 = df_12m["Gewinn"].sum()

# Vereinfachte 3-Jahres-Planung:
# Jahr 1 = Ramp-up
# Jahr 2 = volles Zielniveau
# Jahr 3 = Jahr 2 + 5% Umsatzwachstum, 3% Kostenwachstum

voller_monatsumsatz = anzahl_camper * ziel_mitglieder_pro_camper * beitrag_pro_mitglied
volle_monatskosten = (anzahl_camper * gesamtkosten_pro_camper) + monatliche_fixkosten_gesamt

umsatz_jahr_2 = voller_monatsumsatz * 12
kosten_jahr_2 = volle_monatskosten * 12
gewinn_jahr_2 = umsatz_jahr_2 - kosten_jahr_2

umsatz_jahr_3 = umsatz_jahr_2 * 1.05
kosten_jahr_3 = kosten_jahr_2 * 1.03
gewinn_jahr_3 = umsatz_jahr_3 - kosten_jahr_3

df_3y = pd.DataFrame({
    "Jahr": ["Jahr 1", "Jahr 2", "Jahr 3"],
    "Umsatz": [umsatz_jahr_1, umsatz_jahr_2, umsatz_jahr_3],
    "Kosten": [kosten_jahr_1, kosten_jahr_2, kosten_jahr_3],
    "Gewinn": [gewinn_jahr_1, gewinn_jahr_2, gewinn_jahr_3]
})

break_even_mitglieder = (
    gesamtkosten_pro_camper + (monatliche_fixkosten_gesamt / anzahl_camper)
) / beitrag_pro_mitglied if beitrag_pro_mitglied > 0 else 0

# Szenariovergleich
szenarien = {
    "Worst Case": 15,
    "Realistisch": 25,
    "Best Case": 30
}

szenario_daten = []
for name, mitglieder_szenario in szenarien.items():
    umsatz = anzahl_camper * mitglieder_szenario * beitrag_pro_mitglied
    kosten = (anzahl_camper * gesamtkosten_pro_camper) + monatliche_fixkosten_gesamt
    gewinn = umsatz - kosten
    szenario_daten.append({
        "Szenario": name,
        "Umsatz": umsatz,
        "Kosten": kosten,
        "Gewinn": gewinn
    })

df_szenario = pd.DataFrame(szenario_daten)

# =========================
# TAB 1 - INTERNE SICHT
# =========================

with tab1:
    st.subheader("Ergebnisse interne Planung")

    c1, c2, c3 = st.columns(3)
    c1.metric("Kapitalbedarf Start", f"€{einmalkosten_gesamt:,.0f}")
    c2.metric("Break-even Mitglieder / Camper", f"{break_even_mitglieder:.1f}")
    c3.metric("Liquidität Ende Jahr 1", f"€{df_12m['Liquidität'].iloc[-1]:,.0f}")

    st.markdown("---")

    c4, c5, c6 = st.columns(3)
    c4.metric("Umsatz Jahr 1", f"€{umsatz_jahr_1:,.0f}")
    c5.metric("Kosten Jahr 1", f"€{kosten_jahr_1:,.0f}")
    c6.metric("Gewinn Jahr 1", f"€{gewinn_jahr_1:,.0f}")

    st.subheader("12-Monats-Verlauf")
    st.dataframe(df_12m, use_container_width=True)

    st.subheader("3-Jahres-Plan")
    st.dataframe(df_3y, use_container_width=True)

# =========================
# TAB 2 - BANK / INVESTOREN
# =========================

with tab2:
    st.header("Bank- / Investorensicht")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Kapitalbedarf Start", f"€{einmalkosten_gesamt:,.0f}")
    k2.metric("Break-even Mitglieder", f"{break_even_mitglieder:.1f}")
    k3.metric("Gewinn Jahr 1", f"€{gewinn_jahr_1:,.0f}")
    k4.metric("Liquidität Ende Jahr 1", f"€{df_12m['Liquidität'].iloc[-1]:,.0f}")

    st.markdown("---")

    # Chart 1: Umsatz / Kosten / Gewinn pro Monat
    st.subheader("Monatlicher Verlauf: Umsatz, Kosten und Gewinn")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.bar(df_12m["Monat"], df_12m["Umsatz"], label="Umsatz")
    ax1.bar(df_12m["Monat"], df_12m["Kosten"], alpha=0.7, label="Kosten")
    ax1.plot(df_12m["Monat"], df_12m["Gewinn"], marker="o", label="Gewinn")
    ax1.set_ylabel("€")
    ax1.legend()
    st.pyplot(fig1)

    # Chart 2: Liquiditätsverlauf
    st.subheader("Liquiditätsverlauf über 12 Monate")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(df_12m["Monat"], df_12m["Liquidität"], marker="o")
    ax2.axhline(0, linestyle="--")
    ax2.set_ylabel("€")
    st.pyplot(fig2)

    # Chart 3: 3-Jahres-Plan
    st.subheader("3-Jahres-Plan: Umsatz, Kosten und Gewinn")
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    x = range(len(df_3y))
    ax3.bar([i - 0.25 for i in x], df_3y["Umsatz"], width=0.25, label="Umsatz")
    ax3.bar(x, df_3y["Kosten"], width=0.25, label="Kosten")
    ax3.bar([i + 0.25 for i in x], df_3y["Gewinn"], width=0.25, label="Gewinn")
    ax3.set_xticks(list(x))
    ax3.set_xticklabels(df_3y["Jahr"])
    ax3.set_ylabel("€")
    ax3.legend()
    st.pyplot(fig3)

    # Chart 4: Kostenstruktur
    st.subheader("Monatliche Kostenstruktur")
    kosten_labels = [
        "Leasing",
        "Versicherung",
        "Wartung",
        "Standort",
        "Software Camper",
        "Variable Kosten",
        "Plattform Fixkosten",
        "Buchhaltung",
        "Marketing",
        "Sonstige"
    ]
    kosten_werte = [
        leasing * anzahl_camper,
        versicherung * anzahl_camper,
        wartung * anzahl_camper,
        standort * anzahl_camper,
        software_camper * anzahl_camper,
        variable_kosten * anzahl_camper,
        plattform_fixkosten,
        buchhaltung,
        marketing,
        sonstige_fixkosten
    ]

    fig4, ax4 = plt.subplots(figsize=(7, 7))
    ax4.pie(kosten_werte, labels=kosten_labels, autopct="%1.1f%%", startangle=90)
    ax4.axis("equal")
    st.pyplot(fig4)

    # Chart 5: Szenariovergleich
    st.subheader("Szenariovergleich")
    fig5, ax5 = plt.subplots(figsize=(10, 4))
    ax5.bar(df_szenario["Szenario"], df_szenario["Gewinn"])
    ax5.axhline(0, linestyle="--")
    ax5.set_ylabel("Gewinn / Monat (€)")
    st.pyplot(fig5)

    st.subheader("Kurze Bewertung")
    if gewinn_jahr_1 > 0 and df_12m["Liquidität"].min() > 0:
        st.success(
            "Das Modell ist unter den aktuellen Annahmen bankfähig darstellbar: "
            "positiver Ergebnisverlauf, positiver Liquiditätsverlauf und klarer Break-even."
        )
    elif gewinn_jahr_1 > 0:
        st.warning(
            "Das Modell ist operativ profitabel, zeigt jedoch temporäre Liquiditätsrisiken. "
            "Für das Bankgespräch sollte die Anfangsfinanzierung oder Liquiditätsreserve erhöht werden."
        )
    else:
        st.error(
            "Das Modell ist unter den aktuellen Annahmen noch nicht überzeugend. "
            "Vor einem Bankgespräch sollten Preis, Mitgliederaufbau oder Kostenstruktur nachgeschärft werden."
        )
