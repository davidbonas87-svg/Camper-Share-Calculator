import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Camper Share Finanzmodell", layout="wide")

st.title("Camper Share Finanzmodell")
st.caption("Einfache interne Planung und separate Bank-/Investorensicht")

# Feste interne Modellannahme
ZIELUMSATZ_PRO_CAMPER_BEI_100 = 6000

tab_intern, tab_bank = st.tabs(["Interne Planung", "Bank / Investoren"])

with tab_intern:
    st.header("Interne Planung")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Flottenaufbau")

        start_camper = st.number_input("Start-Camper", min_value=1, value=2, step=1)
        ziel_camper = st.number_input("Ziel-Camper", min_value=1, value=4, step=1)
        monat_erweiterung = st.number_input(
            "Monat der Erweiterung auf Ziel-Camper",
            min_value=1,
            max_value=12,
            value=7,
            step=1
        )

        st.subheader("2. Umsatz- und Hochlauf-Logik")

        auslastung_prozent = st.slider(
            "Auslastung pro Camper (%)",
            min_value=0,
            max_value=100,
            value=80,
            step=5
        )

        ramp_up_monate = st.number_input(
            "Ramp-up Monate bis Ziel-Auslastung",
            min_value=1,
            max_value=12,
            value=8,
            step=1
        )

        st.subheader("3. Laufende Kosten pro Camper")

        leasing_pro_camper = st.number_input(
            "Leasing pro Camper (€)",
            min_value=0,
            value=1100,
            step=50
        )

        versicherung_pro_camper = st.number_input(
            "Versicherung pro Camper (€)",
            min_value=0,
            value=250,
            step=10
        )

        wartung_reinigung_pro_camper = st.number_input(
            "Wartung / Reinigung pro Camper (€)",
            min_value=0,
            value=300,
            step=10
        )

        st.subheader("4. Monatliche Fixkosten gesamt")

        plattform_software = st.number_input(
            "Plattform / Software (€)",
            min_value=0,
            value=1800,
            step=50
        )

        marketing = st.number_input(
            "Marketing (€)",
            min_value=0,
            value=1000,
            step=50
        )

        sonstige_fixkosten = st.number_input(
            "Sonstige Fixkosten (€)",
            min_value=0,
            value=500,
            step=50
        )

    with col2:
        st.subheader("5. Einmalkosten")

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

        sonstige_einmalkosten = st.number_input(
            "Sonstige Einmalkosten (€)",
            min_value=0,
            value=0,
            step=500
        )

# Schutzlogik
ziel_camper = max(ziel_camper, start_camper)

# Berechnungen
einmalkosten_gesamt = (
    plattform_entwicklung
    + schluesselbox_hardware
    + branding_recht_website
    + setup_infrastruktur
    + reserve_puffer
    + sonstige_einmalkosten
)

monatliche_kosten_pro_camper = (
    leasing_pro_camper
    + versicherung_pro_camper
    + wartung_reinigung_pro_camper
)

monatliche_fixkosten_gesamt = (
    plattform_software
    + marketing
    + sonstige_fixkosten
)

ziel_auslastung = auslastung_prozent / 100.0
start_auslastung = min(0.20, ziel_auslastung)

def camper_im_monat(monat: int, start: int, ziel: int, erweiterungsmonat: int) -> int:
    if monat < erweiterungsmonat:
        return start
    return ziel

def auslastung_im_monat(monat: int, start_a: float, ziel_a: float, ramp_monate: int) -> float:
    if ramp_monate <= 1:
        return ziel_a
    if monat >= ramp_monate:
        return ziel_a
    steigung = (ziel_a - start_a) / (ramp_monate - 1)
    return start_a + steigung * (monat - 1)

# 12-Monats-Plan
daten_12m = []

for monat in range(1, 13):
    camper_anzahl = camper_im_monat(monat, start_camper, ziel_camper, monat_erweiterung)
    auslastung_monat = auslastung_im_monat(monat, start_auslastung, ziel_auslastung, ramp_up_monate)

    umsatz_pro_camper = ZIELUMSATZ_PRO_CAMPER_BEI_100 * auslastung_monat
    gesamtumsatz = camper_anzahl * umsatz_pro_camper
    gesamtkosten = (camper_anzahl * monatliche_kosten_pro_camper) + monatliche_fixkosten_gesamt
    gewinn = gesamtumsatz - gesamtkosten

    daten_12m.append({
        "Monat": f"M{monat}",
        "Camper": camper_anzahl,
        "Auslastung %": round(auslastung_monat * 100, 1),
        "Umsatz pro Camper": round(umsatz_pro_camper, 0),
        "Gesamtumsatz": round(gesamtumsatz, 0),
        "Gesamtkosten": round(gesamtkosten, 0),
        "Gewinn / Verlust": round(gewinn, 0)
    })

df_12m = pd.DataFrame(daten_12m)

umsatz_jahr_1 = float(df_12m["Gesamtumsatz"].sum())
kosten_jahr_1 = float(df_12m["Gesamtkosten"].sum())
gewinn_jahr_1 = float(df_12m["Gewinn / Verlust"].sum())

effektiver_zielumsatz_pro_camper = ZIELUMSATZ_PRO_CAMPER_BEI_100 * ziel_auslastung
zielumsatz_gesamt_monat = ziel_camper * effektiver_zielumsatz_pro_camper
zielkosten_gesamt_monat = (ziel_camper * monatliche_kosten_pro_camper) + monatliche_fixkosten_gesamt
gewinn_monat_12 = float(df_12m["Gewinn / Verlust"].iloc[-1])

deckungsbeitrag_pro_camper = effektiver_zielumsatz_pro_camper - monatliche_kosten_pro_camper
if deckungsbeitrag_pro_camper > 0:
    break_even_camper = monatliche_fixkosten_gesamt / deckungsbeitrag_pro_camper
else:
    break_even_camper = 0

# 3-Jahres-Plan
umsatz_jahr_2 = zielumsatz_gesamt_monat * 12
kosten_jahr_2 = zielkosten_gesamt_monat * 12
gewinn_jahr_2 = umsatz_jahr_2 - kosten_jahr_2

umsatz_jahr_3 = umsatz_jahr_2 * 1.05
kosten_jahr_3 = kosten_jahr_2 * 1.03
gewinn_jahr_3 = umsatz_jahr_3 - kosten_jahr_3

df_3y = pd.DataFrame({
    "Jahr": ["Jahr 1", "Jahr 2", "Jahr 3"],
    "Camper-Logik": [f"{start_camper} → {ziel_camper}", ziel_camper, ziel_camper],
    "Umsatz": [round(umsatz_jahr_1, 0), round(umsatz_jahr_2, 0), round(umsatz_jahr_3, 0)],
    "Kosten": [round(kosten_jahr_1, 0), round(kosten_jahr_2, 0), round(kosten_jahr_3, 0)],
    "Gewinn": [round(gewinn_jahr_1, 0), round(gewinn_jahr_2, 0), round(gewinn_jahr_3, 0)]
})

with tab_intern:
    st.markdown("---")
    st.subheader("Automatisch berechnete Summen")

    s1, s2, s3 = st.columns(3)
    s1.metric("Monatliche Kosten pro Camper", f"€{monatliche_kosten_pro_camper:,.0f}")
    s2.metric("Monatliche Fixkosten gesamt", f"€{monatliche_fixkosten_gesamt:,.0f}")
    s3.metric("Einmalkosten gesamt", f"€{einmalkosten_gesamt:,.0f}")

    st.subheader("Ergebnisse")

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Einmalkosten gesamt", f"€{einmalkosten_gesamt:,.0f}")
    k2.metric("Zielumsatz / Monat", f"€{zielumsatz_gesamt_monat:,.0f}")
    k3.metric("Gewinn Monat 12", f"€{gewinn_monat_12:,.0f}")
    k4.metric("Gewinn Jahr 1", f"€{gewinn_jahr_1:,.0f}")
    k5.metric("Gewinn Jahr 2", f"€{gewinn_jahr_2:,.0f}")
    k6.metric("Break-even Camper", f"{break_even_camper:.1f}")

    st.subheader("12-Monats-Plan")
    st.dataframe(df_12m, use_container_width=True)

    st.subheader("3-Jahres-Plan")
    st.dataframe(df_3y, use_container_width=True)

with tab_bank:
    st.header("Bank / Investoren")

    b1, b2, b3, b4, b5 = st.columns(5)
    b1.metric("Einmalkosten gesamt", f"€{einmalkosten_gesamt:,.0f}")
    b2.metric("Zielumsatz / Monat", f"€{zielumsatz_gesamt_monat:,.0f}")
    b3.metric("Gewinn Jahr 1", f"€{gewinn_jahr_1:,.0f}")
    b4.metric("Gewinn Jahr 2", f"€{gewinn_jahr_2:,.0f}")
    b5.metric("Break-even Camper", f"{break_even_camper:.1f}")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("12 Monate: Umsatz, Kosten, Gewinn")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.bar(df_12m["Monat"], df_12m["Gesamtumsatz"], label="Umsatz")
        ax1.bar(df_12m["Monat"], df_12m["Gesamtkosten"], alpha=0.7, label="Kosten")
        ax1.plot(df_12m["Monat"], df_12m["Gewinn / Verlust"], marker="o", label="Gewinn / Verlust")
        ax1.set_ylabel("€")
        ax1.legend()
        st.pyplot(fig1)

    with col_chart2:
        st.subheader("3 Jahre: Umsatz, Kosten, Gewinn")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        x = range(len(df_3y))
        ax2.bar([i - 0.25 for i in x], df_3y["Umsatz"], width=0.25, label="Umsatz")
        ax2.bar(x, df_3y["Kosten"], width=0.25, label="Kosten")
        ax2.bar([i + 0.25 for i in x], df_3y["Gewinn"], width=0.25, label="Gewinn")
        ax2.set_xticks(list(x))
        ax2.set_xticklabels(df_3y["Jahr"])
        ax2.set_ylabel("€")
        ax2.legend()
        st.pyplot(fig2)

    st.subheader("12-Monats-Plan")
    st.dataframe(df_12m, use_container_width=True)

    st.subheader("3-Jahres-Plan")
    st.dataframe(df_3y, use_container_width=True)
