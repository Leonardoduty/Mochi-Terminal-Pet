import sys
import random
import os
import time
import threading

name = "Mochi"

level = 1
xp = 0
hunger = 80
happiness = 80
energy = 80

last_update = time.time()


def show_pet():
    return r"""
          /\_/\
         ( o.o )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|
    """


def show_status():
    return f"""
    +++++++++++++++++++++++++++++
              ---{name}---
    +++++++++++++++++++++++++++++
    
      Level     : {level}
      XP        : {xp}/100

      Hunger    : {hunger}
      Happiness : {happiness}
      Energy    : {energy}

    +++++++++++++++++++++++++++++
    """

def show_screen():
    pet_lines = show_pet().splitlines()
    status_lines = show_status().splitlines()

    max_lines = max(len(pet_lines), len(status_lines))

    for i in range(max_lines):
        pet_line = pet_lines[i] if i < len(pet_lines) else ""
        status_line = status_lines[i] if i < len(status_lines) else ""

        print(f"{pet_line:<32}{status_line}")

while True:
    current_t = time.time()
    elapsed = current_t - last_update

    if xp >= 100:
        level = level + 1
        xp = xp - 100
    os.system("clear")
    show_screen()
    if elapsed >= 5:
            hunger_loss = random.randint(1,3)
            hunger = max(0, hunger - hunger_loss)
            last_update = current_t
    task = input("""What do you want to do?
    1> Feed
    2> Play
    3> Quit
    
    """)
    if task == "1":
        hunger = min(100, hunger + 5)
        xp = xp + 5
    if task == "2":
        happiness = min(100, happiness+10)
        energy= max(0, energy-10)
        hunger = max(0, hunger-5)
        xp = xp + 5
    if task == "3":
        sys.exit()

      