# generateur de rapport pdf complet (Batterie, Radar, Plan d'action, Lexique)
from fpdf import FPDF
import time
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class RapportBouzuSec(FPDF):
    def header(self):
        self.set_font("Arial", "B", 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "CABINET BOUZUSEC   AUDIT DE SÉCURITÉ STRATÉGIQUE", border=0, ln=True, align="R")
        self.line(10, 18, 200, 18)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Document strictement confidentiel et réservé à la direction   Page {self.page_no()}", border=0, align="C")

def securiser_texte(texte):
    texte = str(texte)
    texte = texte.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-").replace("•", "-")
    return texte.encode("latin-1", "replace").decode("latin-1")

def dessiner_section(pdf, titre, contenu):
    pdf.set_fill_color(245, 245, 245)
    pdf.set_text_color(44, 62, 80)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, securiser_texte(titre), border=0, ln=True, fill=True)
    pdf.ln(3)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, securiser_texte(contenu))
    pdf.ln(8)

# fonction pour les definitions du lexique
def dessiner_definition(pdf, terme, definition):
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(230, 126, 34) # Orange
    pdf.cell(0, 6, securiser_texte(terme), ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, securiser_texte(definition))
    pdf.ln(4)

def dessiner_batterie(pdf, x, y, barres_actives, couleur):
    pdf.set_fill_color(40, 40, 40)
    pdf.rect(x, y, 60, 25, 'F') 
    pdf.rect(x + 60, y + 7, 4, 11, 'F') 
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(x + 2, y + 2, 56, 21, 'F')
    largeur_bloc = 12.5
    espacement = 14
    for i in range(4):
        if i < barres_actives:
            pdf.set_fill_color(*couleur)
        else:
            pdf.set_fill_color(230, 230, 230)
        position_x = x + 3 + (i * espacement)
        pdf.rect(position_x, y + 3, largeur_bloc, 19, 'F')

def dessiner_radar(scores, nom_fichier="radar_tmp.png"):
    labels = np.array(['Données Publiques', 'Portes (Réseau)', 'Dossiers Cachés', 'Configuration', 'Code Applicatif'])
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    scores = np.concatenate((scores, [scores[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    
    fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw=dict(polar=True))
    ax.fill(angles, scores, color='#e67e22', alpha=0.4) 
    ax.plot(angles, scores, color='#d35400', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, fontweight='bold', color='#2c3e50')
    ax.set_ylim(0, 10)
    
    plt.savefig(nom_fichier, transparent=True, bbox_inches='tight')
    plt.close()

def creer_pdf(domaine, mode_scan, data_whois, data_whatweb, data_nmap, data_gobuster, data_nikto, barres, energie, note, niveau_texte, couleur_rgb, scores_radar):
    pdf = RapportBouzuSec()
    
    # --- PAGE 1 : DASHBOARD EXECUTIVE ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(230, 126, 34)
    pdf.cell(0, 15, securiser_texte("RAPPORT D'AUDIT EXECUTIVE"), ln=True, align="C")
    
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, securiser_texte(f"Cible de l'audit : {domaine}"), ln=True, align="C")
    pdf.cell(0, 8, securiser_texte(f"Date : {time.strftime('%d/%m/%Y')} | Mode : {mode_scan.capitalize()}"), ln=True, align="C")
    pdf.ln(8)

    pdf.set_fill_color(250, 250, 250)
    pdf.rect(10, 55, 190, 70, 'F')
    
    pdf.set_y(60)
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, securiser_texte("SYNTHÈSE DU NIVEAU DE RISQUE"), ln=True, align="C")

    dessiner_batterie(pdf, 75, 75, barres, couleur_rgb)
    
    pdf.set_y(105)
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(*couleur_rgb)
    pdf.cell(0, 8, securiser_texte(f"Niveau d'énergie vitale : {energie} %"), ln=True, align="C")
    
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, securiser_texte(f"Évaluation ANSSI : {niveau_texte} (Note : {note}/10)"), ln=True, align="C")
    
    dessiner_radar(scores_radar, "radar_tmp.png")
    
    pdf.set_y(140)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, securiser_texte("CARTOGRAPHIE DES VECTEURS DE RISQUE"), ln=True, align="C")
    
    pdf.image("radar_tmp.png", x=45, y=150, w=120)
    
    if os.path.exists("radar_tmp.png"):
        os.remove("radar_tmp.png")
    
    # --- PAGES 2/3 : LES RÉSULTATS DÉTAILLÉS ---
    pdf.add_page()
    intro = "Ce document s'adresse à la direction générale. Il présente un bilan de santé de vos infrastructures numériques vues de l'extérieur. L'objectif est de vous donner une vision claire des risques liés à votre site Internet, sans jargon technique."
    pdf.set_font("Arial", "I", 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, securiser_texte(intro))
    pdf.ln(10)

    dessiner_section(pdf, "I. RECONNAISSANCE ET IDENTITÉ", "Analyse des données publiques et de la carte d'identité de votre serveur.\n\n" + data_whois + "\n\n" + data_whatweb)
    dessiner_section(pdf, "II. EXAMEN DES PORTES D'ACCÈS", data_nmap)
    
    pdf.add_page()
    dessiner_section(pdf, "III. CARTOGRAPHIE DES ZONES CACHÉES", data_gobuster)
    dessiner_section(pdf, "IV. DIAGNOSTIC DES VULNÉRABILITÉS APPLICATIVES", data_nikto)

    # --- PAGE 4 : PLAN D'ACTION (La valeur ajoutée du mode avancé) ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(230, 126, 34)
    pdf.cell(0, 10, securiser_texte("V. PLAN D'ACTION STRATÉGIQUE (FEUILLE DE ROUTE)"), ln=True)
    pdf.ln(5)

    if mode_scan == "simple":
        texte_roadmap = "Vous consultez actuellement la version de synthèse (Mode Simple) de l'audit BouzuSec.\n\nLa feuille de route stratégique, la hiérarchisation des urgences techniques, ainsi que les recommandations de remédiation étape par étape sont exclusivement disponibles dans l'audit en Mode Avancé.\n\nNous vous recommandons vivement de déclencher une analyse approfondie pour fournir à vos équipes techniques un plan d'action clair."
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 6, securiser_texte(texte_roadmap))
    else:
        texte_roadmap = "Sur la base des vulnérabilités identifiées par l'intelligence artificielle BouzuSec, voici la feuille de route priorisée que votre direction informatique doit suivre pour sécuriser l'infrastructure :\n"
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 6, securiser_texte(texte_roadmap))
        pdf.ln(5)
        
        # Generation de la roadmap selon les pires scores
        noms_axes = ["Masquer l'identité du serveur (OSINT)", "Verrouiller les ports d'accès (Pare-feu)", "Sécuriser les dossiers cachés et sauvegardes", "Mettre à jour les logiciels du serveur", "Corriger le code du site web (Injections/XSS)"]
        
        # on associe les scores aux noms et on trie du pire au meilleur
        priorites = sorted(zip(scores_radar, noms_axes), reverse=True)
        
        etape = 1
        for score, action in priorites:
            if score >= 7:
                niveau = "URGENCE ABSOLUE (Correction sous 24h)"
                pdf.set_text_color(229, 57, 53) # Rouge
            elif score >= 4:
                niveau = "PRIORITÉ MODÉRÉE (Correction sous 7 jours)"
                pdf.set_text_color(230, 126, 34) # Orange
            elif score >= 1:
                niveau = "AMÉLIORATION RECOMMANDÉE (Maintenance régulière)"
                pdf.set_text_color(39, 174, 96) # Vert
            else:
                continue # On n'affiche pas les trucs ou le score est 0
                
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 6, securiser_texte(f"Étape {etape} : {action}"), ln=True)
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 6, securiser_texte(f"-> {niveau}"), ln=True)
            pdf.ln(3)
            etape += 1
            
        if etape == 1:
            pdf.set_text_color(39, 174, 96)
            pdf.cell(0, 6, securiser_texte("Félicitations, aucune action urgente n'est requise. Maintenez cette rigueur."), ln=True)

    # --- PAGE 5 : MÉTHODOLOGIE ANSSI ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, securiser_texte("VI. MÉTHODOLOGIE DE L'ÉVALUATION (RÉFÉRENTIEL ANSSI)"), ln=True)
    pdf.ln(5)
    
    texte_anssi = "Le score global de cet audit a été calculé selon la méthode officielle de l'Agence Nationale de la Sécurité des Systèmes d'Information (ANSSI).\n\nEn cybersécurité, on ne fait pas de moyenne. La sécurité d'un système est égale à la solidité de son maillon le plus faible. Notre outil classe la pire vulnérabilité trouvée en croisant deux facteurs :\n\n1. La gravité de l'impact métier (de Mineur à Critique).\n2. La facilité d'exploitation par le pirate (de Très difficile à Facile).\n\nC'est la matrice ci-dessous qui définit le niveau d'énergie vitale de votre batterie."
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, securiser_texte(texte_anssi))
    pdf.ln(5)
    
    # Disclaimer final
    disclaimer = "Cet audit (DAST) analyse la surface sans posséder votre contexte métier interne. Il ne remplace pas l'ingénierie humaine pour les failles logiques de conception (Insecure Design)."
    dessiner_section(pdf, "Limites du diagnostic", disclaimer)

    # --- PAGE 6 : LEXIQUE ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, securiser_texte("VII. LEXIQUE CYBER POUR LA DIRECTION"), ln=True)
    pdf.ln(5)
    
    dessiner_definition(pdf, "Port / Porte d'accès numérique", "Un canal de communication sur votre serveur. Comme un bâtiment a une porte d'entrée et une porte de service, un serveur a des ports. Le port 80 est la porte publique, le port 22 est la porte blindée de maintenance.")
    dessiner_definition(pdf, "Vulnérabilité Applicative (XSS / SQLi)", "Un défaut de fabrication dans le code de votre site web qui permet à un pirate de tromper le système, par exemple pour lire votre base de données à la place du serveur.")
    dessiner_definition(pdf, "WAF (Web Application Firewall)", "Un vigile numérique placé devant votre site web. Il analyse les visiteurs et bloque ceux qui ont un comportement suspect ou qui tentent d'injecter des virus.")
    dessiner_definition(pdf, "OSINT (Open Source Intelligence)", "L'art de recueillir des informations publiques sur une entreprise (carte d'identité du serveur, technologies utilisées) sans même avoir besoin de l'attaquer.")
    dessiner_definition(pdf, "DAST (Dynamic Application Security Testing)", "L'outil que nous avons utilisé. C'est un robot qui interagit avec votre site web de l'extérieur en imitant le comportement d'un vrai pirate informatique.")

    # sauvegarde du fichier
    pdf.output("rapport.pdf")
