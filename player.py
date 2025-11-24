# This file contains the Player class.

class Player():
    """
    This class represents a player. A player is composed of a player name and a player self.

    Attributes:
        name (str): The name word.
        current_room (str): the room where the player is.

    Methods:
        __init__(self, name) : The constructor.
        move(self,direction) : move the player to the next room according to the direction
    
    Examples:
    >>> player = Player("nom du joueur", "la pièce où le joueur se trouve")
    >>> player.name
    "nom du joueur"
    >>> player.current_room
    "la pièce où le joueur se trouve"

    """
    # Define the constructor.
    def __init__(self, name, history):
        self.name = name
        self.current_room = None
        self.history=history
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        self.history.append(self.current_room)
        print(self.current_room.get_long_description())
        return True
    

    