import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Camper Share Finanzmodell",
    layout="wide"
)

# ---------------------------------------------------
# Styling
# ---------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1500px;
}
.section-card {
    background-color: #f8f9fb;
    padding: 18px 18px 8px 18px;
    border-radius: 12px;
    border: 1px solid #e6e8ee;
    margin-bottom: 18px;
}
.kpi-card {
    background-color: #ffffff;
    padding: 14px 16px;
    border-radius: 12px;
    border: 1px solid #e6e8ee;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.kpi-title {
    font-size: 0.9rem;
    color: #6b7280;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #111827;
}
.small-note {
    font-size: 0.85rem;
    color: #6b7280;
}
</style>
""", unsafe_allow_html=True)

st.title("Camper Share Finanzmodell")
st.caption("Einfache interne Planung mit separater Bank- / Investorensicht")

# ---------------------------------------------------
# Feste Modellannahme
# ---------------------------------------------------
ZIELUMSATZ_PRO_CAMPER_BEI_100 = 6000

# ---------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------
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

def euro(value: float) -> str:
    return f"€{value:,.0f}"

def kpi_card(title: str, value: str):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# Tabs
# ---------------------------------------------------
tab_intern, tab_bank = st.tabs(["Interne Planung", "Bank / Investoren"])

# ---------------------------------------------------
# Eingaben nur intern
# ---------------------------------------------------
with tab_intern:
    st.subheader("Eingaben")

    input_left, input_right = st.columns(2)

    with input_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 1. Flottenaufbau")

        start_camper = st.number_input("Start-Camper", min_value=1, value=2, step=1)
        ziel_camper = st.number_input("Ziel-Camper", min_value=1, value=4, step=1)
        monat_erweiterung = st.number_input(
            "Monat der Erweiterung auf Ziel-Camper",
            min_value=1,
            max_value=12,
            value=7,
            step=1
        )

        st.markdown("### 2. Umsatz- und Hochlauf-Logik")

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
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 3. Laufende Kosten pro Camper")

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
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 4. Monatliche Fixkosten gesamt")

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
        st.markdown('</div>', unsafe_allow_html=True)

    with input_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 5. Einmalkosten")

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
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# Gemeinsame Logik
# ---------------------------------------------------
ziel_camper = max(ziel_camper, start_camper)

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

# ---------------------------------------------------
# Interne Ergebnisse
# ---------------------------------------------------
with tab_intern:
    st.markdown("---")
    st.subheader("Automatisch berechnete Summen")

    sum1, sum2, sum3 = st.columns(3)
    with sum1:
        kpi_card("Monatliche Kosten pro Camper", euro(monatliche_kosten_pro_camper))
    with sum2:
        kpi_card("Monatliche Fixkosten gesamt", euro(monatliche_fixkosten_gesamt))
    with sum3:
        kpi_card("Einmalkosten gesamt", euro(einmalkosten_gesamt))

    st.markdown("---")
    st.subheader("Schlüsselkennzahlen")

    row1 = st.columns(3)
    row2 = st.columns(3)

    with row1[0]:
        kpi_card("Zielumsatz / Monat", euro(zielumsatz_gesamt_monat))
    with row1[1]:
        kpi_card("Gewinn Monat 12", euro(gewinn_monat_12))
    with row1[2]:
        kpi_card("Gewinn Jahr 1", euro(gewinn_jahr_1))

    with row2[0]:
        kpi_card("Gewinn Jahr 2", euro(gewinn_jahr_2))
    with row2[1]:
        kpi_card("Gewinn Jahr 3", euro(gewinn_jahr_3))
    with row2[2]:
        kpi_card("Break-even Camper", f"{break_even_camper:.1f}")

    st.markdown("---")

    charts_left, charts_right = st.columns(2)

    with charts_left:
        st.subheader("12 Monate: Umsatz, Kosten, Gewinn")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.bar(df_12m["Monat"], df_12m["Gesamtumsatz"], label="Umsatz")
        ax1.bar(df_12m["Monat"], df_12m["Gesamtkosten"], alpha=0.7, label="Kosten")
        ax1.plot(df_12m["Monat"], df_12m["Gewinn / Verlust"], marker="o", label="Gewinn / Verlust")
        ax1.set_ylabel("€")
        ax1.legend()
        st.pyplot(fig1, use_container_width=True)

    with charts_right:
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
        st.pyplot(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("12-Monats-Plan")
    st.dataframe(df_12m, use_container_width=True, hide_index=True)

    st.subheader("3-Jahres-Plan")
    st.dataframe(df_3y, use_container_width=True, hide_index=True)

# ---------------------------------------------------
# Bankseite
# ---------------------------------------------------
with tab_bank:
    st.header("Bank / Investoren")

    bank_row1 = st.columns(4)
    bank_row2 = st.columns(2)

    with bank_row1[0]:
        kpi_card("Einmalkosten gesamt", euro(einmalkosten_gesamt))
    with bank_row1[1]:
        kpi_card("Zielumsatz / Monat", euro(zielumsatz_gesamt_monat))
    with bank_row1[2]:
        kpi_card("Gewinn Jahr 1", euro(gewinn_jahr_1))
    with bank_row1[3]:
        kpi_card("Break-even Camper", f"{break_even_camper:.1f}")

    with bank_row2[0]:
        kpi_card("Gewinn Jahr 2", euro(gewinn_jahr_2))
    with bank_row2[1]:
        kpi_card("Gewinn Jahr 3", euro(gewinn_jahr_3))

    st.markdown("---")

    bank_chart1, bank_chart2 = st.columns(2)

    with bank_chart1:
        st.subheader("12 Monate: Umsatz, Kosten, Gewinn")
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        ax3.bar(df_12m["Monat"], df_12m["Gesamtumsatz"], label="Umsatz")
        ax3.bar(df_12m["Monat"], df_12m["Gesamtkosten"], alpha=0.7, label="Kosten")
        ax3.plot(df_12m["Monat"], df_12m["Gewinn / Verlust"], marker="o", label="Gewinn / Verlust")
        ax3.set_ylabel("€")
        ax3.legend()
        st.pyplot(fig3, use_container_width=True)

    with bank_chart2:
        st.subheader("3 Jahre: Umsatz, Kosten, Gewinn")
        fig4, ax4 = plt.subplots(figsize=(10, 4))
        x = range(len(df_3y))
        ax4.bar([i - 0.25 for i in x], df_3y["Umsatz"], width=0.25, label="Umsatz")
        ax4.bar(x, df_3y["Kosten"], width=0.25, label="Kosten")
        ax4.bar([i + 0.25 for i in x], df_3y["Gewinn"], width=0.25, label="Gewinn")
        ax4.set_xticks(list(x))
        ax4.set_xticklabels(df_3y["Jahr"])
        ax4.set_ylabel("€")
        ax4.legend()
        st.pyplot(fig4, use_container_width=True)

    st.markdown("---")
    st.subheader("12-Monats-Plan")
    st.dataframe(df_12m, use_container_width=True, hide_index=True)

    st.subheader("3-Jahres-Plan")
    st.dataframe(df_3y, use_container_width=True, hide_index=True)
