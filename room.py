# This file contains the Room class.


class Room:
    """
    This class represents a room. A room is composed of a room name, a description and an exit.

    Attributes:
        name (str): The name word.
        description (str): the description string.
        exit (dict): next room
        inventory (dict): the items that the room has.
        characters (dict): the characters that the room has.

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
        self.characters = {}

    
    # Define the get_inventory method.
    def get_inventory(self):
        if not self.inventory and not self.characters:
            return "Rien ni personne à l’horizon."
       
        result = "Vous voyez :\n"
        for item in self.inventory.values():
            result += f"- {item}\n"
        result+="\n"
        for char in self.characters.values():
            result += f"- {char}\n"
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
        return f"Vous êtes {self.description}\n\n{self.get_exit_string()}\n"
    