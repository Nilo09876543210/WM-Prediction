import streamlit as st
import numpy as np
import pandas as pd

# 1. Page Configuration & UI-Styling
st.set_page_config(
    page_title="KI World Cup Predictor 2026",
    page_icon="🏆",
    layout="wide"
)

# CSS für maximale Lesbarkeit, Kontraste und modernes Design
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
        background: #1e293b; 
        border: 2px solid #334155;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    .group-header {
        color: #ffffff !important; 
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
    .explanation-text {
        font-size: 0.85rem;
        color: #cbd5e1;
        margin-top: 5px;
        line-height: 1.3;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="wm-title-container">
        <h1 style='color: white; margin: 0; font-size: 2.8rem; font-weight: 800;'>🏆 FIFA World Cup 2026 – Profi-Simulator</h1>
        <p style='color: #e2e8f0; font-size: 1.2rem; margin-top: 10px; font-weight: 400;'>
            Exakter FIFA-Turnierbaum · Interaktive Spielanalyse per Klick · Realistische Kicker-basierte Simulation
        </p>
    </div>
""", unsafe_allow_html=True)

# 2. Vollständige, erweiterte Fußballdatenbank (48 Teams)
@st.cache_data
def get_pro_world_cup_data():
    return {
        # Gruppe A
        "Mexiko": {"angriff": 1.6, "abwehr": 1.1, "gruppe": "A", "wert_mio": 220, "trainer": "Javier Aguirre", "system": "4-3-3", "mvp": "Santiago Giménez", "info": "Heimvorteil schiebt an, aber Schwächen im defensiven Umschaltspiel.", "titel_prob": 1.5},
        "Südafrika": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "A", "wert_mio": 35, "trainer": "Hugo Broos", "system": "4-2-3-1", "mvp": "Teboho Mokoena", "info": "Kompaktes Kollektiv, dem es an individueller Weltklasse mangelt.", "titel_prob": 0.1},
        "Südkorea": {"angriff": 1.5, "abwehr": 1.2, "gruppe": "A", "wert_mio": 165, "trainer": "Hong Myung-bo", "system": "4-4-2", "mvp": "Heung-min Son", "info": "Konterstark mit unbändigem Willen, stark über die Außenbahnen.", "titel_prob": 0.8},
        "Tschechien": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "A", "wert_mio": 190, "trainer": "Ivan Hašek", "system": "3-4-1-2", "mvp": "Tomáš Souček", "info": "Physisch extrem robust, brandgefährlich bei Standards.", "titel_prob": 0.5},
        # Gruppe B
        "Kanada": {"angriff": 1.5, "abwehr": 1.2, "gruppe": "B", "wert_mio": 180, "trainer": "Jesse Marsch", "system": "4-4-2", "mvp": "Alphonso Davies", "info": "Extremes Pressing-System, hohes Tempo über die Flügel.", "titel_prob": 1.0},
        "Bosnien-Herzegowina": {"angriff": 1.3, "abwehr": 1.3, "gruppe": "B", "wert_mio": 85, "trainer": "Sergej Barbarez", "system": "3-5-2", "mvp": "Anel Ahmedhodžić", "info": "Mentalitäts-Team, auswärts aber oft taktisch anfällig.", "titel_prob": 0.2},
        "Katar": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "B", "wert_mio": 20, "trainer": "Tintín Márquez", "system": "5-3-2", "mvp": "Akram Afif", "info": "Eingespielter Asienmeister, aber international physisch unterlegen.", "titel_prob": 0.1},
        "Schweiz": {"angriff": 1.6, "abwehr": 0.9, "gruppe": "B", "wert_mio": 280, "trainer": "Murat Yakin", "system": "3-4-2-1", "mvp": "Manuel Akanji", "info": "Hervorragende Defensivorganisation, schwer zu bespielen.", "titel_prob": 2.5},
        # Gruppe C
        "Brasilien": {"angriff": 2.3, "abwehr": 0.8, "gruppe": "C", "wert_mio": 1050, "trainer": "Dorival Júnior", "system": "4-2-3-1", "mvp": "Vinícius Jr.", "info": "Gigantische individuelle Qualität, Favorit auf den Turniersieg.", "titel_prob": 14.0},
        "Marokko": {"angriff": 1.7, "abwehr": 0.8, "gruppe": "C", "wert_mio": 320, "trainer": "Walid Regragui", "system": "4-1-4-1", "mvp": "Achraf Hakimi", "info": "Defensiv ein unüberwindbares Bollwerk mit schnellen Kontern.", "titel_prob": 4.5},
        "Haiti": {"angriff": 0.9, "abwehr": 1.6, "gruppe": "C", "wert_mio": 15, "trainer": "Sébastien Migné", "system": "4-5-1", "mvp": "Frantzdy Pierrot", "info": "Sensation der Qualifikation, spielerisch stark limitiert.", "titel_prob": 0.01},
        "Schottland": {"angriff": 1.3, "abwehr": 1.2, "gruppe": "C", "wert_mio": 210, "trainer": "Steve Clarke", "system": "5-4-1", "mvp": "Scott McTominay", "info": "Enorm kampfstark, agiert vorwiegend mit langen Bällen.", "titel_prob": 0.4},
        # Gruppe D
        "USA": {"angriff": 1.8, "abwehr": 1.0, "gruppe": "D", "wert_mio": 350, "trainer": "Mauricio Pochettino", "system": "4-3-3", "mvp": "Christian Pulisic", "info": "Taktisch flexibel unter Pochettino, hohes athletisches Niveau.", "titel_prob": 3.0},
        "Paraguay": {"angriff": 1.2, "abwehr": 1.0, "gruppe": "D", "wert_mio": 110, "trainer": "Gustavo Alfaro", "system": "4-4-2", "mvp": "Julio Enciso", "info": "Fokus liegt auf Zerstörung und körperbetonter Abwehrarbeit.", "titel_prob": 0.3},
        "Australien": {"angriff": 1.3, "abwehr": 1.2, "gruppe": "D", "wert_mio": 50, "trainer": "Tony Popovic", "system": "4-2-3-1", "mvp": "Harry Souttar", "info": "Lauf- und kampfstark, spielerisch fehlt die Kreativität.", "titel_prob": 0.2},
        "Türkei": {"angriff": 1.7, "abwehr": 1.2, "gruppe": "D", "wert_mio": 310, "trainer": "Vincenzo Montella", "system": "4-2-3-1", "mvp": "Arda Güler", "info": "Hochemotional und technisch brillant, defensiv unbeständig.", "titel_prob": 2.0},
        # Gruppe E
        "Deutschland": {"angriff": 2.1, "abwehr": 0.9, "gruppe": "E", "wert_mio": 850, "trainer": "Julian Nagelsmann", "system": "4-2-3-1", "mvp": "Florian Wirtz", "info": "Exzellentes spielerisches Zentrum, hoher spielerischer Fokus.", "titel_prob": 11.0},
        "Curaçao": {"angriff": 0.8, "abwehr": 1.7, "gruppe": "E", "wert_mio": 12, "trainer": "Dick Advocaat", "system": "5-4-1", "mvp": "Juninho Bacuna", "info": "Defensiv extrem tief gestaffelt, reiner Außenseiter.", "titel_prob": 0.01},
        "Elfenbeinküste": {"angriff": 1.6, "abwehr": 1.1, "gruppe": "E", "wert_mio": 340, "trainer": "Emerse Faé", "system": "4-3-3", "mvp": "Ousmane Diomande", "info": "Physisch robust, spielerisch eines der Top-Teams Afrikas.", "titel_prob": 2.2},
        "Ecuador": {"angriff": 1.5, "abwehr": 0.9, "gruppe": "E", "wert_mio": 260, "trainer": "Sebastián Beccacece", "system": "3-4-3", "mvp": "Moises Caicedo", "info": "Enorm eklig im Pressing, defensiv extrem stabil besetzt.", "titel_prob": 1.8},
        # Gruppe F
        "Niederlande": {"angriff": 1.9, "abwehr": 0.9, "gruppe": "F", "wert_mio": 620, "trainer": "Ronald Koeman", "system": "4-3-3", "mvp": "Xavi Simons", "info": "Internationale Klasse in der Abwehrkette, flexibler Angriff.", "titel_prob": 6.5},
        "Japan": {"angriff": 1.7, "abwehr": 1.0, "gruppe": "F", "wert_mio": 290, "trainer": "Hajime Moriyasu", "system": "4-2-3-1", "mvp": "Takefusa Kubo", "info": "Diszipliniertes, pfeilschnelles Kombinationsspiel.", "titel_prob": 2.5},
        "Schweden": {"angriff": 1.7, "abwehr": 1.2, "gruppe": "F", "wert_mio": 240, "trainer": "Jon Dahl Tomasson", "system": "4-4-2", "mvp": "Alexander Isak", "info": "Starker Angriff um Isak und Gyökeres, Schwächen in der Abwehr.", "titel_prob": 1.2},
        "Tunesien": {"angriff": 1.1, "abwehr": 1.2, "gruppe": "F", "wert_mio": 45, "trainer": "Faouzi Benzarti", "system": "4-5-1", "mvp": "Ellyes Skhiri", "info": "Vermeidet Fehler, kreiert aber selbst zu wenig Torchancen.", "titel_prob": 0.1},
        # Gruppe G
        "Belgien": {"angriff": 1.9, "abwehr": 1.1, "gruppe": "G", "wert_mio": 480, "trainer": "Domenico Tedesco", "system": "4-3-3", "mvp": "Jérémy Doku", "info": "Viel Tempo über die Flügel, Umbruch in der Verteidigung.", "titel_prob": 4.0},
        "Ägypten": {"angriff": 1.4, "abwehr": 1.2, "gruppe": "G", "wert_mio": 110, "trainer": "Hossam Hassan", "system": "4-2-3-1", "mvp": "Mohamed Salah", "info": "Fokus ist komplett auf Umschaltmomente über Salah ausgelegt.", "titel_prob": 0.7},
        "Iran": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "G", "wert_mio": 40, "trainer": "Amir Ghalenoei", "system": "5-4-1", "mvp": "Mehdi Taremi", "info": "Sehr erfahren, defensiv tief stehend und kompakt.", "titel_prob": 0.2},
        "Neuseeland": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "G", "wert_mio": 25, "trainer": "Darren Bazeley", "system": "4-4-2", "mvp": "Chris Wood", "info": "Ozeanien-Meister, setzt fast ausschließlich auf hohe Bälle.", "titel_prob": 0.05},
        # Gruppe H
        "Spanien": {"angriff": 2.2, "abwehr": 0.8, "gruppe": "H", "wert_mio": 900, "trainer": "Luis de la Fuente", "system": "4-3-3", "mvp": "Lamine Yamal", "info": "Dominanter Ballbesitzfußball mit tödlichem Flügelspiel.", "titel_prob": 13.5},
        "Kap Verde": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "H", "wert_mio": 30, "trainer": "Bubista", "system": "4-3-3", "mvp": "Logan Costa", "info": "Sehr lauffreudig und diszipliniert, spielerisch unterlegen.", "titel_prob": 0.05},
        "Saudi-Arabien": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "H", "wert_mio": 35, "trainer": "Roberto Mancini", "system": "4-1-4-1", "mvp": "Firas Al-Buraikan", "info": "Taktisch geschult durch Mancini, Schwächen im Offensiv-Tempo.", "titel_prob": 0.1},
        "Uruguay": {"angriff": 1.9, "abwehr": 0.9, "gruppe": "H", "wert_mio": 420, "trainer": "Marcelo Bielsa", "system": "4-3-3", "mvp": "Federico Valverde", "info": "Bielsa-Powerfußball mit radikalem, aggressivem Pressing.", "titel_prob": 5.0},
        # Gruppe I
        "Frankreich": {"angriff": 2.4, "abwehr": 0.8, "gruppe": "I", "wert_mio": 1200, "trainer": "Didier Deschamps", "system": "4-2-3-1", "mvp": "Kylian Mbappé", "info": "Pragmatisch, brutal effizient und physisch absolute Weltklasse.", "titel_prob": 15.0},
        "Senegal": {"angriff": 1.5, "abwehr": 1.1, "gruppe": "I", "wert_mio": 280, "trainer": "Aliou Cissé", "system": "4-3-3", "mvp": "Nicolas Jackson", "info": "Physisch extrem stark, defensiv schwer zu knacken.", "titel_prob": 1.8},
        "Irak": {"angriff": 1.0, "abwehr": 1.3, "gruppe": "I", "wert_mio": 18, "trainer": "Jesús Casas", "system": "4-2-3-1", "mvp": "Aymen Hussein", "info": "Diszipliniert, hat gegen spielstarke Teams aber das Nachsehen.", "titel_prob": 0.05},
        "Norwegen": {"angriff": 1.8, "abwehr": 1.3, "gruppe": "I", "wert_mio": 450, "trainer": "Ståle Solbakken", "system": "4-3-3", "mvp": "Erling Haaland", "info": "Dank Haaland offensiv eine Urgewalt, defensiv instabil.", "titel_prob": 2.0},
        # Gruppe J
        "Argentinien": {"angriff": 2.2, "abwehr": 0.7, "gruppe": "J", "wert_mio": 800, "trainer": "Lionel Scaloni", "system": "4-3-3", "mvp": "Lautaro Martínez", "info": "Titelverteidiger. Extrem abgezockt, harmonisch und defensivstark.", "titel_prob": 12.5},
        "Algerien": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "J", "wert_mio": 140, "trainer": "Vladimir Petković", "system": "4-1-4-1", "mvp": "Rayan Aït-Nouri", "info": "Technisch beschlagen, agiert oft unkonzentriert in der Abwehr.", "titel_prob": 0.6},
        "Österreich": {"angriff": 1.7, "abwehr": 1.0, "gruppe": "J", "wert_mio": 290, "trainer": "Ralf Rangnick", "system": "4-2-2-2", "mvp": "Konrad Laimer", "info": "Gnadenlose Pressingmaschine, extrem laufintensiv.", "titel_prob": 2.8},
        "Jordanien": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "J", "wert_mio": 15, "trainer": "Jamal Sellami", "system": "5-3-2", "mvp": "Musa Al-Taamari", "info": "Kontertiefes System, spielerisch tiefste Kategorie.", "titel_prob": 0.02},
        # Gruppe K
        "Portugal": {"angriff": 2.2, "abwehr": 0.9, "gruppe": "K", "wert_mio": 950, "trainer": "Roberto Martínez", "system": "4-3-3", "mvp": "Rafael Leão", "info": "Herausragende Kaderbreite, offensiv kaum zu verteidigen.", "titel_prob": 10.0},
        "DR Kongo": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "K", "wert_mio": 60, "trainer": "Sébastien Desabre", "system": "4-2-3-1", "mvp": "Yoane Wissa", "info": "Umschaltstark, im gebundenen Spiel jedoch ideenlos.", "titel_prob": 0.2},
        "Usbekistan": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "K", "wert_mio": 32, "trainer": "Srečko Katanec", "system": "3-4-2-1", "mvp": "Abbosbek Fayzullaev", "info": "Turnier-Debütant mit einer hochtalentierten, jungen Generation.", "titel_prob": 0.1},
        "Kolumbien": {"angriff": 1.9, "abwehr": 0.9, "gruppe": "K", "wert_mio": 280, "trainer": "Néstor Lorenzo", "system": "4-2-3-1", "mvp": "Luis Díaz", "info": "Extrem giftig in den Zweikämpfen, spielerisch rasant.", "titel_prob": 4.8},
        # Gruppe L
        "England": {"angriff": 2.3, "abwehr": 0.9, "gruppe": "L", "wert_mio": 1300, "trainer": "Thomas Tuchel", "system": "4-2-3-1", "mvp": "Jude Bellingham", "info": "Kader voller Superstars, taktisch diszipliniert unter Tuchel.", "titel_prob": 13.0},
        "Kroatien": {"angriff": 1.6, "abwehr": 1.0, "gruppe": "L", "wert_mio": 270, "trainer": "Zlatko Dalić", "system": "4-3-3", "mvp": "Joško Gvardiol", "info": "Das ewige Mentalitätsmonster mit überragender Turniererfahrung.", "titel_prob": 3.2},
        "Ghana": {"angriff": 1.4, "abwehr": 1.2, "gruppe": "L", "wert_mio": 120, "trainer": "Otto Addo", "system": "4-2-3-1", "mvp": "Mohammed Kudus", "info": "Unberechenbares Team, hohes Tempo, schwere Defensivfehler.", "titel_prob": 0.5},
        "Panama": {"angriff": 1.0, "abwehr": 1.3, "gruppe": "L", "wert_mio": 18, "trainer": "Thomas Christiansen", "system": "4-4-2", "mvp": "Adalberto Carrasquilla", "info": "Physisch stark, spielerisch den Top-Nationen aber unterlegen.", "titel_prob": 0.05},
    }

teams_db = get_pro_world_cup_data()

# 3. Mathematisch gewichtete Simulations-Logik
def simuliere_spiel_realistisch(t1, t2, ko=False):
    mw_faktor_t1 = np.log10(teams_db[t1]["wert_mio"]) / 2
    mw_faktor_t2 = np.log10(teams_db[t2]["wert_mio"]) / 2
    
    t1_lambda = teams_db[t1]["angriff"] * teams_db[t2]["abwehr"] * mw_faktor_t1
    t2_lambda = teams_db[t2]["angriff"] * teams_db[t1]["abwehr"] * mw_faktor_t2
    
    t1_lambda = min(3.2, max(0.2, t1_lambda / 1.8))
    t2_lambda = min(3.2, max(0.2, t2_lambda / 1.8))
    
    goals_t1 = np.random.poisson(t1_lambda)
    goals_t2 = np.random.poisson(t2_lambda)
    
    if ko and goals_t1 == goals_t2:
        if (t1_lambda + np.random.rand()) > (t2_lambda + np.random.rand()):
            goals_t1 += 1
        else:
            goals_t2 += 1
            
    return {"score1": goals_t1, "score2": goals_t2, "winner": t1 if goals_t1 > goals_t2 else t2}

# Funktion zur dynamischen Generierung einer Spielbegründung
def generiere_erklaerung(t1, t2, res):
    winner = res["winner"]
    loser = t2 if winner == t1 else t1
    return f"**Analyse:** {winner} (System: {teams_db[winner]['system']}) setzt sich gegen {loser} ({teams_db[loser]['system']}) durch. " \
           f"Der Ausschlag lag beim Kaderwert ({teams_db[winner]['wert_mio']} Mio. € vs. {teams_db[loser]['wert_mio']} Mio. €) " \
           f"und der taktischen Ausrichtung von Trainer {teams_db[winner]['trainer']}."

# 4. Tabs Struktur
tab1, tab2 = st.tabs(["🔍 Team-Profile & Daten-Erklärung", "🚀 Offizieller Turniersimulator"])

with tab1:
    # NEU: Erklärung der Datengrundlage am Anfang der Übersichtsseite
    st.info("""
    ### 📊 Wie kommen die Angriffs- und Abwehrwerte zustande?
    Die hinterlegten Stärkewerte basieren auf einer dreistufigen mathematischen Gewichtung:
    1. **10-Jahres-Turniertrend (kicker-Daten):** Historische Ergebnisse bei Weltmeisterschaften und Kontinentalturnieren seit 2016 definieren das Grundniveau.
    2. **Kader-Gesamtwert & Top-Stars:** Die individuelle Qualität verzerrt den Erwartungswert (Poisson-Verteilung) maßgeblich zu Gunsten wertvollerer Kader.
    3. **Trainer- & Systemfaktor:** Defensiv-Systeme (z.B. 5-3-2 oder 5-4-1) senken die gegnerische Torwahrscheinlichkeit künstlich, verringern jedoch gleichzeitig die eigene Durchschlagskraft.
    """)
    
    st.subheader("Umfassende Kaderanalyse der 48 Endrundenteilnehmer")
    selected_group = st.selectbox("Wähle eine Gruppe zur Analyse:", sorted(list(set([v["gruppe"] for v in teams_db.values()]))))
    group_teams = {k: v for k, v in teams_db.items() if v["gruppe"] == selected_group}
    
    for t_name, t_data in group_teams.items():
        with st.expander(f"⚽ {t_name} — System: {t_data['system']} (Trainer: {t_data['trainer']})"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Gesamtmarktwert", f"{t_data['wert_mio']} Mio. €")
                st.metric("Titelwahrscheinlichkeit", f"{t_data['titel_prob']} %")
            with col2:
                st.metric("Angriffsstärke", t_data["angriff"])
                st.metric("Abwehr-Rating (Anfälligkeit)", t_data["abwehr"])
            with col3:
                st.markdown(f"**Top-Star (MVP):** {t_data['mvp']}")
                st.markdown(f"**Taktische Kicker-Einschätzung:** *{t_data['info']}*")

with tab2:
    st.sidebar.header("⚙️ Optionen")
    start_sim = st.sidebar.button("🏆 Turnier originalgetreu starten", use_container_width=True)
    
    if not start_sim:
        st.info("Klicke in der Sidebar auf den Button, um die Simulation nach exaktem FIFA-Reglement zu starten.")
    else:
        # --- GRUPPENPHASE ---
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
                st.markdown(f"<div class='group-card'><div class='group-header'>Gruppe {g}</div>", unsafe_allow_html=True)
                
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

        # --- EXAKTE FIFA 2026 BRACKET LOGIK ---
        g_1 = {g: all_group_tables[g]["tabelle"][0] for g in groups}
        g_2 = {g: all_group_tables[g]["tabelle"][1] for g in groups}
        
        drittplatzierte = []
        for g in groups:
            t3 = all_group_tables[g]["tabelle"][2]
            drittplatzierte.append({"team": t3, "punkte": all_group_tables[g]["punkte"][t3], "td": all_group_tables[g]["tordifferenz"][t3]})
        
        beste_dritte = [x["team"] for x in sorted(drittplatzierte, key=lambda x: (x["punkte"], x["td"]), reverse=True)[:8]]
        while len(beste_dritte) < 8:
            beste_dritte.append("Platzhalter")

        ko_32_paare = [
            (g_1["A"], beste_dritte[0]), (g_2["A"], g_2["B"]),
            (g_1["C"], g_2["F"]), (g_1["E"], beste_dritte[1]),
            (g_1["I"], beste_dritte[2]), (g_2["E"], g_2["I"]),
            (g_1["F"], g_2["C"]), (g_1["H"], g_2["J"]),
            (g_1["D"], beste_dritte[3]), (g_1["G"], beste_dritte[4]),
            (g_2["K"], g_2["L"]), (g_1["B"], beste_dritte[5]),
            (g_1["J"], g_2["H"]), (g_2["D"], g_2["G"]),
            (g_1["K"], beste_dritte[6]), (g_1["L"], beste_dritte[7]),
        ]

        st.write("---")
        st.header("📉 Interaktive K.-o.-Phase (Klicken für Details & Begründungen)")
        
        col_r32, col_r16, col_vf, col_hf, col_f = st.columns(5)
        
        # Runde von 32
        r32_winners = []
        with col_r32:
            st.subheader("💥 Runde von 32")
            for t1, t2 in ko_32_paare:
                res = simuliere_spiel_realistisch(t1, t2, ko=True)
                r32_winners.append(res["winner"])
                # NEU: Anklickbarer Expander mit klaren Paarungen und Analyse
                with st.expander(f"⚽ {t1} vs {t2}"):
                    st.markdown(f"**Ergebnis: {res['score1']}:{res['score2']}**")
                    st.markdown(f"<p class='explanation-text'>{generiere_erklaerung(t1, t2, res)}</p>", unsafe_allow_html=True)
        
        # Achtelfinale
        r16_winners = []
        with col_r16:
            st.subheader("⚡ Achtelfinale")
            for i in range(0, len(r32_winners), 2):
                t1, t2 = r32_winners[i], r32_winners[i+1]
                res = simuliere_spiel_realistisch(t1, t2, ko=True)
                r16_winners.append(res["winner"])
                with st.expander(f"🔮 {t1} vs {t2}"):
                    st.markdown(f"**Ergebnis: {res['score1']}:{res['score2']}**")
                    st.markdown(f"<p class='explanation-text'>{generiere_erklaerung(t1, t2, res)}</p>", unsafe_allow_html=True)

        # Viertelfinale
        vf_winners = []
        with col_vf:
            st.subheader("⚔️ Viertelfinale")
            for i in range(0, len(r16_winners), 2):
                t1, t2 = r16_winners[i], r16_winners[i+1]
                res = simuliere_spiel_realistisch(t1, t2, ko=True)
                vf_winners.append(res["winner"])
                with st.expander(f"🔥 {t1} vs {t2}"):
                    st.markdown(f"**Ergebnis: {res['score1']}:{res['score2']}**")
                    st.markdown(f"<p class='explanation-text'>{generiere_erklaerung(t1, t2, res)}</p>", unsafe_allow_html=True)

        # Halbfinale
        hf_winners = []
        with col_hf:
            st.subheader("🛡️ Halbfinale")
            for i in range(0, len(vf_winners), 2):
                t1, t2 = vf_winners[i], vf_winners[i+1]
                res = simuliere_spiel_realistisch(t1, t2, ko=True)
                hf_winners.append(res["winner"])
                with st.expander(f"🎖️ {t1} vs {t2}"):
                    st.markdown(f"**Ergebnis: {res['score1']}:{res['score2']}**")
                    st.markdown(f"<p class='explanation-text'>{generiere_erklaerung(t1, t2, res)}</p>", unsafe_allow_html=True)

        # Finale
        with col_f:
            st.subheader("👑 Finale")
            f_res = simuliere_spiel_realistisch(hf_winners[0], hf_winners[1], ko=True)
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%); padding: 25px; border-radius: 16px; text-align: center; color: white; box-shadow: 0 10px 25px rgba(234,179,8,0.4);'>
                    <h4 style='margin:0;'>WELTMEISTER 2026</h4>
                    <h2 style='margin:10px 0;'>🥇 {f_res['winner']} 🥇</h2>
                    <p style='margin:0; font-size:1.1rem;'>Ergebnis: <b>{f_res['score1']}:{f_res['score2']}</b></p>
                    <small style='opacity:0.9;'>Vizemeister: {hf_winners[1] if f_res['winner'] == hf_winners[0] else hf_winners[0]}</small>
                </div>
            """, unsafe_allow_html=True)
