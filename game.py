# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from item import Item
from quest import Quest


class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.Shana=None
        self.direction= set() #ensemble des directions valides
        self.DEBUG=False



    # Setup the game
    def setup(self):
        # Setup commands
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, D, U)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " : obtenir l'historique",Actions.history, 0)
        self.commands["history"]=history
        back=Command("back"," : revenir à la pièce précédente",Actions.back,0)
        self.commands["back"]=back
        look = Command("look", " : décrire l'environnement actuel et les items", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un item", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : déposer un item", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " <item> : vérifier un item dans l'inventaire", Actions.check, 1)
        self.commands["check"] = check
        talk = Command("talk", " <character> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"]=talk
        use = Command("use", " <item> : utiliser un item de l'inventaire", Actions.use, 1)
        self.commands["use"] = use
        self.commands["quests"] = Command("quests", " : afficher la liste des quêtes", Actions.quests, 0)
        self.commands["quest"] = Command("quest", " <titre> : afficher les détails d'une quête", Actions.quest, 1)
        self.commands["activate"] = Command("activate", " <titre> : activer une quête", Actions.activate, 1)
        self.commands["rewards"] = Command("rewards", " : afficher vos récompenses", Actions.rewards, 0)
        self.commands["answer"] = Command("answer", " <réponse> : répondre à une question posée par un personnage", Actions.answer, 1)
                                           
        # Setup rooms
        grotte = Room("Grotte", "dans une grotte sombre et humide, les murs suintent d'humidité et l'air est frais et chargé de l'odeur de la terre mouillée.")
        self.rooms.append(grotte)
        terrain_de_chasse = Room("terrain de chasse", " dans une vaste plaine recouverte de neige, silencieuse et infinie. ")
        self.rooms.append(terrain_de_chasse)
        abri= Room("Grotte du compagnon", "Vous êtes dans la grotte de Varkk. Sa famille est là, abritée entre les parois de pierre.")
        self.rooms.append(abri)
        egypte_antique = Room("couloir dans la pyramide", "dans une pyramide, où la pierre polie reflète faiblement la lumière des torches. L’air est sec et chargé d’une atmosphère mystique, ponctuée par l’écho de tes pas.")
        self.rooms.append(egypte_antique)
        question_chambre_cachee = Room("Impasse Hiéroglyphes", "dans une impasse, face à vous les murs sont couverts de hiéroglyphes, racontant l'histoire des dieux et des rois.")
        self.rooms.append(question_chambre_cachee)
        chambre_cachee = Room("Chambre cachée", " dans une chambre cachée qui s'est debloquée après avoir répondu aux questions d'Imhopen, au sol une clé rouillée que vous ramassez.")
        self.rooms.append(chambre_cachee)
        porte = Room("Porte verouillée", " devant une porte fermée a clé à votre droite se trouve une zone peu éclairée")
        self.rooms.append(porte)
        sphinx = Room("Sphinx", " devant la créature sphinx")
        self.rooms.append(sphinx)

        # Create messages for npcs
        msg_varkk={terrain_de_chasse : ["Je m'appelle Varkk.","Voulez-vous venir dans ma grotte ?"], 
                   abri : ["Etranger, écoute les paroles de Varkk. Mon peuple parcourt ces terres depuis que les montagnes sont nées. Le froid et les bêtes géantes nous ont tout pris, mais nous avons appris à écouter la terre. Sous la neige, ma grand-mère trouvait des racines de feu et des baies de sang. En les mélangeant dans un crâne de bison, elle créait un liquide capable de refermer les plaies les plus profondes.Tu as prouvé ton courage. Je ne peux pas t'accompagner plus loin, mais je te donne ceci : notre secret. C'est une potion de vie. Bois-la quand ton souffle deviendra court, et la force de la terre reviendra en toi."]}
        msg_shana={grotte: ["Tu te réveilles enfin ! Cela fait un moment que tu es inconscient."],
                   terrain_de_chasse:["Nous devons aider cet homme préhistorique à vaincre le mammouth."]}
        
        # Create npc for rooms
        self.varkk = Character("Varkk", "un homme préhistorique robuste, vêtu de peaux de bêtes, maniant une lance en pierre.", terrain_de_chasse, msg_varkk)      
        terrain_de_chasse.characters["Varkk"] = self.varkk 
        self.shana =Character("Shana", "une personne se retrouvant dans le même monde que vous", grotte, msg_shana)
        grotte.characters["Shana"]=self.shana
        asha=Character("Asha", "femme de Varkk, elle porte des peaux de bêtes et a un regard doux mais déterminé.", abri, ["Bonjour étranger, je suis Asha, la femme de Varkk.", "Merci d'avoir aidé mon mari."])
        abri.characters["Asha"]=asha
        milo=Character("Milo", "un jeune garçon curieux, vêtu de peaux de bêtes, avec des yeux brillants d'innocence.", abri, ["Coucou, moi c'est Milo.", "Merci d'avoir aidé mon papa à chasser le mammouth et ramener à manger."])
        abri.characters["Milo"]=milo

        # Create items for rooms
        lance = Item("lance", "lance, faite de bois et de pierre taillée", 0.25)
        terrain_de_chasse.inventory["lance"] = lance
        branche_01 = Item("branche", "une branche sèche", 0.5)
        grotte.inventory["branche"] = branche_01
        branche_02 = Item("branche", "une branche sèche", 0.5)
        abri.inventory["branche"] = branche_02
        cle = Item("cle", "une clé rouillée", 0.1)
        chambre_cachee.inventory["cle"] = cle
        feu = Item("feu", "un feu crépitant", 0)
        potion = Item("potion", "une potion de vie qui vous permet de vous soigner", 0.5)
        abri.inventory["potion"] = potion
        beamer = Item("beamer", "un beamer futuriste", 1)
        sphinx.inventory["beamer"] = beamer


        # Create exits for rooms
        grotte.exits = {"N" : terrain_de_chasse, "E" : None, "S" : None, "O" : None}
        terrain_de_chasse.exits = {"N" : None, "E" : abri , "S" : grotte, "O" : None}
        abri.exits = {"N" : None, "E" : None, "S" : egypte_antique, "O" : terrain_de_chasse}
        egypte_antique.exits = {"D" : porte , "E" : None , "S" : None, "O" : question_chambre_cachee}
        question_chambre_cachee.exits = {"D" : chambre_cachee, "E" : egypte_antique, "S" : None, "O" : None}
        chambre_cachee.exits = {"U" : question_chambre_cachee, "E" : None, "S" : None, "O" : None}
        porte.exits = {"U" : egypte_antique, "E" : None, "S" : None, "O" : None, "N": sphinx}
        sphinx.exits = {"S" : porte, "E" : None, "O" : None, "N" : None}

        """Initialize the player."""     
        player_name = input("\nEntrez votre nom: ")
        self.player = Player(player_name)
        self.player.current_room = grotte  
 
        # Setup quests
        self._setup_quests()

        
    def _setup_quests(self):
        """Initialize all quests."""
        quest_mammouth_01 = Quest(
            title="Le Mammouth I",
            description="Devant vous se déroule un combat opposant un mammouth et un Homme préhistorique. Répondez à la question suivante : Quel est le poids moyen d'un mammouth adulte ?",
            objectives=["Aller à terrain de chasse", "Répondre à Varkk"],
            reward="lance",
            trigger_room="terrain de chasse"
        )

        quest_mammouth_02 = Quest(
            title="Le Mammouth II",
            description=" Vainquez le mammouth et parle avec l'homme. Peut-être qu'il vous donnera quelque chose d'utile.",
            objectives=["Utiliser lance", "Parler à Varkk"],
            reward="potion de vie",
        )

        create_fire = Quest(
            title="Au Temps Des Premières Flammes",
            description="Ramasser du bois et allume un feu",
            objectives=["Ramasser 2 branches", "Utiliser la branche"],
            reward="feu"
        )



        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(quest_mammouth_01)
        self.player.quest_manager.add_quest(quest_mammouth_02)
        self.player.quest_manager.add_quest(create_fire)
        
    def win(self):
        quest_manager=self.player.quest_manager

        for quest in quest_manager.quests:
            if not quest.is_completed:
                return False
        return True
    
    def loose(self):
        player=self.player
        current_room=player.current_room
        if player.alive==False:
            return True
        
        if current_room == "Combat avec un mammouth":
            if "lance" not in player.inventory:
                return True
        
        if current_room == "Grotte du compagnon":
            if "Savoir-faire du feu" not in player.rewards:
                return True
        
        return False

    def trigger_room(self):
        current_room=self.player.current_room
        self.player.quest_manager.check_room_triggers(current_room.name)

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None



    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # Construire automatiquement l'ensemble des directions valides
        for room in self.rooms:
            self.direction |= {dir for dir, adj in room.exits.items() if adj is not None}
 
        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            if command_word=="":
                print(">")
            else:
                print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")

        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)
            # Vérifier les déclencheurs de quêtes basés sur la pièce actuelle
            self.trigger_room()


    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Vos paupières s'ouvrent sur l'obscurité moite d'une grotte au froid ancestral. " \
        "L'air est lourd, saturé d'humidité. Près de la sortie, la silhouette d'une jeune femme, " \
        "se découpe contre la lumière du jour, scrutant nerveusement l'immensité sauvage au-dehors.")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
