"""Define the Room class"""


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
    def __init__(self, name, description, world=None, checkpoint=False, locked_by_quest=None):
        """
        Initialize a new room.

        Args:
            name (str): The name of the room.
            description (str): The description of the room.
            world (str): The world this room belongs to (optional).
            checkpoint (bool): Whether this room is a checkpoint (default: False).
            locked_by_quest (str): Quest title that locks this room (optional).
        """
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}
        self.boss = None
        self.world = world
        self.checkpoint = checkpoint
        self.locked_by_quest = locked_by_quest


    def get_inventory(self):
        """
        Get a description of all items and characters in the room.

        Returns:
            str: A formatted string describing items and characters present.
        """
        if not self.inventory and not self.characters:
            return "Rien ni personne à l’horizon."

        result = "Vous voyez :\n"
        for items in self.inventory.values():
            item=items[0]
            quantity=len(items)
            result += f"- {item.name}(x{quantity}) : {item.description}\n"
        result+="\n"
        for char in self.characters.values():
            result += f"- {char}\n"
        if self.boss is not None :
            result+=f"-{self.boss}\n"
        return result

    def get_exit(self, direction):
        """
        Get the room in the given direction.

        Args:
            direction (str): The direction to check (N, E, S, O, U, D).

        Returns:
            Room: The room in that direction or None if no exit exists.
        """

    # Return a string describing the room's exits.
    def get_exit_string(self):
        """
        Returns:
            exit_string (str) : Sorties : (N, E, S, O, U, D)
        """
        exit_string = "Sorties: "
        for exit in self.exits:
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string


    # Return a long description of this room including exits.
    def get_long_description(self):
        """
        Get a long description of the room including its description and available exits.

        Returns:
            str: A formatted string with the room description and exits.
        """
        return f"Vous êtes {self.description}\n\n{self.get_exit_string()}\n"
