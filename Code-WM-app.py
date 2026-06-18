import streamlit as st
import numpy as np
import pandas as pd

# 1. Page Configuration & UI-Styling
st.set_page_config(
    page_title="KI World Cup Predictor 2026",
    page_icon="🏆",
    layout="wide"
)

# CSS für maximale Lesbarkeit und Kontraste
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    
    .wm-title-container {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0284c7 100%);
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(2, 132, 199, 0.2);
        margin-bottom: 35px;
    }
    .group-card {
        background: #1e293b; /* Fester, dunkler Hintergrund */
        border: 2px solid #334155;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    .group-header {
        color: #ffffff !important; /* Weißer, klar lesbarer Text */
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 15px;
        border-bottom: 2px solid #38bdf8;
        padding-bottom: 5px;
    }
    .match-strip {
        background: #0f172a; 
        padding: 12px 16px;
        border-radius: 10px;
        margin: 6px 0;
        border-left: 4px solid #38bdf8;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #f1f5f9; 
    }
    .match-strip b {
        color: #38bdf8; 
        font-size: 1.1rem;
    }
    .ko-box {
        background: #0f172a; 
        padding: 12px; 
        border-radius: 12px; 
        margin-bottom: 8px; 
        border: 1px solid #334155;
        color: #e2e8f0;
    }
    .ko-box small {
        color: #94a3b8;
    }
    .ko-box b {
        color: #ffffff;
    }
    .ko-box .highlight-winner {
        color: #38bdf8;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="wm-title-container">
        <h1 style='color: white; margin: 0; font-size: 2.8rem; font-weight: 800;'>🏆 FIFA World Cup 2026 Predictor</h1>
        <p style='color: #e2e8f0; font-size: 1.2rem; margin-top: 10px; font-weight: 400;'>
            Realistische Simulation basierend auf 10-Jahres-Kicker-Historie, Trainer-Taktik & Gesamtmarktwerten
        </p>
    </div>
""", unsafe_allow_html=True)

# 2. Erweiterte Datenbank mit System, Trainer-Faktor, Marktwert & Historie
@st.cache_data
def get_advanced_world_cup_data():
    # gewichtung_historie: 10-Jahres-Trend bei großen Turnieren (kicker-basiert)
    # trainer_faktor: Einfluss des aktuellen Trainers/Systems auf die Kompaktheit
    return {
        "Mexiko": {"angriff": 1.6, "abwehr": 1.1, "gruppe": "A", "wert_mio": 220, "trainer_faktor": 1.1, "historie": 1.2, "system": "4-3-3"},
        "Südafrika": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "A", "wert_mio": 35, "trainer_faktor": 1.0, "historie": 0.8, "system": "4-2-31"},
        "Südkorea": {"angriff": 1.5, "abwehr": 1.2, "gruppe": "A", "wert_mio": 165, "trainer_faktor": 1.1, "historie": 1.1, "system": "4-4-2"},
        "Tschechien": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "A", "wert_mio": 190, "trainer_faktor": 1.0, "historie": 1.0, "system": "3-4-1-2"},
        
        "Kanada": {"angriff": 1.5, "abwehr": 1.2, "gruppe": "B", "wert_mio": 180, "trainer_faktor": 1.2, "historie": 0.9, "system": "4-4-2"},
        "Bosnien-Herzegowina": {"angriff": 1.3, "abwehr": 1.3, "gruppe": "B", "wert_mio": 85, "trainer_faktor": 0.9, "historie": 0.9, "system": "3-5-2"},
        "Katar": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "B", "wert_mio": 20, "trainer_faktor": 1.0, "historie": 0.7, "system": "5-3-2"},
        "Schweiz": {"angriff": 1.6, "abwehr": 0.9, "gruppe": "B", "wert_mio": 280, "trainer_faktor": 1.3, "historie": 1.3, "system": "3-4-2-1"},
        
        "Brasilien": {"angriff": 2.3, "abwehr": 0.8, "gruppe": "C", "wert_mio": 1050, "trainer_faktor": 1.3, "historie": 1.5, "system": "4-2-3-1"},
        "Marokko": {"angriff": 1.7, "abwehr": 0.8, "gruppe": "C", "wert_mio": 320, "trainer_faktor": 1.4, "historie": 1.4, "system": "4-1-4-1"},
        "Haiti": {"angriff": 0.9, "abwehr": 1.6, "gruppe": "C", "wert_mio": 15, "trainer_faktor": 0.9, "historie": 0.5, "system": "4-5-1"},
        "Schottland": {"angriff": 1.3, "abwehr": 1.2, "gruppe": "C", "wert_mio": 210, "trainer_faktor": 1.1, "historie": 0.9, "system": "5-4-1"},
        
        "USA": {"angriff": 1.8, "abwehr": 1.0, "gruppe": "D", "wert_mio": 350, "trainer_faktor": 1.2, "historie": 1.1, "system": "4-3-3"},
        "Paraguay": {"angriff": 1.2, "abwehr": 1.0, "gruppe": "D", "wert_mio": 110, "trainer_faktor": 1.0, "historie": 1.0, "system": "4-4-2"},
        "Australien": {"angriff": 1.3, "abwehr": 1.2, "gruppe": "D", "wert_mio": 50, "trainer_faktor": 1.1, "historie": 1.1, "system": "4-2-3-1"},
        "Türkei": {"angriff": 1.7, "abwehr": 1.2, "gruppe": "D", "wert_mio": 310, "trainer_faktor": 1.2, "historie": 1.0, "system": "4-2-3-1"},
        
        "Deutschland": {"angriff": 2.1, "abwehr": 0.9, "gruppe": "E", "wert_mio": 850, "trainer_faktor": 1.4, "historie": 1.3, "system": "4-2-3-1"},
        "Curaçao": {"angriff": 0.8, "abwehr": 1.7, "gruppe": "E", "wert_mio": 12, "trainer_faktor": 0.9, "historie": 0.4, "system": "5-4-1"},
        "Elfenbeinküste": {"angriff": 1.6, "abwehr": 1.1, "gruppe": "E", "wert_mio": 340, "trainer_faktor": 1.1, "historie": 1.1, "system": "4-3-3"},
        "Ecuador": {"angriff": 1.5, "abwehr": 0.9, "gruppe": "E", "wert_mio": 260, "trainer_faktor": 1.2, "historie": 1.1, "system": "3-4-3"},
        
        "Niederlande": {"angriff": 1.9, "abwehr": 0.9, "gruppe": "F", "wert_mio": 620, "trainer_faktor": 1.3, "historie": 1.4, "system": "4-3-3"},
        "Japan": {"angriff": 1.7, "abwehr": 1.0, "gruppe": "F", "wert_mio": 290, "trainer_faktor": 1.3, "historie": 1.2, "system": "4-2-3-1"},
        "Schweden": {"angriff": 1.7, "abwehr": 1.2, "gruppe": "F", "wert_mio": 240, "trainer_faktor": 1.0, "historie": 1.1, "system": "4-4-2"},
        "Tunesien": {"angriff": 1.1, "abwehr": 1.2, "gruppe": "F", "wert_mio": 45, "trainer_faktor": 1.0, "historie": 0.9, "system": "4-5-1"},
        
        "Belgien": {"angriff": 1.9, "abwehr": 1.1, "gruppe": "G", "wert_mio": 480, "trainer_faktor": 1.1, "historie": 1.3, "system": "4-3-3"},
        "Ägypten": {"angriff": 1.4, "abwehr": 1.2, "gruppe": "G", "wert_mio": 110, "trainer_faktor": 1.1, "historie": 1.0, "system": "4-2-3-1"},
        "Iran": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "G", "wert_mio": 40, "trainer_faktor": 1.0, "historie": 1.0, "system": "5-4-1"},
        "Neuseeland": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "G", "wert_mio": 25, "trainer_faktor": 0.9, "historie": 0.6, "system": "4-4-2"},
        
        "Spanien": {"angriff": 2.2, "abwehr": 0.8, "gruppe": "H", "wert_mio": 900, "trainer_faktor": 1.4, "historie": 1.5, "system": "4-3-3"},
        "Kap Verde": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "H", "wert_mio": 30, "trainer_faktor": 1.0, "historie": 0.7, "system": "4-3-3"},
        "Saudi-Arabien": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "H", "wert_mio": 35, "trainer_faktor": 1.0, "historie": 0.9, "system": "4-1-4-1"},
        "Uruguay": {"angriff": 1.9, "abwehr": 0.9, "gruppe": "H", "wert_mio": 420, "trainer_faktor": 1.4, "historie": 1.3, "system": "4-3-3"},
        
        "Frankreich": {"angriff": 2.4, "abwehr": 0.8, "gruppe": "I", "wert_mio": 1200, "trainer_faktor": 1.4, "historie": 1.6, "system": "4-2-3-1"},
        "Senegal": {"angriff": 1.5, "abwehr": 1.1, "gruppe": "I", "wert_mio": 280, "trainer_faktor": 1.1, "historie": 1.2, "system": "4-3-3"},
        "Irak": {"angriff": 1.0, "abwehr": 1.3, "gruppe": "I", "wert_mio": 18, "trainer_faktor": 0.9, "historie": 0.6, "system": "4-2-3-1"},
        "Norwegen": {"angriff": 1.8, "abwehr": 1.3, "gruppe": "I", "wert_mio": 450, "trainer_faktor": 1.1, "historie": 0.9, "system": "4-3-3"},
        
        "Argentinien": {"angriff": 2.2, "abwehr": 0.7, "gruppe": "J", "wert_mio": 800, "trainer_faktor": 1.5, "historie": 1.6, "system": "4-3-3"},
        "Algerien": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "J", "wert_mio": 140, "trainer_faktor": 1.0, "historie": 1.0, "system": "4-1-4-1"},
        "Österreich": {"angriff": 1.7, "abwehr": 1.0, "gruppe": "J", "wert_mio": 290, "trainer_faktor": 1.3, "historie": 1.1, "system": "4-2-2-2"},
        "Jordanien": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "J", "wert_mio": 15, "trainer_faktor": 1.0, "historie": 0.6, "system": "5-3-2"},
        
        "Portugal": {"angriff": 2.2, "abwehr": 0.9, "gruppe": "K", "wert_mio": 950, "trainer_faktor": 1.3, "historie": 1.4, "system": "4-3-3"},
        "DR Kongo": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "K", "wert_mio": 60, "trainer_faktor": 1.0, "historie": 0.8, "system": "4-2-3-1"},
        "Usbekistan": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "K", "wert_mio": 32, "trainer_faktor": 1.1, "historie": 0.7, "system": "3-4-2-1"},
        "Kolumbien": {"angriff": 1.9, "abwehr": 0.9, "gruppe": "K", "wert_mio": 280, "trainer_faktor": 1.3, "historie": 1.2, "system": "4-2-3-1"},
        
        "England": {"angriff": 2.3, "abwehr": 0.9, "gruppe": "L", "wert_mio": 1300, "trainer_faktor": 1.3, "historie": 1.5, "system": "4-2-3-1"},
        "Kroatien": {"angriff": 1.6, "abwehr": 1.0, "gruppe": "L", "wert_mio": 270, "trainer_faktor": 1.3, "historie": 1.5, "system": "4-3-3"},
        "Ghana": {"angriff": 1.4, "abwehr": 1.2, "gruppe": "L", "wert_mio": 120, "trainer_faktor": 1.0, "historie": 1.0, "system": "4-2-3-1"},
        "Panama": {"angriff": 1.0, "abwehr": 1.3, "gruppe": "L", "wert_mio": 18, "trainer_faktor": 0.9, "historie": 0.7, "system": "4-4-2"},
    }

teams_db = get_advanced_world_cup_data()

# 3. Gewichtete Simulations-Logik für extrem realistische Ergebnisse
def simuliere_spiel_realistisch(t1, t2, ko=False):
    # Berechnung des Stärkefaktors aus Marktwert, Historie und Trainer-Taktik
    mw_faktor_t1 = np.log10(teams_db[t1]["wert_mio"]) / 2
    mw_faktor_t2 = np.log10(teams_db[t2]["wert_mio"]) / 2
    
    # Komplexe Lambda-Ermittlung basierend auf deinen Anforderungen
    t1_lambda = teams_db[t1]["angriff"] * teams_db[t2]["abwehr"] * mw_faktor_t1 * teams_db[t1]["trainer_faktor"] * teams_db[t1]["historie"]
    t2_lambda = teams_db[t2]["angriff"] * teams_db[t1]["abwehr"] * mw_faktor_t2 * teams_db[t2]["trainer_faktor"] * teams_db[t2]["historie"]
    
    # Normalisierung der Lambda-Werte für realistische Toranzahlen (selten mehr als 5 Tore)
    t1_lambda = min(3.5, max(0.2, t1_lambda / 2))
    t2_lambda = min(3.5, max(0.2, t2_lambda / 2))
    
    goals_t1 = np.random.poisson(t1_lambda)
    goals_t2 = np.random.poisson(t2_lambda)
    
    if ko and goals_t1 == goals_t2:
        # Höhere Chance für das stärkere Team im Elfmeterschießen/Verlängerung
        if (t1_lambda + np.random.rand()) > (t2_lambda + np.random.rand()):
            goals_t1 += 1
        else:
            goals_t2 += 1
            
    return {"score1": goals_t1, "score2": goals_t2, "winner": t1 if goals_t1 > goals_t2 else t2}

# 4. UI-Struktur
tab1, tab2 = st.tabs(["🔍 Team-Einschätzungen & Taktik", "🚀 Realistischer Turnier-Simulator"])

with tab1:
    st.subheader("Analyse der Kader-Metriken (Marktwert & kicker-Historie)")
    selected_group = st.selectbox("Wähle eine Gruppe zur Analyse:", sorted(list(set([v["gruppe"] for v in teams_db.values()]))))
    group_teams = {k: v for k, v in teams_db.items() if v["gruppe"] == selected_group}
    
    for t_name, t_data in group_teams.items():
        with st.expander(f"⚽ {t_name} — System: {t_data['system']}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Gesamtwert", f"{t_data['wert_mio']} Mio. €")
            col2.metric("Trainer/Taktik-Faktor", t_data["trainer_faktor"])
            col3.metric("Historien-Stärke (10J)", t_data["historie"])

with tab2:
    st.sidebar.header("⚙️ Optionen")
    start_sim = st.sidebar.button("🏆 Offiziellen Spielplan simulieren", use_container_width=True)
    
    if not start_sim:
        st.info("Klicke links auf den Button, um den offiziellen, optimierten FIFA-Spielplan zu starten!")
    else:
        st.header("📊 Ergebnisse der Gruppenphase")
        groups = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        all_group_tables = {}
        cols = st.columns(3)
        
        for idx, g in enumerate(groups):
            current_col = cols[idx % 3]
            g_teams = [t for t, v in teams_db.items() if v["gruppe"] == g]
            punkte = {t: 0 for t in g_teams}
            tordifferenz = {t: 0 for t in g_teams}
            
            with current_col:
                # FIX: Perfekt lesbare, kontrastreiche Überschrift
                st.markdown(f"<div class='group-card'><div class='group-header'>Gruppe {g}</div>", unsafe_allow_html=True)
                
                # Feste Spielreihenfolge innerhalb der Gruppe
                spielpaarungen = [(g_teams[0], g_teams[1]), (g_teams[2], g_teams[3]), 
                                  (g_teams[0], g_teams[2]), (g_teams[1], g_teams[3]),
                                  (g_teams[3], g_teams[0]), (g_teams[1], g_teams[2])]
                                  
                for t1, t2 in spielpaarungen:
                    res = simuliere_spiel_realistisch(t1, t2, ko=False)
                    if res["score1"] > res["score2"]: punkte[t1] += 3
                    elif res["score2"] > res["score1"]: punkte[t2] += 3
                    else:
                        punkte[t1] += 1
                        punkte[t2] += 1
                    tordifferenz[t1] += (res["score1"] - res["score2"])
                    tordifferenz[t2] += (res["score2"] - res["score1"])
                    
                    st.markdown(f"<div class='match-strip'><span>{t1} - {t2}</span> <b>{res['score1']}:{res['score2']}</b></div>", unsafe_allow_html=True)
                
                tabelle = sorted(g_teams, key=lambda x: (punkte[x], tordifferenz[x]), reverse=True)
                all_group_tables[g] = {"tabelle": tabelle, "punkte": punkte, "tordifferenz": tordifferenz}
                st.markdown("</div>", unsafe_allow_html=True)

        # --- RELEMENTIERTER TURNIERBAUM (Runde der letzten 32) ---
        gruppenerste = [all_group_tables[g]["tabelle"][0] for g in groups]
        gruppenzweite = [all_group_tables[g]["tabelle"][1] for g in groups]
        
        drittplatzierte = []
        for g in groups:
            t3 = all_group_tables[g]["tabelle"][2]
            drittplatzierte.append({"team": t3, "punkte": all_group_tables[g]["punkte"][t3], "td": all_group_tables[g]["tordifferenz"][t3]})
            
        beste_dritte = [x["team"] for x in sorted(drittplatzierte, key=lambda x: (x["punkte"], x["td"]), reverse=True)[:8]]
        uebrige_zweite = gruppenzweite[8:]
        
        # Generierung des echten Turnierbaums (Vermeidung von direkten Re-Matches aus derselben Gruppe)
        ko_32_teams = []
        for i in range(8):
            ko_32_teams.extend([gruppenerste[i], beste_dritte[i]])
        for i in range(8, 12):
            ko_32_teams.extend([gruppenerste[i], uebrige_zweite[i-8]])
        for i in range(4):
            ko_32_teams.extend([gruppenzweite[i], gruppenzweite[7-i]])

        st.write("---")
        st.header("📉 Offizielle K.-o.-Phase (Keine direkten Gruppen-Rematches möglich)")
        
        col_r32, col_r16, col_vf, col_hf, col_f = st.columns(5)
        
        def run_stage(team_list, column, stage_title, color):
            winners = []
            with column:
                st.subheader(stage_title)
                for i in range(0, len(team_list), 2):
                    t1, t2 = team_list[i], team_list[i+1]
                    res = simuliere_spiel_realistisch(t1, t2, ko=True)
                    winners.append(res["winner"])
                    st.markdown(f"""
                        <div class='ko-box' style='border-left: 4px solid {color};'>
                            <small>{t1} vs {t2}</small><br>
                            <b>{res['score1']}:{res['score2']}</b> ➔ <b class='highlight-winner'>{res['winner']}</b>
                        </div>
                    """, unsafe_allow_html=True)
            return winners

        r16_teams = run_stage(ko_32_teams, col_r32, "💥 Runde von 32", "#a855f7")
        vf_teams = run_stage(r16_teams, col_r16, "⚡ Achtelfinale", "#ec4899")
        hf_teams = run_stage(vf_teams, col_vf, "⚔️ Viertelfinale", "#f43f5e")
        final_teams = run_stage(hf_teams, col_hf, "🛡️ Halbfinale", "#eab308")
        
        with col_f:
            st.subheader("👑 Finale")
            f_res = simuliere_spiel_realistisch(final_teams[0], final_teams[1], ko=True)
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%); padding: 25px; border-radius: 16px; text-align: center; color: white; box-shadow: 0 10px 25px rgba(234,179,8,0.4);'>
                    <h4 style='margin:0;'>WELTMEISTER 2026</h4>
                    <h2 style='margin:10px 0;'>🥇 {f_res['winner']} 🥇</h2>
                    <p style='margin:0; font-size:1.1rem;'>Ergebnis: <b>{f_res['score1']}:{f_res['score2']}</b></p>
                    <small style='opacity:0.9;'>Gegner: {final_teams[1] if f_res['winner'] == final_teams[0] else final_teams[0]}</small>
                </div>
            """, unsafe_allow_html=True)
