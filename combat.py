import keyboard
import time
import random
from players import *
from trivia import generate_trivia
import functions
from Tools import timed_imput
from matplotlib import pyplot


class Combat:
    def __init__ (self, player1:Player, player2:Player):
        self.player1 = player1
        self.player2 = player2
        self.player1_in_combat = player1.Clone()
        self.player2_in_combat = player2.Clone()
        self.turn = 0
        self.player1_states = []
        self.player2_states = []
        self.end = False
        self.winner = None

    def clean_status(self, player: Player):
        if player == self.player1_in_combat:
            if self.player1_states.__contains__("Graphic Vision"):
                pyplot.close()
            self.player1_states.clear()
            self.player1_in_combat.damage = self.player1.damage
            self.player1_in_combat.epsilon = self.player1.epsilon
        else:
            if self.player2_states.__contains__("Graphic Vision"):
                pyplot.close()
            self.player2_states.clear()
            self.player2_in_combat.damage = self.player2.damage
            self.player2_in_combat.epsilon = self.player2.epsilon





    def get_answer(self, player, start_time, solution):
        actual_time = time.time()
        first_answer = timed_imput()
        if first_answer == solution:
            print("Great. Your answer is correct")
            return player
        elif first_answer == None:
            print(f"Time over. Now {self.player2_in_combat.name if player == self.player1_in_combat else self.player1_in_combat.name} can answer it in {300 - (time.time() - start_time) if 300 - (time.time() - start_time) > 0 else 30} seconds")
        else:
            print(f"Wrong answer, now {self.player2_in_combat.name if player == self.player1_in_combat else self.player1_in_combat.name} can answer it in {300 - (time.time() - start_time) if 300 - (time.time() - start_time) > 0 else 30} seconds")   

        left_time = 300 - (time.time() - start_time) if 300 - (time.time() - start_time) > 0 else 30
        actual_time = time.time()

        second_answer = timed_imput(wait_time=left_time)
        if second_answer == solution:
            print("Great. Your answer is correct")
            return self.player1_in_combat if player == self.player2_in_combat else self.player2_in_combat
        elif second_answer == None:
            print("Time over. Now a random player will attack first")
        else:
            print("Wrong answer too. Now a random player will attack first")
        return random.choice([self.player1_in_combat,self.player2_in_combat])

    def play(self):
        while not self.end:
            print(f"{self.player1_in_combat.name}, what armor do you like to use?")

            for i in range(len(self.player1_in_combat.armors)): #TODO: Only show armors in your current level
                if self.player1_in_combat.armors[i][2]>self.player1_in_combat.level:
                    break
                print(f"{i} : {self.player1_in_combat.armors[i][1]}")
                max_selection=i
            while True:
                armor_selection = int(input())
                if armor_selection > max_selection:
                    print("Invalid Input")
                else:
                    break
            self.player1_armor = self.player1_in_combat.armors[armor_selection][0]

            print(f"{self.player2_in_combat.name}, what armor do you like to use?")

            for i in range(len(self.player2_in_combat.armors)):
                if self.player2_in_combat.armors[i][2]>self.player2_in_combat.level:
                    break
                print(f"{i} : {self.player2_in_combat.armors[i][1]}")
                max_selection = i
            while True:
                armor_selection = int(input())
                if armor_selection > max_selection:
                    print("Invalid Input")
                else:
                    break
            self.player2_armor = self.player2_in_combat.armors[armor_selection][0]

            first_one_to_attack = None
            trivia = generate_trivia()
            print(trivia[0])
            start_time = time.time()
            print(f"Players have 5 minutes to solve the trivia problem. To answer the question {self.player1_in_combat.name} must have to press the key 'A' and {self.player2_in_combat.name} the key 'L',\n the first one to get the correct answer will attack first")

            while True:
                if keyboard.is_pressed('a'): 
                    print(f"{self.player1_in_combat.name} has 30 seconds to write the answer")
                    first_one_to_attack = self.get_answer(self.player1_in_combat,start_time,trivia[1])
                    break
                if keyboard.is_pressed('l'):
                    print(f"{self.player2_in_combat.name} has 30 seconds to write the answer")
                    first_one_to_attack = self.get_answer(self.player2_in_combat,start_time,trivia[1])
                    break
                if time.time() - start_time > 300:
                    print("Time out. Now a random player will atack first")
                    first_one_to_attack = random.choice([self.player1_in_combat, self.player2_in_combat])
                    break
            self.playTurn(first_one_to_attack)
            if not self.end:
                if self.player1_in_combat == first_one_to_attack:
                    self.clean_status(self.player1_in_combat)
                    self.playTurn(self.player2_in_combat)
                    self.clean_status(self.player2_in_combat)
                else:
                    self.clean_status(self.player2_in_combat)
                    self.playTurn(self.player1_in_combat)
                    self.clean_status(self.player1_in_combat)
        return self.winner


    def calculateDamage(self, player : Player, attack_selected):
        if player == self.player1_in_combat:
            toprint, armor_value = player.attacks[attack_selected][0](self.player2_armor,player.epsilon,player.damage)
            print(f"The zero founded was {toprint}. \nIt was founded in {armor_value} steps.")
            damage = player.damage- armor_value
            print(f"The attack caused a damage of {damage}")
        else:
            toprint, armor_value = player.attacks[attack_selected][0](self.player1_armor,player.epsilon,player.damage)
            print(f"The zero founded was {toprint}. \nIt was founded in {armor_value} steps.")
            damage = player.damage- armor_value
            print(f"The attack caused a damage of {damage}")
        return damage

    def playTurn(self, player : Player):
        print(f"{player.name}'s states:\n Life: {player.life}\n Damage: {player.damage}\n Epsilon: {player.epsilon}")
        if player == self.player1_in_combat:
            print(self.player1_states)
            print(f"{self.player2_in_combat.name}'s states:\n Life: {self.player2_in_combat.life}\n Damage: {self.player2_in_combat.damage}\n Epsilon: {self.player2_in_combat.epsilon}")
            print(self.player2_states)
        else:
            print(self.player2_states)
            print(f"{self.player1_in_combat.name}'s states:\n Life: {self.player1_in_combat.life}\n Damage: {self.player1_in_combat.damage}\n Epsilon: {self.player1_in_combat.epsilon}")
            print(self.player1_states)
        action = input(f"Is the turn of {player.name}\nWhat do you like to do? \nAttack(1) \nUse Skill(2)")


        if action == '1':
            print('Select your attack. Select 0 to return')
            for i in range(len(player.attacks)):
                if player.attacks[i][2] > player.level:
                    break
                print(f"{i+1}) {player.attacks[i][1]}")
                max_selection=i+1
            while True:
                attack_selection = int(input())
                if attack_selection > max_selection:
                    print("Invalid Input")
                else:
                    break
            if attack_selection == 0:
                return self.playTurn(player)
            else:
                damage = self.calculateDamage(player, attack_selection-1)
                if self.player1_in_combat == player:
                    self.player2_in_combat.life = self.player2_in_combat.life - damage
                    if self.player2_in_combat.life<=0:
                        self.end = True
                        self.winner = self.player1
                        print(f"That was an epic combat! {player.name} has emerged victorious")
                else:
                    self.player1_in_combat.life = self.player1_in_combat.life - damage
                    if self.player1_in_combat.life <= 0:
                        self.end = True
                        self.winner = self.player2
                        print(f"That was an epic combat! {player.name} has emerged victorious")                      

        elif action == '2':
            print('Select your skill. Select 0 to return')
            max_selection = 0
            for i in range(len(player.skills)):
                if player.skills[i][2] > player.level:
                    break
                print(f"{i+1}) {player.skills[i][1]}")
                max_selection=i+1
            while True:
                skill_selection = int(input())
                if skill_selection > max_selection: #TODO: Improve bobos-catcher
                    print("Invalid Input")
                else:
                    break
            if skill_selection == 0:
                return self.playTurn(player)
            else:
                player.skills[skill_selection-1][0](self,player)
            
            print("Now you most attack")

            print(f"{player.name}'s states:\n Life: {player.life}\n Damage: {player.damage}\n Epsilon: {player.epsilon}")
            if player == self.player1_in_combat:
                print(self.player1_states)
                print(f"{self.player2_in_combat.name}'s states:\n Life: {self.player2_in_combat.life}\n Damage: {self.player2_in_combat.damage}\n Epsilon: {self.player2_in_combat.epsilon}")
                print(self.player2_states)
            else:
                print(self.player2_states)
                print(f"{self.player1_in_combat.name}'s states:\n Life: {self.player1_in_combat.life}\n Damage: {self.player1_in_combat.damage}\n Epsilon: {self.player1_in_combat.epsilon}")
                print(self.player1_states)

            print('Select your attack.')



            for i in range(len(player.attacks)):
                if player.attacks[i][2] > player.level:
                    break
                print(f"{i+1}) {player.attacks[i][1]}")
                max_selection=i+1
            while True:
                attack_selection = int(input())
                if attack_selection > max_selection:
                    print("Invalid Input")
                else:
                    break

            damage = self.calculateDamage(player, attack_selection-1)
            if self.player1_in_combat == player:
                self.player2_in_combat.life = self.player2_in_combat.life - damage
                if self.player2_in_combat.life < 0 or (self.player1_states.__contains__("Culling Blade") and self.player2_in_combat.life <= damage and not print("The culling blade has succeded!!")):
                    self.end = True
                    self.winner = self.player1
                    print(f"That was an epic combat! {player.name} has emerged victorious")
            else:
                self.player1_in_combat.life = self.player1_in_combat.life - damage
                if self.player1_in_combat.life < 0 or (self.player2_states.__contains__("Culling Blade") and self.player1_in_combat.life <= damage and not print("The cullling blade has succeded!!")):
                    self.end = True
                    self.winner = self.player2
                    print(f"That was an epic combat! {player.name} has emerged victorious")

        else:
            print('Invalid input')
            return self.playTurn(player)