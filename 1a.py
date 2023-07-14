import random

# creating characters
CHARACTERS = ["archer","wizard","knight","werewolf"]
CHAR_ATTR = {
    "archer": [10, 1, 3, 10, ""],   # [ap, dp, sp, critical_chance, image]
    "wizard": [15, 2, 2, 20, ""],
    "knight": [12, 3, 1, 25, ""],
    "werewolf": [13, 2, 2, 30, ""]
}

class Character:
    def __init__(self,jobClass):
        self.hp = 150
        if jobClass in CHAR_ATTR:
            self.ap, self.dp, self.sp, self.crital_chance, self.image = CHAR_ATTR[jobClass]
        self.jobClass = jobClass
        
    def attack(self, target):
        # adding extra damage according to each character's critacal chance
        chance = random.randint(1, 100)
        critical_damage = 0
        if chance <= self.crital_chance:
            critical_damage +=2
        damage = self.ap + critical_damage
        target.receive_damage(damage)

    def receive_damage(self, damage):
        # dp is always lower than than damage in any circumstances
        self.hp -= damage - self.dp

class PlayerCharacter(Character):
    def __init__(self,jobClass):
        super().__init__(jobClass)
        self.hp = 100
        self.mp = 5

    def defend(self):
        self.dp += 8 #this should only last for 1 round

    def useSkill(self,skill,target):
        self.mp -= 1
        damage = skill(target)
        target.receive_damage(damage)

# skills
def pierce_shot(target):
    return 20 + target.dp

# main game flow
print("You can choose two characters to fight from these: archer, wizard, knight and werewolf")
not_finished = True
round = 1

while not_finished:
    # chosing characters
    choice1 = input("Choose your first character to fight: ")
    player1 = PlayerCharacter(choice1)
    choice2 = input("Choose another one: ")
    player2 = PlayerCharacter(choice2)
    player_team = [player1, player2]
    # creating enemy character from remaing options
    remaining_options = list(set(CHARACTERS) - {choice1, choice2})
    enemy1 = Character(remaining_options[0])
    enemy2 = Character(remaining_options[1])
    enemy_team = [enemy1,enemy2]

    print(f"You chose {player1.jobClass} and {player2.jobClass}.\nThe enemy characters are {enemy1.jobClass} and {enemy2.jobClass}.")
    # letting the player choose which fighter to fight first
    first_fighter = input(f"You will fight with the {enemy1.jobClass} first,\nchoose your first character to fight, 1){player1.jobClass} or 2){player2.jobClass} : ")
    print()
    if first_fighter == "2":
        player_team.reverse()

    while True:
        player_fighter = player_team[0]
        enemy_fighter = enemy_team[0]
        print(f"Round: {round}*")
        round += 1
        print()
        # showing stats
        print("       |  Fighter   |   HP   |   MP   |   AP   |   DP   ")
        print("        ------------------------------------------------")
        print(f"Player | {player_fighter.jobClass:<10} | {player_fighter.hp:<6} | {player_fighter.mp:<6} | {player_fighter.ap:<6} | {player_fighter.dp:<6}")
        print(f"Enemy  | {enemy_fighter.jobClass:<10} | {enemy_fighter.hp:<6} | -      | {enemy_fighter.ap:<6} | {enemy_fighter.dp:<6}")
        print()

        print(f"Actions: 1)Attack 2)Defend 3)Use skill 4)Quit/Restart")
        action = input("Action: ")

        if action == "1":
            # speed point will decide who attack first (player attacks first if they have same sp)
            if player_fighter.sp >= enemy_fighter.sp:
                player_fighter.attack(enemy_fighter)
                # Check the opponent is still alive after the attack
                if enemy_fighter.hp > 0:
                    enemy_fighter.attack(player_fighter)
            else:
                enemy_fighter.attack(player_fighter)
                if player_fighter.hp > 0:
                    player_fighter.attack(enemy_fighter)
        elif action == "2":
            player_fighter.defend()
            enemy_fighter.attack(player_fighter)
        # skill action
        elif action == "3":
            if player_fighter.sp >= enemy_fighter.sp:
                player_fighter.useSkill(pierce_shot,enemy_fighter)
                enemy_fighter.attack(player_fighter)
            else:
                enemy_fighter.attack(player_fighter)
                player_fighter.useSkill(pierce_shot,enemy_fighter)
        elif action == "4":
                choice = input("Do you want to quit (q) or restart (r)? ")
                if choice.lower() == "q":
                    not_finished = False
                    break
                elif choice.lower() == "r":
                    print("Restarting...")
                    # resetting the turn number to 1
                    turn = 1
                    break

        # If fighter or enemy fighter's HP drops to 0, remove them from the list
        if player_fighter.hp <= 0:
            player_team.remove(player_fighter)
            if len(player_team) == 1:
                print(f"Your {player_fighter.jobClass} is defeated! \nYour second fighter {player_team[0].jobClass} came in")
        if enemy_fighter.hp <= 0:
            enemy_team.remove(enemy_fighter)
            if len(enemy_team) == 1:
                print(f"Enemy {enemy_fighter.jobClass} is defeated! Second fighter {enemy_team[0].jobClass} came in")

        if len(player_team) == 0:
            print("You lost")
            not_finished = False
            break
        elif len(enemy_team) == 0:
            print("Congratulation, You won!!")
            not_finished = False
            break
        # line after each round
        print("-"*20)