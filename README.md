#Voyage à travers le temps -Projet TBA


## Guide utilisateur

### Installation 
    1. Installez une version égale ou supérieure à Python 3.9
    2. Forkez ou téléchargez le projet
    3. Lancez le jeu avec la commande: python game.py

### Contexte général

Le joueur explore différents mondes (ères), interagit avec des personnages, combat des boss et accomplit des quêtes pour progresser.

L’histoire débute dans une grotte préhistorique et vous mènera jusqu’à une mystérieuse pyramide égyptienne. Vos choix, vos objets et votre progression dans les quêtes détermineront votre victoire… ou votre défaite.

### Univers du jeu

Le jeu est divisé en ères temporelles :

Aethern (Préhistoire), elle est composée de **4 lieux**:
    
    **Grotte** (checkpoint) : point de départ du joueur, lieu du réveil et premières interactions avec Shana.

    **Terrain de chasse** : vaste plaine enneigée où se déroule le combat contre le Mammouth.

    **Grotte du compagnon** : abri de Varkk et de sa famille, lieu de repos et d’interactions sociales.

    **Coin feu** : zone dédiée à la création du feu, liée à une quête essentielle.

Iskhet (Égypte antique), elle est composée de **7lieux**:
    
    -**Couloir** du 1er étage (checkpoint) : entrée principale de la pyramide.

    -**Impasse** : mur d’hiéroglyphes déclenchant une énigme.

    -**Pièce secrète** : salle cachée accessible après résolution des hiéroglyphes.

    -**Escalier sombre** : escalier reliant les différents niveaux de la pyramide.

    -**Couloir du 2ᵉ étage** : couloir menant à des objets et à la sortie.

    -**Sortie** : zone précédant l’affrontement final.

    -**Osireon** : salle du boss final, le sphinx Osirakh.

### Conditions de victoire et de défaite

    Victoire: Le joueur gagne lorsque toutes les quêtes sont complétées, toutes époques confondues.

        Message final :

        « Toutes les quêtes ont été validées. Vous avez triomphé à travers les âges ! »

    Défaite: Le joueur perd si:
                        -ses points de vie tombent à zéro
                        -il échoue à des étapes clés (ex : combattre sans l’objet requis)
                        -il ne remplit pas certaines conditions vitales (ex : créer du feu dans l’abri)

### Les commandes

- `help` → liste des commandes
- `quit` → quitter
- `go <direction>` → se déplacer (N/S/E/O/U/D)
- `back` → revenir à la pièce précédente
- `history` → afficher l'historique des déplacements
- `inventory` → afficher l'inventaire du joueur
- `look` → description + objets
- `take <objet>` → ramasser un objet
- `drop <objet>` → déposer un objet
- `check <objet>` → examiner un objet de l'inventaire
- `use <objet>` → utiliser un objet
- `talk <personnage>` → parler à un personnage
- `answer` → répondre à une question posée par un personnage
- `fight` → combattre le boss présent dans la pièce
- `quests` → afficher la liste des quêtes
- `quest <titre>` → afficher les détails d’une quête
- `activate <titre>` → activer une quête

### Les quêtes et les solutions

Le jeu possède actuellement **6 quêtes**:

    -**Le Mammouth I** : Un combat oppose un mammouth à un homme préhistorique. Une question vous est posée.

        Déclenchement : entrée dans la pièce Terrain de chasse

        Objectifs : Aller au terrain de chasse. Répondre correctement à la question :« Quel est le poids moyen d’un mammouth adulte ? »

            **Solution** : `answer 7`

        Spécificité : question à choix avec nombre de tentatives limité

        Récompense : lance

    
    -**Le Mammouth II**: Vaincre le mammouth et parler à Varkk.

        Déclenchement : après la quête Le Mammouth I

        Objectifs : Vaincre le Mammouth avec la lance obtenue à la quête précédente. Parler à Varkk

                **Solution**: utiliser les commandes `fight` et `talk Varkk`

        Récompense : potion

    -**Au Temps des Premières Flammes**: Apprendre à maîtriser le feu.

        Déclenchement : quête disponible dès l’ère préhistorique

        Objectifs : Ramasser 3 branches. Aller au coin feu. Déposer 3 branches. Utiliser le silex
            **Solution**: utiliser les commandes `take branche` `drop branche` et `use silex`

        Spécificité : débloque une compétence

        Récompense : fire skill


    -**Les Hiéroglyphes de la Pyramide**: Une énigme apparaît sous forme de question.

    Déclenchement : entrée dans la pièce Impasse

    Objectifs :Aller à l’Impasse. Répondre correctement à la question « Qui est le dieu égyptien de la sagesse et de l’écriture ? »
        **Solution**: `answer B`

    Spécificité : question à choix multiples

    Récompense : accès à la Pièce secrète

    -**Les Mystères d’Iskhet**: Trouver la sortie de la pyramide.

    Déclenchement : entrée dans le Couloir du 1er étage

    Objectifs : Aller à Osireon. Utiliser la clé
        **Solution**: `take cle` et 'use cle'

    Récompense : progression vers la fin de l’ère

    -**Le Gardien d’Osireon**: Vaincre le sphinx gardien de la pyramide.

    Déclenchement : entrée dans la salle Osireon

    Objectifs : Aller à Osireon. Vaincre Osirakh

    Récompense : beamer






## Guide développeur: Structuration


- `game.py` / `Game` : description de l'environnement, interface avec le joueur ;
- `room.py` / `Room` : propriétés génériques d'un lieu  ;
- `player.py` / `Player` : le joueur ;
- `command.py` / `Command` : les consignes données par le joueur ;
- `actions.py` / `Action` : les interactions entre le joueur et l'état du jeu ;
- `character.py` / `Character` : : personnages non-joueurs, dialogues et position dans les pièces ;
- `boss.py` / `Boss` : gestion des ennemis puissants, points de vie et attaques ;
-`quest.py` / `Quest` `QuestManager` : gestion des quêtes, objectifs, déclencheurs et récompenses ;
- `item.py` / `Item` : définition des objets récupérables, poids, effets ;

### Diagramme des classes

classDiagram
    %% Classes principales
    class Game {
        - finished: bool
        - rooms: list
        - commands: dict
        - player: Player
        - shana: Player
        - direction: set
        - debug: bool
        - current_era: str
        - era_checkpoints: dict
        + setup()
        + play()
        + can_leave_current_era()
        + move_shana()
        + trigger_room()
        + teleport_to_era_checkpoint()
    }

    class Player {
        - name: str
        - current_room: Room
        - inventory: dict
        - max_weight: int
        - history: list
        - hp: int
        - quest_manager: QuestManager
        + move(direction)
        + get_inventory()
        + get_history()
        + take_damage(dmg)
    }

    class QuestManager {
        - quests: list
        - active_quests: list
        - player: Player
        + get_quest_by_title(title)
        + activate_quest(title)
        + show_quests()
        + show_quest_details(title, current_counts)
        + check_action_objectives(action, target)
        + check_room_objectives(room_name)
        + get_active_question_quest()
    }

    class Quest {
        - title: str
        - description: str
        - objectives: list
        - is_completed: bool
        - is_active: bool
        - reward: str
        - trigger_room: str
        - era: str
        - question: Question
        + check_answer(response, player)
        + check_action_objective(action, target)
        + check_counter_objective(action, counter_name, value)
    }

    class Question {
        - question_text: str
        - correct_answer: str
        - max_attempts: int
        - attempts_left: int
        - failed: bool
        + answer(player_answer)
    }

    class Room {
        - name: str
        - description: str
        - exits: dict
        - inventory: dict
        - characters: dict
        - boss: Boss
        - era: str
        - checkpoint: bool
        - locked_by_quest: str
        + get_exit(direction)
        + get_exit_string()
        + get_long_description()
        + get_inventory()
    }

    class Item {
        - name: str
        - description: str
        - weight: int
        + __str__()
    }

    class Character {
        - name: str
        - description: str
        - current_room: Room
        - msgs: list
        + move()
        + get_msg()
    }

    class Boss {
        - name: str
        - description: str
        - hp: int
        - max_hp: int
        - attack: int
        - current_room: Room
        - is_alive: bool
        + take_damage(dmg)
    }

    class Command {
        - command_word: str
        - help_string: str
        - action: function
        - number_of_parameters: int
        + __str__()
    }

    class Actions {
        <<static>>
        + go(game, list_of_words, number_of_parameters)
        + quit(game, list_of_words, number_of_parameters)
        + help(game, list_of_words, number_of_parameters)
        + history(game, list_of_words, number_of_parameters)
        + inventory(game, list_of_words, number_of_parameters)
        + back(game, list_of_words, number_of_parameters)
        + look(game, list_of_words, number_of_parameters)
        + take(game, list_of_words, number_of_parameters)
        + drop(game, list_of_words, number_of_parameters)
        + check(game, list_of_words, number_of_parameters)
        + use(game, list_of_words, number_of_parameters)
        + talk(game, list_of_words, number_of_parameters)
        + answer(game, list_of_words, number_of_parameters)
        + fight(game, list_of_words, number_of_parameters)
        + quests(game, list_of_words, number_of_parameters)
        + quest(game, list_of_words, number_of_parameters)
        + activate(game, list_of_words, number_of_parameters)
        + rewards(game, list_of_words, number_of_parameters)
    }

    %% Relations
    Game "1" --> "1" Player
    Player "1" --> "1" QuestManager
    QuestManager "1" --> "*" Quest
    Quest "0..1" --> "1" Question
    Player "*" --> "*" Item : inventory
    Room "*" --> "*" Item : inventory
    Room "*" --> "*" Character : characters
    Room "0..1" --> "0..1" Boss
    Player "1" --> "1" Room : current_room
    Character "1" --> "1" Room : current_room
    Boss "1" --> "1" Room : current_room
    Game "1" --> "*" Command


