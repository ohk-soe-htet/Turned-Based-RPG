import random

# offensive skills
def pierce_shot(target):  # archer 
    return [20 + target.dp,"Evasion"]
def fireball(target):  # wizard 
    return [30,"Fireball"]
def shield_bash(target):  # knight
    return [23,"Shield Bash"]
def claw_swipe(target):  # werewolf
    return [23,"Claw Swipe"]
# defensive skills 
def evasion(user):  # archer
    user.temp_dp += 5
    print(f"Archer used Evasion and increased their DP by 5.")
def ice_barrier(user):  # wizard 
    user.temp_dp += 5
    print(f"Wizard used Ice Barrier and increased their DP by 5.")
def shield_of_valor(user):  # knight 
    user.temp_dp += 10
    print(f"Knight used Shield of Valor and increased their DP by 10.")
def regen(user):  # werewolf
    user.hp += 15
    print(f"Werewolf used Regen and healed themselves for 15 HP.")

# creating characters
CHARACTERS = ["archer","wizard","knight","werewolf"]
CHAR_ATTR = {
    "archer": [10, 1, 3, 10, [pierce_shot, evasion], ""],   # [ap, dp, sp, critical_chance, skills, image] # in this game, dp acts like armour
    "wizard": [15, 2, 2, 20, [fireball, ice_barrier], ""],
    "knight": [12, 3, 1, 25, [shield_bash, shield_of_valor], ""],
    "werewolf": [13, 2, 2, 30, [claw_swipe, regen], ""]
}
# Enemy characters can only have these
class Character:
    def __init__(self,jobClass):
        self.hp = 150 # +50 hp handicap for the enemy for not being able to defend or use skill
        if jobClass in CHAR_ATTR:
            self.ap, self.dp, self.sp, self.crital_chance, self.skill, self.image = CHAR_ATTR[jobClass]
        self.jobClass = jobClass
        
    def attack(self, target):
        # adding extra damage according to each character's critacal chance
        chance = random.randint(1, 100)
        critical_damage = 0
        if chance <= self.crital_chance:
            critical_damage += random.randint(2,5)
            print(f"{target.jobClass.capitalize()} got hit in the critical point. Received extra damage")
        # When dp is higher than ap, there would be no damage
        damage = self.ap + critical_damage
        armour = target.dp
        if isinstance(target, PlayerCharacter): # only if the target is player
            armour = target.temp_dp
        effective_damage = max(damage - armour, 0)
        target.receive_damage(effective_damage)
        print(f"{self.jobClass.capitalize()} dealt {effective_damage} damage on {target.jobClass}")

    def receive_damage(self, damage):
        self.hp -= damage
# inherit and add extra actions for Player characters
class PlayerCharacter(Character):
    def __init__(self,jobClass):
        super().__init__(jobClass)
        self.hp = 100
        self.mp = 4
        self.temp_dp = self.dp
        self.got_attacked = False

    def defend(self):
        self.temp_dp += 8
        print(f"{self.jobClass.capitalize()} raised its dp by 8")
    
    def reset_temp_dp(self):
        if self.got_attacked:  # reset temp_dp only if the player got attacked
            self.temp_dp = self.dp
        self.got_attacked = False

    def use_skill(self,skill_type,target):
        if skill_type == 0: # offensive
            self.mp -= 1
            damage,skill_name = self.skill[0](target)
            target.receive_damage(damage)
            print(f"{self.jobClass.capitalize()} used {skill_name} and dealt {damage} damage")
        else: # defensive
            self.mp -= 1 # will only have 2 chance to use to make the game more balenced
            self.skill[1](self)

# main game flow
print("You can choose two characters to fight from these: archer, wizard, knight and werewolf")
not_finished = True
round_number = 1
# all these inputs and creating characters are wrapped in while loop so that the game can restart from this point
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
        # round counter
        print(f"Round: {round_number}*")
        round_number += 1
        print()
        # showing stats
        print(f"       |  Fighter   |   HP   |   MP   |   AP   |   DP   ")
        print(f"        ------------------------------------------------")
        print(f"Player | {player_fighter.jobClass:<10} | {player_fighter.hp:<6} | {player_fighter.mp:<6} | {player_fighter.ap:<6} | {player_fighter.dp:<6}")
        print(f"Enemy  | {enemy_fighter.jobClass:<10} | {enemy_fighter.hp:<6} | -      | {enemy_fighter.ap:<6} | {enemy_fighter.dp:<6}")
        print()
        # options
        print(f"Actions: 1)Attack 2)Defend 3)Use skill 4)Quit/Restart")
        action = input("Action: ")
        # attack
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
            # after the enemy's attack, dp should be reset
            player_fighter.got_attacked = True
        # defend
        elif action == "2":
            player_fighter.defend()
            enemy_fighter.attack(player_fighter)
            # after the enemy's attack, dp should be reset
            player_fighter.got_attacked = True
        # skill action
        elif action == "3":
            skill_type = int(input("Chose which type of skills you would like to use: 1)Offensive or 2)Defensive: "))
            if player_fighter.sp >= enemy_fighter.sp:
                if player_fighter.mp <= 0:
                    print("Not enough mana, try other actions")
                    round -= 1
                    continue
                else:
                    player_fighter.use_skill(skill_type-1,enemy_fighter)
                    enemy_fighter.attack(player_fighter)
                    # after the enemy's attack, dp should be reset
                    player_fighter.got_attacked = True
            else:
                enemy_fighter.attack(player_fighter)
                if player_fighter.mp <= 0:
                    print("Not enough mana, try other actions")
                    round -= 1
                    continue
                else:
                    player_fighter.use_skill(skill_type-1,enemy_fighter)
        # quit or restart
        elif action == "4":
                choice = input("Do you want to quit (q) or restart (r)? ")
                if choice.lower() == "q":
                    not_finished = False
                    break
                elif choice.lower() == "r":
                    print("Restarting...")
                    # resetting the round number to 1
                    turn = 1
                    break
    
        # if fighter or enemy fighter's HP drops to 0, remove them from the list
        if player_fighter.hp <= 0:
            player_team.remove(player_fighter)
            if len(player_team) == 1:
                print(f"Your {player_fighter.jobClass} is defeated! \nYour second fighter {player_team[0].jobClass} came in")
        if enemy_fighter.hp <= 0:
            enemy_team.remove(enemy_fighter)
            if len(enemy_team) == 1:
                print(f"Enemy {enemy_fighter.jobClass} is defeated! Second fighter {enemy_team[0].jobClass} came in")
        # team with 0 fighter lose
        if len(player_team) == 0:
            print("You lost")
            not_finished = False
            break
        elif len(enemy_team) == 0:
            print("Congratulation, You won!!")
            not_finished = False
            break

        # reset before the start of a new round if the player got attacked
        player_fighter.reset_temp_dp()

        # line after each round
        print("-"*20)