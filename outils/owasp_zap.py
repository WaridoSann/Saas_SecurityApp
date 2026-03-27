# module d attaque lourde avec owasp zap
# on importe de quoi lancer la commande et de quoi lire le xml que zap va cracher
import subprocess
import os
import xml.etree.ElementTree as ET

# dictionnaire des failles applicatives graves pour faire pro devant le boss
# c est ici qu on traduit les trucs hyper techniques en risques pour l entreprise
ANALYSE_ZAP = {
    "xss": {
        "mots_cles": ["cross site scripting", "xss"],
        "titre": "Injection de code malveillant",
        "explication": "Notre outil d'attaque a réussi à injecter du code dans les pages de votre site. Cela signifie qu'un pirate pourrait forcer le navigateur de vos visiteurs à exécuter des actions à leur insu, comme voler leurs identifiants de connexion ou les rediriger vers un site frauduleux. C'est une faille critique qui brise la confiance de vos utilisateurs."
    },
    "sqli": {
        "mots_cles": ["sql injection", "sqli", "injection sql"],
        "titre": "Manipulation de la base de données",
        "explication": "Nous avons pu manipuler les requêtes que votre site envoie à sa base de données. C'est l'équivalent numérique d'un braquage de banque : un attaquant peut lire, modifier ou effacer l'intégralité de vos données clients, y compris les mots de passe et les historiques d'achats. Une correction immédiate du code est requise."
    },
    "csrf": {
        "mots_cles": ["csrf", "cross-site request forgery"],
        "titre": "Falsification de requête",
        "explication": "Le site ne vérifie pas correctement si une action provient bien de l'utilisateur légitime. Un pirate pourrait envoyer un lien piégé à l'un de vos clients ou administrateurs. Si ce dernier clique, le pirate pourra effectuer des actions en son nom (comme changer un mot de passe ou valider un paiement) sans qu'il ne s'en rende compte."
    },
    "traversal": {
        "mots_cles": ["path traversal", "directory traversal"],
        "titre": "Exploration illicite des dossiers",
        "explication": "Une faille permet de remonter dans l'arborescence de votre serveur au-delà du dossier public du site web. L'attaquant peut ainsi lire des fichiers internes du système d'exploitation, ce qui est le premier pas vers une prise de contrôle totale de la machine."
    }
}

# la fonction principale qui va invoquer le monstre
def faire_zap(cible_url, mode_scan):
    # si c est pas le mode avance on lance pas cette machine de guerre
    if mode_scan != "avance":
        return "Scan applicatif ZAP ignoré (réservé au mode avancé)."
        
    # on definit ou zap va sauvegarder son rapport temporaire
    fichier_rapport = "/tmp/rapport_zap.xml"
    
    # on efface l ancien rapport s il existe pour pas melanger les cibles
    if os.path.exists(fichier_rapport):
        os.remove(fichier_rapport)
        
    try:
        # la commande pour lancer zap en mode invisible et generer un xml rapide
        commande = [
            "zaproxy", "-cmd",
            "-quickurl", cible_url,
            "-quickout", fichier_rapport
        ]
        
        # on lance le scan avec un timeout de 5 minutes car zap peut etre tres long
        subprocess.run(commande, capture_output=True, text=True, timeout=300)
        
        # on verifie si le fichier a bien ete cree sinon on arrete les frais
        if not os.path.exists(fichier_rapport):
            return "Le module d'attaque applicative n'a pas pu générer son rapport. Le serveur a peut-être bloqué l'outil ou ZAP n'est pas bien installé."
            
        # on lit le fichier xml avec la librairie python etree
        arbre = ET.parse(fichier_rapport)
        racine = arbre.getroot()
        
        failles_trouvees = set()
        
        # on fouille dans le xml pour trouver les alertes generees par zap
        for alerte in racine.iter('alertitem'):
            nom_alerte = alerte.find('name').text.lower() if alerte.find('name') is not None else ""
            
            # on compare le nom de l alerte avec notre super dictionnaire
            for cle, data in ANALYSE_ZAP.items():
                for mot_cle in data["mots_cles"]:
                    if mot_cle in nom_alerte:
                        failles_trouvees.add(cle)
                        
        # si zap n a rien trouve de grave
        if not failles_trouvees:
            return "Nous avons soumis vos formulaires et vos pages à des tentatives d'injections complexes. La très bonne nouvelle est que vos défenses applicatives ont résisté à ces attaques scénarisées."
            
        # la redaction du texte final pour le pdf (sans les tirets, bien propre)
        texte_final = "Notre outil d'attaque dynamique a simulé le comportement d'un pirate cherchant à forcer les champs de saisie et les formulaires de votre site web. Ce test intrusif a révélé des failles applicatives majeures :\n\n"
        
        for faille in failles_trouvees:
            # on ajoute le raccourci entre parentheses (xss) etc.
            texte_final += f"Titre : {ANALYSE_ZAP[faille]['titre']} ({faille})\nExplication : {ANALYSE_ZAP[faille]['explication']}\n\n"
            
        texte_final += "Ces vulnérabilités permettent à un attaquant d'interagir directement avec vos bases de données ou vos clients. Une intervention de vos développeurs pour filtrer les saisies utilisateurs est indispensable."
        
        return texte_final
        
    except subprocess.TimeoutExpired:
        # si le site est trop gros zap va tourner dans le vide
        return "L'analyse applicative a pris trop de temps. L'audit a été interrompu pour ne pas saturer la bande passante de vos serveurs."
    except Exception as e:
        # en cas de crash de zap
        return "Une erreur inattendue a empêché la finalisation des tests d'injection sur vos formulaires."
