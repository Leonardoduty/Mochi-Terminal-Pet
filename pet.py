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
mood = "Happy"

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

eating_frames = [
r"""
          /\_/\
         ( o.o )  ---->
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|

             ______
            /      \
           |  Food  |
            \______/
""",

r"""
          /\_/\
         ( o_o )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|

             ______
            /      \
           |  Food  |
            \______/
""",

r"""
           /\_/\
          ( o_o )
         /  >♥<  \
        /         \
       (   _____   )
        \_/     \_/
          |     |
          |_| |_|

             ______
            /      \
           |  Food  |
            \______/
""",

r"""
            /\_/\
           ( o_o )
          /  >♥<  \
         /         \
        (   _____   )
         \_/     \_/
           |     |
           |_| |_|

             ______
            /      \
           |  FOOD  |
            \______/
""",

r"""
             /\_/\
            ( >.< )
           /  >♥<  \
          /         \
         (   _____   )
          \_/     \_/
            |     |
            |_| |_|

             ____
            |Food|
             ‾‾‾
""",

r"""
             /\_/\
            ( ^.^ )
           /  >♥<  \
          /         \
         (   _____   )
          \_/     \_/
            |     |
            |_| |_|

          om nom...
""",

r"""
             /\_/\
            ( ^o^ )
           /  >♥<  \
          /         \
         (   _____   )
          \_/     \_/
            |     |
            |_| |_|

         om nom nom...
""",

r"""
             /\_/\
            ( ^.^ )
           /  >♥<  \
          /         \
         (   _____   )
          \_/     \_/
            |     |
            |_| |_|

           om nom!
""",

r"""
           /\_/\
          ( o.o )
         /  >♥<  \
        /         \
       (   _____   )
        \_/     \_/
          |     |
          |_| |_|

              ______
             | Food |
              ‾‾‾‾‾
""",

r"""
          /\_/\
         ( ^.^ )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|
""",

r"""
          /\_/\
         ( ^.^ )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|

          mmm...
""",

r"""
          /\_/\
         ( o.o )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|
"""
]

playing_frames = [

r"""
          /\_/\
         ( o.o )  ---->
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|

                         .---.
                        (     )
                         '---'
""",

r"""
          /\_/\
         ( o.o )  ---->
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|

                      .---.
                     (     )
                      '---'
""",

r"""
           /\_/\
          ( ^.^ )
         /  >♥<  \
        /         \
       (   _____   )
        \_/     \_/
          |     |
          |_| |_|

                   .---.
                  (     )
                   '---'
""",

r"""
            /\_/\
           ( ^.^ )
          /  >♥<  \
         /         \
        (   _____   )
         \_/     \_/
           |     |
           |_| |_|

                .---.
               (     )
                '---'
""",

r"""
              /\_/\
             ( ^.^ )
            /  >♥<  \
           /         \
          (   _____   )
           \_/     \_/
             |     |
             |_| |_|

             .---.
            (     )
             '---'
""",

r"""
                 /\_/\
                ( ^.^ )
               /  >♥<  \
              /         \
             (   _____   )
              \_/     \_/
                |     |
                |_| |_|

          .---.
         (     )
          '---'
""",

r"""
                    /\_/\
                   ( ^.^ )
                  /  >♥<  \
                 /         \
                (   _____   )
                 \_/     \_/
                   |     |
                   |_| |_|

              .---.
             (     )
              '---'
""",

r"""
                       /\_/\
                      ( ^.^ )
                     /  >♥<  \
                    /         \
                   (   _____   )
                    \_/     \_/
                      |     |
                      |_| |_|

                   .---.
                  (     )
                   '---'
""",

r"""
                         /\_/\
                        ( ^o^ )
                       /  >♥<  \
                      /         \
                     (   _____   )
                      \_/     \_/
                        |     |
                        |_| |_|

                    .---.
                   (     )
                    '---'
""",

r"""
                      /\_/\
                     ( ^.^ )
                    /  >♥<  \
                   /         \
                  (   _____   )
                   \_/     \_/
                     |     |
                     |_| |_|

                   .---.
                  (     )
                   '---'
""",

r"""
                      /\_/\
                     ( ^.^ )
                    /  >♥<  \
                   /         \
                  (   _____   )
                   \_/     \_/
                     |     |
                     |_| |_|

                  YAY!
                 .---.
                (     )
                 '---'
""",

r"""
          /\_/\
         ( o.o )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|
"""
]

sleeping_frames = [

r"""
          /\_/\
         ( o.o )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|
""",

r"""
          /\_/\
         ( -.- )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|
""",

r"""
          /\_/\
         ( -.- )
        /  >♥<  \
       /         \
      (   _____   )
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|
""",

r"""
           /\_/\
          ( -.- )
         /  >♥<  \
        /         \
       (  _______  )
        \_/     \_/
          |     |
          |_| |_|
""",

r"""
           /\_/\
          ( -_- )
         /  >♥<  \
        /         \
       (  _______  )
        \_/     \_/
          |     |
          |_| |_|
""",

r"""
            /\_/\
           ( -_- )
          /  >♥<  \
         /         \
        (  _______  )
         \_/     \_/
           |     |
           |_| |_|

             z
""",

r"""
            /\_/\
           ( -_- )
          /  >♥<  \
         /         \
        (  _______  )
         \_/     \_/
           |     |
           |_| |_|

            z z
""",

r"""
            /\_/\
           ( -.- )
          /  >♥<  \
         /         \
        (  _______  )
         \_/     \_/
           |     |
           |_| |_|

          z z z...
""",

r"""
             /\_/\
            ( -.- )
           /  >♥<  \
          /         \
         (  _______  )
          \_/     \_/
            |     |
            |_| |_|

          Z z z...
""",

r"""
             /\_/\
            ( -_- )
           /  >♥<  \
          /         \
         (  _______  )
          \_/     \_/
            |     |
            |_| |_|

          Z Z Z...
""",

r"""
           /\_/\
          ( o.o )
         /  >♥<  \
        /         \
       (   _____   )
        \_/     \_/
          |     |
          |_| |_|

          *yawn*
""",

r"""
          /\_/\
         ( ^.^ )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|
"""
]

gift_frames = [

r"""
          /\_/\
         ( o.o )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|

                         _______
                        /       \
                       /  Gift   \
                       \_________/
""",

r"""
          /\_/\
         ( o.o )  ---->
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|

                         _______
                        /       \
                       /  Gift   \
                       \_________/
""",

r"""
           /\_/\
          ( o_o )
         /  >♥<  \
        /         \
       (   _____   )
        \_/     \_/
          |     |
          |_| |_|

                      _______
                     /       \
                    /  Gift   \
                    \_________/
""",

r"""
             /\_/\
            ( o_o )
           /  >♥<  \
          /         \
         (   _____   )
          \_/     \_/
            |     |
            |_| |_|

                   _______
                  /       \
                 /  Gift   \
                 \_________/
""",

r"""
               /\_/\
              ( o.o )
             /  >♥<  \
            /         \
           (   _____   )
            \_/     \_/
              |     |
              |_| |_|

             _______
            /       \
           /  Gift   \
           \_________/
""",

r"""
                /\_/\
               ( ^.^ )
              /  >♥<  \
             /         \
            (   _____   )
             \_/     \_/
               |     |
               |_| |_|

              _______
             /       \
            /  Gift   \
            \_________/
""",

r"""
                /\_/\
               ( o.o )
              /  >♥<  \
             /         \
            (   _____   )
             \_/     \_/
               |     |
               |_| |_|

              _______
             /       \
            /         \
            \_________/
              |     |
              |     |
""",

r"""
                 /\_/\
                ( O.O )
               /  >♥<  \
              /         \
             (   _____   )
              \_/     \_/
                |     |
                |_| |_|

              \  ^  /
               \ | /
                \|/
              _______
             /       \
            /         \
            \_________/
""",

r"""
                 /\_/\
                ( ^.^ )
               /  >♥<  \
              /         \
             (   _____   )
              \_/     \_/
                |     |
                |_| |_|

              \  ^  /
               \ | /
                \|/
              _______
             /       \
            /         \
            \_________/
""",

r"""
                 /\_/\
                ( ^o^ )
               /  >♥<  \
              /         \
             (   _____   )
              \_/     \_/
                |     |
                |_| |_|

             "Thank You!"
""",

r"""
                 /\_/\
                ( ^.^ )
               /  >♥<  \
              /         \
             (   _____   )
              \_/     \_/
                |     |
                |_| |_|

              _______
             /       \
            /  Gift   \
            \_________/
""",

r"""
          /\_/\
         ( ^.^ )
        /  >♥<  \
       /         \
      (   _____   )
       \_/     \_/
         |     |
         |_| |_|
"""
]


def show_status():
    return f"""
    +++++++++++++++++++++++++++++
              ---{name}---
    +++++++++++++++++++++++++++++
    
      Level     : {level}
      XP        : {xp}/100
      Mood : {mood}

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

def show_animation_frame(frame):
    status_lines = show_status().splitlines()
    pet_lines = frame.splitlines()

    max_lines = max(len(pet_lines), len(status_lines))

    for i in range(max_lines):
        pet_line = pet_lines[i] if i < len(pet_lines) else ""
        status_line = status_lines[i] if i < len(status_lines) else ""

        print(f"{pet_line:<32}{status_line}")

def play_animation(frames, delay=0.15):
    for frame in frames:
        os.system("clear")
        show_animation_frame(frame)
        time.sleep(delay)

def feed():
    global hunger, xp
    play_animation(eating_frames, 0.2)
    hunger = min(100, hunger + 5)
    xp = xp + 5
    reaction("Mochi: Yum! Thanks!")

def play():
    global happiness, energy, hunger, xp

    play_animation(playing_frames, 0.15)

    happiness = min(100, happiness+10)
    energy= max(0, energy-10)
    hunger = max(0, hunger-5)
    xp = xp + 5
    reaction("Mochi: Yay! That was Fun!")

def sleep():
    global energy, hunger, happiness, xp

    play_animation(sleeping_frames, 0.2)

    energy = min(100, energy  + 20)
    hunger = max(0, hunger - 5)
    happiness = min(100, happiness + 2)
    xp = min(100, xp + 5)
    reaction("Mochi: Zzz...Zzz...Zzz")

def gift():
    global happiness, energy, xp

    play_animation(gift_frames, 0.2)

    happiness = min(100, happiness + 15)
    energy = max(0, energy  - 5)
    xp = min(100, xp + 10)
    reaction("Mochi: A gift? Thank you!")

def get_mood():
    global happiness, energy, hunger, mood
    if happiness < 25:
        mood = "Sad"
    elif energy < 25:
        mood = "Sleppy"
    elif hunger < 25:
        mood = "Hungry"
    else:
        mood = "Happy"

def reaction(message):
    print(message)
    input("Press Enter to Continue")

def activities():
    while True:
        os.system("clear")
        get_mood()
        show_screen()
        act = input("""What activity do you want to do?

    1> Feed
    2> Play
    3> Sleep
    4> Gift
    5> Back
        """)
        if act == "1":
            feed()
        if act == "2":
            play()
        if act == "3":
            sleep()
        if act == "4":
            gift()
        if act == "5":
            return  

while True:
    current_t = time.time()
    elapsed = current_t - last_update

    if xp >= 100:
        level = level + 1
        xp = xp - 100
    os.system("clear")
    if elapsed >= 5:
        hunger_loss = random.randint(1,3)
        hunger = max(0, hunger - hunger_loss)
        last_update = current_t
    get_mood()
    show_screen()
    task = input("""What do you want to do?
    1> Activities
    2> XYZ
    3> ABC
    4> EFG
    5> Quit
    
    
    """)
    if task == "1":
        activities()
    if task == "5":
        sys.exit()


