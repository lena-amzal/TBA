"""
Define the Player class
"""

from quest import QuestManager
from item import Item

class Player:
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

    def __init__(
        self,
        name,
    ):
        """
        Initialize a new player.

        Args:
            name (str): The name of the player.

        Initializes all player attributes including inventory, health, and quest manager.
        """
        self.name = name
        self.current_room = None
        self.inventory = {}
        self.history = []
        self.max_weight = 10
        self.hp = 20000
        self.max_hp = 20000
        self.is_alive = True
        self.quest_manager = QuestManager(self)
        self.last_checkpoint = None
        self.rewards = []  # List to store earned rewards

    def move(self, direction):
        """
        Move the player to the next room in the given direction.

        Args:
            direction (str): The direction to move (N, E, S, O, U, D).

        Returns:
            Room: The destination room or None if move is invalid.
        """
        # Get the next room from the exits dictionary of the current room.
        destination = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if destination is None :
            print("\nAucune porte dans cette direction !\n")
            return False

        # Set the current room to the next room.
        self.history.append(self.current_room)
        self.current_room = destination
        print(self.current_room.get_long_description())
        return True

    # Define the get_history method.
    def get_history(self) :
        """
        Get a description of the player's room history.

        Returns:
            str: A formatted string listing all visited rooms or a message if no rooms visited.
        """
        if not self.history:
            return "Vous êtes à votre point de départ, il n'y a pas d'historique."

        result = "Vous avez visité les pièces suivantes :\n"
        for room in self.history:
            result += f"- {room.name}\n"
        return result

    # Define the get_inventory method.
    def get_inventory(self):
        """
        Get a description of all items in the player's inventory.
        Returns:
            str: A formatted string listing all inventory items or a message if empty.
        """
        if len(self.inventory) == 0:
            return "Votre inventaire est vide.\n"

        result = "Vous disposez des items suivants :\n"
        for items in self.inventory.values():
            item = items[0]
            quantity = len(items)
            result += f"- {item.name}(x{quantity}) : {item.description}\n"
        return result

    def get_inventory_weight(self):
        """
        return the weight of the inventory
        """
        total = 0
        for items in self.inventory.values():
            for item in items:
                total += item.weight
        return total

    def take_damage(self, damage):
        """
        Arg : int
        Returns : str
        """
        self.hp -= damage
        self.hp = max(self.hp,0)
        print(
        f"\nVous avez subi {damage} points de dégâts.\n"
        f"Points de vie restants : {self.hp}/{self.max_hp}\n"
        )
        if self.hp == 0:
            self.is_alive = False

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
        if isinstance(reward, Item):
            if reward.name in self.inventory:
                self.inventory[reward.name].append(reward)
            else:
                self.inventory[reward.name] = [reward]
            print(f"🎁 Vous avez obtenu: {reward.name}\n")

        elif reward not in self.rewards:
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
