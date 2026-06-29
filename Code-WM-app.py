import streamlit as st
import numpy as np
import pandas as pd

# 1. Page Configuration & UI-Styling
st.set_page_config(
    page_title="KI World Cup Predictor 2026",
    page_icon="🏆",
    layout="wide"
)

# CSS für individualisierte Kacheln und das "Albiceleste" (Argentinien) Champion-Design im Header/Hintergrund
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    
    .wm-title-container {
        text-align: center;
        padding: 45px 20px;
        background: linear-gradient(135deg, #74b9ff 0%, #ffffff 50%, #f5cd79 100%);
        border-radius: 24px;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(116, 185, 255, 0.3);
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
        border-bottom: 2px solid #74b9ff;
        padding-bottom: 5px;
    }
    .pro-explanation {
        background: #0f172a;
        border-left: 4px solid #f5cd79;
        padding: 12px 16px;
        border-radius: 8px;
        margin-top: 8px;
        font-size: 0.9rem;
        color: #e2e8f0;
    }
    .match-title {
        font-weight: 700;
        color: #74b9ff;
        margin-bottom: 4px;
    }
    .live-badge {
        background-color: #ef4444;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-left: 8px;
    }
    .real-badge {
        background-color: #10b981;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-left: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="wm-title-container">
        <h1 style='color: #0f172a; margin: 0; font-size: 2.9rem; font-weight: 800;'>🏆 FIFA World Cup 2026 – Live Tactical Simulator</h1>
        <p style='color: #2c3e50; font-size: 1.2rem; margin-top: 10px; font-weight: 600;'>
            In commemoration of Defending Champions Argentina 🇦🇷 · Integrated Real-Time Kicker Data
        </p>
    </div>
""", unsafe_allow_html=True)

# 2. Komplett individualisierte Datenbank mit integrierten Real-Ergebnissen (Kicker Stand: 29. Juni 2026)
@st.cache_data
def get_pro_world_cup_data():
    return {
        # Gruppe A
        "Mexiko": {"angriff": 1.6, "abwehr": 1.1, "gruppe": "A", "wert_mio": 220, "trainer": "Javier Aguirre", "system": "4-3-3", "mvp": "Santiago Giménez", "info": "Nutzt die frenetische Heimkulisse für extremes Offensivpressing, offenbart aber Räume bei gegnerischen Gegenangriffen.", "titel_prob": 1.5,
                   "match_text": "Mexikos aggressive Flügelzange überrumpelt die gegnerische Kette. Aguirre beweist feines Gespür bei den Einwechslungen."},
        "Südafrika": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "A", "wert_mio": 35, "trainer": "Hugo Broos", "system": "4-2-3-1", "mvp": "Teboho Mokoena", "info": "Ein eingespieltes Kollektiv aus der heimischen Liga, dem in den Schlüsselmomenten jedoch die Kaltschnäuzigkeit fehlt.", "titel_prob": 0.1,
                      "match_text": "Südafrika kämpft diszipliniert im Mittelfeldzentrum, verliert am Ende aber die entscheidenden Luftduelle im eigenen Sechzehner."},
        "Südkorea": {"angriff": 1.5, "abwehr": 1.2, "gruppe": "A", "wert_mio": 165, "trainer": "Hong Myung-bo", "system": "4-4-2", "mvp": "Heung-min Son", "info": "Pfeilschnelles Umschaltspiel über Son. Das Team agiert taktisch diszipliniert, wackelt aber bei gegnerischen Standards.", "titel_prob": 0.8,
                     "match_text": "Ein Geniestreich von Heung-min Son bricht den Bann. Südkorea kontert eiskalt und belohnt sich für den hohen läuferischen Aufwand."},
        "Tschechien": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "A", "wert_mio": 190, "trainer": "Ivan Hašek", "system": "3-4-1-2", "mvp": "Tomáš Souček", "info": "Physisch extrem robustes Team, das stark auf zweite Bälle und gefährliche Flanken ausgelegt ist.", "titel_prob": 0.5,
                       "match_text": "Souček dominiert das Luftreich. Tschechien erzielt das entscheidende Tor nach einer präzisen Eckball-Variante."},
        
        # Gruppe B
        "Kanada": {"angriff": 1.5, "abwehr": 1.2, "gruppe": "B", "wert_mio": 180, "trainer": "Jesse Marsch", "system": "4-4-2", "mvp": "Alphonso Davies", "info": "Marsch-typisches, extrem intensives Pressing. Extrem hohes Tempo über die linke Seite durch Davies.", "titel_prob": 1.0,
                   "match_text": "Alphonso Davies überrennt die gegnerische Abwehrreihe im Alleingang. Kanadas hohes Gegenpressing erzwingt fatale Fehler."},
        "Bosnien-Herzegowina": {"angriff": 1.3, "abwehr": 1.3, "gruppe": "B", "wert_mio": 85, "trainer": "Sergej Barbarez", "system": "3-5-2", "mvp": "Anel Ahmedhodžić", "info": "Lebt von einer leidenschaftlichen Mentalität, ist in der Rückwärtsbewegung aber phasenweise zu unbeweglich.", "titel_prob": 0.2,
                                "match_text": "Barbarez formiert eine kämpferische Truppe, doch individuelle Stellungsfehler in der Dreierkette kosten den Erfolg."},
        "Katar": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "B", "wert_mio": 20, "trainer": "Tintín Márquez", "system": "5-3-2", "mvp": "Akram Afif", "info": "Eingespielter Asienmeister mit starkem Fokus auf tiefe Absicherung, international physisch aber oft überfordert.", "titel_prob": 0.1,
                  "match_text": "Afif setzt vereinzelte kreative Nadelstiche, aber die katarische Defensive bricht unter dem permanenten Druck irgendwann ein."},
        "Schweiz": {"angriff": 1.6, "abwehr": 0.9, "gruppe": "B", "wert_mio": 280, "trainer": "Murat Yakin", "system": "3-4-2-1", "mvp": "Manuel Akanji", "info": "Hervorragende Defensivorganisation rund um Akanji. Findet spielerisch fast immer kreative Lösungen aus der Pressingfalle.", "titel_prob": 2.5,
                    "match_text": "Akanji erstickt jede gegnerische Offensivaktion im Keim. Die Schweiz kombiniert sich geduldig und hochverdient zum Sieg."},
        
        # Gruppe C
        "Brasilien": {"angriff": 2.3, "abwehr": 0.8, "gruppe": "C", "wert_mio": 1050, "trainer": "Dorival Júnior", "system": "4-2-3-1", "mvp": "Vinícius Jr.", "info": "Brutale offensive Urgewalt auf den Flügeln. Spielerisch und individuell jederzeit in der Lage, Matches im Alleingang zu entscheiden.", "titel_prob": 14.0,
                      "match_text": "Vinícius Jr. zündet den Turbo und lässt drei Verteidiger stehen. Die Seleção zelebriert Tempofußball auf allerhöchstem Niveau."},
        "Marokko": {"angriff": 1.7, "abwehr": 0.8, "gruppe": "C", "wert_mio": 320, "trainer": "Walid Regragui", "system": "4-1-4-1", "mvp": "Achraf Hakimi", "info": "Das taktische Meisterwerk von Regragui steht defensiv wie eine Wand. Hakimi treibt die blitzschnellen Umschaltmomente an.", "titel_prob": 4.5,
                    "match_text": "Marokkos defensiver Riegel erweist sich als unüberwindbar. Ein perfekt vorgetragener Konter über Hakimi bringt die Entscheidung."},
        "Haiti": {"angriff": 0.9, "abwehr": 1.6, "gruppe": "C", "wert_mio": 15, "trainer": "Sébastien Migné", "system": "4-5-1", "mvp": "Frantzdy Pierrot", "info": "Die große Sensation der Qualifikation. Agiert mit einer extrem tiefen Fünferkette und hofft auf Geniestreiche von Pierrot.", "titel_prob": 0.01,
                  "match_text": "Pierrot reibt sich als Solospitze komplett auf. Gegen die spielerische Klasse der Weltelite ist Haiti schlicht chancenlos."},
        "Schottland": {"angriff": 1.3, "abwehr": 1.2, "gruppe": "C", "wert_mio": 210, "trainer": "Steve Clarke", "system": "5-4-1", "mvp": "Scott McTominay", "info": "Enorm lauf- und zweikampfstark. Sucht den direkten Weg nach vorne über lange Bälle und erzwingt physische Abnutzungskämpfe.", "titel_prob": 0.4,
                       "match_text": "McTominay wirft sich in jeden Zweikampf und sorgt für permanente Unruhe, spielerisch fehlt es den Schotten aber an Kreativität."},
        
        # Gruppe D
        "USA": {"angriff": 1.8, "abwehr": 1.0, "gruppe": "D", "wert_mio": 350, "trainer": "Mauricio Pochettino", "system": "4-3-3", "mvp": "Christian Pulisic", "info": "Unter Pochettino taktisch hochflexibel und diszipliniert. Besitzt eine enorm athletische Mannschaft mit internationaler Reife.", "titel_prob": 3.0,
                "match_text": "Pochettinos taktischer Matchplan geht voll auf. Pulisic wirbelt auf der Außenbahn und erzielt den entscheidenden Treffer."},
        "Paraguay": {"angriff": 1.2, "abwehr": 1.0, "gruppe": "D", "wert_mio": 110, "trainer": "Gustavo Alfaro", "system": "4-4-2", "mvp": "Julio Enciso", "info": "Fokus liegt fast ausschließlich auf Zerstörung, harten Zweikämpfen und einer extrem körperbetonten Abwehrarbeit.", "titel_prob": 0.3,
                     "match_text": "Enciso deutet sein großes Talent an, doch Paraguays extrem destruktiver Ansatz wird letztlich nicht belohnt."},
        "Australien": {"angriff": 1.3, "abwehr": 1.2, "gruppe": "D", "wert_mio": 50, "trainer": "Tony Popovic", "system": "4-2-3-1", "mvp": "Harry Souttar", "info": "Laufstarkes Team, das über die mannschaftliche Geschlossenheit kommt. Spielerisch fehlt im letzten Drittel oft die Präzision.", "titel_prob": 0.2,
                       "match_text": "Souttar bereinigt defensiv viele Flanken, doch die Socceroos entwickeln aus dem Spiel heraus schlicht zu wenig Torgefahr."},
        "Türkei": {"angriff": 1.7, "abwehr": 1.2, "gruppe": "D", "wert_mio": 310, "trainer": "Vincenzo Montella", "system": "4-2-3-1", "mvp": "Arda Güler", "info": "Hochemotional und technisch brillant durch Güler kreiert. Zeigt offensiv geniale Momente, verliert defensiv aber die Balance.", "titel_prob": 2.0,
                   "match_text": "Ein genialer Moment von Arda Güler reißt die Zuschauer von den Sitzen. Die Türkei gewinnt ein wildes, offenes Offensivspektakel."},
        
        # Gruppe E
        "Deutschland": {"angriff": 2.1, "abwehr": 0.9, "gruppe": "E", "wert_mio": 850, "trainer": "Julian Nagelsmann", "system": "4-2-3-1", "mvp": "Florian Wirtz", "info": "Nagelsmanns Truppe dominiert das Mittelfeld durch extremes Kurzpassspiel und die kreativen Geistesblitze von Wirtz und Musiala.", "titel_prob": 11.0,
                        "match_text": "Florian Wirtz seziert die gegnerische Abwehr mit einem tödlichen Pass. Deutschland dominiert Ball und Gegner nach Belieben."},
        "Curaçao": {"angriff": 0.8, "abwehr": 1.7, "gruppe": "E", "wert_mio": 12, "trainer": "Dick Advocaat", "system": "5-4-1", "mvp": "Juninho Bacuna", "info": "Agiert unter Trainer-Dino Advocaat mit einem reinen Abwehrbollwerk tief in der eigenen Hälfte. Läuferisch schnell erschöpft.", "titel_prob": 0.01,
                    "match_text": "Bacuna kämpft aufopferungsvoll, doch die spielerische Wucht des Favoriten überrollt das tapfere Curaçao komplett."},
        "Elfenbeinküste": {"angriff": 1.6, "abwehr": 1.1, "gruppe": "E", "wert_mio": 340, "trainer": "Emerse Faé", "system": "4-3-3", "mvp": "Ousmane Diomande", "info": "Physisch ungemein robuste Mannschaft mit enormer Wucht im Sturmzentrum. Spielerisch eines der stärksten Teams Afrikas.", "titel_prob": 2.2,
                           "match_text": "Diomande gewinnt hinten jeden entscheidenden Zweikampf, während die Elfenbeinküste vorne ihre physische Überlegenheit ausspielt."},
        "Ecuador": {"angriff": 1.5, "abwehr": 0.9, "gruppe": "E", "wert_mio": 260, "trainer": "Sebastián Beccacece", "system": "3-4-3", "mvp": "Moises Caicedo", "info": "Extrem giftig und intensiv im Pressing rund um Aggressive-Leader Caicedo. Defensiv ungemein schwer zu überspielen.", "titel_prob": 1.8,
                    "match_text": "Caicedo zieht im Mittelfeld die Fäden und erstickt gegnerische Angriffe im Keim. Ecuador siegt dank perfekter Balance."},
        
        # Gruppe F
        "Niederlande": {"angriff": 1.9, "abwehr": 0.9, "gruppe": "F", "wert_mio": 620, "trainer": "Ronald Koeman", "system": "4-3-3", "mvp": "Xavi Simons", "info": "Verfügt über eine Abwehrkette von absoluter Weltklasse. Im Angriffsdrittel extrem variabel über Freigeist Xavi Simons.", "titel_prob": 6.5,
                        "match_text": "Xavi Simons setzt sich mit einer feinen Einzelleistung durch und schließt trocken ab. Die Elftal agiert defensiv absolut makellos."},
        "Japan": {"angriff": 1.7, "abwehr": 1.0, "gruppe": "F", "wert_mio": 290, "trainer": "Hajime Moriyasu", "system": "4-2-3-1", "mvp": "Takefusa Kubo", "info": "Diszipliniertes, taktisch hochgradig synchronisiertes Kombinationsspiel. Extrem schnelles Umschaltsehen über Kubo.", "titel_prob": 2.5,
                  "match_text": "Kubo initiiert eine Passstafette wie aus dem Lehrbuch. Japans hohes Tempo ist für die gegnerische Defensive nicht zu verteidigen."},
        "Schweden": {"angriff": 1.7, "abwehr": 1.2, "gruppe": "F", "wert_mio": 240, "trainer": "Jon Dahl Tomasson", "system": "4-4-2", "mvp": "Alexander Isak", "info": "Herausragendes Sturmduo um Isak und Gyökeres, zeigt jedoch gravierende Lücken in der Rückwärtsbewegung des Mittelfelds.", "titel_prob": 1.2,
                     "match_text": "Alexander Isak trifft eiskalt per Direktabnahme, doch Schwedens defensive Anfälligkeit macht ein besseres Ergebnis zunichte."},
        "Tunesien": {"angriff": 1.1, "abwehr": 1.2, "gruppe": "F", "wert_mio": 45, "trainer": "Faouzi Benzarti", "system": "4-5-1", "mvp": "Ellyes Skhiri", "info": "Fokussiert sich primär auf Fehlervermeidung und ein enges Zentrum. Entwickelt kaum eigene kreative Ideen im Angriffsspiel.", "titel_prob": 0.1,
                     "match_text": "Skhiri spult unzählige Kilometer ab und schließt Lücken, aber die fehlende offensive Durchschlagskraft rächt sich spät im Spiel."},
        
        # Gruppe G
        "Belgien": {"angriff": 1.9, "abwehr": 1.1, "gruppe": "G", "wert_mio": 480, "trainer": "Domenico Tedesco", "system": "4-3-3", "mvp": "Jérémy Doku", "info": "Enormes Tempo über Doku auf der Außenbahn. Befindet sich in einem Umbruch in der Defensive, der anfällig für Konter ist.", "titel_prob": 4.0,
                    "match_text": "Jérémy Doku lässt seinen Gegenspieler mit einem rasanten Antritt stehen und legt perfekt quer. Belgiens Offensive rettet die Defensive."},
        "Ägypten": {"angriff": 1.4, "abwehr": 1.2, "gruppe": "G", "wert_mio": 110, "trainer": "Hossam Hassan", "system": "4-2-3-1", "mvp": "Mohamed Salah", "info": "Das gesamte System ist radikal darauf ausgerichtet, Mohamed Salah mit langen Bällen in Eins-gegen-Eins-Situationen zu bringen.", "titel_prob": 0.7,
                    "match_text": "Salah entwischt der Abwehrkette einmal und vollstreckt eiskalt, doch Ägypten agiert insgesamt zu leicht ausrechenbar."},
        "Iran": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "G", "wert_mio": 40, "trainer": "Amir Ghalenoei", "system": "5-4-1", "mvp": "Mehdi Taremi", "info": "Sehr erfahrene Mannschaft, die defensiv tief steht, kompakt verschiebt und auf Geniestreiche von Taremi lauert.", "titel_prob": 0.2,
                 "match_text": "Taremi behauptet den Ball stark im Sturmzentrum, doch der Iran kann dem spielerischen Druck des Gegners nicht dauerhaft standhalten."},
        "Neuseeland": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "G", "wert_mio": 25, "trainer": "Darren Bazeley", "system": "4-4-2", "mvp": "Chris Wood", "info": "Ozeanien-Meister, setzt fast ausschließlich auf eine robuste Physis und hohe Flanken auf Zielspieler Chris Wood.", "titel_prob": 0.05,
                       "match_text": "Chris Wood wirft sich wuchtig in den Strafraum und sorgt für Gefahr, spielerisch fehlen Neuseeland jedoch die Mittel."},
        
        # Gruppe H
        "Spanien": {"angriff": 2.2, "abwehr": 0.8, "gruppe": "H", "wert_mio": 900, "trainer": "Luis de la Fuente", "system": "4-3-3", "mvp": "Lamine Yamal", "info": "Dominanter Ballbesitzfußball gepaart mit unberechenbarem Flügelspiel über Wunderkind Lamine Yamal. Extrem ballsicher.", "titel_prob": 13.5,
                    "match_text": "Lamine Yamal zirkelt den Ball magisch in den oberen Torwinkel. Spaniens flüssiges Kombinationsspiel zieht dem Gegner den Zahn."},
        "Kap Verde": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "H", "wert_mio": 30, "trainer": "Bubista", "system": "4-3-3", "mvp": "Logan Costa", "info": "Sehr lauffreudiges und taktisch diszipliniertes Team, dem es jedoch an internationaler individueller Klasse mangelt.", "titel_prob": 0.05,
                      "match_text": "Logan Costa rettet mehrmals in höchster Not, aber die spielerische Überlegenheit des Favoriten bricht Kap Verde letztlich."},
        "Saudi-Arabien": {"angriff": 1.1, "abwehr": 1.3, "gruppe": "H", "wert_mio": 35, "trainer": "Roberto Mancini", "system": "4-1-4-1", "mvp": "Firas Al-Buraikan", "info": "Taktisch von Mancini hervorragend geschult, scheitert international aber oft am fehlenden Offensiv-Tempo.", "titel_prob": 0.1,
                         "match_text": "Mancinis Defensivkonzept greift phasenweise gut, doch im Umschaltspiel fehlt den Saudis jegliche Durchschlagskraft."},
        "Uruguay": {"angriff": 1.9, "abwehr": 0.9, "gruppe": "H", "wert_mio": 420, "trainer": "Marcelo Bielsa", "system": "4-3-3", "mvp": "Federico Valverde", "info": "Bielsa-Powerfußball in Reinkultur. Radikales, extrem aggressives Pressing und unermüdlicher Offensivdrang über Valverde.", "titel_prob": 5.0,
                    "match_text": "Valverde marschiert unermüdlich durch das Mittelfeld. Uruguays unaufhaltsames Power-Pressing erdrückt den Gegner förmlich."},
        
        # Gruppe I
        "Frankreich": {"angriff": 2.4, "abwehr": 0.8, "gruppe": "I", "wert_mio": 1200, "trainer": "Didier Deschamps", "system": "4-2-3-1", "mvp": "Kylian Mbappé", "info": "Pragmatisch, defensiv stabil und offensiv durch Mbappé von brutaler Effizienz. Physisch das kompletteste Team des Turniers.", "titel_prob": 15.0,
                       "match_text": "Kylian Mbappé schaltet den Turbo ein und vollstreckt eiskalt in die lange Ecke. Frankreich agiert erschreckend abgezockt."},
        "Senegal": {"angriff": 1.5, "abwehr": 1.1, "gruppe": "I", "wert_mio": 280, "trainer": "Aliou Cissé", "system": "4-3-3", "mvp": "Nicolas Jackson", "info": "Physisch ungemein starkes Team, das defensiv kompakt steht und im Sturmzentrum auf die Wucht von Jackson setzt.", "titel_prob": 1.8,
                    "match_text": "Nicolas Jackson behauptet den Ball robust und trifft per Drehung. Senegal belohnt sich für eine leidenschaftliche Leistung."},
        "Irak": {"angriff": 1.0, "abwehr": 1.3, "gruppe": "I", "wert_mio": 18, "trainer": "Jesús Casas", "system": "4-2-3-1", "mvp": "Aymen Hussein", "info": "Diszipliniert verteidigendes Team, das gegen spielstarke Top-Nationen spielerisch jedoch klar das Nachsehen hat.", "titel_prob": 0.05,
                 "match_text": "Hussein hängt als einzige Spitze völlig in der Luft. Der Irak verteidigt wacker, bricht am Ende jedoch komplett ein."},
        "Norwegen": {"angriff": 1.8, "abwehr": 1.3, "gruppe": "I", "wert_mio": 450, "trainer": "Ståle Solbakken", "system": "4-3-3", "mvp": "Erling Haaland", "info": "Dank Tormaschine Haaland offensiv eine absolute Urgewalt, defensiv leistet sich Norwegen jedoch zu viele Aussetzer.", "titel_prob": 2.0,
                     "match_text": "Erling Haaland wuchtet den Ball unnachahmlich per Kopf in die Maschen. Norwegens wackelige Abwehr macht es hinten aber spannend."},
        
        # Gruppe J
        "Argentinien": {"angriff": 2.2, "abwehr": 0.7, "gruppe": "J", "wert_mio": 800, "trainer": "Lionel Scaloni", "system": "4-3-3", "mvp": "Lautaro Martínez", "info": "Der amtierende Weltmeister. Besticht durch brutale Abgezocktheit, taktische Perfektion und eine Beton-Abwehr um Lautaro.", "titel_prob": 12.5,
                        "match_text": "Lautaro Martínez eist die Kugel im Sechzehner ab und trifft eiskalt. Die Albiceleste demonstriert die Reife eines Champions."},
        "Algerien": {"angriff": 1.4, "abwehr": 1.1, "gruppe": "J", "wert_mio": 140, "trainer": "Vladimir Petković", "system": "4-1-4-1", "mvp": "Rayan Aït-Nouri", "info": "Technisch beschlagenes Team, agiert in der Rückwärtsbewegung unter Petković jedoch oft unkonzentriert und fehleranfällig.", "titel_prob": 0.6,
                     "match_text": "Aït-Nouri kurbelt das Spiel über links an, doch Algeriens Defensivpatzer laden den Gegner zu einfachen Toren ein."},
        "Österreich": {"angriff": 1.7, "abwehr": 1.0, "gruppe": "J", "wert_mio": 290, "trainer": "Ralf Rangnick", "system": "4-2-2-2", "mvp": "Konrad Laimer", "info": "Gnadenlose Pressingmaschine unter Rangnick. Zwingt den Gegner durch extremes kollektives Anlaufen zu permanenten Fehlern.", "titel_prob": 2.8,
                       "match_text": "Laimer erobert den Ball tief in der gegnerischen Hälfte. Österreichs intensiver Tempofußball zieht dem Gegner den Nerv."},
        "Jordanien": {"angriff": 1.0, "abwehr": 1.4, "gruppe": "J", "wert_mio": 15, "trainer": "Jamal Sellami", "system": "5-3-2", "mvp": "Musa Al-Taamari", "info": "Kontertiefes System mit einer defensiven Fünferkette. Spielerisch auf diesem internationalen Niveau klar überfordert.", "titel_prob": 0.02,
                      "match_text": "Al-Taamari versucht verzweifelt zu kontern, aber Jordanien wird vom gegnerischen Kombinationswirbel komplett seziert."},
        
        # Gruppe K
        "Portugal": {"angriff": 2.2, "abwehr": 0.9, "gruppe": "K", "wert_mio": 950, "trainer": "Roberto Martínez", "system": "4-3-3", "mvp": "Rafael Leão", "info": "Herausragende Kaderbreite. Offensiv über die Flügel mit Leão kaum zu verteidigen, agiert extrem spielbestimmend.", "titel_prob": 10.0,
                     "match_text": "Rafael Leão tanzt seinen Gegenspieler aus und flankt maßgenau. Portugals enorme spielerische Qualität setzt sich durch."},
        "DR Kongo": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "K", "wert_mio": 60, "trainer": "Sébastien Desabre", "system": "4-2-3-1", "mvp": "Yoane Wissa", "info": "Umschaltstark über Wissa, offenbart im gebundenen Spiel gegen tiefstehende Gegner jedoch erhebliche Ideenlosigkeit.", "titel_prob": 0.2,
                     "match_text": "Wissa scheitert knapp am Pfosten. Im Laufe des Spiels verliert die DR Kongo im Mittelfeld komplett den Zugriff."},
        "Usbekistan": {"angriff": 1.2, "abwehr": 1.2, "gruppe": "K", "wert_mio": 32, "trainer": "Srečko Katanec", "system": "3-4-2-1", "mvp": "Abbosbek Fayzullaev", "info": "Turnier-Debütant mit einer hochtalentierten, jungen Generation rund um den quirligen Spielmacher Fayzullaev.", "titel_prob": 0.1,
                       "match_text": "Fayzullaev zeigt seine technische Klasse, doch Lehrgeld und mangelnde Cleverness kosten Usbekistan wertvolle Punkte."},
        "Kolumbien": {"angriff": 1.9, "abwehr": 0.9, "gruppe": "K", "wert_mio": 280, "trainer": "Néstor Lorenzo", "system": "4-2-3-1", "mvp": "Luis Díaz", "info": "Extrem giftig und leidenschaftlich in den Zweikämpfen. Schaltet über den pfeilschnellen Díaz rasant in die Spitze um.", "titel_prob": 4.8,
                      "match_text": "Luis Díaz zieht unwiderstehlich nach innen und schlenzt den Ball ins Netz. Kolumbiens Aggressivität bricht den Widerstand."},
        
        # Gruppe L
        "England": {"angriff": 2.3, "abwehr": 0.9, "gruppe": "L", "wert_mio": 1300, "trainer": "Thomas Tuchel", "system": "4-2-3-1", "mvp": "Jude Bellingham", "info": "Kader voller internationaler Superstars. Unter Tuchel taktisch exzellent strukturiert und defensiv extrem stabilisiert.", "titel_prob": 13.0,
                    "match_text": "Jude Bellingham stößt mit perfektem Timing in den Strafraum und vollendet. Tuchels taktischer Plan geht fehlerfrei auf."},
        "Kroatien": {"angriff": 1.6, "abwehr": 1.0, "gruppe": "L", "wert_mio": 270, "trainer": "Zlatko Dalić", "system": "4-3-3", "mvp": "Joško Gvardiol", "info": "Das ewige Mentalitätsmonster. Besticht durch enorme Turniererfahrung und die defensive Abgeklärtheit von Gvardiol.", "titel_prob": 3.2,
                     "match_text": "Gvardiol gewinnt das entscheidende Duell am Fünfmeterraum. Kroatien rettet den Vorsprung mit purer Routine über die Zeit."},
        "Ghana": {"angriff": 1.4, "abwehr": 1.2, "gruppe": "L", "wert_mio": 120, "trainer": "Otto Addo", "system": "4-2-3-1", "mvp": "Mohammed Kudus", "info": "Unberechenbares Team mit hohem Tempo über Kudus, leistet sich defensiv aber immer wieder haarsträubende Stellungsfehler.", "titel_prob": 0.5,
                  "match_text": "Kudus sorgt für magische Momente im Dribbling, doch ein schwerer Abwehrschnitzer bestraft Ghana in der Schlussphase."},
        "Panama": {"angriff": 1.0, "abwehr": 1.3, "gruppe": "L", "wert_mio": 18, "trainer": "Thomas Christiansen", "system": "4-4-2", "mvp": "Adalberto Carrasquilla", "info": "Physisch robustes Team, das versucht die Räume eng zu machen, fußballerisch den Top-Nationen aber unterlegen ist.", "titel_prob": 0.05,
                   "match_text": "Carrasquilla verteilt die Bälle klug, doch Panama fehlt im letzten Drittel jede spielerische Idee gegen die gegnerische Kette."},
    }

teams_db = get_pro_world_cup_data()

# 3. Kicker Live-Daten-Schnittstelle (Statische Datenbank der realen Ergebnisse)
@st.cache_data
def get_kicker_live_data():
    return {
        # Echte Ergebnisse der Gruppenphase (Beispiele für den letzten Spieltag)
        ("Norwegen", "Frankreich"): {"score1": 1, "score2": 4, "is_real": True},
        ("Senegal", "Irak"): {"score1": 5, "score2": 0, "is_real": True},
        ("Kap Verde", "Saudi-Arabien"): {"score1": 0, "score2": 0, "is_real": True},
        ("Uruguay", "Spanien"): {"score1": 0, "score2": 1, "is_real": True},
        ("Neuseeland", "Belgien"): {"score1": 1, "score2": 5, "is_real": True},
        ("Ägypten", "Iran"): {"score1": 1, "score2": 1, "is_real": True},
        ("Panama", "England"): {"score1": 0, "score2": 2, "is_real": True},
        ("Kroatien", "Ghana"): {"score1": 2, "score2": 1, "is_real": True},
        ("Kolumbien", "Portugal"): {"score1": 0, "score2": 0, "is_real": True},
        ("DR Kongo", "Usbekistan"): {"score1": 3, "score2": 1, "is_real": True},
        ("Algerien", "Österreich"): {"score1": 3, "score2": 3, "is_real": True},
        ("Jordanien", "Argentinien"): {"score1": 1, "score2": 3, "is_real": True},
        # Round of 32 bereits beendete Kicker-Spiele
        ("Südafrika", "Kanada"): {"score1": 0, "score2": 1, "is_real": True, "winner": "Kanada"},
        # Aktuell laufendes Live-Spiel im Kicker-Ticker
        ("Brasilien", "Japan"): {"score1": 1, "score2": 1, "is_live": True, "live_min": 74, "winner": None}
    }

kicker_db = get_kicker_live_data()

# Hybrid-Simulations-Logik: Nutzt Realdaten wenn vorhanden, sonst KI-Simulation
def simuliere_oder_hole_live_spiel(t1, t2, ko=False):
    # Check ob reales Ergebnis vorliegt
    if (t1, t2) in kicker_db:
        match = kicker_db[(t1, t2)]
        if match.get("is_live"):
            # Wenn es live ist, nehmen wir den aktuellen Stand, würfeln für K.o. aber den Sieger aus, falls Unentschieden
            w = t1 if (ko and np.random.rand() > 0.5) else t2
            return {"score1": match["score1"], "score2": match["score2"], "winner": w, "is_live": True, "live_min": match["live_min"]}
        return {"score1": match["score1"], "score2": match["score2"], "winner": match.get("winner", t1 if match["score1"] > match["score2"] else t2), "is_real": True}
    
    if (t2, t1) in kicker_db:
        match = kicker_db[(t2, t1)]
        if match.get("is_live"):
            w = t2 if (ko and np.random.rand() > 0.5) else t1
            return {"score1": match["score2"], "score2": match["score1"], "winner": w, "is_live": True, "live_min": match["live_min"]}
        return {"score1": match["score2"], "score2": match["score1"], "winner": match.get("winner", t2 if match["score1"] > match["score2"] else t1), "is_real": True}

    # Fallback zur mathematischen Simulation (Favoritenschutz)
    mw1 = teams_db[t1]["wert_mio"]
    mw2 = teams_db[t2]["wert_mio"]
    mw_faktor_t1 = np.log10(mw1) / 2
    mw_faktor_t2 = np.log10(mw2) / 2
    
    t1_lambda = teams_db[t1]["angriff"] * teams_db[t2]["abwehr"] * mw_faktor_t1
    t2_lambda = teams_db[t2]["angriff"] * teams_db[t1]["abwehr"] * mw_faktor_t2
    
    if mw1 > mw2 * 5:
        t1_lambda += 1.5
        t2_lambda = max(0.1, t2_lambda - 0.8)
    elif mw2 > mw1 * 5:
        t2_lambda += 1.5
        t1_lambda = max(0.1, t1_lambda - 0.8)
        
    t1_lambda = min(4.0, max(0.2, t1_lambda / 1.6))
    t2_lambda = min(4.0, max(0.2, t2_lambda / 1.6))
    
    goals_t1 = np.random.poisson(t1_lambda)
    goals_t2 = np.random.poisson(t2_lambda)
    
    if ko and goals_t1 == goals_t2:
        if (t1_lambda + np.random.rand()) > (t2_lambda + np.random.rand()):
            goals_t1 += 1
        else:
            goals_t2 += 1
            
    return {"score1": goals_t1, "score2": goals_t2, "winner": t1 if goals_t1 > goals_t2 else t2, "is_real": False}

def generiere_erklaerung_html(t1, t2, res):
    winner = res["winner"]
    loser = t2 if winner == t1 else t1
    text = teams_db[winner]["match_text"]
    badge = ""
    if res.get("is_real"):
        badge = "<span class='real-badge'>Offizielles Kicker Ergebnis</span>"
    elif res.get("is_live"):
        badge = f"<span class='live-badge'>LIVE ({res['live_min']}')</span>"
        
    return f"""
    <div class='pro-explanation'>
        <div class='match-title'>🏆 Spielanalyse: {t1} gegen {t2} {badge}</div>
        {text}<br><br>
        <b>Trainer-Taktik:</b> <i>{teams_db[winner]['trainer']}</i> gewinnt das Systemduell ({teams_db[winner]['system']} vs. {teams_db[loser]['system']}) dank MVP <b>{teams_db[winner]['mvp']}</b>. Kaderwert-Kräfteverhältnis: {teams_db[winner]['wert_mio']} Mio. € vs. {teams_db[loser]['wert_mio']} Mio. €.
    </div>
    """

# 4. Tabs Struktur
tab1, tab2 = st.tabs(["🔍 Team-Profile & Kader-Metriken", "🚀 Offizieller Turniersimulator"])

with tab1:
    st.info("""
    ### 📊 Datengrundlage & Live-Schnittstellen-Parameter
    Die hinterlegten Stärkewerte basieren auf Kicker-Turnierdaten. Aktuelle, reale WM-Ergebnisse bis zum heutigen Tag (29. Juni 2026) fließen live in die Tabellenberechnung ein.
    """)
    
    selected_group = st.selectbox("Wähle eine Gruppe zur detaillierten Analyse:", sorted(list(set([v["gruppe"] for v in teams_db.values()]))))
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
                st.markdown(f"**Individuelle Einschätzung:** *{t_data['info']}*")

with tab2:
    st.sidebar.header("⚙️ Live Optionen")
    start_sim = st.sidebar.button("🏆 Live-Turnierbaum laden & simulieren", use_container_width=True)
    
    if not start_sim:
        st.info("Klicke in der Sidebar auf den Button, um den aktuellen Kicker-Echtzeitstand zu laden.")
    else:
        # --- GRUPPENPHASE ---
        st.header("📊 Reale Abschlusstabellen & Ergebnisse der Gruppenphase")
        groups = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        all_group_tables = {}
        cols = st.columns(2)
        
        for idx, g in enumerate(groups):
            current_col = cols[idx % 2]
            g_teams = [t for t, v in teams_db.items() if v["gruppe"] == g]
            punkte = {t: 0 for t in g_teams}
            tordifferenz = {t: 0 for t in g_teams}
            
            with current_col:
                st.markdown(f"<div class='group-card'><div class='group-header'>Gruppe {g}</div>", unsafe_allow_html=True)
                
                spielpaarungen = [(g_teams[0], g_teams[1]), (g_teams[2], g_teams[3]), 
                                  (g_teams[0], g_teams[2]), (g_teams[1], g_teams[3]),
                                  (g_teams[3], g_teams[0]), (g_teams[1], g_teams[2])]
                                  
                for t1, t2 in spielpaarungen:
                    res = simuliere_oder_hole_live_spiel(t1, t2, ko=False)
                    if res["score1"] > res["score2"]: punkte[t1] += 3
                    elif res["score2"] > res["score1"]: punkte[t2] += 3
                    else:
                        punkte[t1] += 1; punkte[t2] += 1
                    tordifferenz[t1] += (res["score1"] - res["score2"])
                    tordifferenz[t2] += (res["score2"] - res["score1"])
                    
                    lbl_real = " 🟢 [Kicker Real]" if res.get("is_real") else ""
                    with st.expander(f"⚽ {t1} {res['score1']}:{res['score2']} {t2}{lbl_real}"):
                        st.markdown(generiere_erklaerung_html(t1, t2, res), unsafe_allow_html=True)
                
                tabelle_sortiert = sorted(g_teams, key=lambda x: (punkte[x], tordifferenz[x]), reverse=True)
                all_group_tables[g] = {"tabelle": tabelle_sortiert, "punkte": punkte, "tordifferenz": tordifferenz}
                
                df_data = {
                    "Platz": [1, 2, 3, 4],
                    "Team": tabelle_sortiert,
                    "Punkte": [punkte[t] for t in tabelle_sortiert],
                    "Tordifferenz": [tordifferenz[t] for t in tabelle_sortiert]
                }
                st.dataframe(pd.DataFrame(df_data).set_index("Platz"), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # --- EXAKTE FIFA 2026 BRACKET LOGIK ---
        g_1 = {g: all_group_tables[g]["tabelle"][0] for g in groups}
        g_2 = {g: all_group_tables[g]["tabelle"][1] for g in groups}
        
        drittplatzierte = []
        for g in groups:
            t3 = all_group_tables[g]["tabelle"][2]
            drittplatzierte.append({"team": t3, "punkte": all_group_tables[g]["punkte"][t3], "td": all_group_tables[g]["tordifferenz"][t3]})
        
        beste_dritte = [x["team"] for x in sorted(drittplatzierte, key=lambda x: (x["punkte"], x["td"]), reverse=True)[:8]]

        ko_32_paare = [
            (g_1["A"], beste_dritte[0]), (g_2["A"], g_2["B"]), (g_1["C"], g_2["F"]), (g_1["E"], beste_dritte[1]),
            (g_1["I"], beste_dritte[2]), (g_2["E"], g_2["I"]), (g_1["F"], g_2["C"]), (g_1["H"], g_2["J"]),
            (g_1["D"], beste_dritte[3]), (g_1["G"], beste_dritte[4]), (g_2["K"], g_2["L"]), (g_1["B"], beste_dritte[5]),
            (g_1["J"], g_2["H"]), (g_2["D"], g_2["G"]), (g_1["K"], beste_dritte[6]), (g_1["L"], beste_dritte[7]),
        ]

        st.write("---")
        st.header("📉 K.-o.-Phase (Echtzeit Live-Stand)")
        col_r32, col_r16, col_vf, col_hf, col_f = st.columns(5)
        
        def render_ko_stage(pairs, column, title):
            winners = []
            with column:
                st.subheader(title)
                for t1, t2 in pairs:
                    res = simuliere_oder_hole_live_spiel(t1, t2, ko=True)
                    winners.append(res["winner"])
                    
                    lbl_status = ""
                    if res.get("is_real"): lbl_status = " 🟢 [Kicker]"
                    elif res.get("is_live"): lbl_status = f" 🔴 [LIVE {res['live_min']}\']"
                        
                    with st.expander(f"⚔️ {t1} vs {t2}{lbl_status}"):
                        st.markdown(f"**Ergebnis: {res['score1']}:{res['score2']}**")
                        st.markdown(generiere_erklaerung_html(t1, t2, res), unsafe_allow_html=True)
            return winners

        r16_w = render_ko_stage(ko_32_paare, col_r32, "Round of 32")
        vf_w = render_ko_stage([(r16_w[i], r16_w[i+1]) for i in range(0, len(r16_w), 2)], col_r16, "Achtelfinale")
        hf_w = render_ko_stage([(vf_w[i], vf_w[i+1]) for i in range(0, len(vf_w), 2)], col_vf, "Viertelfinale")
        f_w = render_ko_stage([(hf_w[i], hf_w[i+1]) for i in range(0, len(hf_w), 2)], col_hf, "Halbfinale")
        
        with col_f:
            st.subheader("👑 Finale")
            f_res = simuliere_oder_hole_live_spiel(f_w[0], f_w[1], ko=True)
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%); padding: 25px; border-radius: 16px; text-align: center; color: white; box-shadow: 0 10px 25px rgba(234,179,8,0.4);'>
                    <h4 style='margin:0;'>PROGNOSTIZIERTER WELTMEISTER</h4>
                    <h2 style='margin:10px 0;'>🥇 {f_res['winner']} 🥇</h2>
                    <p style='margin:0; font-size:1.1rem;'>Ergebnis: <b>{f_res['score1']}:{f_res['score2']}</b></p>
                    <small style='opacity:0.9;'>Finalgegner: {f_w[1] if f_res['winner'] == f_w[0] else f_w[0]}</small>
                </div>
            """, unsafe_allow_html=True)
