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
from room import Room
from quest import Quest
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
        if direction is None:
            print(f"Direction '{direction}' non reconnue.")
            print(game.player.current_room.get_long_description())  # Affiche la salle actuelle
            return False

        # Vérifier que la direction est valide dans tout le jeu
        if direction not in game.direction:
            print(f"Direction '{direction}' non reconnue.")
            return False
        old_room = player.current_room

        # Tenter déplacement dans la direction choisie
        result = player.move(direction)
        current_room = player.current_room

        # Move Shana to follow the player
        if current_room is not None and game.Shana is not None:
            del old_room.characters["Shana"]
            current_room.characters["Shana"] = game.Shana
            game.Shana.current_room = current_room

        # Move Varkk if second quest completed
        quest = game.player.quest_manager.get_quest_by_title("Chasseur de Mammouths")
        abri = game.rooms[2]
        if quest and quest.is_completed:
            if "Varkk" in old_room.characters and current_room == abri:
                del old_room.characters["Varkk"]
                abri.characters["Varkk"] = game.Varkk
                game.Varkk.current_room = abri

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
            old_room = game.player.current_room
            game.player.current_room = previous_room
            current_room = game.player.current_room
            print(f"Vous êtes retourné à la pièce : {previous_room.name}")
            print(previous_room.get_long_description())
            if game.Shana is not None:
                del old_room.characters["Shana"]
                current_room.characters["Shana"] = game.Shana
                game.Shana.current_room = current_room
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
            item= game.player.current_room.inventory[item_name]
            if item_name not in game.player.inventory:
                game.player.inventory[item_name]=[item]
            else:
                game.player.inventory[item_name].append(item)
            del game.player.current_room.inventory[item_name]
            print(f"Vous avez pris '{item_name}'.")
        
        # Check quest objectives related to taking items
        for quest in game.player.quest_manager.active_quests:
            for objective in quest.objectives:
                words=objective.split(" ")
                counter_name="".join(words[2:])
                current_count= len(game.player.inventory.get(item_name))
                game.player.quest_manager.check_counter_objectives(counter_name, current_count)

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
            game.player.current_room.inventory[item_name] = item
            print(f"Vous avez déposé '{item_name}'.")

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
        # Use the item if it is in the inventory
        item_name = list_of_words[1]
        if item_name not in game.player.inventory:
            print(f"Vous n'avez pas '{item_name}' dans votre inventaire.")
            return False
        else :
            print(f"Vous utilisez '{item_name}'.")

        # Check quest objectives related to using items
        for quest in game.player.quest_manager.active_quests:
            for objective in quest.objectives:
                words=objective.split(" ")
                action=words[0]
                game.player.quest_manager.check_action_objectives(action, item_name)


        """if item_name == "Lance préhistorique" and game.player.current_room == "Combat avec un mammouth":
            print("🦣 Vous avez vaincu le mammouth avec votre lance préhistorique !")
            quest = next((q for q in game.player.quest_manager.active_quests if q.title == "Chasseur de Mammouths"), None)
            if quest:
                quest.complete_objective("Visiter le terrain de chasse", game.player)
                quest.complete_objective("Répondre à la question du chasseur", game.player)

            return True
        
        #utiliser la branche pour allumer un feu
        if item_name == "branche":
            quest = next((q for q in game.player.quest_manager.active_quests if q.title == "Détenteur de feu"), None)
            if (
            "Récupérer une branche de la grotte" in quest.completed_objectives and
            "Récupérer une branche de l'abri" in quest.completed_objectives
            ):
                print("🔥 Vous utilisez les branches pour allumer un feu.   ")

                quest.complete_objective("Allumer un feu", game.player)

                if quest.reward:
                    game.player.add_reward(quest.reward)
                    game.player.inventory["feu"] = Item("feu", "un feu crépitant", 0)
                    if "branche" in game.player.inventory:
                        del game.player.inventory["branche"]"""
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
        return True
        

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
        quest_title = " ".join(list_of_words[1:])

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

    def answer(game, list_of_words, number_of_parameters):
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        if len(list_of_words) < 2:
            print("❌ Utilisation : answer <ta réponse>")
            return
    
        quest = game.player.quest_manager.get_quest_by_title("Le Mammouth I")
    
        if not quest or not quest.is_active:
            print("❌ Aucune quête active liée à cette question.")
            return
        try:
            user_answer = int(list_of_words[1])
        except ValueError:
            print("❌ Réponse invalide. Donne un nombre.")
            return
        bonne_reponse = 7

        if not hasattr(quest, "errors"):
            quest.errors = 0

        if user_answer == bonne_reponse:
            game.player.quest_manager.check_action_objectives("Répondre à", "Varkk")

        else:
            quest.errors += 1
            remaining = 3 - quest.errors

            if remaining > 0:
                print(f"❌ Mauvaise réponse. Il te reste {remaining} tentative(s).")
                print("💡 Indice : en dessous de 8")
            else:
                print("💀 Tu as échoué trop de fois.")
                game.player.is_alive = False
                print("☠️ Tu es mort.")
        
        """
        quest = game.quest_manager.get_active_quest_by_title("Chasseur de Mammouths")

        if not quest or not quest.is_active:
            print("❌ Aucune quête active liée à cette question.")
            return False
        
        if not hasattr(quest, "errors"):
            quest.errors = 0

        bonne_reponse = 7
        max_errors = 3

        try:
            answer = int(answer)
        except ValueError:
            print("❌ Réponse invalide. Donne un nombre.")
            return False
    
        # ✅ Bonne réponse
        if answer == bonne_reponse:
            print("✅ Bonne réponse !")
            print("🏹 Le chasseur te donne une lance faite de bois et de pierre.")

        game.player.add_reward("Lance préhistorique")
        quest.complete_objective("Répondre à la question du chasseur", game.player)
        return True
    
        # ❌ Mauvaise réponse
        quest.errors += 1
        remaining = max_errors - quest.errors

        if remaining > 0:
            print(f"❌ Mauvaise réponse. Il te reste {remaining} tentative(s).")
        if quest.errors == 1:
            print("💡 Indice : en dessous de 8")
        else:
            print("💀 Tu as échoué trop de fois.")
            print("🦣 Le mammouth te piétine.")
            game.player.is_alive = False
            print("☠️ Tu es mort.")
        return False
        
        print("🧠 Question : Quel est le poids moyen d’un mammouth (en tonnes) ?")
        
        bonne_réponse = "7"
        """
        
        

    

        
    
        
    



    
        


            

        
        