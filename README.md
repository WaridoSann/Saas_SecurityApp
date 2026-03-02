# 🛡️ BouzuSec - SaaS Security Audit Platform

> ⚠️ **Statut : Projet en cours de développement (Work In Progress)** ⚠️
> 
> **Projet SAÉ 401** : Plateforme SaaS visant à réaliser un audit de cybersécurité (boîte noire) sur un site web, conçu pour être accessible, compréhensible et professionnel.

## 📋 En quoi consiste ce projet ?
BouzuSec (dépôt `Saas_SecurityApp`) est un outil d'audit cyber pensé pour vulgariser les résultats de tests d'intrusion. 

L'objectif final est de permettre à un utilisateur (même non-expert) de cibler une URL depuis une interface web simple. En arrière-plan, notre orchestrateur lancera de manière automatisée divers outils de reconnaissance et de scan open-source, puis générera un rapport de sécurité au format PDF. Ce rapport sera clair, visuel, et se basera sur le système de notation de risques de l'ANSSI.

## ✨ Fonctionnalités prévues
* **Audit à 360° :** Analyse du périmètre complet (nom de domaine, arborescence, vulnérabilités web).
* **Deux modes d'analyse :**
  * `Mode Simple` : Scan de surface et reconnaissance de base (Whois, balayage réseau rapide).
  * `Mode Avancé` : Scans approfondis pour identifier des failles spécifiques (Injections SQL, XSS, etc.).
* **Reporting PDF Vulgarisé :** Génération automatique d'un document stylisé, traduisant les sorties consoles complexes (CLI) en un résumé exécutif compréhensible par un client.
* **Approche "White Hat" :** Tests non destructifs, sans violation du système cible, avec des temporisations pour éviter toute surcharge (pas de DDoS involontaire).

## 🛠️ Architecture & Technologies (en cours d'implémentation)
* **Frontend :** HTML5, CSS3, PHP (Interface UI/UX épurée).
* **Backend (Orchestrateur) :** Python 3 (Nettoyage des données de formulaires, exécution des commandes système Linux, création du livrable).
* **Outils Cyber au cœur du moteur :** `whois`, `Nmap`, `GoBuster`, `SQLmap` (intégration progressive).
* **Librairie tierce :** `fpdf` (Python) pour dessiner et générer le rapport PDF à la volée.

---
*Projet développé dans le cadre du BUT - Cybersécurité.*
