"""Define the Boss class"""


class Boss:
    """
    This class represents a boss enemy in the game.

    Attributes:
        name (str): The name of the boss.
        description (str): The description of the boss.
        hp (int): The current health points of the boss.
        max_hp (int): The maximum health points of the boss.
        attack (int): The attack damage of the boss.
        current_room (Room): The room where the boss is located.
        is_alive (bool): Whether the boss is still alive.

    Methods:
        __init__(self, name, description, hp, attack, current_room): The constructor.
        take_damage(self, dmg): Apply damage to the boss.
    """

    def __init__(self, name, description, hp, attack, current_room):
        """
        Initialize a new boss.

        Args:
            name (str): The name of the boss.
            description (str): The description of the boss.
            hp (int): The health points of the boss.
            attack (int): The attack damage of the boss.
            current_room (Room): The room where the boss is located.
        """
        self.name = name
        self.description = description
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.current_room = current_room
        self.is_alive = True

    def take_damage(self, dmg):
        """
        Apply damage to the boss.

        Args:
            dmg (int): The amount of damage to inflict.

        Returns:
            str: A message describing the damage dealt and the boss's remaining health.
        """
        self.hp -= dmg
        self.hp=max(self.hp, 0)
        if self.hp > 0:
            return f"Vous infligez {dmg} points de dégâts. PV du boss: {self.hp}/{self.max_hp}"
        self.is_alive = False
        return f"🏆 Félicitations ! Vous avez vaincu {self.name} !"

    def __str__(self):
        return f"{self.name} : {self.description}"
