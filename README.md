# Système de Gestion des Notes Scolaires

## Informations de l'étudiant

- **Nom**: [VOTRE_NOM]
- **Prénom**: [VOTRE_PRÉNOM]
- **Matricule**: [VOTRE_MATRICULE]
- **Classe**: [VOTRE_CLASSE]

## Description

Application console en Python pour la gestion complète des notes scolaires d'un établissement. Le système permet de gérer les étudiants, les matières, les notes et de calculer des statistiques académiques détaillées.

## Installation

### Prérequis

- Python 3.6 ou supérieur
- Aucune dépendance externe requise (utilise uniquement les bibliothèques standard de Python)

### Étapes d'installation

1. Téléchargez ou clonez le projet
2. Assurez-vous d'être dans le répertoire du projet
3. Vérifiez que Python est installé en exécutant :
   ```bash
   python --version
   ```

## Exécution

Pour lancer l'application, exécutez simplement :

```bash
python main.py
```

L'application démarrera et vous demandera le mot de passe pour vous authentifier.

## Mot de passe par défaut

Le mot de passe par défaut est : **password**

> **Note** : Vous pouvez modifier le mot de passe dans le fichier `data/config.json`

## Organisation des fichiers

### Structure du projet

```
student_grade_manager/
├── main.py                 # Point d'entrée avec authentification
├── models/                 # Modèles de données
│   ├── __init__.py
│   ├── student.py          # Classe Student
│   ├── subject.py         # Classe Subject
│   └── grade.py           # Classe Grade
├── services/              # Services métier
│   ├── __init__.py
│   ├── file_manager.py    # Gestion des fichiers JSON
│   ├── menu.py           # Gestion des menus console
│   └── statistics.py     # Calculs statistiques
├── data/                  # Données de l'application
│   ├── config.json       # Configuration (mot de passe)
│   ├── students.json     # Données des étudiants
│   ├── subjects.json    # Données des matières
│   └── grades.json      # Données des notes
└── README.md            # Ce fichier
```

### Format de stockage

Toutes les données sont stockées dans des fichiers JSON dans le répertoire `data/` :

- **config.json** : Contient la configuration du système (mot de passe)
- **students.json** : Liste de tous les étudiants avec leurs informations (nom, prénom, matricule, niveau)
- **subjects.json** : Liste de toutes les matières avec leurs caractéristiques (nom, code, coefficient, niveau)
- **grades.json** : Liste de toutes les notes avec les références aux étudiants et matières

### Avantages de cette organisation

- **Simplicité** : Format JSON lisible et facile à manipuler
- **Persistance** : Les données sont sauvegardées automatiquement après chaque modification
- **Fiabilité** : Utilisation d'un fichier temporaire pour éviter la corruption des données
- **Portabilité** : Pas de base de données externe nécessaire

## Fonctionnalités implémentées

### 1. Authentification ✓

- Demande de mot de passe au démarrage
- Limitation à 3 tentatives de connexion
- Gestion des erreurs de saisie

### 2. Gestion des étudiants ✓

- **Ajouter** un étudiant (nom, prénom, matricule unique, niveau/classe)
- **Modifier** les informations d'un étudiant
- **Supprimer** un étudiant (supprime aussi toutes ses notes)
- **Rechercher** un étudiant (par matricule, nom ou prénom)
- **Lister** les étudiants (par classe ou tous)

### 3. Gestion des matières ✓

- **Ajouter** une matière (nom, code, coefficient, niveau/classe concerné)
- **Modifier** une matière
- **Supprimer** une matière (supprime aussi toutes ses notes)
- **Lister** les matières par niveau/classe

### 4. Saisie des notes ✓

- **Enregistrer** les notes des étudiants par matière et par niveau
- **Validation** que les notes sont comprises entre 0 et 20
- **Modifier** les notes existantes
- **Supprimer** des notes
- Gestion des cas particuliers (étudiant sans note, etc.)
- Un étudiant ne peut avoir qu'une seule note par matière

### 5. Consultation des notes ✓

- **Notes d'un étudiant spécifique** : Affiche toutes les notes d'un étudiant
- **Notes d'une classe pour une matière donnée** : Affiche les notes de tous les étudiants d'une classe dans une matière
- **Bulletin complet d'un étudiant** : Affiche toutes les notes avec les moyennes et le rang dans la classe

### 6. Statistiques et analyses ✓

#### Par étudiant :
- Moyenne générale (notes pondérées par les coefficients)
- Rang dans sa classe

#### Par classe :
- Moyenne générale de la classe
- Meilleur étudiant de la classe
- Classement complet des étudiants

#### Par matière :
- Moyenne générale par matière
- Meilleur étudiant par matière

#### Globalement (toute l'école) :
- Moyenne générale de l'établissement
- Meilleur étudiant de l'école

## Données d'exemple

Le système est livré avec des données d'exemple pré-remplies :

- **12 étudiants** répartis sur 3 niveaux (L1, L2, L3)
- **9 matières** avec différents coefficients
- **36 notes** réparties sur les différents étudiants et matières

Ces données permettent de tester immédiatement toutes les fonctionnalités du système.

## Utilisation

### Navigation dans les menus

L'application utilise un système de menus hiérarchiques :

1. **Menu principal** : Accès à toutes les fonctionnalités principales
2. **Sous-menus** : Accès aux opérations spécifiques (CRUD, consultation, statistiques)

### Conseils d'utilisation

- Utilisez les numéros pour naviguer dans les menus
- Laissez les champs vides lors de la modification pour conserver les valeurs actuelles
- Les matricules et codes de matières doivent être uniques
- Les notes doivent être comprises entre 0 et 20
- Les données sont sauvegardées automatiquement après chaque modification

## Gestion des erreurs

Le système gère plusieurs types d'erreurs :

- **Erreurs de saisie** : Validation des données entrées
- **Erreurs de fichiers** : Gestion des fichiers corrompus ou manquants
- **Erreurs de logique** : Vérification de l'unicité des matricules et codes
- **Interruptions** : Gestion propre de l'interruption par Ctrl+C

## Technologies utilisées

- **Python 3.x** : Langage de programmation
- **JSON** : Format de stockage des données
- **POO** : Programmation orientée objet pour la structure du code
- **Bibliothèques standard** : Aucune dépendance externe

## Auteur

Développé dans le cadre des Travaux Pratiques Python de l'Institut Universitaire Catholique Sainte Thérèse de Yaoundé - École Polytechnique Supérieure / VOGT HIGH TECH

## Licence

Ce projet est un travail académique.

