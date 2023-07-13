import random

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
        self.dp += 8 #this should only last for 1 round

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
print("You can choose two characters to fight from these: archer,wizard,knight and werewolf")

choice1 = input("choose your first character to fight: ")
player1 = PlayerCharacter(choice1)
choice2 = input("choose another one: ")
player2 = PlayerCharacter(choice2)
player_team = [player1,player2]

enemy_team = list(set(CHARACTERS) - {choice1, choice2})
enemy1 = Character(enemy_team[0])
enemy2 = Character(enemy_team[1])

# chosing characters
print(f"You chose {player1.jobClass} and {player2.jobClass}. The enemy characters are {enemy1.jobClass} and {enemy2.jobClass}.")
first_fighter = input(f"You will fight with the {enemy1.jobClass} first, choose your first character to fight, 1/2 : ")
if first_fighter == "2":
    player_team.reverse()

not_finished = True

while not_finished:
    fighter = player_team[0]
    enemy_fighter = enemy_team[0]
    #options
    print(ACTION_TEXT)
    action = input("Action: ")

    if action == "1":
        # 1.attack(2) and 2.attack(2) # both attacks, depend on the sp
        print("attacked")
    elif action == "2":
        # 1.defend() and 2.attack(2) # player defend, dont know if it should depends on sp
        print("defended") 
    elif action == "3":
        fighter.useSkill(test)
    if action == "4":
        # will ask whether user will quit or restart
        not_finished = False

    # if fighter or enemy fighter hp drops to 0, removes it from the list

    if len(player_team) == 0:
        print("You lose")
    elif len(enemy_team) == 0:
        print("You win")