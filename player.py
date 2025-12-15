# This file contains the Player class.
from room import Door

class Player():
    """
    This class represents a player. A player is composed of a player name and a player self.

    Attributes:
        name (str): The name word.
        current_room (str): the room where the player is.
        inventory (dict): the items that the player has .
        max_weight  (int): the maximum weight that the player can carry.

    Methods:
        __init__(self, name) : The constructor.
        move(self,direction) : move the player to the next room according to the direction
        get_inventory(str) : return the inventory of the player.
    
    Examples:
    >>> player = Player("nom du joueur", "la pièce où le joueur se trouve")
    >>> player.name
    "nom du joueur"
    >>> player.current_room
    "la pièce où le joueur se trouve"

    """
    from item import Item

    # Define the constructor.
    def __init__(self, name, history):
        self.name = name
        self.current_room = None
        self.inventory = {}
        self.history=history
        self.max_weight=10

    
    #Define the get_inventory method.
    def get_inventory(self):
        print(self.inventory)
        if len(self.inventory) == 0:
            return "Votre inventaire est vide."
        
        result= "Vous disposez des items suivants :\n"
        for item in self.inventory.values():
            result += f"- {item}\n"
        return result
    
            

        

    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        destination = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if destination is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # cas endroit verrouillé
        if isinstance(destination, Door) and destination.locked:
            if not destination.unlock(self):
                return False
            destination = destination.destination  # accéder à la pièce de destination après le déverrouillage
        else:  
        # Set the current room to the next room.
            self.history.append(self.current_room)
            self.current_room = destination
            print(self.current_room.get_long_description())
            return True
    

    