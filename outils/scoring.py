# module de calcul objectif des risques (methode du maillon faible anssi et cvss)

# on evalue chaque outil pour lui donner une note de risque sur 10
def evaluer_osint(texte):
    t = texte.lower()
    if "phpmyadmin" in t or "wordpress" in t: return 6
    if "cloudflare" in t or "waf" in t or "sucuri" in t: return 1
    return 3

def evaluer_reseau(texte):
    t = texte.lower()
    if "smb 445" in t or "ftp 21" in t: return 10
    if "base de données ouverte" in t or "3306" in t: return 8
    if "serveur pur" in t: return 2
    if "ouvert" in t: return 4
    return 1

def evaluer_enum(texte):
    t = texte.lower()
    # les pires failles de gobuster
    if ".env" in t or ".git" in t or ".ssh" in t or "dump.sql" in t: return 10
    if "admin" in t or "phpmyadmin" in t: return 8
    if "upload" in t or "backup" in t: return 6
    if "standards" in t: return 2
    return 0

def evaluer_config(texte):
    t = texte.lower()
    if "périmé" in t or "obsolète" in t: return 9
    if "écrans de surveillance" in t: return 7
    if "détournement de clics" in t or "mime" in t: return 4
    return 1

def evaluer_app(texte):
    t = texte.lower()
    # les failles critiques de zap
    if "injection" in t or "xss" in t or "csrf" in t: return 10
    if "traversal" in t: return 9
    return 0

# la fonction principale appelee par l orchestrateur
def calculer_score_global(texte_osint, texte_nmap, texte_gobuster, texte_diag):
    # 1. on calcule les 5 scores pour le graphique radar
    score_osint = evaluer_osint(texte_osint)
    score_reseau = evaluer_reseau(texte_nmap)
    score_enum = evaluer_enum(texte_gobuster)
    score_config = evaluer_config(texte_diag)
    score_app = evaluer_app(texte_diag)

    # on range ca dans une liste pour l envoyer au dessinateur pdf
    scores_radar = [score_osint, score_reseau, score_enum, score_config, score_app]

    # 2. la regle d or de l anssi : un systeme vaut son maillon le plus faible
    # on cherche le risque le plus eleve parmi les 5
    pire_risque = max(scores_radar)

    # 3. on transforme ce risque en energie (risque 10 = energie 10%)
    energie_sante = 100 - (pire_risque * 9)
    if energie_sante < 5: 
        energie_sante = 5 # on bloque a 5% minimum pour le visuel
        
    note_sur_10 = round(energie_sante / 10, 1)

    # 4. on deduit la matrice de couleur anssi en fonction du pire risque
    if pire_risque >= 9:
        barres = 1
        niveau_texte = "RISQUE CRITIQUE"
        couleur = (229, 57, 53) # rouge
    elif pire_risque >= 7:
        barres = 2
        niveau_texte = "RISQUE ÉLEVÉ"
        couleur = (230, 126, 34) # orange
    elif pire_risque >= 4:
        barres = 3
        niveau_texte = "RISQUE MODÉRÉ"
        couleur = (253, 216, 53) # jaune
    else:
        barres = 4
        niveau_texte = "RISQUE FAIBLE"
        couleur = (39, 174, 96) # vert

    # on renvoie tout ca a l orchestrateur, y compris le tableau du radar
    return barres, energie_sante, note_sur_10, niveau_texte, couleur, scores_radar
