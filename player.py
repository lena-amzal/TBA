# This file contains the Player class.

from quest import QuestManager
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
    def __init__(self, name,):
        self.name = name
        self.current_room = None
        self.inventory = {}
        self.history = []
        self.max_weight=10
        self.hp=100
        self.max_hp=100
        self.alive=True
        self.move_count = 0  # Counter for player movements
        self.quest_manager = QuestManager(self)
        self.rewards = []  # List to store earned rewards
      # Define the move method.

    #Define the get_inventory method.
    def get_inventory(self):
        print(self.inventory)
        if len(self.inventory) == 0:
            return "Votre inventaire est vide."
        
        result= "Vous disposez des items suivants :\n"
        for item in self.inventory.values():
            result += f"- {item}\n"
        return result
    
    # Check room visit objectives
        self.quest_manager.check_room_objectives(self.current_room.name)


        # Increment move counter and check movement objectives
        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)


        return True

    def get_inventory_weight(self):
        total = 0
        for item in self.inventory.values():
            total += item.weight
        return total
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
        print(f"\nVous avez subi {damage} points de dégâts. Points de vie restants : {self.hp}/{self.max_hp}\n")
        if self.hp == 0:
            self.alive = False
            print("\n Vous êtes mort !\n")


    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
       
        Args:
            reward (str): The reward to add.
           
        Examples:
       
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")




    def show_rewards(self):
        """
        Display all rewards earned by the player.
       
        Examples:
       
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        destination = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if destination is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.history.append(self.current_room)
        self.current_room = destination
        print(self.current_room.get_long_description())
        return True


    

    