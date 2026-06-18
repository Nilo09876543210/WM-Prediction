import streamlit as st
import numpy as np
import pandas as pd

# 1. Page Configuration & UI-Styling
st.set_page_config(
    page_title="KI World Cup Predictor 2026",
    page_icon="🏆",
    layout="wide"
)

# Visuelles High-End-Tuning via CSS
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
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    .match-strip {
        background: #1e293b;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 6px 0;
        border-left: 4px solid #06b6d4;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .mvp-badge {
        background: linear-gradient(90deg, #b45309 0%, #d97706 100%);
        color: white;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="wm-title-container">
        <h1 style='color: white; margin: 0; font-size: 2.8rem; font-weight: 800;'>🏆 FIFA World Cup 2026 Predictor</h1>
        <p style='color: #e2e8f0; font-size: 1.2rem; margin-top: 10px; font-weight: 400;'>
            48 Teams · 12 Gruppen · KI-Simulation basierend auf Formstärke & Transfermarkt-Daten
        </p>
    </div>
""", unsafe_allow_html=True)

# 2. Volle Datenbank für alle 48 Teams der WM 2026
@st.cache_data
def get_world_cup_2026_data():
    return {
        # Gruppe A
        "Mexiko": {"angriff": 1.6, "abwehr": 1.1, "gruppe": "A", "mvp": "Santiago Giménez", "wert": "40 Mio. €", "info": "Heimvorteil treibt die Mexikaner an, defensiv anfällig."},
        "Südafrika": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "A", "mvp": "Teboho Mokoena", "wert": "4 Mio. €", "info": "Außenseiter in der Gruppe, taktisch kompakt orientiert."},
        "Südkorea": {"angriff": 1.5, "abwehr": 1.2, "gruppe": "A", "mvp": "Heung-min Son", "wert": "45 Mio. €", "info": "Konterstark mit unbändigem Willen und internationaler Erfahrung."},
        "Tschechien": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "A", "mvp": "Tomas Soucek", "wert": "30 Mio. €", "info": "Physisch robustes Team mit gefährlichen Standardsituationen."},
        # Gruppe B
        "Kanada": {"angriff": 1.5, "abwehr": 1.2, "gruppe": "B", "mvp": "Alphonso Davies", "wert": "50 Mio. €", "info": "Enormes Tempo über die Außenbahnen im Heimturnier."},
        "Bosnien-Herzegowina": {"angriff": 1.3, "abwehr": 1.3, "gruppe": "B", "mvp": "Anel Ahmedhodzic", "wert": "18 Mio. €", "info": "Über die Playoffs qualifiziert, unberechenbare Mentalität."},
        "Katar": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "B", "mvp": "Akram Afif", "wert": "5 Mio. €", "info": "Eingespielter Asienmeister, international spielerisch limitiert."},
        "Schweiz": {"angriff": 1.5, "abwehr": 0.9, "gruppe": "B", "mvp": "Manuel Akanji", "wert": "45 Mio. €", "info": "Turniermannschaft par excellence mit stabiler Defensivachse."},
        # Gruppe C
        "Brasilien": {"angriff": 2.2, "abwehr": 0.8, "gruppe": "C", "mvp": "Vinicius Jr.", "wert": "180 Mio. €", "info": "Einer der Top-Favoriten mit Weltklasse-Individualisten."},
        "Marokko": {"angriff": 1.6, "abwehr": 0.8, "gruppe": "C", "mvp": "Achraf Hakimi", "wert": "60 Mio. €", "info": "Defensiv extrem stabil und umschaltstark."},
        "Haiti": {"angriff": 0.9, "abwehr": 1.6, "gruppe": "C", "mvp": "Frantzdy Pierrot", "wert": "3 Mio. €", "info": "Große Sensation der Qualifikation, krasser Außenseiter."},
        "Schottland": {"angriff": 1.3, "abwehr": 1.2, "gruppe": "C", "mvp": "Scott McTominay", "wert": "32 Mio. €", "info": "Kampfstark mit lautstarker Fan-Unterstützung im Rücken."},
        # Gruppe D
        "USA": {"angriff": 1.7, "abwehr": 1.0, "gruppe": "D", "mvp": "Christian Pulisic", "wert": "40 Mio. €", "info": "Die 'Golden Generation' will im eigenen Land historisches schaffen."},
        "Paraguay": {"angriff": 1.2, "abwehr": 1.0, "gruppe": "D", "mvp": "Julio Enciso", "wert": "22 Mio. €", "info": "Unbequemer Gegner aus Südamerika mit Fokus auf Zerstörung."},
        "Australien": {"angriff": 1.3, "abwehr": 1.2, "gruppe": "D", "mvp": "Harry Souttar", "wert": "15 Mio. €", "info": "Physisch starke 'Socceroos' leben vom Teamgeist."},
        "Türkei": {"angriff": 1.6, "abwehr": 1.2, "gruppe": "D", "mvp": "Arda Güler", "wert": "45 Mio. €", "info": "Junges, hochemotionales Team mit viel spielerischer Kreativität."},
        # Gruppe E
        "Deutschland": {"angriff": 2.0, "abwehr": 1.0, "gruppe": "E", "mvp": "Florian Wirtz", "wert": "130 Mio. €", "info": "Zurück in der Weltspitze. Extrem starkes Mittelfeld-Duo."},
        "Curaçao": {"angriff": 0.8, "abwehr": 1.7, "gruppe": "E", "mvp": "Juninho Bacuna", "wert": "2 Mio. €", "info": "Exotischer Teilnehmer, jede knappe Niederlage ist ein Erfolg."},
        "Elfenbeinküste": {"angriff": 1.5, "abwehr": 1.1, "gruppe": "E", "mvp": "Ousmane Diomande", "wert": "40 Mio. €", "info": "Physisch starke Truppe, amtierender Afrika-Gigant."},
        "Ecuador": {"angriff": 1.4, "abwehr": 0.9, "gruppe": "E", "mvp": "Moises Caicedo", "wert": "75 Mio. €", "info": "Sehr unterschätztes Team, extrem eklig zu bespielen."},
        # Gruppe F
        "Niederlande": {"angriff": 1.8, "abwehr": 0.9, "gruppe": "F", "mvp": "Xavi Simons", "wert": "80 Mio. €", "info": "Taktisch flexibel, defensiv besetzt auf Weltklasse-Niveau."},
        "Japan": {"angriff": 1.6, "abwehr": 1.1, "gruppe": "F", "mvp": "Takefusa Kubo", "wert": "50 Mio. €", "info": "Diszipliniert, pfeilschnell und technisch brillant."},
        "Schweden": {"angriff": 1.7, "abwehr": 1.2, "gruppe": "F", "mvp": "Alexander Isak", "wert": "75 Mio. €", "info": "Kopflastig im Angriff, wackelig bei gegnerischem Druck."},
        "Tunesien": {"angriff": 1.1, "abwehr": 1.2, "gruppe": "F", "mvp": "Ellyes Skhiri", "wert": "13 Mio. €", "info": "Kompaktes Kollektiv, dem es an Durchschlagskraft fehlt."},
        # Gruppe G
        "Belgien": {"angriff": 1.8, "abwehr": 1.1, "gruppe": "G", "mvp": "Jérémy Doku", "wert": "65 Mio. €", "info": "Umbruch geschafft. Viel Tempo über die Flügel."},
        "Ägypten": {"angriff": 1.4, "abwehr": 1.2, "gruppe": "G", "mvp": "Mohamed Salah", "wert": "55 Mio. €", "info": "Alles steht und fällt mit der Genialität ihres Superstars."},
        "Iran": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "G", "mvp": "Mehdi Taremi", "wert": "10 Mio. €", "info": "Erfahrenes Team, das defensiv tief steht."},
        "Neuseeland": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "G", "mvp": "Chris Wood", "wert": "7 Mio. €", "info": "Ozeanien-Meister, physisch robust bei hohen Bällen."},
        # Gruppe H
        "Spanien": {"angriff": 2.1, "abwehr": 0.8, "gruppe": "H", "mvp": "Lamine Yamal", "wert": "120 Mio. €", "info": "Ballbesitz-Könige mit tödlichen Flügelspielern."},
        "Kap Verde": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "H", "mvp": "Logan Costa", "wert": "12 Mio. €", "info": "Kleine Inselnation mit extrem leidenschaftlichem Fußball."},
        "Saudi-Arabien": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "H", "mvp": "Firas Al-Buraikan", "wert": "6 Mio. €", "info": "Taktisch diszipliniert, fehlt aber an Tempo gegen Top-Nationen."},
        "Uruguay": {"angriff": 1.8, "abwehr": 0.9, "gruppe": "H", "mvp": "Federico Valverde", "wert": "100 Mio. €", "info": "Bielsa-Powerfußball mit unbändigem Pressing."},
        # Gruppe I
        "Frankreich": {"angriff": 2.3, "abwehr": 0.8, "gruppe": "I", "mvp": "Kylian Mbappé", "wert": "180 Mio. €", "info": "Der wertvollste Kader des Turniers. Qualität im Überfluss."},
        "Senegal": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "I", "mvp": "Nicolas Jackson", "wert": "35 Mio. €", "info": "Physisch eines der stärksten Teams des afrikanischen Kontinents."},
        "Irak": {"angriff": 1.0, "abwehr": 1.3, "gruppe": "I", "mvp": "Aymen Hussein", "wert": "3 Mio. €", "info": "Außenseiter, lebt primär von der mannschaftlichen Geschlossenheit."},
        "Norwegen": {"angriff": 1.7, "abwehr": 1.3, "gruppe": "I", "mvp": "Erling Haaland", "wert": "180 Mio. €", "info": "Dank Haaland offensiv eine Waffe, defensiv anfällig."},
        # Gruppe J
        "Argentinien": {"angriff": 2.1, "abwehr": 0.7, "gruppe": "J", "mvp": "Lautaro Martínez", "wert": "110 Mio. €", "info": "Titelverteidiger. Extrem abgezockt und harmonisch eingespielt."},
        "Algerien": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "J", "mvp": "Rayan Aït-Nouri", "wert": "35 Mio. €", "info": "Technisch versiert, scheitert oft an der eigenen Effizienz."},
        "Österreich": {"angriff": 1.6, "abwehr": 1.0, "gruppe": "J", "mvp": "Konrad Laimer", "wert": "30 Mio. €", "info": "Rangnick-Pressingmaschine. Extrem unangenehm zu bespielen."},
        "Jordanien": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "J", "mvp": "Musa Al-Taamari", "wert": "8 Mio. €", "info": "Asien-Überraschungsteam, taktisch defensiv fokussiert."},
        # Gruppe K
        "Portugal": {"angriff": 2.1, "abwehr": 0.9, "gruppe": "K", "mvp": "Rafael Leão", "wert": "90 Mio. €", "info": "Unglaubliche Tiefe im Kader, Luxusprobleme im Sturm."},
        "DR Kongo": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "K", "mvp": "Yoane Wissa", "wert": "28 Mio. €", "info": "Konterstark mit unberechenbaren Einzelspielern."},
        "Usbekistan": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "K", "mvp": "Abbosbek Fayzullaev", "wert": "12 Mio. €", "info": "Erstmals qualifiziert, technisch hochspannende Generation."},
        "Kolumbien": {"angriff": 1.8, "abwehr": 0.9, "gruppe": "K", "mvp": "Luis Díaz", "wert": "75 Mio. €", "info": "Seit Monaten in Topform. Extrem giftig und offensivstark."},
        # Gruppe L
        "England": {"angriff": 2.2, "abwehr": 0.9, "gruppe": "L", "mvp": "Jude Bellingham", "wert": "180 Mio. €", "info": "Kader voller Superstars. Die Erwartungshaltung ist gigantisch."},
        "Kroatien": {"angriff": 1.5, "abwehr": 1.0, "gruppe": "L", "mvp": "Josko Gvardiol", "wert": "75 Mio. €", "info": "Die ewigen Mentalitätsmonster. Letzter Tanz einer großen Generation."},
        "Ghana": {"angriff": 1.4, "abwehr": 1.2, "gruppe": "L", "mvp": "Mohammed Kudus", "wert": "50 Mio. €", "info": "Unberechenbar. An guten Tagen schlagen sie jeden."},
        "Panama": {"angriff": 1.0, "abwehr": 1.3, "gruppe": "L", "mvp": "Adalberto Carrasquilla", "wert": "4 Mio. €", "info": "Physisch robust, spielerisch den Top-Nationen unterlegen."},
    }

teams_db = get_world_cup_2026_data()

# 3. Poisson Simulations-Logik
def simuliere_spiel(t1, t2, ko=False):
    t1_lambda = teams_db[t1]["angriff"] * teams_db[t2]["abwehr"]
    t2_lambda = teams_db[t2]["angriff"] * teams_db[t1]["abwehr"]
    
    sim_t1 = np.random.poisson(t1_lambda, 5000)
    sim_t2 = np.random.poisson(t2_lambda, 5000)
    
    t1_win_p = np.sum(sim_t1 > sim_t2) / 5000 * 100
    t2_win_p = np.sum(sim_t2 > sim_t1) / 5000 * 100
    
    goals_t1 = int(round(np.mean(sim_t1)))
    goals_t2 = int(round(np.mean(sim_t2)))
    
    if ko and goals_t1 == goals_t2:
        if np.random.rand() > 0.5: goals_t1 += 1
        else: goals_t2 += 1
        
    return {
        "score1": goals_t1, "score2": goals_t2,
        "p1": round(t1_win_p, 1), "p2": round(t2_win_p, 1),
        "winner": t1 if goals_t1 > goals_t2 else t2
    }

# 4. Tabs für saubere UI-Struktur
tab1, tab2 = st.tabs(["🔍 Team-Einschätzungen (Marktwerte)", "🚀 KI-Turnier-Simulator"])

with tab1:
    st.subheader("Kader-Analyse & wertvollste Spieler (Transfermarkt)")
    selected_group = st.selectbox("Wähle eine Gruppe zur Analyse:", sorted(list(set([v["gruppe"] for v in teams_db.values()]))))
    
    group_teams = {k: v for k, v in teams_db.items() if v["gruppe"] == selected_group}
    
    for t_name, t_data in group_teams.items():
        with st.expander(f"⚽ {t_name} — Top-Star: {t_data['mvp']} ({t_data['wert']})"):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric(label="Offensiv-Rating", value=t_data["angriff"])
                st.metric(label="Defensiv-Anfälligkeit", value=t_data["abwehr"])
            with col2:
                st.markdown(f"**Einschätzung:** {t_data['info']}")
                st.markdown(f"<span class='mvp-badge'>TM-Wertvollster Spieler</span> **{t_data['mvp']}** ({t_data['wert']})", unsafe_allow_html=True)

with tab2:
    st.sidebar.header("⚙️ Optionen")
    start_sim = st.sidebar.button("🏆 WM 2026 simulieren", use_container_width=True)
    
    if not start_sim:
        st.info("Klicke auf den Button in der linken Sidebar, um die komplette Weltmeisterschaft mit 104 Spielen live zu simulieren!")
    else:
        # --- GRUPPENPHASE ---
        st.header("📊 Ergebnisse der Gruppenphase")
        groups = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        
        all_group_tables = {}
        
        # Grid-Layout für die 12 Gruppen
        cols = st.columns(3)
        for idx, g in enumerate(groups):
            current_col = cols[idx % 3]
            g_teams = [t for t, v in teams_db.items() if v["gruppe"] == g]
            punkte = {t: 0 for t in g_teams}
            tordifferenz = {t: 0 for t in g_teams}
            
            with current_col:
                st.markdown(f"<div class='group-card'><h3>Gruppe {g}</h3>", unsafe_allow_html=True)
                
                # Jeder gegen jeden
                for i in range(len(g_teams)):
                    for j in range(i + 1, len(g_teams)):
                        t1, t2 = g_teams[i], g_teams[j]
                        res = simuliere_spiel(t1, t2, ko=False)
                        
                        # Punktevergabe
                        if res["score1"] > res["score2"]: punkte[t1] += 3
                        elif res["score2"] > res["score1"]: punkte[t2] += 3
                        else:
                            punkte[t1] += 1
                            punkte[t2] += 1
                        
                        tordifferenz[t1] += (res["score1"] - res["score2"])
                        tordifferenz[t2] += (res["score2"] - res["score1"])
                        
                        st.markdown(f"<div class='match-strip'><span>{t1} - {t2}</span> <b>{res['score1']}:{res['score2']}</b></div>", unsafe_allow_html=True)
                
                # Tabelle berechnen
                tabelle = sorted(g_teams, key=lambda x: (punkte[x], tordifferenz[x]), reverse=True)
                all_group_tables[g] = {"tabelle": tabelle, "punkte": punkte}
                st.markdown("</div>", unsafe_allow_html=True)

        # Qualifikanten ermitteln (Top 2 + 8 beste Dritte)
        ko_32_teams = []
        drittplatzierte = []
        
        for g in groups:
            tab = all_group_tables[g]["tabelle"]
            pts = all_group_tables[g]["punkte"]
            ko_32_teams.append(tab[0]) # 1. Platz
            ko_32_teams.append(tab[1]) # 2. Platz
            drittplatzierte.append((tab[2], pts[tab[2]])) # 3. Platz mit Punkten
            
        # Sortiere beste Dritte aus
        beste_dritte = sorted(drittplatzierte, key=lambda x: x[1], reverse=True)[:8]
        for t, p in beste_dritte:
            ko_32_teams.append(t)

        # --- SECHZEHNTELFINALE (Round of 32) ---
        st.write("---")
        st.header("📉 K-o.-Phase (Der Turnierbaum ab Runde der letzten 32)")
        
        col_r32, col_r16, col_vf, col_hf, col_f = st.columns(5)
        
        # Hilfsfunktion für sauberes Rendering im Baum
        def run_stage(team_list, column, stage_title, color):
            winners = []
            with column:
                st.subheader(stage_title)
                for i in range(0, len(team_list), 2):
                    t1, t2 = team_list[i], team_list[i+1]
                    res = simuliere_spiel(t1, t2, ko=True)
                    winners.append(res["winner"])
                    st.markdown(f"""
                        <div style='background:#1e293b; padding:10px; border-radius:12px; margin-bottom:8px; border-left:4px solid {color};'>
                            <small>{t1} vs {t2}</small><br>
                            <b>{res['score1']}:{res['score2']}</b> ➔ <b>{res['winner']}</b>
                        </div>
                    """, unsafe_allow_html=True)
            return winners

        # Durchführung aller K-o.-Runden
        r16_teams = run_stage(ko_32_teams, col_r32, "💥 Runde von 32", "#a855f7")
        vf_teams = run_stage(r16_teams, col_r16, "⚡ Achtelfinale", "#ec4899")
        hf_teams = run_stage(vf_teams, col_vf, "⚔️ Viertelfinale", "#f43f5e")
        final_teams = run_stage(hf_teams, col_hf, "🛡️ Halbfinale", "#eab308")
        
        # Finale & Siegerehrung
        with col_f:
            st.subheader("👑 Finale")
            f_res = simuliere_spiel(final_teams[0], final_teams[1], ko=True)
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%); padding: 25px; border-radius: 16px; text-align: center; color: white; box-shadow: 0 10px 25px rgba(234,179,8,0.4);'>
                    <h4 style='margin:0;'>WELTMEISTER 2026</h4>
                    <h2 style='margin:10px 0;'>🥇 {f_res['winner']} 🥇</h2>
                    <p style='margin:0; font-size:1.1rem;'>Ergebnis: <b>{f_res['score1']}:{f_res['score2']}</b></p>
                    <small style='opacity:0.9;'>Gegner: {final_teams[1] if f_res['winner'] == final_teams[0] else final_teams[0]}</small>
                </div>
            """, unsafe_allow_html=True)
