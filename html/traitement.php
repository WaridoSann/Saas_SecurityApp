<?php
// on verifie que la requete vient bien du formulaire
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    $cible = htmlspecialchars($_POST['cible']);
    $mode = htmlspecialchars($_POST['mode']);

    // on prepare et on lance la commande python
    $commande = "python3 orchestrateur.py " . escapeshellarg($cible) . " " . escapeshellarg($mode);
    $resultat = shell_exec($commande);

    // quand le script python a fini (et que le json est cree), on redirige vers l'accueil avec un petit mot-clé dans l'url
    header("Location: index.php?scan=termine&cible=" . urlencode($cible));
    exit();

} else {
    // si on force l'acces a la page, on renvoie a l'accueil
    header("Location: index.php");
    exit();
}
?>
