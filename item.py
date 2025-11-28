#This file contains the Item class.

class Item:
    """
    This class represents an item. An item is composed of a name, a description and a weight.

    Attributes:
        name (str): The name word.
        description (str): the description string.
        weight (int): the weight of the item.

    Methods:
        __init__(self, name, description) : The constructor.
        __str__(self) : return string representation of the item.
    
    Examples:
    >>> item = Item("nom de l'objet","description de l'objet")
    >>> item.name
    "nom de l'objet"
    >>> item.description
    "description de l'objet"

    """
    # Define the constructor. 
    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight 

    # Define the string representation method.
    def __str__(self):
        return f"{self.name} : {self.description} ( {self.weight} kg)"
    
  

