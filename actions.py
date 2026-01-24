# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

from quest import Quest
from room import Room
from item import Item
class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False


        """

        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        direction = list_of_words[1][0].upper()
        if direction not in game.direction:
            print(f"Direction '{direction}' non reconnue.")
            print(player.current_room.get_long_description())  # Affiche la salle actuelle
            return False


        # Check if the player can leave the current era
        next_room = player.current_room.exits.get(direction)
        try:
            if next_room.era != game.current_era :
                if not game.can_leave_current_era():
                    print("\n⛔ Vous devez terminer toutes les quêtes de ce monde avant de le quitter.\n")
                    return False
                # If the player is entering a new era, update the current_era
                game.current_era = next_room.era
                print(f"\nBienvenue dans le monde : {game.current_era}\n")

        except AttributeError:
            print("Direction invalide.")
            return False


        # Tenter déplacement dans la direction choisie
        old_room = player.current_room
        result = player.move(direction)
        current_room = player.current_room

        # Check for questions in active quests
        for quest in player.quest_manager.active_quests:
            if quest.trigger_room:
                    if current_room.name == quest.trigger_room:
                        quest.show_question()

        # Move Shana to follow the player
        game.move_shana()

        # Move some characters randomly
        character = list(current_room.characters.keys())
        for char_name in character:
            if char_name not in ["Varkk", "Shana"]:
                char = current_room.characters[char_name]
                char.move()
        player.get_history()

        # Trigger room-based quests
        game.trigger_room()

        # Check room visit objectives
        game.player.quest_manager.check_room_objectives(current_room.name)
        return result


    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False
        """
        l=len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))

        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    def history(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Display the player's room visit history
        print(game.player.get_history())
        return True

    def inventory(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Display the player's inventory
        print(game.player.get_inventory())
        return True

    def back (game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Go back to the previous room in history
        if not game.player.history:
            print("Vous êtes de retour à votre point de départ")
            return False
        else:

            previous_room = game.player.history.pop()
            game.player.current_room = previous_room
            print(f"Vous êtes retourné à la pièce : {previous_room.name}")
            print(previous_room.get_long_description())
            game.move_shana()
            return True

    def look(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Display the current room's long description and inventory
        print(game.player.current_room.get_long_description())
        print(game.player.current_room.get_inventory())
        return True

    def take(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Take the item if it is in the room
        item_name = list_of_words[1]
        if item_name not in game.player.current_room.inventory.keys():
            print(f"L'objet '{item_name}' n'est pas dans la pièce.")
            return False
        else :
            item= game.player.current_room.inventory[item_name].pop(0)
            if item_name not in game.player.inventory:
                game.player.inventory[item_name]=[item]
            else:
                game.player.inventory[item_name].append(item)
            if len( game.player.current_room.inventory[item_name]) == 0:
                del game.player.current_room.inventory[item_name]
            print(f"Vous avez pris '{item_name}'.")

        # Check quest objectives related to taking items
        for quest in game.player.quest_manager.active_quests:
            for objective in quest.objectives:
                words=objective.split(" ")
                counter_name="".join(words[2:])
                current_count= len(game.player.inventory.get(item_name, []))
                for action in ["Ramasser", "Prendre"]:
                    quest.check_counter_objective(action, counter_name, current_count)
                    quest.check_action_objective(action, item_name)

    def drop(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Drop the item if it is in the inventory
        item_name = list_of_words[1]
        if item_name not in game.player.inventory:
            print(f"Vous n'avez pas '{item_name}' dans votre inventaire.")
            return False
        else :
            item = game.player.inventory[item_name].pop()
            if len( game.player.inventory[item_name]) == 0:
                del game.player.inventory[item_name]
            if item_name not in game.player.current_room.inventory:
                game.player.current_room.inventory[item_name]=[item]
            else:
                game.player.current_room.inventory[item_name].append(item)
            print(f"Vous avez déposé '{item_name}'.")

        # Check quest objectives related to using items
        for quest in game.player.quest_manager.active_quests:
            for objective in quest.objectives:
                words=objective.split(" ")
                counter_name="".join(words[2:])
                current_count= len(game.player.current_room.inventory.get(item_name, []))
                quest.check_counter_objective("Déposer", counter_name, current_count)
                quest.check_action_objective("Déposer", item_name)



    def check(game, list_of_words, number_of_parameters):
        l=len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Display the player's inventory
        print(game.player.get_inventory())
        return True

    def use(game, list_of_words, number_of_parameters):
        l=len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        item_name = list_of_words[1]

        if item_name not in game.player.inventory:
            print(f"Vous n'avez pas '{item_name}' dans votre inventaire.")
            return False
        print(f"Vous utilisez '{item_name}'.")

        # Check quest objectives related to using items
        game.player.quest_manager.check_action_objectives("Utiliser", item_name)
        return True

    def talk(game, list_of_words, number_of_parameters):
        l=len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Check if the NPC is in the current room
        npc_name = list_of_words[1].capitalize()
        if npc_name not in game.player.current_room.characters:
            print(f"Il n'y a personne nommé '{npc_name}' ici.")
            return False

        # Display the message from the NPC
        npc = game.player.current_room.characters[npc_name]
        npc.get_msg()

        # Check quest objectives related to talking to NPCs
        game.player.quest_manager.check_action_objectives("Parler à", npc_name)



    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:]).lower().strip()

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True

    @staticmethod
    def answer(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the response from the command
        response = " ".join(list_of_words[1:])
        quest = game.player.quest_manager.get_active_question_quest()
        if not quest.question:
            print("Aucune question n'est posée.")
            return False

        status = quest.check_answer(response, game.player)
        if status is False:
            quest.question.reset()
            game.teleport_to_era_checkpoint()
            return False

        return True