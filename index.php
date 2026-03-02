<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BouzuSec - Diagnostic Cybersécurité</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header>
        <div class="logo">🛡️ BouzuSec</div>
        <nav>
            <ul>
                <li><a href="#fonctionnalites">Fonctionnalités</a></li>
                <li><a href="#comment-ca-marche">Comment ça marche ?</a></li>
                <li><a href="#docs">Docs</a></li>
            </ul>
        </nav>
    </header>

    <section class="hero">
        <div class="hero-content">
            <div class="scan-module">
                <h1>BouzuSec <span>Scanner</span></h1>
                <h2>L'énergie vitale de votre site en un clin d'œil.</h2>
                <p>Des cyberattaques silencieuses peuvent vider les ressources de votre entreprise. Lancez un diagnostic visuel et compréhensible pour protéger votre avenir digital.</p>
                
                <form action="traitement.php" method="POST">
                    <div class="radio-group">
                        <label><input type="radio" name="mode" value="simple" checked> Mode Simple</label>
                        <label><input type="radio" name="mode" value="avance"> Mode Avancé</label>
                    </div>
                    
                    <div class="form-group">
                        <input type="text" name="cible" placeholder="Ex: https://www.votre-site.fr" required>
                        <button type="submit">Diagnostiquer</button>
                    </div>
                </form>

                <div class="status-placeholder">
                    <em>Cible : En attente d'analyse...</em>
                </div>
            </div>
        </div>
        
        <div class="hero-bg"></div>
    </section>

    <section id="fonctionnalites" class="content-section">
        <h2>Fonctionnalités de l'Audit</h2>
        <div class="grid-3">
            <div class="card">
                <h3>Audit à 360°</h3>
                <p>Nous analysons votre périmètre complet : le nom de domaine, chaque page de votre site web, ainsi que l'hébergement sous-jacent.</p>
            </div>
            <div class="card">
                <h3>Deux vitesses d'analyse</h3>
                <p>Choisissez le <strong>Mode Simple</strong> pour identifier les vulnérabilités les plus courantes, ou le <strong>Mode Avancé</strong> pour une recherche exhaustive et profonde.</p>
            </div>
            <div class="card">
                <h3>Approche "White Hat"</h3>
                <p>Notre audit en boîte noire est 100% sécurisé et éthique. Aucune violation de votre système n'est réalisée et nos outils sont temporisés pour éviter toute surcharge.</p>
            </div>
        </div>
    </section>

    <section id="comment-ca-marche" class="content-section" style="background-color: white;">
        <h2>Comment ça marche ?</h2>
        <div class="grid-3">
            <div class="card">
                <h3>1. Reconnaissance</h3>
                <p>Notre orchestrateur identifie les technologies de votre site (ex: CMS utilisé) et collecte des informations publiques (Whois, Dig).</p>
            </div>
            <div class="card">
                <h3>2. Traque des failles</h3>
                <p>Des moteurs open-source spécialisés (comme Nikto ou sqlmap) sont lancés en parallèle pour rechercher activement les vulnérabilités.</p>
            </div>
            <div class="card">
                <h3>3. Synthèse simplifiée</h3>
                <p>Les données techniques complexes sont traduites en un rapport visuel simple et vulgarisé, avec un système de scoring clair basé sur le risque et l'impact.</p>
            </div>
        </div>
    </section>

    <section id="docs" class="content-section">
        <h2>Documentation Technique</h2>
        <div class="grid-3">
            <div class="card">
                <h3>Matrice de Risque (ANSSI)</h3>
                <p>Nos résultats sont classés selon les standards de l'ANSSI, croisant la difficulté d'exploitation (Facile à Très difficile) avec l'impact métier (Mineur à Critique).</p>
            </div>
            <div class="card">
                <h3>Moteurs Open-Source</h3>
                <p>BouzuSec repose exclusivement sur des outils reconnus par la communauté cyber : <em>Nmap</em> pour le réseau, <em>SQLMap</em> pour les bases de données, ou encore <em>GoBuster</em> pour l'arborescence.</p>
            </div>
            <div class="card">
                <h3>Rapport Boîte Noire</h3>
                <p>L'audit est réalisé depuis l'extérieur, sans accès à votre code source ou à vos serveurs, simulant ainsi l'approche réelle d'un attaquant externe.</p>
            </div>
        </div>
    </section>

    <footer>
        <p>Projet SAÉ 401 - Cybersécurité | BouzuSec Scanner</p>
    </footer>

</body>
</html>
