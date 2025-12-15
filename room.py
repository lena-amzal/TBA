# This file contains the Room class.


class Room:
    """
    This class represents a room. A room is composed of a room name, a description and an exit.

    Attributes:
        name (str): The name word.
        description (str): the description string.
        exit (dict): next room
        inventory (dict): the items that the room has.

    Methods:
        __init__(self, name, description) : The constructor.
        get_exit(self, direction) : Return Room.
        get_exit_string(self) : Return string according to the room.
        get_long_description(self) : return long description of the room.
        get_inventory(self) : return the inventory of the room.

    Examples:
    >>> room = room("nom de la pièce","description de la pièce")
    >>> room.name
    "nom de la pièce"
    >>> room.description
    "description de la pièce"
    >>> type(room.exits)
    <class 'dict'>

    """
    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}

    
     # Define the get_inventory method.
    def get_inventory(self):
        print(self.inventory)
        if len(self.inventory) == 0:
            return "Il n'y a rien ici."
       
               
        result= "La pièce contient:\n"
        for item in self.inventory.items():
            result += f"- {item}\n"
        return result

    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
        

    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
    
 #create locked door
class Door:
    def __init__(self, name, destination, locked=True, key_name=None):
        self.name = name
        self.destination = destination
        self.locked = locked
        self.key_name = key_name  # nom de la clé nécessaire

    def unlock(self, player):
        if self.key_name in player.inventory:
            self.locked = False
            print(" La porte se déverrouille.")
            return True
        else:
            print(" La porte est verrouillée. Il te faut une clé.")
            return False