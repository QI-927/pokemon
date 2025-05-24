import time
import random
import json
import os

SAVE_FILE = "save_data.json"

class Pokemon:
    def __init__(self, name, level, hp, atk, defense):
        self.name = name
        self.level = level
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.xp = 0
        self.max_hp = hp

    def summary(self):
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Attack: {self.atk}")
        print(f"Defense: {self.defense}")
        print(f"XP: {self.xp}/10")

    def is_fainted(self):
        return self.hp <= 0

    def take_damage(self, dmg):
        self.hp = max(0, self.hp - dmg)

    def attack_target(self, target):
        damage = max(1, self.atk - target.defense)
        target.take_damage(damage)
        return damage

    def gain_xp(self, amount):
        self.xp += amount
        print(f"{self.name} gained {amount} XP!")
        while self.xp >= 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= 10
        self.max_hp += 5
        self.hp = self.max_hp
        self.atk += 2
        self.defense += 1
        print(f"{self.name} leveled up to {self.level}!")
        print("Stats increased!")
        self.summary()

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "atk": self.atk,
            "defense": self.defense,
            "xp": self.xp,
            "max_hp": self.max_hp
        }

    @staticmethod
    def from_dict(data):
        p = Pokemon(data["name"], data["level"], data["hp"], data["atk"], data["defense"])
        p.xp = data["xp"]
        p.max_hp = data["max_hp"]
        return p

def slow_print(text, delay=0.04):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def battle(player_pokemon):
    wild_names = ["Pidgey", "Rattata", "Weedle", "Zubat"]
    wild_name = random.choice(wild_names)
    level = random.randint(1, min(5, player_pokemon.level))
    wild = Pokemon(wild_name, level, hp=10 + level * 2, atk=3 + level, defense=2 + level // 2)

    print(f"\nA wild {wild.name} (Lv {wild.level}) appeared!")

    while not player_pokemon.is_fainted() and not wild.is_fainted():
        action = input("\nChoose action: [A]ttack | [S]ummary | [R]un: ").lower()
        if action == 'a':
            dmg = player_pokemon.attack_target(wild)
            print(f"{player_pokemon.name} attacks {wild.name} and deals {dmg} damage! {wild.name}'s HP: {wild.hp}")
            if wild.is_fainted():
                print(f"{wild.name} has fainted! You won the battle!")
                player_pokemon.gain_xp(5)
                return
            edmg = wild.attack_target(player_pokemon)
            print(f"{wild.name} attacks {player_pokemon.name} and deals {edmg} damage! {player_pokemon.name}'s HP: {player_pokemon.hp}")
            if player_pokemon.is_fainted():
                print(f"{player_pokemon.name} has fainted... You've been defeated.")
                return
        elif action == 's':
            player_pokemon.summary()
        elif action == 'r':
            print("You ran away safely.")
            return
        else:
            print("Invalid input. Please choose again.")

def save_game(pokemon):
    with open(SAVE_FILE, "w") as f:
        json.dump(pokemon.to_dict(), f)
    print("Game saved.")

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return Pokemon.from_dict(data)
    return None

def final_event(pokemon):
    slow_print("\nSuddenly, alarms ring out across the town... Team Rocket is attacking!")
    slow_print("A shadowy figure appears... It's Osaka, the mastermind behind the chaos!")
    slow_print("He summons Mewtwo to destroy the city!")
    choice = input("\nWill you [F]ight or [R]un?: ").lower()

    if choice == 'r':
        slow_print("You chose to run...")
        slow_print("Your heart filled with fear, your Caterpie's spirit shatters.")
        slow_print("It reverts to level 5. You live your days as a humble bug catcher.")
        pokemon.level = 5
        pokemon.hp = 20
        pokemon.atk = 7
        pokemon.defense = 4
        return

    slow_print("You chose to fight!")
    slow_print("Mewtwo strikes you down instantly.")
    pokemon.take_damage(pokemon.hp)
    time.sleep(1)
    slow_print("But wait... your Pokémon begins to glow!")
    slow_print(f"{pokemon.name} is evolving... into RAYQUAZA!")

    rayquaza = Pokemon("Rayquaza", level=100, hp=500, atk=150, defense=100)
    slow_print("RAYQUAZA roars, challenging Mewtwo!")

    mewtwo = Pokemon("Mewtwo", level=100, hp=350, atk=140, defense=90)

    while not rayquaza.is_fainted() and not mewtwo.is_fainted():
        input("\nPress Enter to attack!")
        dmg = rayquaza.attack_target(mewtwo)
        print(f"Rayquaza deals {dmg} damage! Mewtwo's HP: {mewtwo.hp}")
        if mewtwo.is_fainted():
            slow_print("Mewtwo is defeated! The town is saved!")
            slow_print("You are hailed as a hero across the region.")
            return
        edmg = mewtwo.attack_target(rayquaza)
        print(f"Mewtwo deals {edmg} damage! Rayquaza's HP: {rayquaza.hp}")

    slow_print("The battle ends.")
    if rayquaza.is_fainted():
        slow_print("Even Rayquaza fell... the town is doomed...")

def intro():
    pokemon = load_game()
    if pokemon:
        print("Loaded previous save.")
        pokemon.summary()
        while not pokemon.is_fainted():
            if pokemon.level >= 100:
                final_event(pokemon)
                break
            choice = input("\nWhat would you like to do? [B]attle | [S]ummary | [Q]uit | [Save]: ").lower()
            if choice == 'b':
                battle(pokemon)
            elif choice == 's':
                pokemon.summary()
            elif choice == 'save':
                save_game(pokemon)
            elif choice == 'q':
                save_game(pokemon)
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        return
    slow_print("......")
    time.sleep(1)
    slow_print("You wake up at the entrance of a dark tunnel, your mind blank.")
    slow_print("The sky is dim and the air smells of soil and mystery.")
    slow_print("An elderly man with white hair approaches, holding a strange device.")
    time.sleep(1)

    slow_print("???: Hey, are you alright? Who are you?")
    name = input("You: I... I'm... my name is: ")
    slow_print(f"???: So your name is {name}. Strange... why is there a Pokémon egg beside you?")

    slow_print("Professor Oak: Hello, I'm Professor Oak. This is quite a rare egg.")
    slow_print("Professor Oak: Come with me to the lab, let's see what hatches from it.")

    slow_print("You follow him through the grass to his cozy lab.")
    time.sleep(1)

    slow_print("He carefully places the egg into an incubator... tick... tick...")
    time.sleep(2)
    slow_print("Ding! The egg begins to crack...")
    slow_print("A wet little bug jumps out — it's a Caterpie!")
    slow_print("Professor Oak: Wow, a healthy Caterpie!")

    nickname = input("What will you name your Caterpie?: ")
    slow_print(f"Professor Oak: I see. So your new partner is {nickname}.")
    slow_print("From here, your grand adventure begins...")
    pokemon = Pokemon(nickname, level=5, hp=20, atk=7, defense=4)

    while not pokemon.is_fainted():
        if pokemon.level >= 100:
            final_event(pokemon)
            break
        choice = input("\nWhat would you like to do? [B]attle | [S]ummary | [Q]uit | [Save]: ").lower()
        if choice == 'b':
            battle(pokemon)
        elif choice == 's':
            pokemon.summary()
        elif choice == 'save':
            save_game(pokemon)
        elif choice == 'q':
            save_game(pokemon)
            print("Game saved. Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    intro()
