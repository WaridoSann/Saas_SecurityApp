# Saas_SecurityApp (BouzuSec)

> **Branche : Livrables (V1)**

[cite_start]Projet visant à réaliser une plateforme SaaS permettant de réaliser un audit de sécurité sur un site web de manière automatisée et vulgarisée[cite: 250, 251].

## 📁 Structure de cette branche

Cette branche contient la première version fonctionnelle de notre outil :

* `html/` : Code source principal de l'application (Interface Web HTML/PHP, feuille de style CSS et l'orchestrateur Python).
* `config/` : Fichiers de configuration du projet.
* `docs/` : Documentation technique de l'architecture et du projet.
* `tests/` : Scripts et environnements de tests.

## ✨ Fonctionnalités implémentées (V1)
* Interface utilisateur claire et responsive.
* Formulaire de ciblage nettoyant automatiquement les URL.
* Liaison PHP -> Python pour l'exécution de commandes système sur le serveur (ex: `whois`).
* Génération à la volée d'un rapport de diagnostic au format PDF via la librairie Python `fpdf`.

## 🚀 Démarrage rapide pour tester
1. Transférez le contenu du dossier `html/` dans le répertoire de votre serveur web (ex: `/var/www/html/`).
2. Assurez-vous d'avoir installé la librairie pour la génération des PDF sur votre machine/serveur :
   ```bash
   pip install fpdf
