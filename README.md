# Application de Gestion de Tâches

Cette application Flask permet de gérer des tâches, d'ajouter, de modifier, de supprimer des tâches, et d'afficher les tâches archivées.

## Fonctionnalités

### Connexion et Inscription

- **Page de connexion** (`/` ou `/login`): Les utilisateurs peuvent se connecter en fournissant leur nom d'utilisateur et mot de passe. Si les informations sont correctes, ils sont redirigés vers la page de visualisation des tâches.
- **Page d'inscription** (`/register`): Permet aux nouveaux utilisateurs de créer un compte en fournissant un nom d'utilisateur et un mot de passe.

### Gestion des Tâches

- **Affichage des tâches** (`/view-tasks`): Affiche la liste des tâches actuelles de l'utilisateur connecté. Cette page permet également de charger plus de tâches avec pagination.
- **Ajout de tâche** (`/ajouter`): Un formulaire pour ajouter une nouvelle tâche avec un titre, une description et un statut. Si les informations sont valides et que la tâche n'existe pas déjà, elle est ajoutée à la base de données.
- **Modification de tâche** (`/modifier/<int:id>`): Permet de modifier une tâche existante en changeant son titre, sa description et son statut.
- **Suppression de tâche** (`/supprimer/<int:id>`): Supprime une tâche et l'archive en la déplaçant dans une table d'archivage.

### API

- **Récupération des tâches** (`/api/tasks`): Retourne les tâches actuelles en format JSON avec une prise en charge de la pagination. Si le nombre de tâches récupérées est inférieur à la limite demandée, des tâches supplémentaires sont récupérées depuis une API externe.
- **Récupération des tâches archivées** (`/api/archived-tasks`): Retourne les tâches archivées en format JSON.

### Archivage des Tâches

- Lorsque vous supprimez une tâche, elle est déplacée de la table des tâches actuelles vers une table d'archivage. Les tâches archivées peuvent être consultées via l'API dédiée.

## Détails Techniques

- **Connexion à la base de données**: Utilise MySQL pour stocker les utilisateurs, les tâches actuelles et les tâches archivées.
- **Gestion des sessions**: Les utilisateurs restent connectés grâce aux sessions gérées par Flask.
- **Génération de données**: Utilise la bibliothèque Faker pour générer des descriptions aléatoires pour les tâches importées depuis l'API externe.
- **Traduction**: Intègre Google Translate pour traduire les descriptions des tâches importées.

## Instructions de Déploiement

1. **Installation des dépendances**: Utilisez pip pour installer les dépendances listées dans `requirements.txt`.
2. **Configuration de la base de données**: Créez la base de données MySQL et les tables nécessaires en utilisant les scripts SQL fournis.
3. **Exécution de l'application**: Lancez l'application Flask avec `python app.py` et accédez-y via le navigateur à l'adresse `http://127.0.0.1:5000/`.

## Utilisation

1. **Connexion/Inscription**: Créez un compte ou connectez-vous avec des identifiants existants.
2. **Gestion des tâches**: Ajoutez, modifiez, supprimez et visualisez les tâches actuelles et archivées.
3. **API**: Utilisez les endpoints API pour intégrer les fonctionnalités de gestion des tâches dans d'autres applications.

---

Ce README fournit une vue d'ensemble sur le fonctionnement de l'application de gestion de tâches, sans toucher au code existant. Pour toute question ou problème, veuillez consulter le code source ou contacter le mainteneur du projet.
