<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BouzuSec - Diagnostic Cybersécurité</title>
    <link rel="stylesheet" href="style.css?v=2">
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
                
                <form id="scanForm" action="traitement.php" method="POST">
                    <div class="radio-group">
                        <label><input type="radio" name="mode" value="simple" checked> Mode Simple</label>
                        <label><input type="radio" name="mode" value="avance"> Mode Avancé</label>
                    </div>
                    
                    <div class="form-group">
                        <input type="text" name="cible" placeholder="Ex: tesla.com ou localhost:8080" required>
                        <button type="submit">Diagnostiquer</button>
                    </div>
                </form>

                <div class="status-placeholder">
                    <?php
                    // Vérification si le scan vient de se terminer via l'URL
                    if (isset($_GET['scan']) && $_GET['scan'] == 'termine') {
                        
                        $cible_affichee = htmlspecialchars($_GET['cible']);
                        $fichier_pdf = 'rapport.pdf';

                        // On affiche le bouton seulement si le script Python a bien créé le fichier
                        if (file_exists($fichier_pdf)) {
                            echo "<div style='background: white; padding: 20px; border-radius: 8px; border-left: 5px solid var(--primary-orange); box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: left;'>";
                            echo "<h3 style='margin-top: 0; color: #2c3e50;'>✅ Diagnostic terminé !</h3>";
                            echo "<p style='margin-bottom: 15px; color: #333;'>L'audit en boîte noire de <strong>" . $cible_affichee . "</strong> a été généré avec succès.</p>";
                            echo "<a href='rapport.pdf' download='Audit_Cyber_" . $cible_affichee . ".pdf' style='display: inline-block; padding: 12px 20px; background-color: #2c3e50; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;'>📄 Télécharger le Rapport (PDF)</a>";
                            echo "</div>";
                        } else {
                            // Message d'erreur vulgarisé si le PDF est manquant
                            echo "<div style='color: #e74c3c; background: #fdeaea; padding: 15px; border-radius: 8px; text-align: left;'>";
                            echo "<strong>Anomalie détectée :</strong> Le rapport n'a pas pu être généré. Cela peut arriver si la cible bloque nos outils ou si le serveur manque de droits d'écriture.";
                            echo "</div>";
                        }

                    } else {
                        // État par défaut au chargement de la page
                        echo "<em style='color: #7f8c8d;'>Cible : En attente d'analyse...</em>";
                    }
                    ?>
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
                <p>Analyse complète de votre écosystème : du nom de domaine jusqu'à l'hébergement serveur, en passant par le code de vos pages web.</p>
            </div>
            <div class="card">
                <h3>Deux modes d'analyse</h3>
                <p>Mode Simple pour un bilan de santé rapide (Top 10 OWASP), ou Mode Avancé pour une investigation approfondie de type "boîte noire".</p>
            </div>
            <div class="card">
                <h3>Éthique White Hat</h3>
                <p>Diagnostic 100% bienveillant et sécurisé. Nos outils n'altèrent pas vos données et garantissent la continuité de vos services.</p>
            </div>
        </div>
    </section>

    <footer>
        <p>Projet SAÉ 401 - Cybersécurité | BouzuSec Scanner</p>
    </footer>

    <div id="cyber-loader" style="display: none;">
        <div class="loader-content">
            <h2 id="loader-title">ANALYSE DE SÉCURITÉ EN COURS...</h2>
            
            <div class="big-progress-track">
                <div id="big-progress-fill"></div>
            </div>
            
            <div class="loader-stats">
                <span id="loader-percent">0%</span>
            </div>
            
            <p id="loader-message">Initialisation des protocoles de reconnaissance...</p>
        </div>
    </div>

    <script>
        const form = document.getElementById('scanForm');
        
        form.addEventListener('submit', function(e) {
            // Empêche l'envoi immédiat pour afficher l'animation
            e.preventDefault();
            
            // Affichage de l'overlay
            document.getElementById('cyber-loader').style.display = 'flex';
            
            const messageElement = document.getElementById('loader-message');
            const fillElement = document.getElementById('big-progress-fill');
            const percentElement = document.getElementById('loader-percent');

            // Envoi de la requête en arrière-plan (AJAX) au fichier PHP de traitement
            const formData = new FormData(form);
            fetch('traitement.php', {
                method: 'POST',
                body: formData
            }).then(() => {
                // Quand le script PHP a terminé, on redirige vers la page de résultat
                window.location.href = 'index.php?scan=termine&cible=' + encodeURIComponent(formData.get('cible'));
            });

            // LA MASTERCLASS : Lecture du fichier JSON généré par Python en temps réel !
            const pollInterval = setInterval(() => {
                // On ajoute un timestamp à l'URL pour éviter le cache du navigateur
                fetch('statut_audit.json?t=' + new Date().getTime())
                    .then(response => response.json())
                    .then(data => {
                        // Mise à jour de la barre et du texte selon ce que Python a écrit
                        if(data.pourcentage !== undefined) {
                            fillElement.style.width = data.pourcentage + '%';
                            percentElement.innerText = data.pourcentage + '%';
                        }
                        if(data.message) {
                            messageElement.innerText = data.message;
                        }
                        
                        // Si le scan est fini on arrête d'interroger le fichier
                        if(data.pourcentage >= 100) {
                            clearInterval(pollInterval);
                        }
                    })
                    .catch(err => {
                        // Le fichier n'existe pas encore (Python vient de démarrer)
                        console.log("En attente de la création du fichier statut par Python...");
                    });
            }, 1000); // On vérifie toutes les 1 secondes
        });
    </script>
</body>
</html>
