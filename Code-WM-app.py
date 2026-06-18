import streamlit as st
import numpy as np
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="KI World Cup Predictor 2026",
    page_icon="🏆",
    layout="wide"
)

# Sauberes Grundstyling für das Hintergrundbild und den Titel
bg_url = "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1600&auto=format&fit=crop"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    .stApp {{
        background: url('{bg_url}') no-repeat center center fixed; 
        background-size: cover;
    }}
    
    html, body, [class*="css"], .stMarkdown, p, li {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}
    
    .main-title {{ 
        font-size: 3.5rem; 
        font-weight: 800; 
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; 
        margin-bottom: 0.2rem; 
        letter-spacing: -1px;
    }}
    
    .subtitle {{ 
        font-size: 1.2rem; 
        text-align: center; 
        color: #e2e8f0; 
        font-weight: 500;
        margin-bottom: 3rem; 
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏆 FIFA World Cup 2026 Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">48 Teams · 12 Gruppen · KI-Simulation basierend auf Formstärke & Transfermarkt-Daten</div>', unsafe_allow_html=True)

# 2. Erweiterte Datenbank (Beispiele für Top-Teams voll ausgebaut)
@st.cache_data
def get_world_cup_2026_data():
    return {
        "Deutschland": {
            "angriff": 2.0, "abwehr": 1.0, "gruppe": "E", 
            "kaderwert": "950 Mio. €", "trainer": "Julian Nagelsmann", "system": "4-2-3-1 (Dominantes Ballbesitz- & Pressingspiel)",
            "mvp": "Florian Wirtz", "wert": "130 Mio. €", 
            "info": "Zurück in der Weltspitze. Extrem kreatives Mittelfeldzentrum mit viel Tiefgang."
        },
        "Frankreich": {
            "angriff": 2.3, "abwehr": 0.8, "gruppe": "I", 
            "kaderwert": "1.20 Mrd. €", "trainer": "Didier Deschamps", "system": "4-3-3 (Umschaltstark mit enormem Flügeltempo)",
            "mvp": "Kylian Mbappé", "wert": "180 Mio. €", 
            "info": "Der wertvollste Kader des Turniers. Unglaubliche Physis und individuelle Qualität im Überfluss."
        },
        "Argentinien": {
            "angriff": 2.1, "abwehr": 0.7, "gruppe": "J", 
            "kaderwert": "850 Mio. €", "trainer": "Lionel Scaloni", "system": "4-3-3 / 4-4-2 (Kompaktes Zentrum, hohe Spielintelligenz)",
            "mvp": "Lautaro Martínez", "wert": "110 Mio. €", 
            "info": "Titelverteidiger. Extrem abgezockt, eingespielt und defensiv kaum zu knacken."
        },
        "England": {
            "angriff": 2.2, "abwehr": 0.9, "gruppe": "L", 
            "kaderwert": "1.15 Mrd. €", "trainer": "Thomas Tuchel", "system": "3-4-2-1 (Flexibler Offensivfußball mit starkem Gegenpressing)",
            "mvp": "Jude Bellingham", "wert": "180 Mio. €", 
            "info": "Kader voller internationaler Superstars. Unter Tuchel taktisch noch unberechenbarer."
        },
        "Spanien": {
            "angriff": 2.1, "abwehr": 0.8, "gruppe": "H", 
            "kaderwert": "900 Mio. €", "trainer": "Luis de la Fuente", "system": "4-3-3 (Klassisches Positionsspiel mit extrem schnellen Flügeln)",
            "mvp": "Lamine Yamal", "wert": "120 Mio. €", 
            "info": "Ballbesitz-Könige, die durch junge, vertikale Dribbler extrem gefährlich geworden sind."
        },
        "Brasilien": {
            "angriff": 2.2, "abwehr": 0.8, "gruppe": "C", 
            "kaderwert": "1.05 Mrd. €", "trainer": "Dorival Júnior", "system": "4-2-3-1 (Kreatives Offensivspiel, Fokus auf 1-gegen-1-Situationen)",
            "mvp": "Vinicius Jr.", "wert": "180 Mio. €", 
            "info": "Traditionell enorme Offensivpower mit Weltklasse-Individualisten auf den Außenbahnen."
        },
        # (Die restlichen Teams werden zur Vereinfachung mit Standardwerten gefüllt – im echten Code erweiterbar)
        "Mexiko": {"angriff": 1.6, "abwehr": 1.1, "gruppe": "A", "kaderwert": "220 Mio. €", "trainer": "Javier Aguirre", "system": "4-3-3", "mvp": "Santiago Giménez", "wert": "40 Mio. €", "info": "Heimvorteil."},
        "Südafrika": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "A", "kaderwert": "30 Mio. €", "trainer": "Hugo Broos", "system": "4-5-1", "mvp": "Teboho Mokoena", "wert": "4 Mio. €", "info": "Kompakt."},
        "Südkorea": {"angriff": 1.5, "abwehr": 1.2, "gruppe": "A", "kaderwert": "170 Mio. €", "trainer": "Hong Myung-bo", "system": "4-2-3-1", "mvp": "Heung-min Son", "wert": "45 Mio. €", "info": "Konterstark."},
        "Tschechien": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "A", "kaderwert": "190 Mio. €", "trainer": "Ivan Hašek", "system": "3-4-2-1", "mvp": "Tomas Soucek", "wert": "30 Mio. €", "info": "Standards."},
        "Kanada": {"angriff": 1.5, "abwehr": 1.2, "gruppe": "B", "kaderwert": "180 Mio. €", "trainer": "Jesse Marsch", "system": "4-4-2", "mvp": "Alphonso Davies", "wert": "50 Mio. €", "info": "Tempo."},
        "Bosnien-Herzegowina": {"angriff": 1.3, "abwehr": 1.3, "gruppe": "B", "kaderwert": "80 Mio. €", "trainer": "Sergej Barbarez", "system": "4-2-3-1", "mvp": "A. Ahmedhodzic", "wert": "18 Mio. €", "info": "Playoffs."},
        "Katar": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "B", "kaderwert": "20 Mio. €", "trainer": "Tintín Márquez", "system": "5-3-2", "mvp": "Akram Afif", "wert": "5 Mio. €", "info": "Eingespielt."},
        "Schweiz": {"angriff": 1.5, "abwehr": 0.9, "gruppe": "B", "kaderwert": "280 Mio. €", "trainer": "Murat Yakin", "system": "3-4-2-1", "mvp": "Manuel Akanji", "wert": "45 Mio. €", "info": "Turniererfahren."},
        "Marokko": {"angriff": 1.6, "abwehr": 0.8, "gruppe": "C", "kaderwert": "350 Mio. €", "trainer": "Walid Regragui", "system": "4-1-4-1", "mvp": "Achraf Hakimi", "wert": "60 Mio. €", "info": "Konterstark."},
        "Haiti": {"angriff": 0.9, "abwehr": 1.6, "gruppe": "C", "kaderwert": "15 Mio. €", "trainer": "Sébastien Migné", "system": "4-4-2", "mvp": "Frantzdy Pierrot", "wert": "3 Mio. €", "info": "Außenseiter."},
        "Schottland": {"angriff": 1.3, "abwehr": 1.2, "gruppe": "C", "kaderwert": "210 Mio. €", "trainer": "Steve Clarke", "system": "5-4-1", "mvp": "Scott McTominay", "wert": "32 Mio. €", "info": "Kampfstark."},
        "USA": {"angriff": 1.7, "abwehr": 1.0, "gruppe": "D", "kaderwert": "320 Mio. €", "trainer": "Mauricio Pochettino", "system": "4-3-3", "mvp": "Christian Pulisic", "wert": "40 Mio. €", "info": "Heim-WM."},
        "Paraguay": {"angriff": 1.2, "abwehr": 1.0, "gruppe": "D", "kaderwert": "130 Mio. €", "trainer": "Gustavo Alfaro", "system": "4-4-2", "mvp": "Julio Enciso", "wert": "22 Mio. €", "info": "Defensiv."},
        "Australien": {"angriff": 1.3, "abwehr": 1.2, "gruppe": "D", "kaderwert": "50 Mio. €", "trainer": "Tony Popovic", "system": "4-4-2", "mvp": "Harry Souttar", "wert": "15 Mio. €", "info": "Physisch."},
        "Türkei": {"angriff": 1.6, "abwehr": 1.2, "gruppe": "D", "kaderwert": "340 Mio. €", "trainer": "Vincenzo Montella", "system": "4-2-3-1", "mvp": "Arda Güler", "wert": "45 Mio. €", "info": "Technisch stark."},
        "Curaçao": {"angriff": 0.8, "abwehr": 1.7, "gruppe": "E", "kaderwert": "12 Mio. €", "trainer": "Dick Advocaat", "system": "4-5-1", "mvp": "Juninho Bacuna", "wert": "2 Mio. €", "info": "Exot."},
        "Elfenbeinküste": {"angriff": 1.5, "abwehr": 1.1, "gruppe": "E", "kaderwert": "310 Mio. €", "trainer": "Emerse Faé", "system": "4-3-3", "mvp": "Ousmane Diomande", "wert": "40 Mio. €", "info": "Physisch."},
        "Ecuador": {"angriff": 1.4, "abwehr": 0.9, "gruppe": "E", "kaderwert": "230 Mio. €", "trainer": "Sebastián Beccacece", "system": "3-4-3", "mvp": "Moises Caicedo", "wert": "75 Mio. €", "info": "Pressing."},
        "Niederlande": {"angriff": 1.8, "abwehr": 0.9, "gruppe": "F", "kaderwert": "700 Mio. €", "trainer": "Ronald Koeman", "system": "4-3-3", "mvp": "Xavi Simons", "wert": "80 Mio. €", "info": "Ausgewogen."},
        "Japan": {"angriff": 1.6, "abwehr": 1.1, "gruppe": "F", "kaderwert": "290 Mio. €", "trainer": "Hajime Moriyasu", "system": "4-2-3-1", "mvp": "Takefusa Kubo", "wert": "50 Mio. €", "info": "Diszipliniert."},
        "Schweden": {"angriff": 1.7, "abwehr": 1.2, "gruppe": "F", "kaderwert": "380 Mio. €", "trainer": "Jon Dahl Tomasson", "system": "4-2-3-1", "mvp": "Alexander Isak", "wert": "75 Mio. €", "info": "Starker Sturm."},
        "Tunesien": {"angriff": 1.1, "abwehr": 1.2, "gruppe": "F", "kaderwert": "45 Mio. €", "trainer": "Faouzi Benzarti", "system": "4-3-2-1", "mvp": "Ellyes Skhiri", "wert": "13 Mio. €", "info": "Kollektiv."},
        "Belgien": {"angriff": 1.8, "abwehr": 1.1, "gruppe": "G", "kaderwert": "580 Mio. €", "trainer": "Domenico Tedesco", "system": "4-3-3", "mvp": "Jérémy Doku", "wert": "65 Mio. €", "info": "Tempo."},
        "Ägypten": {"angriff": 1.4, "abwehr": 1.2, "gruppe": "G", "kaderwert": "120 Mio. €", "trainer": "Hossam Hassan", "system": "4-3-3", "mvp": "Mohamed Salah", "wert": "55 Mio. €", "info": "Salah-Fokus."},
        "Iran": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "G", "kaderwert": "40 Mio. €", "trainer": "Amir Ghalenoei", "system": "4-4-2", "mvp": "Mehdi Taremi", "wert": "10 Mio. €", "info": "Erfahren."},
        "Neuseeland": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "G", "kaderwert": "25 Mio. €", "trainer": "Darren Bazeley", "system": "4-4-2", "mvp": "Chris Wood", "wert": "7 Mio. €", "info": "Robust."},
        "Kap Verde": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "H", "kaderwert": "30 Mio. €", "trainer": "Pedro Bubista", "system": "4-3-3", "mvp": "Logan Costa", "wert": "12 Mio. €", "info": "Leidenschaft."},
        "Saudi-Arabien": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "H", "kaderwert": "25 Mio. €", "trainer": "Roberto Mancini", "system": "4-3-3", "mvp": "Firas Al-Buraikan", "wert": "6 Mio. €", "info": "Taktisch."},
        "Uruguay": {"angriff": 1.8, "abwehr": 0.9, "gruppe": "H", "kaderwert": "480 Mio. €", "trainer": "Marcelo Bielsa", "system": "4-3-3", "mvp": "Federico Valverde", "wert": "100 Mio. €", "info": "Powerfußball."},
        "Senegal": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "I", "kaderwert": "260 Mio. €", "trainer": "Aliou Cissé", "system": "4-3-3", "mvp": "Nicolas Jackson", "wert": "35 Mio. €", "info": "Physisch."},
        "Irak": {"angriff": 1.0, "abwehr": 1.3, "gruppe": "I", "kaderwert": "15 Mio. €", "trainer": "Jesús Casas", "system": "4-2-3-1", "mvp": "Aymen Hussein", "wert": "3 Mio. €", "info": "Kollektiv."},
        "Norwegen": {"angriff": 1.7, "abwehr": 1.3, "gruppe": "I", "kaderwert": "450 Mio. €", "trainer": "Ståle Solbakken", "system": "4-3-3", "mvp": "Erling Haaland", "wert": "18 Mio. €", "info": "Haand-Fokus."},
        "Algerien": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "J", "kaderwert": "220 Mio. €", "trainer": "Vladimir Petković", "system": "4-3-3", "mvp": "Rayan Aït-Nouri", "wert": "35 Mio. €", "info": "Technisch."},
        "Österreich": {"angriff": 1.6, "abwehr": 1.0, "gruppe": "J", "kaderwert": "290 Mio. €", "trainer": "Ralf Rangnick", "system": "4-2-2-2", "mvp": "Konrad Laimer", "wert": "30 Mio. €", "info": "Pressingmaschine."},
        "Jordanien": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "J", "kaderwert": "18 Mio. €", "trainer": "Jamal Sellami", "system": "5-4-1", "mvp": "Musa Al-Taamari", "wert": "8 Mio. €", "info": "Defensiv."},
        "Portugal": {"angriff": 2.1, "abwehr": 0.9, "gruppe": "K", "kaderwert": "980 Mio. €", "trainer": "Roberto Martínez", "system": "4-3-3", "mvp": "Rafael Leão", "wert": "90 Mio. €", "info": "Kaderbreite."},
        "DR Kongo": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "K", "kaderwert": "110 Mio. €", "trainer": "Sébastien Desabre", "system": "4-2-3-1", "mvp": "Yoane Wissa", "wert": "28 Mio. €", "info": "Konter."},
        "Usbekistan": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "K", "kaderwert": "45 Mio. €", "trainer": "Srečko Katanec", "system": "3-4-2-1", "mvp": "A. Fayzullaev", "wert": "12 Mio. €", "info": "Debütant."},
        "Kolumbien": {"angriff": 1.8, "abwehr": 0.9, "gruppe": "K", "kaderwert": "320 Mio. €", "trainer": "Néstor Lorenzo", "system": "4-2-3-1", "mvp": "Luis Díaz", "wert": "75 Mio. €", "info": "Formstark."},
        "Kroatien": {"angriff": 1.5, "abwehr": 1.0, "gruppe": "L", "kaderwert": "360 Mio. €", "trainer": "Zlatko Dalić", "system": "4-3-3", "mvp": "Josko Gvardiol", "wert": "75 Mio. €", "info": "Erfahren."},
        "Ghana": {"angriff": 1.4, "abwehr": 1.2, "gruppe": "L", "kaderwert": "240 Mio. €", "trainer": "Otto Addo", "system": "4-2-3-1", "mvp": "Mohammed Kudus", "wert": "50 Mio. €", "info": "Dynamisch."},
        "Panama": {"angriff": 1.0, "abwehr": 1.3, "gruppe": "L", "kaderwert": "25 Mio. €", "trainer": "Thomas Christiansen", "system": "3-4-3", "mvp": "A. Carrasquilla", "wert": "4 Mio. €", "info": "Robust."}
    }

teams_db = get_world_cup_2026_data()

# 3. Poisson Simulations-Logik
def simuliere_spiel(t1, t2, ko=False):
    t1_lambda = teams_db[t1]["angriff"] * teams_db[t2]["abwehr"]
    t2_lambda = teams_db[t2]["angriff"] * teams_db[t1]["abwehr"]
    
    sim_t1 = np.random.poisson(t1_lambda, 3000)
    sim_t2 = np.random.poisson(t2_lambda, 3000)
    
    goals_t1 = int(round(np.mean(sim_t1)))
    goals_t2 = int(round(np.mean(sim_t2)))
    
    if ko and goals_t1 == goals_t2:
        if np.random.rand() > 0.5: goals_t1 += 1
        else: goals_t2 += 1
        
    return {
        "score1": goals_t1, "score2": goals_t2,
        "winner": t1 if goals_t1 > goals_t2 else t2
    }

# 4. Haupt-Präsentation mit Tabs
tab1, tab2 = st.tabs(["🔍 Team-Einschätzungen (Kader-Details)", "🚀 KI-Turnier-Simulator"])

with tab1:
    st.subheader("Umfassende Kader-Analyse & Transfermarkt-Daten")
    selected_group = st.selectbox("Wähle eine Gruppe zur Analyse:", sorted(list(set([v["gruppe"] for v in teams_db.values()]))))
    
    group_teams = {k: v for k, v in teams_db.items() if v["gruppe"] == selected_group}
    
    for t_name, t_data in group_teams.items():
        # Native st.expander garantieren perfekte Lesbarkeit ohne CSS-Farbfehler!
        with st.expander(f"⚽ {t_name} (Gruppe {t_data['gruppe']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Coach:** {t_data['trainer']}")
                st.write(f"**Taktisches System:** {t_data['system']}")
                st.write(f"**Gesamtwert des Kaders:** {t_data['kaderwert']}")
            with col2:
                st.write(f"**Wertvollster Spieler (TM):** {t_data['mvp']} ({t_data['wert']})")
                st.write(f"**Offensiv-Rating:** {t_data['angriff']} | **Defensiv-Anfälligkeit:** {t_data['abwehr']}")
                st.write(f"**Kurz-Analyse:** {t_data['info']}")

with tab2:
    st.sidebar.header("⚙️ Optionen")
    start_sim = st.sidebar.button("🏆 WM 2026 simulieren", use_container_width=True)
    
    if not start_sim:
        st.info("Klicke auf den Button in der linken Sidebar, um die komplette Weltmeisterschaft live zu simulieren!")
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
            tordifferenz = {t: 0 for t
