# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.direction= set() #ensemble des directions valides
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        
        # Setup rooms


        grotte = Room("Prehistoire", "  à l'ère préhistorique, tu es dans une grotte, l'air y est humide et froid. Face à toi, l'entrée de la grotte .")
        self.rooms.append(grotte)
        mammouths = Room("Prehistoire", "  face à un combat opposant un mammouths et un Homme préhistorique.")
        self.rooms.append(mammouths)
        abri= Room("Abris", "avec votre nouveau compagnon, il vous amène dans son abri sous roche et vous aide à faire du feu")
        self.rooms.append(abri)
        egypte_antique = Room("Egypte Antique", "dans une pyramide, où la pierre polie reflète faiblement la lumière des torches. L’air est sec et chargé d’une atmosphère mystique, ponctuée par l’écho de tes pas.")
        self.rooms.append(egypte_antique)
        question_chambre_cachée = Room("Egypte Antique", "dans une impasse, face à vous les murs sont couverts de hiéroglyphes, racontant l'histoire des dieux et des rois.")
        self.rooms.append(question_chambre_cachée)
        chambre_cachée = Room("Egypte Antique", " dans une chambre cachée qui s'est debloquée après avoir répondu aux questions d'Imhopen, au sol une clé rouillée que vous ramassez.")
        self.rooms.append(chambre_cachée)
        porte = Room("Egypte Antique", " devant une porte fermée a clé à votre droite se trouve une zone peu éclairée")
        self.rooms.append(porte)
        passage_interdit = Room("Egypte Antique", " faire l'exercice")
        self.rooms.append(passage_interdit)
        sphinxe = Room("Egypte Antique", " devant la créature sphinxe")
        self.rooms.append(sphinxe)

        

        # Create exits for rooms

        grotte.exits = {"N" : mammouths, "E" : None, "S" : None, "O" : None}
        mammouths.exits = {"N" : None, "E" : abri , "S" : grotte, "O" : None}
        abri.exits = {"N" : passage_interdit, "E" : None, "S" : egypte_antique, "O" : None}
        passage_interdit.exits = {"N" : None, "E" : None, "S" : abri, "O" : None}
        egypte_antique.exits = {"D" : porte , "E" : None , "S" : None, "O" : question_chambre_cachée}
        question_chambre_cachée.exits = {"D" : chambre_cachée, "E" : egypte_antique, "S" : None, "O" : None}
        chambre_cachée.exits = {"U" : question_chambre_cachée, "E" : None, "S" : None, "O" : None}
        porte.exits = {"U" : egypte_antique, "E" : None, "S" : None, "O" : None}
        

        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = grotte

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
      
    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
