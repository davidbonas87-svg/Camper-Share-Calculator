import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Camper Share Finanzmodell",
    layout="wide"
)

st.title("Camper Share Finanzmodell")
st.caption("Interne Planung und separate Bank-/Investorensicht mit gemeinsamer Berechnungslogik")

# =========================================================
# TABS
# =========================================================
tab_intern, tab_bank = st.tabs(["Interne Planung", "Bank / Investoren"])

# =========================================================
# INTERNE EINGABEN
# NUR HIER EDITIERBAR
# =========================================================
with tab_intern:
    st.header("Interne Planung")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Flottenaufbau")

        start_camper = st.number_input(
            "Start-Camper",
            min_value=1,
            value=2,
            step=1
        )

        ziel_camper = st.number_input(
            "Ziel-Camper",
            min_value=1,
            value=4,
            step=1
        )

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

        start_liquiditaet = st.number_input(
            "Startliquidität (€)",
            min_value=0,
            value=70000,
            step=1000
        )

        st.subheader("3. Laufende Kosten")

        monatliche_kosten_pro_camper = st.number_input(
            "Monatliche Kosten pro Camper (€)",
            min_value=0,
            value=2200,
            step=50
        )

        monatliche_fixkosten_gesamt = st.number_input(
            "Monatliche Fixkosten gesamt (€)",
            min_value=0,
            value=3300,
            step=50
        )

    with col2:
        st.subheader("4. Einmalkosten")

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

# =========================================================
# GEMEINSAME LOGIK FÜR BEIDE TABS
# ALLES AB HIER WIRD EINMAL BERECHNET
# =========================================================

# Schutzlogik
ziel_camper = max(ziel_camper, start_camper)

# Feste interne Modellannahmen
MAX_MITGLIEDER_PRO_CAMPER = 30
PREIS_PRO_MITGLIED = 200
START_AUSLASTUNG_BASIS = 0.20
UMSATZWACHSTUM_JAHR_3 = 0.05
KOSTENWACHSTUM_JAHR_3 = 0.03

# Einmalkosten
einmalkosten_gesamt = (
    plattform_entwicklung
    + schluesselbox_hardware
    + branding_recht_website
    + setup_infrastruktur
    + reserve_puffer
    + sonstige_einmalkosten
)

# Abgeleitete Umsatzlogik
ziel_auslastung = auslastung_prozent / 100.0
start_auslastung = min(START_AUSLASTUNG_BASIS, ziel_auslastung)

zielumsatz_pro_camper = MAX_MITGLIEDER_PRO_CAMPER * PREIS_PRO_MITGLIED
effektiver_zielumsatz_pro_camper = zielumsatz_pro_camper * ziel_auslastung

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
liquiditaet = start_liquiditaet - einmalkosten_gesamt

for monat in range(1, 13):
    camper_anzahl = camper_im_monat(monat, start_camper, ziel_camper, monat_erweiterung)
    auslastung_monat = auslastung_im_monat(monat, start_auslastung, ziel_auslastung, ramp_up_monate)

    mitglieder_pro_camper_monat = MAX_MITGLIEDER_PRO_CAMPER * auslastung_monat
    umsatz_pro_camper_monat = zielumsatz_pro_camper * auslastung_monat
    gesamtumsatz_monat = camper_anzahl * umsatz_pro_camper_monat

    gesamtkosten_monat = (
        camper_anzahl * monatliche_kosten_pro_camper
        + monatliche_fixkosten_gesamt
    )

    gewinn_monat = gesamtumsatz_monat - gesamtkosten_monat
    liquiditaet += gewinn_monat

    daten_12m.append({
        "Monat": f"M{monat}",
        "Camper": camper_anzahl,
        "Auslastung %": round(auslastung_monat * 100, 1),
        "Mitglieder pro Camper": round(mitglieder_pro_camper_monat, 1),
        "Umsatz pro Camper": round(umsatz_pro_camper_monat, 0),
        "Gesamtumsatz": round(gesamtumsatz_monat, 0),
        "Gesamtkosten": round(gesamtkosten_monat, 0),
        "Gewinn / Verlust": round(gewinn_monat, 0),
        "Liquidität": round(liquiditaet, 0)
    })

df_12m = pd.DataFrame(daten_12m)

umsatz_jahr_1 = float(df_12m["Gesamtumsatz"].sum())
kosten_jahr_1 = float(df_12m["Gesamtkosten"].sum())
gewinn_jahr_1 = float(df_12m["Gewinn / Verlust"].sum())

min_liquiditaet = float(df_12m["Liquidität"].min())
liquiditaet_ende_jahr_1 = float(df_12m["Liquidität"].iloc[-1])
funding_gap = abs(min_liquiditaet) if min_liquiditaet < 0 else 0

# Break-even Logik
deckungsbeitrag_pro_camper = effektiver_zielumsatz_pro_camper - monatliche_kosten_pro_camper
if deckungsbeitrag_pro_camper > 0:
    break_even_camper = monatliche_fixkosten_gesamt / deckungsbeitrag_pro_camper
else:
    break_even_camper = 0

# 3-Jahres-Plan
voller_monatsumsatz_j2 = ziel_camper * effektiver_zielumsatz_pro_camper
volle_monatskosten_j2 = ziel_camper * monatliche_kosten_pro_camper + monatliche_fixkosten_gesamt

umsatz_jahr_2 = voller_monatsumsatz_j2 * 12
kosten_jahr_2 = volle_monatskosten_j2 * 12
gewinn_jahr_2 = umsatz_jahr_2 - kosten_jahr_2

umsatz_jahr_3 = umsatz_jahr_2 * (1 + UMSATZWACHSTUM_JAHR_3)
kosten_jahr_3 = kosten_jahr_2 * (1 + KOSTENWACHSTUM_JAHR_3)
gewinn_jahr_3 = umsatz_jahr_3 - kosten_jahr_3

liquiditaet_ende_jahr_2 = liquiditaet_ende_jahr_1 + gewinn_jahr_2
liquiditaet_ende_jahr_3 = liquiditaet_ende_jahr_2 + gewinn_jahr_3

df_3y = pd.DataFrame({
    "Jahr": ["Jahr 1", "Jahr 2", "Jahr 3"],
    "Camper-Logik": [
        f"{start_camper} → {ziel_camper}",
        ziel_camper,
        ziel_camper
    ],
    "Umsatz": [round(umsatz_jahr_1, 0), round(umsatz_jahr_2, 0), round(umsatz_jahr_3, 0)],
    "Kosten": [round(kosten_jahr_1, 0), round(kosten_jahr_2, 0), round(kosten_jahr_3, 0)],
    "Gewinn": [round(gewinn_jahr_1, 0), round(gewinn_jahr_2, 0), round(gewinn_jahr_3, 0)],
    "Liquidität Jahresende": [
        round(liquiditaet_ende_jahr_1, 0),
        round(liquiditaet_ende_jahr_2, 0),
        round(liquiditaet_ende_jahr_3, 0)
    ]
})

# =========================================================
# TAB 1: INTERNE PLANUNG
# =========================================================
with tab_intern:
    st.markdown("---")
    st.subheader("Ergebnisse interne Planung")

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Einmalkosten gesamt", f"€{einmalkosten_gesamt:,.0f}")
    k2.metric("Funding Gap", f"€{funding_gap:,.0f}")
    k3.metric("Mindestliquidität", f"€{min_liquiditaet:,.0f}")
    k4.metric("Gewinn Jahr 1", f"€{gewinn_jahr_1:,.0f}")
    k5.metric("Break-even Camper", f"{break_even_camper:.1f}")

    k6, k7, k8, k9 = st.columns(4)
    k6.metric("Zielumsatz pro Camper", f"€{zielumsatz_pro_camper:,.0f}")
    k7.metric("Effektiver Umsatz pro Camper", f"€{effektiver_zielumsatz_pro_camper:,.0f}")
    k8.metric("Mitglieder / Camper bei Ziel", f"{MAX_MITGLIEDER_PRO_CAMPER * ziel_auslastung:.1f}")
    k9.metric("Liquidität Ende Jahr 1", f"€{liquiditaet_ende_jahr_1:,.0f}")

    if funding_gap > 0:
        st.error(
            f"Die Liquidität fällt unter 0 €. Zusätzlicher Finanzierungsbedarf: ca. €{funding_gap:,.0f}."
        )
    elif min_liquiditaet < 10000:
        st.warning(
            "Die Liquidität bleibt positiv, ist aber knapp. Ein zusätzlicher Sicherheitspuffer wäre sinnvoll."
        )
    else:
        st.success(
            "Die Liquidität bleibt im gesamten 12-Monats-Verlauf stabil positiv."
        )

    st.subheader("12-Monats-Plan")
    st.dataframe(df_12m, use_container_width=True)

    st.subheader("3-Jahres-Plan")
    st.dataframe(df_3y, use_container_width=True)

# =========================================================
# TAB 2: BANK / INVESTOREN
# NUR ANZEIGE, KEINE EINGABEN
# =========================================================
with tab_bank:
    st.header("Bank / Investoren")

    b1, b2, b3, b4, b5 = st.columns(5)
    b1.metric("Kapitalbedarf Start", f"€{einmalkosten_gesamt:,.0f}")
    b2.metric("Funding Gap", f"€{funding_gap:,.0f}")
    b3.metric("Mindestliquidität", f"€{min_liquiditaet:,.0f}")
    b4.metric("Gewinn Jahr 1", f"€{gewinn_jahr_1:,.0f}")
    b5.metric("Break-even Camper", f"{break_even_camper:.1f}")

    if funding_gap > 0:
        st.error(
            f"Das Modell zeigt zusätzlichen Finanzierungsbedarf von ca. €{funding_gap:,.0f}."
        )
    elif gewinn_jahr_1 > 0 and min_liquiditaet > 0:
        st.success(
            "Das Modell ist unter den aktuellen Annahmen schlüssig darstellbar."
        )
    else:
        st.warning(
            "Das Modell ist grundsätzlich darstellbar, sollte aber weiter geschärft werden."
        )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("12-Monats-Verlauf: Umsatz, Kosten, Gewinn")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.bar(df_12m["Monat"], df_12m["Gesamtumsatz"], label="Umsatz")
        ax1.bar(df_12m["Monat"], df_12m["Gesamtkosten"], alpha=0.7, label="Kosten")
        ax1.plot(df_12m["Monat"], df_12m["Gewinn / Verlust"], marker="o", label="Gewinn / Verlust")
        ax1.set_ylabel("€")
        ax1.legend()
        st.pyplot(fig1)

    with c2:
        st.subheader("12-Monats-Verlauf: Liquidität")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(df_12m["Monat"], df_12m["Liquidität"], marker="o")
        ax2.axhline(0, linestyle="--")
        ax2.set_ylabel("€")
        st.pyplot(fig2)

    st.subheader("3-Jahres-Plan")
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

    st.subheader("12-Monats-Plan")
    st.dataframe(df_12m, use_container_width=True)

    st.subheader("3-Jahres-Plan Tabelle")
    st.dataframe(df_3y, use_container_width=True)
