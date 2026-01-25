class Boss:
    def __init__(self, name, description, hp, attack, current_room):
        self.name = name
        self.description = description
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.current_room = current_room
        self.is_alive = True

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def is_defeated(self):
        return self.hp == 0