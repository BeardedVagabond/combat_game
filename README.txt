# combat_game
A text-based rpg style fighter based largely on DnD5e rules

NOTE: Originally coded in PyCharm using a Conda environment (Python 3.6)
      All combatants are currently instantiated as a level 1 rogue for simplicity (1d8 hit dice) 
      All combatants wear leather armor (AC = 10 + DEX modifier)
      All combatants deal (1d8 + STR modifier) damage on successful hit
      
Possible future improvements: Choice of random stats (current), player involved allocation/rolls, or pre-determined class stats
                              Add choices for player class (barbarian, druid, rogue, etc.)
                              Add enemy combatant classes for more variety
                              Add more combat actions such as spells and two-handed attacks
                              Add special attacks/characteristics for enemy combatants

Game consists of two files: 1. bv_combat_game.py and 2. actors.py
1. bv_combat_game.py contains all functions and UI output required to run the main game loop
2. actors.py is imported as a module to bv_combat_game.py and includes all required classes to instantiate combatants etc.

The game consists of easy to read console output and prompts that guide the user through several phases:

1. Player name input
    - input is verified to be a string before continuing, however, any string input will be accepted
    
2. Combatant Instantiation
    a. This phase is completed "behind the scenes" with no input from the player
    b. First, d6, d8, and d20 Die objects are created
    c. The d6 object is used to determine stat allocation according to computer exectution of dice rolls for each Combatant
        - For each stat (STR, DEX, CON, INT, WIS, CHR), 4d6 are rolled
        - Once rolled, the lowest roll is removed and the remaining are summed
        - This sum then temporarily becomes the corresponding stat (the above performed through a for loop)
        - When all stats have been rolled for, the values are shuffled to introduce a random factor to allocations
    d. Next, the Player object is instantiated using the player's inputed name and stat rolls method from d6
    e. The enemy Combatant objects are then instantiated in a list using names taken from Sword Art Online and stat rolls
    f. Finally, all combatants (player and enemies) are listed in detail before being returned and passed to the main game loop
        - The details include: stats, modifiers, armor class, and current/maximum health points
        
3. Main game loop
    a. Command input
        - Possible commands are: [F]ight, [C]heck Health, [R]est, [L]ook Around, and E[x]it
        - Commands are made thrugh hinted character input
        - Sring input is processed using lower() and strip() methods to simplify selection
        - A blank input yields a no input message before looping
        - Invalid string input tields a message stating the string is not recognized before looping
    b. Combat
        - When this command is selected, the player must first select their target
            - If the target exists, combat will begin between the player and the targeted combatant
            - If the target does not exist (i.e. input number outside of range), the player may fall victim to their mistakes...
            - If the input is not numeric, a warning message is output and a input verification loop continues
        - Once combat has begun, the player has two command options: [A]ttack and [R]un
        - If attack is chosen, the player attacks the target first (no initiative rolls at this time to determine order)
            - After the attack, enemy health is checked
            - If the enemy is still alive, they retaliate and attack the player
            - A similar health check is then performed on the palyer
            - If either health check determines the combatant is defeated, the combat loop ends and the main loop continues
            - To determine if an attack hits, the simple rule that a d20 roll must be greater than the target AC is applied
            - Furthermore, a critial hit is scored if a d20 roll results in a value of 20
                - A critical hit then doubles the amount of damage dice rolled (2d8 in this version)
            - Damage is then calculated by rolling damage dice and adding the attackers STR modifier
            - Once calculated, damage is sustained by the target and health is saturated to 0 if dropped below
            - If an enemy combatant is defeated, they are removed from the enemies list and the main loop continues
            - If the player is defeated, combat ends and the palyer awakens with 1HP restored and the chance to fight again...
        - If run is chosen, a unique method is employed to determine the palyer's sucess
            - 3d20 are rolled, and the highest value is removed
            - If the maximum value of the remaining dice is above (10 + DEX modifier), the attempt succeeds
            - If the attempt fails, the enemy attacks the palyer before the combat loop continues
        - At the end of a combat round (either attack or run), the loop continues and asks for another player command
    c. Check Health
        - This command lists the player's current/maximum health points
        - After lsiting, the main loop continues
    d. Rest
        - The rest command allows for player health to be restored according to the "short rest" rules from DnD5e
        - This involves a hit die roll (1d8) + CON modifier to determine amount of health restored
        - Health points are saturated at maximum HP to eliminate over healing
        - If the player is already at maximum HP when resting, an indicating message will be shown and no HP will be restored
    e. Look Around
        - This command lists detailed information of all remaining combatants in the game
        - The details include: stats, modifiers, armor class, and current/maximum health points
        - After listing the combatants, the main loop continues
    f. Exit
        - This command simply exits the game with a "Thanks for playing" message
    - NOTE: If all enemy combatants are defeated, the main loop will end printing a congratulatory message and exiting the game

