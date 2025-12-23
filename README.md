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

## Authentification

### Implémentation

L'authentification est implémentée dans le fichier `main.py` via la fonction `authenticate()`. Le système fonctionne de la manière suivante :

1. **Chargement du mot de passe** : Au démarrage, le système charge le mot de passe depuis le fichier `data/config.json` via le `FileManager`. Si le fichier n'existe pas ou ne contient pas de mot de passe, le mot de passe par défaut "'password" est utilisé.

2. **Demande de saisie** : L'utilisateur est invité à saisir le mot de passe via la console. La saisie est masquée (texte visible, pas de masquage automatique pour une application console simple).

3. **Vérification** : Le mot de passe saisi est comparé avec celui stocké dans la configuration. La comparaison est effectuée de manière stricte (sensible à la casse).

4. **Limitation des tentatives** : Le système limite le nombre de tentatives à **3 essais maximum**. Après chaque tentative échouée, l'utilisateur est informé du nombre de tentatives restantes.

5. **Gestion des erreurs** : 
   - Si le mot de passe est correct, l'accès est autorisé et l'application se lance
   - Si le mot de passe est incorrect, l'utilisateur peut réessayer (dans la limite des 3 tentatives)
   - Si les 3 tentatives sont épuisées, l'accès est refusé et le programme se termine
   - Les interruptions par Ctrl+C sont gérées proprement

### Fonctionnement technique

```python
# Pseudo-code de l'authentification
1. Charger config.json → récupérer le mot de passe
2. Afficher l'interface d'authentification
3. Pour chaque tentative (max 3) :
   a. Demander la saisie du mot de passe
   b. Comparer avec le mot de passe stocké
   c. Si correct → retourner True et autoriser l'accès
   d. Si incorrect → incrémenter le compteur et afficher message
4. Si 3 tentatives échouées → retourner False et refuser l'accès
```

### Fichiers concernés

- **`main.py`** : Contient la fonction `authenticate()` qui gère tout le processus d'authentification
- **`services/file_manager.py`** : Fournit les méthodes `load_config()` et `save_config()` pour lire/écrire la configuration
- **`data/config.json`** : Fichier JSON contenant le mot de passe (format : `{"password": "votre_mot_de_passe"}`)

### Sécurité

Le système d'authentification est conçu pour être simple et adapté à une application console académique :

- **Stockage en clair** : Le mot de passe est stocké en texte clair dans le fichier JSON (adapté pour un projet académique, mais pas pour une production)
- **Pas de hachage** : Pour simplifier l'implémentation, aucun algorithme de hachage n'est utilisé
- **Protection basique** : La limitation des tentatives offre une protection minimale contre les attaques par force brute

### Modification du mot de passe

Pour changer le mot de passe, vous pouvez :

1. **Modifier directement le fichier** `data/config.json` :
   ```json
   {
     "password": "nouveau_mot_de_passe"
   }
   ```

2. **Via le code** : Utiliser le `FileManager` pour modifier la configuration programmatiquement

### Exemple d'utilisation

```
============================================================
    SYSTÈME DE GESTION DES NOTES SCOLAIRES
============================================================

Authentification requise
Vous avez 3 tentative(s) pour vous connecter

Mot de passe: password

✓ Authentification réussie !
```

## Gestion des Étudiants

### Implémentation

La gestion des étudiants est implémentée dans plusieurs fichiers pour assurer une séparation claire des responsabilités :

1. **Modèle de données** (`models/student.py`) : La classe `Student` représente un étudiant avec ses attributs (nom, prénom, matricule, niveau) et ses méthodes de validation.

2. **Service de fichiers** (`services/file_manager.py`) : Gère la persistance des données via les méthodes `load_students()` et `save_students()` qui lisent/écrivent dans `data/students.json`.

3. **Interface utilisateur** (`services/menu.py`) : La classe `Menu` contient toutes les méthodes pour interagir avec les étudiants via le menu "Gestion des étudiants".

### Fonctionnement technique

#### Structure de données

Chaque étudiant est représenté par un objet `Student` avec les attributs suivants :
- `nom` (str) : Nom de famille
- `prenom` (str) : Prénom
- `matricule` (str) : Identifiant unique de l'étudiant
- `niveau` (str) : Niveau/classe (ex: L1, L2, L3)

Les données sont stockées dans `data/students.json` sous forme de tableau JSON :
```json
[
  {
    "nom": "Dupont",
    "prenom": "Jean",
    "matricule": "ETU001",
    "niveau": "L1"
  }
]
```

#### Opérations CRUD

**1. Ajouter un étudiant** (`add_student()`)
- Demande la saisie de tous les champs (nom, prénom, matricule, niveau)
- Vérifie l'unicité du matricule (un matricule ne peut exister qu'une seule fois)
- Valide les données via la méthode `validate()` de la classe `Student`
- Ajoute l'étudiant à la liste en mémoire
- Sauvegarde automatiquement dans le fichier JSON

**2. Modifier un étudiant** (`modify_student()`)
- Recherche l'étudiant par son matricule
- Permet de modifier chaque champ (nom, prénom, niveau)
- Le matricule ne peut pas être modifié (identifiant unique)
- Conserve les valeurs actuelles si l'utilisateur laisse un champ vide
- Valide et sauvegarde les modifications

**3. Supprimer un étudiant** (`delete_student()`)
- Recherche l'étudiant par son matricule
- Demande une confirmation avant suppression
- Supprime l'étudiant de la liste
- **Supprime automatiquement toutes les notes associées** à cet étudiant (cohérence des données)
- Sauvegarde les modifications

**4. Rechercher un étudiant** (`search_student()`)
- Recherche par matricule, nom ou prénom (recherche partielle, insensible à la casse)
- Affiche tous les résultats correspondants
- Permet de trouver rapidement un étudiant même avec une information partielle

**5. Lister les étudiants** (`list_students()`)
- Option 1 : Lister tous les étudiants
- Option 2 : Filtrer par niveau/classe
- Affiche les informations formatées de manière lisible

### Validation des données

La classe `Student` implémente une méthode `validate()` qui vérifie :
- Que le nom n'est pas vide
- Que le prénom n'est pas vide
- Que le matricule n'est pas vide
- Que le niveau n'est pas vide

Si une validation échoue, un message d'erreur explicite est affiché à l'utilisateur.

### Gestion de l'unicité

Le système garantit l'unicité des matricules :
- Lors de l'ajout : vérification que le matricule n'existe pas déjà
- Le matricule sert d'identifiant unique pour toutes les opérations (modification, suppression, recherche)
- Les notes sont liées aux étudiants via leur matricule

### Persistance des données

- **Chargement** : Au démarrage de l'application, tous les étudiants sont chargés depuis `data/students.json` en mémoire
- **Sauvegarde** : Après chaque modification (ajout, modification, suppression), les données sont automatiquement sauvegardées dans le fichier JSON
- **Sauvegarde atomique** : Utilisation d'un fichier temporaire pour éviter la corruption en cas d'interruption

### Fichiers concernés

- **`models/student.py`** : Classe `Student` avec validation et conversion JSON
- **`services/file_manager.py`** : Méthodes `load_students()` et `save_students()`
- **`services/menu.py`** : Méthodes `handle_students_menu()`, `add_student()`, `modify_student()`, `delete_student()`, `search_student()`, `list_students()`
- **`data/students.json`** : Fichier JSON contenant toutes les données des étudiants

### Exemple d'utilisation

```
============================================================
    GESTION DES ÉTUDIANTS
============================================================

1. Ajouter un étudiant
2. Modifier un étudiant
3. Supprimer un étudiant
4. Rechercher un étudiant
5. Lister les étudiants
6. Retour au menu principal

Votre choix: 1

============================================================
    AJOUT D'UN ÉTUDIANT
============================================================
Nom: Dupont
Prénom: Jean
Matricule: ETU001
Niveau/Classe: L1

✓ Étudiant ajouté avec succès: Jean DUPONT (ETU001) - L1
```

### Intégration avec les autres modules

La gestion des étudiants est étroitement liée aux autres fonctionnalités :
- **Notes** : Les notes sont liées aux étudiants via le matricule
- **Statistiques** : Les calculs de moyennes et classements utilisent les données des étudiants
- **Bulletins** : Les bulletins affichent les informations de l'étudiant avec ses notes

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

## Gestion des Matières

### Implémentation

La gestion des matières est implémentée de manière similaire à la gestion des étudiants, avec une architecture modulaire :

1. **Modèle de données** (`models/subject.py`) : La classe `Subject` représente une matière avec ses attributs (nom, code, coefficient, niveau) et ses méthodes de validation.

2. **Service de fichiers** (`services/file_manager.py`) : Gère la persistance des données via les méthodes `load_subjects()` et `save_subjects()` qui lisent/écrivent dans `data/subjects.json`.

3. **Interface utilisateur** (`services/menu.py`) : La classe `Menu` contient toutes les méthodes pour interagir avec les matières via le menu "Gestion des matières".

### Fonctionnement technique

#### Structure de données

Chaque matière est représentée par un objet `Subject` avec les attributs suivants :
- `nom` (str) : Nom de la matière (ex: "Mathématiques", "Informatique")
- `code` (str) : Code unique de la matière (ex: "MATH", "INFO")
- `coefficient` (float) : Coefficient utilisé pour le calcul de la moyenne pondérée (doit être > 0)
- `niveau` (str) : Niveau/classe concerné par cette matière (ex: L1, L2, L3)

Les données sont stockées dans `data/subjects.json` sous forme de tableau JSON :
```json
[
  {
    "nom": "Mathématiques",
    "code": "MATH",
    "coefficient": 3.0,
    "niveau": "L1"
  }
]
```

#### Opérations CRUD

**1. Ajouter une matière** (`add_subject()`)
- Demande la saisie de tous les champs (nom, code, coefficient, niveau)
- Vérifie l'unicité du code (un code ne peut exister qu'une seule fois)
- Valide que le coefficient est un nombre positif
- Valide les données via la méthode `validate()` de la classe `Subject`
- Ajoute la matière à la liste en mémoire
- Sauvegarde automatiquement dans le fichier JSON

**2. Modifier une matière** (`modify_subject()`)
- Recherche la matière par son code
- Permet de modifier chaque champ (nom, coefficient, niveau)
- Le code ne peut pas être modifié (identifiant unique)
- Conserve les valeurs actuelles si l'utilisateur laisse un champ vide
- Valide que le nouveau coefficient est un nombre positif
- Valide et sauvegarde les modifications

**3. Supprimer une matière** (`delete_subject()`)
- Recherche la matière par son code
- Demande une confirmation avant suppression
- Supprime la matière de la liste
- **Supprime automatiquement toutes les notes associées** à cette matière (cohérence des données)
- Sauvegarde les modifications

**4. Lister les matières** (`list_subjects()`)
- Option 1 : Lister toutes les matières
- Option 2 : Filtrer par niveau/classe
- Affiche les informations formatées avec le nom, code, coefficient et niveau

### Validation des données

La classe `Subject` implémente une méthode `validate()` qui vérifie :
- Que le nom n'est pas vide
- Que le code n'est pas vide
- Que le niveau n'est pas vide
- Que le coefficient est supérieur à 0 (strictement positif)

Si une validation échoue, un message d'erreur explicite est affiché à l'utilisateur.

### Gestion de l'unicité

Le système garantit l'unicité des codes de matières :
- Lors de l'ajout : vérification que le code n'existe pas déjà
- Le code sert d'identifiant unique pour toutes les opérations (modification, suppression)
- Les notes sont liées aux matières via leur code

### Coefficient et calcul de moyenne

Le coefficient est un élément crucial pour le calcul des moyennes :
- **Moyenne pondérée** : La moyenne générale d'un étudiant est calculée en tenant compte des coefficients
  - Formule : `Moyenne = Σ(note × coefficient) / Σ(coefficient)`
- **Importance relative** : Un coefficient plus élevé signifie que la matière a plus de poids dans la moyenne
- **Exemple** : Si une matière a un coefficient de 4.0 et une autre de 2.0, la première compte deux fois plus dans la moyenne

### Association avec les niveaux

Chaque matière est associée à un niveau/classe :
- Permet de filtrer les matières par niveau
- Assure que seuls les étudiants du bon niveau peuvent avoir des notes dans cette matière
- Facilite l'organisation des matières par année d'étude

### Persistance des données

- **Chargement** : Au démarrage de l'application, toutes les matières sont chargées depuis `data/subjects.json` en mémoire
- **Sauvegarde** : Après chaque modification (ajout, modification, suppression), les données sont automatiquement sauvegardées dans le fichier JSON
- **Sauvegarde atomique** : Utilisation d'un fichier temporaire pour éviter la corruption en cas d'interruption

### Fichiers concernés

- **`models/subject.py`** : Classe `Subject` avec validation et conversion JSON
- **`services/file_manager.py`** : Méthodes `load_subjects()` et `save_subjects()`
- **`services/menu.py`** : Méthodes `handle_subjects_menu()`, `add_subject()`, `modify_subject()`, `delete_subject()`, `list_subjects()`
- **`data/subjects.json`** : Fichier JSON contenant toutes les données des matières

### Exemple d'utilisation

```
============================================================
    GESTION DES MATIÈRES
============================================================

1. Ajouter une matière
2. Modifier une matière
3. Supprimer une matière
4. Lister les matières
5. Retour au menu principal

Votre choix: 1

============================================================
    AJOUT D'UNE MATIÈRE
============================================================
Nom de la matière: Mathématiques
Code de la matière: MATH
Coefficient [1.0]: 3.0
Niveau/Classe concerné: L1

✓ Matière ajoutée avec succès: Mathématiques (MATH) - Coef: 3.0 - L1
```

### Intégration avec les autres modules

La gestion des matières est étroitement liée aux autres fonctionnalités :
- **Notes** : Les notes sont liées aux matières via le code de la matière
- **Statistiques** : Les calculs de moyennes utilisent les coefficients des matières pour la pondération
- **Bulletins** : Les bulletins affichent les matières avec leurs coefficients et les notes correspondantes
- **Validation** : Lors de la saisie d'une note, le système vérifie que la matière existe et que l'étudiant appartient au bon niveau

### Cas particuliers

- **Matière sans notes** : Une matière peut exister sans avoir de notes associées (matière nouvellement créée)
- **Suppression en cascade** : La suppression d'une matière supprime automatiquement toutes ses notes pour maintenir la cohérence
- **Modification du coefficient** : Si le coefficient d'une matière est modifié, les moyennes existantes sont recalculées automatiquement lors de la consultation

## Saisie des Notes

### Implémentation

La saisie des notes est implémentée avec une architecture modulaire similaire aux autres fonctionnalités :

1. **Modèle de données** (`models/grade.py`) : La classe `Grade` représente une note avec ses attributs (matricule_etudiant, code_matiere, note, date) et ses méthodes de validation.

2. **Service de fichiers** (`services/file_manager.py`) : Gère la persistance des données via les méthodes `load_grades()` et `save_grades()` qui lisent/écrivent dans `data/grades.json`.

3. **Interface utilisateur** (`services/menu.py`) : La classe `Menu` contient toutes les méthodes pour gérer les notes via le menu "Saisie des notes".

### Fonctionnement technique

#### Structure de données

Chaque note est représentée par un objet `Grade` avec les attributs suivants :
- `matricule_etudiant` (str) : Matricule de l'étudiant (référence vers un étudiant)
- `code_matiere` (str) : Code de la matière (référence vers une matière)
- `note` (float) : Note obtenue (doit être entre 0 et 20)
- `date` (str) : Date de saisie de la note (format YYYY-MM-DD, générée automatiquement si non fournie)

Les données sont stockées dans `data/grades.json` sous forme de tableau JSON :
```json
[
  {
    "matricule_etudiant": "ETU001",
    "code_matiere": "MATH",
    "note": 15.5,
    "date": "2024-10-15"
  }
]
```

#### Opérations CRUD

**1. Enregistrer une note** (`add_grade()`)
- Demande le matricule de l'étudiant et vérifie qu'il existe
- Demande le code de la matière et vérifie qu'elle existe
- **Vérifie l'unicité** : Un étudiant ne peut avoir qu'une seule note par matière
- Demande la note et valide qu'elle est entre 0 et 20
- Génère automatiquement la date de saisie si non fournie
- Valide les données via la méthode `validate()` de la classe `Grade`
- Ajoute la note à la liste en mémoire
- Sauvegarde automatiquement dans le fichier JSON

**2. Modifier une note** (`modify_grade()`)
- Recherche la note par matricule d'étudiant et code de matière
- Permet de modifier uniquement la note (les autres champs sont fixes)
- Valide que la nouvelle note est entre 0 et 20
- Conserve la date originale de saisie
- Sauvegarde les modifications

**3. Supprimer une note** (`delete_grade()`)
- Recherche la note par matricule d'étudiant et code de matière
- Demande une confirmation avant suppression
- Supprime la note de la liste
- Sauvegarde les modifications

### Validation des données

La classe `Grade` implémente une méthode `validate()` qui vérifie :
- Que le matricule de l'étudiant n'est pas vide
- Que le code de la matière n'est pas vide
- Que la note est comprise entre 0 et 20 (inclus)

Si une validation échoue, un message d'erreur explicite est affiché à l'utilisateur.

### Règle d'unicité : Une note par étudiant et par matière

Le système garantit qu'un étudiant ne peut avoir qu'une seule note par matière :
- **Lors de l'ajout** : Vérification qu'aucune note n'existe déjà pour cette combinaison (matricule + code matière)
- **Lors de la modification** : La note existante est mise à jour plutôt que créée
- **Cohérence des données** : Cette règle assure que les calculs de moyennes sont cohérents

### Validation des références

Avant d'enregistrer une note, le système vérifie :
- **Existence de l'étudiant** : Le matricule doit correspondre à un étudiant existant
- **Existence de la matière** : Le code doit correspondre à une matière existante
- **Cohérence du niveau** : L'étudiant et la matière doivent appartenir au même niveau (vérification optionnelle selon l'implémentation)

### Gestion de la date

- **Génération automatique** : Si aucune date n'est fournie lors de la création, la date actuelle est utilisée automatiquement
- **Format** : Les dates sont stockées au format ISO (YYYY-MM-DD) pour faciliter le tri et la comparaison
- **Conservation** : Lors de la modification d'une note, la date originale est conservée

### Persistance des données

- **Chargement** : Au démarrage de l'application, toutes les notes sont chargées depuis `data/grades.json` en mémoire
- **Sauvegarde** : Après chaque modification (ajout, modification, suppression), les données sont automatiquement sauvegardées dans le fichier JSON
- **Sauvegarde atomique** : Utilisation d'un fichier temporaire pour éviter la corruption en cas d'interruption

### Fichiers concernés

- **`models/grade.py`** : Classe `Grade` avec validation et conversion JSON
- **`services/file_manager.py`** : Méthodes `load_grades()` et `save_grades()`
- **`services/menu.py`** : Méthodes `handle_grades_menu()`, `add_grade()`, `modify_grade()`, `delete_grade()`
- **`data/grades.json`** : Fichier JSON contenant toutes les notes

### Exemple d'utilisation

```
============================================================
    SAISIE DES NOTES
============================================================

1. Enregistrer une note
2. Modifier une note
3. Supprimer une note
4. Retour au menu principal

Votre choix: 1

============================================================
    ENREGISTREMENT D'UNE NOTE
============================================================
Matricule de l'étudiant: ETU001
Code de la matière: MATH
Note (0-20): 15.5

✓ Note enregistrée avec succès: Note: 15.5/20 - Matricule: ETU001 - Matière: MATH
```

### Cas d'erreur gérés

Le système gère plusieurs cas d'erreur :

1. **Étudiant inexistant** : Si le matricule n'existe pas, un message d'erreur est affiché
2. **Matière inexistante** : Si le code de matière n'existe pas, un message d'erreur est affiché
3. **Note déjà existante** : Si une note existe déjà pour cet étudiant dans cette matière, le système propose de la modifier plutôt que d'en créer une nouvelle
4. **Note invalide** : Si la note n'est pas entre 0 et 20, un message d'erreur est affiché
5. **Note non trouvée** : Lors de la modification ou suppression, si la note n'existe pas, un message d'erreur est affiché

### Intégration avec les autres modules

La saisie des notes est au cœur du système et s'intègre avec tous les autres modules :

- **Étudiants** : Les notes sont liées aux étudiants via leur matricule
- **Matières** : Les notes sont liées aux matières via leur code
- **Statistiques** : Les notes sont utilisées pour calculer les moyennes, classements et rangs
- **Bulletins** : Les notes sont affichées dans les bulletins avec les informations des matières
- **Consultation** : Les notes peuvent être consultées par étudiant, par classe ou par matière

### Calcul des moyennes

Les notes sont utilisées pour calculer :
- **Moyenne par matière** : Moyenne de toutes les notes d'une matière
- **Moyenne par étudiant** : Moyenne pondérée de toutes les notes d'un étudiant (en tenant compte des coefficients)
- **Moyenne par classe** : Moyenne de toutes les notes d'une classe
- **Moyenne globale** : Moyenne de toutes les notes de l'établissement

### Gestion des cas particuliers

- **Étudiant sans note** : Un étudiant peut exister sans avoir de notes (nouvellement inscrit)
- **Matière sans note** : Une matière peut exister sans avoir de notes (nouvellement créée)
- **Suppression en cascade** : La suppression d'un étudiant ou d'une matière supprime automatiquement toutes les notes associées
- **Notes manquantes** : Lors de l'affichage d'un bulletin, les matières sans note sont affichées avec "-" ou "Pas de note"

### Format d'affichage

Les notes sont affichées de manière cohérente dans tout le système :
- **Format standard** : `15.5/20` (note sur 20)
- **Avec matière** : `Mathématiques: 15.5/20`
- **Avec date** : `Mathématiques: 15.5/20 (Date: 2024-10-15)`
- **Dans les bulletins** : Tableau formaté avec matière, note, coefficient et points

## Consultation des Notes

### Implémentation

La consultation des notes est implémentée dans le module `services/menu.py` avec trois modes de consultation différents :

1. **Notes d'un étudiant spécifique** : Affiche toutes les notes d'un étudiant donné
2. **Notes d'une classe pour une matière** : Affiche les notes de tous les étudiants d'une classe dans une matière donnée
3. **Bulletin complet d'un étudiant** : Affiche un bulletin détaillé avec toutes les notes, moyennes et classement

### Fonctionnement technique

#### 1. Consultation des notes d'un étudiant (`show_student_grades()`)

**Fonctionnement** :
- Demande le matricule de l'étudiant
- Vérifie que l'étudiant existe
- Récupère toutes les notes associées à ce matricule
- Affiche les notes avec le nom de la matière et la date

**Format d'affichage** :
```
Étudiant: Jean DUPONT (ETU001) - L1

3 note(s) trouvée(s):

  - Mathématiques: 15.5/20 (Date: 2024-10-15)
  - Physique: 14.0/20 (Date: 2024-10-16)
  - Informatique: 16.5/20 (Date: 2024-10-17)
```

**Cas particuliers** :
- Si l'étudiant n'a aucune note, affiche "Aucune note enregistrée"
- Si l'étudiant n'existe pas, affiche un message d'erreur

#### 2. Consultation des notes d'une classe pour une matière (`show_class_grades_for_subject()`)

**Fonctionnement** :
- Demande le niveau/classe
- Demande le code de la matière
- Vérifie que la matière existe
- Récupère tous les étudiants de la classe
- Pour chaque étudiant, affiche sa note dans cette matière (ou "Pas de note" si absente)

**Format d'affichage** :
```
Matière: Mathématiques
Classe: L1

4 étudiant(s) dans la classe:

  - Jean DUPONT (ETU001): 15.5/20
  - Marie MARTIN (ETU002): 18.0/20
  - Pierre BERNARD (ETU003): 12.0/20
  - Sophie DUBOIS (ETU004): Pas de note
```

**Utilité** :
- Permet de voir rapidement les performances d'une classe dans une matière
- Identifie les étudiants sans note dans une matière
- Facilite la comparaison des notes entre étudiants d'une même classe

#### 3. Bulletin complet d'un étudiant (`show_student_bulletin()`)

**Fonctionnement** :
- Demande le matricule de l'étudiant
- Vérifie que l'étudiant existe
- Récupère toutes les matières du niveau de l'étudiant
- Pour chaque matière, affiche la note (si elle existe)
- Calcule la moyenne générale pondérée
- Calcule le rang de l'étudiant dans sa classe
- Affiche un tableau formaté avec toutes les informations

**Format d'affichage** :
```
============================================================
  BULLETIN DE NOTES
============================================================

Étudiant: Jean DUPONT
Matricule: ETU001
Niveau: L1

============================================================
Matière                          Note        Coef       Points
============================================================
Mathématiques                    15.50       3.00       46.50
Physique                         14.00       2.50       35.00
Informatique                     16.50       4.00       66.00
============================================================

Moyenne générale: 15.33/20
Rang dans la classe: 2ème
============================================================
```

**Calculs effectués** :
- **Points** : `note × coefficient` pour chaque matière
- **Moyenne générale** : `Σ(points) / Σ(coefficients)`
- **Rang** : Position de l'étudiant dans le classement de sa classe (basé sur la moyenne)

**Cas particuliers** :
- Si une matière n'a pas de note, affiche "-" pour la note et les points
- Si l'étudiant n'a aucune note, affiche "Aucune note enregistrée"
- Le rang est calculé uniquement si l'étudiant a au moins une note

### Intégration avec les modules de statistiques

La consultation des notes utilise le module `services/statistics.py` pour :
- **Calcul de la moyenne** : Utilise `calculate_student_average()` pour obtenir la moyenne pondérée
- **Calcul du rang** : Utilise `calculate_student_rank()` pour déterminer la position dans la classe
- **Cohérence des données** : Les calculs sont effectués en temps réel à partir des données actuelles

### Fichiers concernés

- **`services/menu.py`** : Contient les méthodes de consultation :
  - `handle_consultation_menu()` : Menu principal de consultation
  - `show_student_grades()` : Notes d'un étudiant
  - `show_class_grades_for_subject()` : Notes d'une classe pour une matière
  - `show_student_bulletin()` : Bulletin complet
- **`services/statistics.py`** : Fournit les méthodes de calcul :
  - `calculate_student_average()` : Moyenne d'un étudiant
  - `calculate_student_rank()` : Rang d'un étudiant
- **`models/`** : Utilise les classes `Student`, `Subject` et `Grade` pour accéder aux données

### Exemple d'utilisation

```
============================================================
    CONSULTATION DES NOTES
============================================================

1. Notes d'un étudiant
2. Notes d'une classe pour une matière
3. Bulletin complet d'un étudiant
4. Retour au menu principal

Votre choix: 3

============================================================
    BULLETIN COMPLET D'UN ÉTUDIANT
============================================================
Matricule de l'étudiant: ETU001

============================================================
  BULLETIN DE NOTES
============================================================
...
```

### Avantages de cette implémentation

1. **Flexibilité** : Trois modes de consultation pour répondre à différents besoins
2. **Clarté** : Affichage formaté et lisible pour faciliter la compréhension
3. **Complétude** : Le bulletin inclut toutes les informations nécessaires (notes, moyennes, rangs)
4. **Temps réel** : Les calculs sont effectués à chaque consultation avec les données actuelles
5. **Gestion des erreurs** : Vérification de l'existence des étudiants et matières avant affichage

### Cas d'erreur gérés

- **Étudiant inexistant** : Message d'erreur si le matricule n'existe pas
- **Matière inexistante** : Message d'erreur si le code de matière n'existe pas
- **Classe vide** : Affichage approprié si aucun étudiant n'est dans la classe
- **Aucune note** : Affichage clair quand un étudiant ou une classe n'a pas de notes

### Performance

- **Chargement en mémoire** : Toutes les données sont chargées au démarrage, les consultations sont rapides
- **Calculs optimisés** : Les calculs de moyennes et rangs sont effectués uniquement quand nécessaire
- **Pas de requêtes multiples** : Les données sont déjà en mémoire, pas besoin de lire les fichiers à chaque consultation

### Intégration avec les autres fonctionnalités

La consultation des notes s'intègre naturellement avec :
- **Gestion des étudiants** : Utilise les données des étudiants pour l'affichage
- **Gestion des matières** : Utilise les données des matières pour l'affichage
- **Saisie des notes** : Affiche les notes saisies dans le système
- **Statistiques** : Utilise les calculs statistiques pour les moyennes et rangs
- **Navigation** : Accessible depuis le menu principal pour un accès rapide

## Statistiques et Analyses

### Implémentation

Le module de statistiques est implémenté dans `services/statistics.py` avec la classe `Statistics` qui centralise tous les calculs statistiques. Le système offre quatre niveaux d'analyse :

1. **Statistiques par étudiant** : Moyenne générale et rang dans la classe
2. **Statistiques par classe** : Moyenne générale, meilleur étudiant et classement complet
3. **Statistiques par matière** : Moyenne générale et meilleur étudiant
4. **Statistiques globales** : Moyenne générale de l'établissement et meilleur étudiant

### Fonctionnement technique

#### Architecture du module Statistics

La classe `Statistics` est initialisée avec les trois listes de données :
- `students` : Liste des étudiants
- `subjects` : Liste des matières
- `grades` : Liste des notes

Elle fournit des méthodes pour chaque type de calcul statistique.

#### Calcul de la moyenne pondérée

**Formule utilisée** :
```
Moyenne = Σ(note × coefficient) / Σ(coefficient)
```

**Exemple** :
- Mathématiques : 15/20 (coef 3.0) → 45 points
- Physique : 14/20 (coef 2.5) → 35 points
- Informatique : 16/20 (coef 4.0) → 64 points
- **Total points** : 144
- **Total coefficients** : 9.5
- **Moyenne** : 144 / 9.5 = 15.16/20

### Statistiques par étudiant

#### Moyenne générale (`calculate_student_average()`)

**Fonctionnement** :
- Récupère toutes les notes de l'étudiant
- Pour chaque note, multiplie par le coefficient de la matière
- Somme tous les points pondérés
- Divise par la somme des coefficients
- Retourne la moyenne ou `None` si aucune note

**Cas particuliers** :
- Si l'étudiant n'a aucune note → retourne `None`
- Seules les matières du niveau de l'étudiant sont prises en compte
- Les matières sans note ne sont pas comptabilisées

#### Rang dans la classe (`calculate_student_rank()`)

**Fonctionnement** :
- Récupère tous les étudiants du même niveau
- Calcule la moyenne de chaque étudiant
- Trie les étudiants par moyenne décroissante
- Détermine la position (rang) de l'étudiant dans cette liste triée
- Retourne le rang (1 = premier) ou `None` si non calculable

**Exemple d'affichage** :
- Rang 1 → "1er"
- Rang 2 → "2ème"
- Rang 3 → "3ème"

### Statistiques par classe

#### Moyenne générale de la classe (`calculate_class_average()`)

**Fonctionnement** :
- Récupère tous les étudiants du niveau/classe
- Calcule la moyenne de chaque étudiant
- Fait la moyenne arithmétique de toutes les moyennes individuelles
- Retourne la moyenne de la classe ou `None` si aucune note

**Formule** :
```
Moyenne_classe = Σ(moyenne_étudiant) / nombre_étudiants_avec_notes
```

#### Meilleur étudiant de la classe (`get_best_student_in_class()`)

**Fonctionnement** :
- Récupère tous les étudiants du niveau/classe
- Calcule la moyenne de chaque étudiant
- Trouve l'étudiant avec la moyenne la plus élevée
- Retourne un tuple (étudiant, moyenne) ou `None`

**Cas d'égalité** : Si plusieurs étudiants ont la même meilleure moyenne, le premier trouvé est retourné.

#### Classement complet (`get_class_ranking()`)

**Fonctionnement** :
- Récupère tous les étudiants du niveau/classe
- Calcule la moyenne de chaque étudiant
- Trie par moyenne décroissante
- Assigne un rang à chaque étudiant
- Retourne une liste de tuples (étudiant, moyenne, rang)

**Format de retour** :
```python
[
  (Student(...), 18.5, 1),  # 1er
  (Student(...), 17.2, 2),  # 2ème
  (Student(...), 15.8, 3),  # 3ème
  ...
]
```

### Statistiques par matière

#### Moyenne générale par matière (`calculate_subject_average()`)

**Fonctionnement** :
- Récupère toutes les notes de la matière
- Calcule la moyenne arithmétique simple (sans pondération)
- Retourne la moyenne ou `None` si aucune note

**Formule** :
```
Moyenne_matière = Σ(note) / nombre_notes
```

**Note** : Cette moyenne est simple (non pondérée) car elle compare les notes de tous les étudiants dans la même matière.

#### Meilleur étudiant par matière (`get_best_student_in_subject()`)

**Fonctionnement** :
- Récupère toutes les notes de la matière
- Trouve la note la plus élevée
- Récupère l'étudiant correspondant à cette note
- Retourne un tuple (étudiant, note) ou `None`

**Cas d'égalité** : Si plusieurs étudiants ont la même meilleure note, le premier trouvé est retourné.

### Statistiques globales

#### Moyenne générale de l'établissement (`calculate_global_average()`)

**Fonctionnement** :
- Récupère toutes les notes de tous les étudiants
- Calcule la moyenne arithmétique simple de toutes les notes
- Retourne la moyenne globale ou `None` si aucune note

**Formule** :
```
Moyenne_globale = Σ(toutes_les_notes) / nombre_total_notes
```

**Utilité** : Donne une vue d'ensemble de la performance de l'établissement.

#### Meilleur étudiant de l'établissement (`get_best_student_global()`)

**Fonctionnement** :
- Parcourt tous les étudiants
- Calcule la moyenne de chaque étudiant
- Trouve l'étudiant avec la moyenne la plus élevée
- Retourne un tuple (étudiant, moyenne) ou `None`

**Note** : Compare les moyennes pondérées de tous les étudiants, tous niveaux confondus.

### Fichiers concernés

- **`services/statistics.py`** : Module principal contenant la classe `Statistics` et toutes les méthodes de calcul
- **`services/menu.py`** : Contient les méthodes d'affichage des statistiques :
  - `handle_statistics_menu()` : Menu principal des statistiques
  - `show_student_statistics()` : Statistiques d'un étudiant
  - `show_class_statistics()` : Statistiques d'une classe
  - `show_subject_statistics()` : Statistiques d'une matière
  - `show_global_statistics()` : Statistiques globales
- **`models/`** : Utilise les classes `Student`, `Subject` et `Grade` pour accéder aux données

### Exemple d'utilisation

```
============================================================
    STATISTIQUES ET ANALYSES
============================================================

1. Statistiques par étudiant
2. Statistiques par classe
3. Statistiques par matière
4. Statistiques globales
5. Retour au menu principal

Votre choix: 2

============================================================
    STATISTIQUES PAR CLASSE
============================================================
Niveau/Classe: L1

Classe: L1

Moyenne générale de la classe: 15.33/20

Meilleur étudiant: Marie MARTIN (ETU002)
Moyenne: 18.17/20

Classement complet (4 étudiant(s)):

Rang   Étudiant                                  Moyenne
------------------------------------------------------------
1      Marie MARTIN (ETU002) - L1                18.17
2      Jean DUPONT (ETU001) - L1                 15.33
3      Sophie DUBOIS (ETU004) - L1                15.17
4      Pierre BERNARD (ETU003) - L1              12.17
```

### Méthodes utilitaires internes

La classe `Statistics` utilise des méthodes privées pour faciliter les calculs :

- `_get_student_by_matricule()` : Trouve un étudiant par son matricule
- `_get_subject_by_code()` : Trouve une matière par son code
- `_get_grades_by_matricule()` : Récupère toutes les notes d'un étudiant
- `_get_grades_by_code_matiere()` : Récupère toutes les notes d'une matière
- `_get_grades_by_niveau()` : Récupère toutes les notes d'un niveau

### Gestion des cas particuliers

Le module gère plusieurs cas particuliers :

1. **Étudiant sans note** : Retourne `None` pour la moyenne, pas d'erreur
2. **Matière sans note** : Retourne `None` pour la moyenne de la matière
3. **Classe vide** : Retourne `None` pour la moyenne de la classe
4. **Étudiant inexistant** : Retourne `None` pour toutes les statistiques
5. **Matière inexistante** : Retourne `None` pour les statistiques de la matière
6. **Égalité de moyennes** : Le premier étudiant trouvé est considéré comme meilleur

### Performance et optimisation

- **Calculs en temps réel** : Tous les calculs sont effectués à la demande, garantissant des données toujours à jour
- **Pas de cache** : Les statistiques ne sont pas mises en cache, elles sont recalculées à chaque demande
- **Efficacité** : Les algorithmes sont optimisés pour parcourir les listes de manière efficace
- **Complexité** : La plupart des calculs ont une complexité O(n) où n est le nombre d'étudiants/notes

### Intégration avec les autres modules

Les statistiques s'intègrent avec tous les autres modules :

- **Gestion des étudiants** : Utilise les données des étudiants pour les calculs
- **Gestion des matières** : Utilise les coefficients des matières pour la pondération
- **Saisie des notes** : Les notes saisies sont immédiatement utilisables pour les statistiques
- **Consultation des notes** : Les bulletins utilisent les statistiques pour afficher les moyennes et rangs
- **Menu principal** : Accessible depuis le menu principal pour un accès rapide

### Formules mathématiques utilisées

1. **Moyenne pondérée** : `M = Σ(ni × ci) / Σ(ci)` où ni = note, ci = coefficient
2. **Moyenne simple** : `M = Σ(ni) / n` où n = nombre de notes
3. **Rang** : Position dans une liste triée par ordre décroissant

### Affichage des résultats

Les statistiques sont affichées de manière claire et formatée :

- **Moyennes** : Toujours affichées avec 2 décimales (ex: 15.33/20)
- **Rangs** : Affichés avec le suffixe approprié (1er, 2ème, 3ème, etc.)
- **Tableaux** : Utilisation de tableaux formatés pour les classements
- **Messages** : Messages clairs quand les statistiques ne sont pas calculables

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

