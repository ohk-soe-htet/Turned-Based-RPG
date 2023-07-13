import random
#test
# texts
ACTION_TEXT = "Actions: \n1. Attack \n2. Defend \n3. Use skill \n4. Quit/Restart"
# creating characters
CHARACTERS = ["archer","wizard","knight","werewolf"]
CHAR_ATTR = {   
    "archer": [10, 1, 3,10,""],   # [ap, dp, sp, image]
    "mage": [15, 2, 2,20,""],
    "knight": [12, 3, 1,25,""],
    "werewolf": [13, 2, 2,30,""]
}

class Character:
    def __init__(self,jobClass):
        self.hp = 150
        if jobClass in CHAR_ATTR:
            self.ap,self.dp,self.sp,self.crital_chance,self.image = CHAR_ATTR[jobClass]
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

    def defend(self):
        self.dp += 8

class PlayerCharacter(Character):
    def __init__(self,jobClass):
        super().__init__(jobClass)
        self.hp = 100
        self.mp = 5

    def useSkill(self,skill):
        skill()

# skills
def test():
    print("skill used")

# main game flow
not_finished = True
print("You can choose two characters to fight from these: archer,wizard,knight and werewolf")

choice1 = input("choose your first character to fight: ")
player1 = PlayerCharacter(choice1)
choice2 = input("choose another one: ")
player2 = PlayerCharacter(choice2)

enemy_team = list(set(CHARACTERS) - {choice1, choice2})
enemy1 = Character(enemy_team[0])
enemy2 = Character(enemy_team[1])

# chosing characters
print(f"You chose {player1.jobClass} and {player2.jobClass}. The enemy characters are {enemy1.jobClass} and {enemy2.jobClass}.")
print("Choose your first character to fight")

while not_finished:
    #options
    print(ACTION_TEXT)
    action = input("Action: ")

    if action == "1":
        player1.attack(enemy1)
        print(enemy1.hp)
    elif action == "2":
        player1.defend()
        print(player1.dp)
    elif action == "3":
        player1.useSkill(test)
    else:
        break