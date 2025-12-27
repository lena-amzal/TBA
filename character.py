# Define the Character class.
import random

class Character():
    """
    This class represents a character. A character is composed of a character name, a description, a room and a message.

    Attributes:
        name (str): The name word.
        description (str): the description string.
        current_room (str): the room where the character is.
        msgs (list): the messages of the character.

    Methods:
        __init__(self, name, description, current_room,msgs) : The constructor.
        __str__(self) : The string representation of the character.
        move(self) : move the character to the next room.
        get_msg(self) : print the messages of the character.
        

    Examples:
    >>> character = Character("nom du personnage","description du personnage","la pièce où le personnage se trouve",["msg1","msg2"])
    >>> character.name
    "nom du personnage"
    >>> character.description
    "description du personnage"
    >>> type(character.current_room)
    <class 'str'>
    >>> type(character.msgs)
    <class 'list'>

    """
    # Define the constructor.
    def __init__(self, name, description, current_room,msgs): 
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs=msgs

    def __str__(self):
        return f"{self.name}:{self.description}\n"
    
    def move(self):
        L=["se déplace","reste"]
        move_choice=random.choice(L)
        if move_choice=="se déplace":
            if self.current_room.exits:
                room_choice=[room for room in self.current_room.exits.values() if room is not None]
                # Retirer de l'ancienne pièce
                del self.current_room.characters[self.name]
                # Changer de pièce
                self.current_room = random.choice(room_choice)
                # Ajouter à la nouvelle pièce
                self.current_room.characters[self.name] = self
            return True
        else:
            return False        
    
    def get_msg(self):
        msg_supp=self.msgs.pop(0)
        print(msg_supp)
        self.msgs.append(msg_supp)
    

