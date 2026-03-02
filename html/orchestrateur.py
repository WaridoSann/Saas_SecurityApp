import sys
import subprocess
import time
from fpdf import FPDF

# on verifie les arguments
if len(sys.argv) < 3:
    print("Erreur d'arguments")
    sys.exit(1)

cible_url = sys.argv[1]
mode_scan = sys.argv[2]
domaine = cible_url.replace("https://", "").replace("http://", "").split("/")[0]

# 1. On lance la commande whois
try:
    res = subprocess.run(["whois", domaine], capture_output=True, text=True)
    # on garde juste les premieres lignes pour pas saturer le PDF
    lignes_whois = res.stdout.split('\n')[:10]
    whois_propre = "\n".join(lignes_whois)
except:
    whois_propre = "Impossible de recuperer les infos publiques."

# 2. On cree le PDF
pdf = FPDF()
pdf.add_page()

# Titre du document (en orange)
pdf.set_font("Arial", 'B', 22)
pdf.set_text_color(230, 126, 34)
pdf.cell(0, 15, "BouzuSec - Audit de Securite", ln=True, align='C')

# Ligne de separation
pdf.line(10, 25, 200, 25)
pdf.ln(10)

# Infos de base
pdf.set_font("Arial", '', 12)
pdf.set_text_color(0, 0, 0) # on remet en noir
pdf.cell(0, 10, f"Cible analysee : {domaine}", ln=True)
pdf.cell(0, 10, f"Date du scan : {time.strftime('%d/%m/%Y a %H:%M')}", ln=True)
pdf.cell(0, 10, f"Mode choisi : {mode_scan}", ln=True)
pdf.ln(10)

# Section Vulgarisee (Pour le prof/client)
pdf.set_font("Arial", 'B', 14)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 10, "1. Resume Executif (Vulgarise)", ln=True)

pdf.set_font("Arial", '', 11)
pdf.set_text_color(0, 0, 0)
intro = ("Ce document presente les resultats de notre audit en boite noire. "
         "Notre approche est non intrusive (White Hat). "
         "Les vulnerabilites sont classees selon la matrice de risques de l'ANSSI, "
         "croisant la difficulte d'exploitation et l'impact metier.")
pdf.multi_cell(0, 8, intro)
pdf.ln(10)

# Section Technique
pdf.set_font("Arial", 'B', 14)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 10, "2. Reconnaissance (OSINT)", ln=True)

pdf.set_font("Arial", '', 11)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 8, "Voici les premieres informations publiques (Whois) recoltees sur la cible :")
pdf.ln(5)

# On affiche le terminal brut dans une police type "code"
pdf.set_font("Courier", '', 9)
pdf.set_fill_color(240, 240, 240)
pdf.multi_cell(0, 6, whois_propre, fill=True)

# On sauvegarde le pdf dans notre dossier web
pdf.output("rapport.pdf")

print("OK")
