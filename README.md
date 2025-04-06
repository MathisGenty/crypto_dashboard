Objectif global du projet
Le projet vise à utiliser Linux et Dash pour créer un webscraper qui extrait les prix de cryptomonnaies via des scripts Bash. Ces données sont affichées en temps réel sur un tableau de bord interactif hébergé sur un serveur virtuel. Les informations sont régulièrement mises à jour grâce à des scripts d’automatisation.

Collecte des données
Les scripts scrape.sh et scrape_eth.sh téléchargent des pages web et extraient les prix du Bitcoin et de l’Ethereum avec curl et grep. Ces informations sont sauvegardées dans des fichiers CSV. Le script Ethereum utilise aussi des API pour garantir des données structurées.

Automatisation avec Cron et tmux
Cron planifie l’exécution des scripts toutes les 5 minutes, et tmux permet de maintenir l’application active même après une déconnexion, assurant une disponibilité continue du tableau de bord.

Génération des rapports quotidiens
Un script Python analyse les fichiers CSV pour générer un rapport quotidien sur les prix, la volatilité, et d’autres indicateurs du marché. Ce rapport est mis à jour chaque jour et accessible via l’application.

Tableau de bord interactif avec Dash
Le tableau de bord, développé avec Dash, affiche des graphiques dynamiques des prix des cryptomonnaies en temps réel et les rapports quotidiens. Cela permet à l’utilisateur de suivre l’évolution du marché.

Conclusion
Ce projet combine la gestion des données avec Linux et la visualisation interactive via Dash. Il illustre l’automatisation de l’extraction des données et leur affichage en temps réel sur un tableau de bord interactif.
