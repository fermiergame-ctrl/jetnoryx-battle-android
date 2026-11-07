# JetNoryx Battle — Android

Ce dépôt sert uniquement à distribuer l'application Android signée de JetNoryx Battle.

Dans **Releases**, télécharger **JetNoryx-Battle.apk** puis l'ouvrir sur Android 7 ou plus. Un seul fichier à télécharger et installer, sans compte GitHub, sans archive à extraire. Pour mettre à jour, installer par-dessus la version existante, sans désinstaller ni effacer les données.

Le jeu Web reste disponible sur https://jetnoryx-battle.fermiergame.workers.dev .

Le code source privé du jeu et la clé privée de signature ne sont pas stockés ici. L'entrée de publication interne sert à contourner une limitation de l'outil de transfert du développeur ; le workflow la réassemble et vérifie le fichier signé avant de publier **un APK complet**. Les joueurs utilisent uniquement le fichier de la Release.

Le workflow utilise un runner Ubuntu standard d'un dépôt public, sans cache/artefact Actions persistant, sans secret de signature et sans accès Cloudflare/D1. L'APK original est déjà signé. Les versions conservent leur identité d'application et leur certificat ; le versionCode augmente pour chaque mise à jour.

Version BÊTA : les contrôles automatisés et l’intégrité du paquet sont vérifiés ; les essais sur téléphones physiques restent à poursuivre.
