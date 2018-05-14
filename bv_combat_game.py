"""
A text-based combat game based mainly on DnD5e rules.
All characters are created as level 1 rogues for simplicity of hit dice etc.
All characters also wear leather armor (AC = 10 + DEX modifier)
Damage is calculated as 1d8 + STR modifier
Upon being defeated, player is revived outside of combat with 1HP
Game exits on command or when all enemies have been defeated
"""

import random
import time

import actors


def print_header():
    print('=============================================')
    print()
    print("        BeardedVagabond's Combat Game")
    print()
    print('=============================================')
    print()


def initialize():
    """
    Instantiates objects from actors class, receives verified player name input, and lists enemies in the field
    :return: Objects required for main game loop (d6 only used for stats allocation in this version)
    """
    # initialize_combatants
    d6 = actors.Die(6)
    d8 = actors.Die(8)
    d20 = actors.Die(20)

    # verify player name input
    player_name = ''
    while not player_name:

        player_name = input('What is your name? ')  # input "Kirito" for thematic continuity

        if not player_name:
            print('Input not recognized. Please re-enter a name.\n')

    player = actors.Player(player_name, d6.stats_rolls())
    enemies = [
        actors.Combatant('Heathcliffe', d6.stats_rolls()),
        actors.Combatant('Oberon', d6.stats_rolls()),
        actors.Combatant('Death Gun', d6.stats_rolls()),
    ]

    # display combatants
    print("This round's combatants are... \n")
    time.sleep(1)
    print(player)
    player.look(enemies)
    return d20, d8, enemies, player


def game_loop(d20, d8, enemies, player):
    """
    Performs main game loop functions such as command input verifications, combat loops, and other player actions
    :param d20: A 20 sided Die object
    :param d8: An 8 sided Die object
    :param enemies: A list of enemies in the field
    :param player: A Player object with name from user input
    :return: N/A
    """
    while True:

        cmd = input('Do you wish to [F]ight, [C]heck Health, [R]est, [L]ook around, or E[x]it? ')
        if not cmd:
            print("No input detected, please re-enter a command\n")
            continue
        cmd = cmd.lower().strip()

        if cmd == 'f':
            fight_loop(d20, d8, enemies, player)

        elif cmd == 'c':
            print(f'{player.name} currently has {player.HP}/{player.MaxHP}HP.\n')

        elif cmd == 'r':
            rest(d8, player, enemies)

        elif cmd == 'l':
            player.look(enemies)

        elif cmd == 'x':
            print("Thank's for playing!")
            break

        else:
            print(f"Sorry, the command '{cmd}' wasn't recognized. Please re-enter a command")

        if not enemies:
            print(f'Congratulations! {player.name} has defeated all of their enemies!!')
            print("Thank's for playing!")
            break


def rest(d8, player, enemies):
    # Player rest
    print(f'{player.name} takes a short rest at a fire...')
    rest_roll = sum(d8.roll(1))
    rest_heal = player.heal(rest_roll)
    print(f'{player.name} regains {rest_heal}HP.') if rest_heal > 0 \
        else print(f'{player.name} is already at full HP!')
    # Enemy rest loop
    for enemy in enemies:
        rest_roll = sum(d8.roll(1))
        rest_heal = enemy.heal(rest_roll // 2)
        if rest_heal > 0:
            print(f'{enemy.name} took a short rest as well...')
    print()


def fight_loop(d20, d8, enemies, player):
    print('Which combatant do you wish to fight?\n')
    for idx, entry in enumerate(enemies):
        print(f'[{idx + 1}] {entry.name}')
    selected = 0
    while not selected:
        enemy = input('==> ')
        if not enemy:
            print('No enemy selected. Please re-enter your target.\n')
            continue
        try:
            enemy = int(enemy)
            selected = 1

        except ValueError:
            print('Invalid target selection. Please re-enter your target.\n')
    combat = player.fight(enemy, enemies)
    if combat:
        fighter = enemies[enemy - 1]
        print(f'{player.name} charges at {enemies[enemy - 1].name}!!\n')

        while combat:

            combat_cmd = input('What would you like to do? [A]ttack, [R]un away: ')
            if not combat_cmd:
                print("No input detected, please re-enter a command.\n")
                continue
            combat_cmd = combat_cmd.lower().strip()

            if combat_cmd == 'a':
                print('Rolling some dice...\n')
                # no initiative rolls for now, player always goes first...
                # Kirito has the fastest reaction times after all :)

                # player attacks target
                attack_target(d20, d8, fighter, player)  # d20, d8, target, attacker
                enemy_defeated = health_status(player, fighter, enemies, 'enemy')
                if enemy_defeated:
                    combat = 0

                else:
                    # target attacks player
                    attack_target(d20, d8, player, fighter)
                    player_defeated = health_status(player, fighter, enemies, 'player')
                    if player_defeated:
                        combat = 0

                    else:
                        print(f'{player.name} now has {player.HP}HP')
                        print(f'{fighter.name} now has {fighter.HP}HP\n')
                    # time.sleep(1)

            elif combat_cmd == 'r':  # this isn't from DnD reference materials... just needed something
                run_roll = d20.roll(3)
                run_roll.sort()
                run_roll = run_roll[0:2]

                if max(run_roll) >= 10 - player.modifiers[1]:  # DEX modifiers adds to escape chance
                    print(f'{player.name} makes a narrow escape!\n')
                    combat = 0

                else:
                    print(f"{player.name} stumbles and can't get away!\n")
                    # target attacks player
                    attack_target(d20, d8, player, fighter)
                    player_defeated = health_status(player, fighter, enemies, 'player')
                    if player_defeated:
                        combat = 0

            else:
                print(f"Sorry, the command '{combat_cmd}' wasn't recognized. Please re-enter a command\n")

    else:
        print(f'{player.name} charges at... thin air!?')
        reaction_enemy = random.choice(enemies)
        print(f'{reaction_enemy.name} reacts to the opening and attacks {player.name}!!...\n')
        attack_target(d20, d8, player, reaction_enemy)
        health_status(player, reaction_enemy, enemies, 'player')


def attack_target(d20, d8, target, attacker):
    """
    Performs UI output and calls required Combatant methods
    :param d20: A 20 sided Die object
    :param d8: An 8 sided Die object
    :param target: The targeted Combatant object (can be player or fighter)
    :param attacker: The attacker Combatant object (can be player or fighter)
    :return: UI output for combat summary
    """
    roll = sum(d20.roll(1))
    print(f'{attacker.name} rolled a {roll}!')
    hit = attacker.attack(roll, target)
    print(f"{target.name}'s AC is {target.AC}...")

    if hit == 2:
        print(f'{attacker.name} scored a critical hit!!')
        damage_dice = sum(d8.roll(2))  # double rolls for critical
        damage = target.sustain_damage(damage_dice, attacker)
        print(f'{attacker.name} dealt {damage} damage to {target.name}!\n')

    elif hit == 1:
        print(f'{attacker.name} scored a hit!')
        damage_dice = sum(d8.roll(1))
        damage = target.sustain_damage(damage_dice, attacker)
        print(f'{attacker.name} dealt {damage} damage to {target.name}!\n')

    else:
        print(f"{attacker.name}'s attack missed...\n")


def health_status(player, enemy, enemies, target):
    """
    Checks the health status of the target
    :param player: The Player object
    :param enemy: The current/attacking enemy Combatant object
    :param enemies: A list of enemies in the field
    :param target: A string for 'player' or 'enemy' to indicate which health to check
    :return: 0 if target is alive, 1 if target is defeated (related to action required or not)
    """
    if target == 'player':

        if player.HP == 0:
            print(f'{enemy.name} has defeated {player.name}!...')
            print(f'{player.name} awakens, bruised, embarrassed, and barely alive to fight another day...')
            print('* Your health points have been restored to 1 *\n')
            player.HP = 1
            return 1

        else:
            return 0

    elif target == 'enemy':

        if enemy.HP == 0:
            print(f'{player.name} defeated {enemy.name}!\n')
            enemies.remove(enemy)
            return 1

        else:
            return 0


def main():
    """
    Contains function calls in order required to execute the game
    :return: Standard 0 for completion and 1 for error
    """
    print_header()
    d20, d8, enemies, player = initialize()
    game_loop(d20, d8, enemies, player)


if __name__ == '__main__':
    main()
