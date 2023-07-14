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
        chance = random.randint(1, 100)
        critical_damage = 0
        if chance <= self.crital_chance:
            critical_damage +=2
        damage = self.ap + critical_damage
        target.receive_damage(damage)

    def receive_damage(self, damage):
        self.hp -= damage - self.dp

class PlayerCharacter(Character):
    def __init__(self,jobClass):
        super().__init__(jobClass)
        self.hp = 100
        self.mp = 5

    def defend(self):
        self.dp += 8 #this should only last for 1 round

    def useSkill(self,skill):
        skill()

# skills
def test():
    print("skill used")

# main game flow
print("You can choose two characters to fight from these: archer,wizard,knight and werewolf")
not_finished = True
turn = 1

while not_finished:
    # chosing characters
    choice1 = input("Choose your first character to fight: ")
    player1 = PlayerCharacter(choice1)
    choice2 = input("Choose another one: ")
    player2 = PlayerCharacter(choice2)
    player_team = [player1, player2]

    remaining_options = list(set(CHARACTERS) - {choice1, choice2})
    enemy1 = Character(remaining_options[0])
    enemy2 = Character(remaining_options[1])
    enemy_team = [enemy1,enemy2]

    print(f"You chose {player1.jobClass} and {player2.jobClass}. The enemy characters are {enemy1.jobClass} and {enemy2.jobClass}.")
    print()
    # letting the player choose which fighter to fight first
    first_fighter = input(f"You will fight with the {enemy1.jobClass} first, choose your first character to fight, 1/2 : ")
    if first_fighter == "2":
        player_team.reverse()

    while True:
        player_fighter = player_team[0]
        enemy_fighter = enemy_team[0]
        print(f"Turn: {turn}")
        turn += 1
        #options
        print(f"Player - {player_fighter.hp}hp {player_fighter.mp}mp")
        print(f"Enemy - {enemy_fighter.hp}hp")
        print(f"Actions: 1) Attack 2) Defend 3) Use skill 4) Quit/Restart")
        action = input("Action: ")

        if action == "1":
            if player_fighter.sp > enemy_fighter.sp:
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
        elif action == "3":
            if player_fighter.sp > enemy_fighter.sp:
                player_fighter.useSkill(test)
                enemy_fighter.attack(player_fighter)
            else:
                enemy_fighter.attack(player_fighter)
                player_fighter.useSkill(test)
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
            not_finished == False
            break

        print("-"*20)