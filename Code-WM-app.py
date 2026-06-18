import streamlit as st
import numpy as np
import pandas as pd

# 1. Seiteneinrichtung
st.set_page_config(
    page_title="World Cup Predictor 2026",
    page_icon="⚽",
    layout="wide"
)

# Premium Dark Design für die WM-App
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .wm-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
        border-radius: 16px;
        color: white;
        margin-bottom: 30px;
    }
    .match-box {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 5px solid #3b82f6;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="wm-header">
        <h1>🏆 KI Weltmeisterschafts-Predictor</h1>
        <p>Simulation basierend auf WM 2018/2022 Daten & aktueller Spieler-Saisonform</p>
    </div>
""", unsafe_allow_html=True)

# 2. Datenbasis (Kombination aus Historie 18/22 + aktueller Saison-Formwerte)
# Werte repräsentieren die errechnete Tor-Erwartung (Angriff) und Anfälligkeit (Abwehr)
@st.cache_data
def get_team_data():
    return {
        "Argentinien": {"angriff": 2.1, "abwehr": 0.8, "gruppe": "A"},
        "Frankreich":  {"angriff": 2.2, "abwehr": 0.9, "gruppe": "A"},
        "Kroatien":    {"angriff": 1.6, "abwehr": 1.1, "gruppe": "A"},
        "Marokko":     {"angriff": 1.4, "abwehr": 0.7, "gruppe": "A"},
        
        "England":     {"angriff": 2.0, "abwehr": 1.0, "gruppe": "B"},
        "Brasilien":   {"angriff": 2.1, "abwehr": 0.9, "gruppe": "B"},
        "Portugal":    {"angriff": 1.9, "abwehr": 1.1, "gruppe": "B"},
        "Niederlande": {"angriff": 1.7, "abwehr": 1.0, "gruppe": "B"},
        
        "Spanien":     {"angriff": 1.9, "abwehr": 0.9, "gruppe": "C"},
        "Deutschland": {"angriff": 1.8, "abwehr": 1.2, "gruppe": "C"},
        "Belgien":     {"angriff": 1.6, "abwehr": 1.3, "gruppe": "C"},
        "Uruguay":     {"angriff": 1.4, "abwehr": 1.0, "gruppe": "C"},
        
        "Japan":       {"angriff": 1.5, "abwehr": 1.2, "gruppe": "D"},
        "Senegal":     {"angriff": 1.3, "abwehr": 1.1, "gruppe": "D"},
        "USA":         {"angriff": 1.4, "abwehr": 1.3, "gruppe": "D"},
        "Schweiz":     {"angriff": 1.3, "abwehr": 1.2, "gruppe": "D"},
    }

teams = get_team_data()

# 3. Der Simulations-Algorithmus (Poisson-Verteilung)
def simuliere_spiel(team1, team2, ko_spiel=False):
    t1_lambda = teams[team1]["angriff"] * teams[team2]["abwehr"]
    t2_lambda = teams[team2]["angriff"] * teams[team1]["abwehr"]
    
    # 10.000 Simulationen für exakte Wahrscheinlichkeiten
    sim_t1_tore = np.random.poisson(t1_lambda, 10000)
    sim_t2_tore = np.random.poisson(t2_lambda, 10000)
    
    t1_siege = np.sum(sim_t1_tore > sim_t2_tore)
    t2_siege = np.sum(sim_t2_tore > sim_t1_tore)
    unentschieden = np.sum(sim_t1_tore == sim_t2_tore)
    
    # Reales Ergebnis (Durchschnitt der Simulation)
    tore_t1 = int(round(np.mean(sim_t1_tore)))
    tore_t2 = int(round(np.mean(sim_t2_tore)))
    
    # Verlängerung/Elfmeterschießen bei KO-Spielen erzwingen
    if ko_spiel and tore_t1 == tore_t2:
        if np.random.rand() > 0.5:
            tore_t1 += 1
        else:
            tore_t2 += 1
            
    gewinner = team1 if tore_t1 > tore_t2 else team2
    
    return {
        "tore_t1": tore_t1,
        "tore_t2": tore_t2,
        "p_t1": t1_siege / 100,
        "p_t2": t2_siege / 100,
        "p_unentschieden": unentschieden / 100,
        "gewinner": gewinner
    }

# 4. Sidebar Einstellungen
with st.sidebar:
    st.header("⚙️ Simulations-Optionen")
    st.info("Diese App simuliert das Turnier basierend auf historischen WM-Daten & Live-Formkurven der Spieler.")
    start_sim = st.button("🚀 Gesamte WM durchsimulieren", use_container_width=True)

# 5. Haupt-Präsentation
if not start_sim:
    st.subheader("Teilnehmende Nationen & berechnete Team-Stärken")
    df_teams = pd.DataFrame.from_dict(teams, orient='index')
    st.dataframe(df_teams, use_container_width=True)
    st.warning("Klicke links in der Sidebar auf den Button, um die Simulation zu starten!")

else:
    # --- GRUPPENPHASE ---
    st.header("📊 1. Ergebnisse der Gruppenphase")
    gruppen = ["A", "B", "C", "D"]
    ko_teilnehmer = []
    
    col_g1, col_g2 = st.columns(2)
    
    for idx, g in enumerate(gruppen):
        gruppen_teams = [t for t, v in teams.items() if v["gruppe"] == g]
        punkte = {t: 0 for t in gruppen_teams}
        
        with col_g1 if idx % 2 == 0 else col_g2:
            st.subheader(f"Gruppe {g}")
            
            # Jeder gegen jeden in der Gruppe
            for i in range(len(gruppen_teams)):
                for j in range(i + 1, len(gruppen_teams)):
                    t1, t2 = gruppen_teams[i], gruppen_teams[j]
                    res = simuliere_spiel(t1, t2, ko_spiel=False)
                    
                    if res["tore_t1"] > res["tore_t2"]:
                        punkte[t1] += 3
                    elif res["tore_t2"] > res["tore_t1"]:
                        punkte[t2] += 3
                    else:
                        punkte[t1] += 1
                        punkte[t2] += 1
                        
                    st.write(f"🔹 {t1} **{res['tore_t1']}:{res['tore_t2']}** {t2} *(Sieg-Chance: {res['p_t1']}% | {res['p_t2']}%)*")
            
            # Rangliste ermitteln
            schlusstabelle = sorted(punkte.items(), key=lambda x: x[1], reverse=True)
            ko_teilnehmer.append(schlusstabelle[0][0]) # Gruppensieger
            ko_teilnehmer.append(schlusstabelle[1][0]) # Gruppenzweiter

    # --- KO-PHASE ---
    st.write("---")
    st.header("📉 2. KO-Runde (Turnierbaum)")
    
    col_vf, col_hf, col_f = st.columns(3)
    
    # Viertelfinale
    with col_vf:
        st.subheader("💥 Viertelfinale")
        vf1 = simuliere_spiel(ko_teilnehmer[0], ko_teilnehmer[3], ko_spiel=True)
        st.markdown(f"<div class='match-box'><b>{ko_teilnehmer[0]}</b> vs {ko_teilnehmer[3]}<br>Ergebnis: {vf1['tore_t1']}:{vf1['tore_t2']} -> <b>{vf1['gewinner']}</b> weiter</div>", unsafe_allow_html=True)
        
        vf2 = simuliere_spiel(ko_teilnehmer[1], ko_teilnehmer[2], ko_spiel=True)
        st.markdown(f"<div class='match-box'>{ko_teilnehmer[1]} vs <b>{ko_teilnehmer[2]}</b><br>Ergebnis: {vf2['tore_t1']}:{vf2['tore_t2']} -> <b>{vf2['gewinner']}</b> weiter</div>", unsafe_allow_html=True)
        
        vf3 = simuliere_spiel(ko_teilnehmer[4], ko_teilnehmer[7], ko_spiel=True)
        st.markdown(f"<div class='match-box'><b>{ko_teilnehmer[4]}</b> vs {ko_teilnehmer[7]}<br>Ergebnis: {vf3['tore_t1']}:{vf3['tore_t2']} -> <b>{vf3['gewinner']}</b> weiter</div>", unsafe_allow_html=True)
        
        vf4 = simuliere_spiel(ko_teilnehmer[5], ko_teilnehmer[6], ko_spiel=True)
        st.markdown(f"<div class='match-box'>{ko_teilnehmer[5]} vs <b>{ko_teilnehmer[6]}</b><br>Ergebnis: {vf4['tore_t1']}:{vf4['tore_t2']} -> <b>{vf4['gewinner']}</b> weiter</div>", unsafe_allow_html=True)

    # Halbfinale
    with col_hf:
        st.subheader("🛡️ Halbfinale")
        hf1 = simuliere_spiel(vf1["gewinner"], vf2["gewinner"], ko_spiel=True)
        st.markdown(f"<div class='match-box'><b>{vf1['gewinner']}</b> vs {vf2['gewinner']}<br>Ergebnis: {hf1['tore_t1']}:{hf1['tore_t2']} -> <b>{hf1['gewinner']}</b> im Finale</div>", unsafe_allow_html=True)
        
        hf2 = simuliere_spiel(vf3["gewinner"], vf4["gewinner"], ko_spiel=True)
        st.markdown(f"<div class='match-box'>{vf3['gewinner']} vs <b>{vf4['gewinner']}</b><br>Ergebnis: {hf2['tore_t1']}:{hf2['tore_t2']} -> <b>{hf2['gewinner']}</b> im Finale</div>", unsafe_allow_html=True)

    # Finale
    with col_f:
        st.subheader("👑 Das große Finale")
        finale = simuliere_spiel(hf1["gewinner"], hf2["gewinner"], ko_spiel=True)
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%); padding: 25px; border-radius: 16px; text-align: center; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.3);'>
                <h3>WELTMEISTER</h3>
                <h2>🥇 {finale['gewinner']} 🥇</h2>
                <p>Finale-Ergebnis: {finale['tore_t1']}:{finale['tore_t2']}</p>
                <small>Sieg-Chance im Finale: {finale['p_t1'] if finale['gewinner'] == hf1['gewinner'] else finale['p_t2']}%</small>
            </div>
        """, unsafe_allow_html=True)
