import sys
import random
import os
import time
import threading
import json


from openai import OpenAI
from dotenv import load_dotenv

name = "Mochi"

level = 1
evo_stage = 1
xp = 0
hunger = 80
happiness = 80
energy = 80
mood = "Happy"
theme = "classic"
animations_enabled = True
thoughts_enabled = True
hunger_decay_enabled = True
themes = {
    "classic": {
        "border": "+",
        "title": "=",
        "arrow": ">",
    },

    "dark": {
        "border": "#",
        "title": "#",
        "arrow": ">>",
    },

    "minimal": {
        "border": "-",
        "title": "-",
        "arrow": ">",
    }
}
def get_theme():
    return themes.get(theme, themes["classic"])

def theme_menu():
    global theme

    while True:
        os.system("clear")

        print("""
++++++++++++++++++++++++++++
          THEMES
++++++++++++++++++++++++++++
""")

        print(f"1> Classic {'[ACTIVE]' if theme == 'classic' else ''}")
        print(f"2> Dark    {'[ACTIVE]' if theme == 'dark' else ''}")
        print(f"3> Minimal {'[ACTIVE]' if theme == 'minimal' else ''}")
        print("4> Back")

        choice = input("\nChoose a theme: ")

        if choice == "1":
            theme = "classic"

        elif choice == "2":
            theme = "dark"

        elif choice == "3":
            theme = "minimal"

        elif choice == "4":
            return

last_update = time.time()

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

achievements = {
    "first_meal": False,
    "first_play": False,
    "first_sleep": False,
    "first_gift": False,
    "level_5": False,
    "meals_25": False,
    "plays_25": False,
    "gifts_10": False
}

meals = 0
plays = 0
sleeps = 0
gifts = 0
last_thought = ""

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
    global hunger, xp, meals
    play_animation(eating_frames, 0.2)
    hunger = min(100, hunger + 5)
    xp = xp + 5
    meals += 1
    check_level_up()
    check_achievements()
    reaction("Mochi: Yum! Thanks!")


def check_level_up():
    global level, xp

    while xp >= 100:
        xp -= 100
        level += 1
        check_evolution()

        print(f"""++++++++++++++++++++++++++++
                        Level Up!   
                  ++++++++++++++++++++++++++++
                
                 Mochi reached Levl {level}!
                 Mochi: I am Getiing Stronger!
                 
                 Press Enter to Continue
                 
        
        """)

def check_evolution():
    global evo_stage

    if level >= 5 and evolution_stage == 1:
        evolution_stage = 2

        print("""
++++++++++++++++++++++++++++
         EVOLUTION! 
++++++++++++++++++++++++++++

        Mochi evolved!

        Stage 2: Young Mochi

++++++++++++++++++++++++++++
""")

    elif level >= 15 and evolution_stage == 2:
        evolution_stage = 3

        print("""
++++++++++++++++++++++++++++
         EVOLUTION! 
++++++++++++++++++++++++++++

        Mochi evolved!

        Stage 3: Mature Mochi

++++++++++++++++++++++++++++
""")

    elif level >= 25 and evolution_stage == 3:
        evolution_stage = 4

        print("""
++++++++++++++++++++++++++++
         EVOLUTION! 
++++++++++++++++++++++++++++

        Mochi evolved!

       Stage 4: Legendary Mochi

++++++++++++++++++++++++++++
""")
        
def play():
    global happiness, energy, hunger, xp, plays

    play_animation(playing_frames, 0.15)

    happiness = min(100, happiness+10)
    energy= max(0, energy-10)
    hunger = max(0, hunger-5)
    xp = xp + 5
    plays += 1
    check_level_up()
    check_achievements()
    reaction("Mochi: Yay! That was Fun!")

def sleep():
    global energy, hunger, happiness, xp, sleeps

    play_animation(sleeping_frames, 0.2)

    energy = min(100, energy  + 20)
    hunger = max(0, hunger - 5)
    happiness = min(100, happiness + 2)
    xp = min(100, xp + 5)
    sleeps += 1
    check_level_up()
    check_achievements()
    reaction("Mochi: Zzz...Zzz...Zzz")

def gift():
    global happiness, energy, xp, gifts
    
    play_animation(gift_frames, 0.2)

    happiness = min(100, happiness + 15)
    energy = max(0, energy  - 5)
    xp = min(100, xp + 10)
    gifts += 1
    check_level_up()
    check_achievements()
    reaction("Mochi: A gift? Thank you!")

def check_achievements():
    global achievements

    if meals >= 1 and not achievements["first_meal"]:
        achievements["first_meal"] = True
        print("🏆 Achievement Unlocked: First Meal!")

    if plays >= 1 and not achievements["first_play"]:
        achievements["first_play"] = True
        print("🏆 Achievement Unlocked: First Play!")

    if sleeps >= 1 and not achievements["first_sleep"]:
        achievements["first_sleep"] = True
        print("🏆 Achievement Unlocked: First Sleep!")

    if gifts >= 1 and not achievements["first_gift"]:
        achievements["first_gift"] = True
        print("🏆 Achievement Unlocked: First Gift!")




def get_mood():
    global happiness, energy, hunger, mood
    if happiness < 25:
        mood = "Sad"
    elif energy < 25:
        mood = "Sleepy"
    elif hunger < 25:
        mood = "Hungry"
    else:
        mood = "Happy"

def reaction(message):
    get_mood()
    print(message)
    print(f"Mochi is feeling {mood}.")  
    input("Press Enter to Continue")

def mochi_thought():
    global last_thought

    get_mood()

    if mood == "Hungry":
        thought = "Mochi: I am hungry... can you feed me?"
    elif mood == "Sleepy":
        thought = "Mochi: I am getting sleppy..."
    elif mood == "Sad":
        thought = "Mochi: I am felling a little sad..."
    else:
        thought = ""
        last_thought = ""

    if thought and thought != last_thought:
        print(thought)
        last_thought = thought

def activities():
    while True:
        check_level_up()
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

def settings_menu():
    global animations_enabled, thoughts_enabled, hunger_decay_enabled

    while True:
        os.system("clear")

        print("""
++++++++++++++++++++++++++++
          SETTINGS
++++++++++++++++++++++++++++
""")

        print(f"1> Animations    : {'ON' if animations_enabled else 'OFF'}")
        print(f"2> Thoughts      : {'ON' if thoughts_enabled else 'OFF'}")
        print(f"3> Hunger Decay  : {'ON' if hunger_decay_enabled else 'OFF'}")
        print("4> Themes")
        print("5> Back")

        choice = input("\n> ")

        if choice == "1":
            animations_enabled = not animations_enabled

        elif choice == "2":
            thoughts_enabled = not thoughts_enabled

        elif choice == "3":
            hunger_decay_enabled = not hunger_decay_enabled

        elif choice == "4":
            theme_menu()

        elif choice == "5":
            return

def show_achievements():
    os.system("clear")

    print("""
++++++++++++++++++++++++++++
        ACHIEVEMENTS
++++++++++++++++++++++++++++
""")

    print(f"1. First Meal   : {'Unlocked' if achievements['first_meal'] else 'Locked'}")
    print(f"2. First Play   : {'Unlocked' if achievements['first_play'] else 'Locked'}")
    print(f"3. First Sleep  : {'Unlocked' if achievements['first_sleep'] else 'Locked'}")
    print(f"4. First Gift   : {'Unlocked' if achievements['first_gift'] else 'Locked'}")

    print("""
++++++++++++++++++++++++++++
""")

    input("Press Enter to Continue")

def save_game():
    data = {
        "name" : name,
        "level" : level,
        "xp": xp,
        "hunger": hunger,
        "happiness": happiness,
        "energy": energy,
        "mood": mood,
        "last_update": last_update,
        "evo_stage": evo_stage,
        "theme" : theme
    }

    with open("save.json", "w") as file:
        json.dump(data, file, indent=4)

def load_memory():
    try:
        with open("memory.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return {
            "name": None,
            "hobbies": [],
            "likes": [],
            "dislikes": [],
            "favorite_topics": [],
            "facts": []
        }


def save_memory(memory):
    with open("memory.json", "w") as file:
        json.dump(memory, file, indent=4)

memory = load_memory()

memory_text = json.dumps(memory, indent=2)

def chat_mochi():
    os.system("clear")

    print("""++++++++++++++++++++++++++++
        Chat With Mochi
++++++++++++++++++++++++++++
Type "bye" to leave.
""")

    conversation = [
        {
            "role": "system",
            "content": f"""
You are Mochi, a friendly virtual cat living inside a terminal game.

You are playful, curious, affectionate, and sometimes silly.

Speak naturally like a little pet, not like an AI assistant.

Current pet stats:

Hunger: {hunger}/100
Happiness: {happiness}/100
Energy: {energy}/100
Mood: {mood}
Level: {level}

React naturally to the player's messages.

If Mochi is hungry, tired, sad, or happy, let that affect your response.

Keep responses short, usually 1-3 sentences.

Do not mention the memory system.

PLAYER MEMORY:
{json.dumps(memory, indent=2)}
"""
        }
    ]

    while True:

        message = input("You: ")

        if message.lower().strip() == "bye":
            return

        update_memory(message)

        conversation[0]["content"] = f"""
You are Mochi, a friendly virtual cat living inside a terminal game.

You are playful, curious, affectionate, and sometimes silly.

Speak naturally like a little pet, not like an AI assistant.

Current pet stats:

Hunger: {hunger}/100
Happiness: {happiness}/100
Energy: {energy}/100
Mood: {mood}
Level: {level}

React naturally to the player's messages.

If Mochi is hungry, tired, sad, or happy, let that affect your response.

Keep responses short, usually 1-3 sentences.

PLAYER MEMORY:
{json.dumps(memory, indent=2)}

Use these memories naturally.

Do not mention the memory system.
"""

        conversation.append({
            "role": "user",
            "content": message
        })

        try:
            response = client.chat.completions.create(
                model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
                messages=conversation,
                temperature=0.8,
                max_tokens=150,
                extra_body={
                    "chat_template_kwargs": {
                        "enable_thinking": False
                    }
                }
            )

            reply = response.choices[0].message.content

            print(f"Mochi: {reply}")

            conversation.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:
            print("Mochi: Uh oh... I can't think right now!")
            print(f"[AI error: {e}]")

        print()

def update_memory(message):
    global memory

    prompt = f"""
You are Mochi's memory system.

Current memory:
{json.dumps(memory, indent=2)}

The player just said:
{message}

Update the memory ONLY if the player clearly tells you something
about themselves that could be useful later.

Remember:
- name
- hobbies
- likes
- dislikes
- favorite_topics
- facts

Rules:
- Keep existing memories.
- Add new information.
- Never guess.
- Never invent.
- Never duplicate.
- Do not store temporary conversation details.
- If the player corrects an old memory, update it.

Return ONLY valid JSON in this exact format:

{{
    "name": null,
    "hobbies": [],
    "likes": [],
    "dislikes": [],
    "favorite_topics": [],
    "facts": []
}}
"""

    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=300,
            extra_body={
                "chat_template_kwargs": {
                    "enable_thinking": False
                }
            }
        )

        result = response.choices[0].message.content.strip()

        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        memory = json.loads(result)

        save_memory(memory)

    except Exception as e:
        print(f"[Memory error: {e}]")

def load_game():
    global name, level, xp, hunger, happiness, energy, mood, last_update, evo_stage, theme

    try:
        with open("save.json", "r") as file:
            data = json.load(file)

        name = data.get("name", name)
        level = data.get("level", level)
        xp = data.get("xp", xp)
        hunger = data.get("hunger", hunger)
        happiness = data.get("happiness", happiness)
        energy = data.get("energy", energy)
        mood = data.get("mood", mood)
        last_update = data.get("last_update", last_update)
        evo_stage = data.get("evo_stage", evo_stage)
        theme = data.get("theme", theme)

    except FileNotFoundError:
        pass

if os.path.exists("save.json"):
    load_game()

    elapsed_offline = time.time() - last_update

    days = int(elapsed_offline // 86400)
    hours = int((elapsed_offline % 86400) // 3600)
    minutes = int((elapsed_offline % 3600) // 60)

    print(f"""
++++++++++++++++++++++++++++
       Welcome Back!
++++++++++++++++++++++++++++

Mochi missed you! 

You were away for:
{days} days, {hours} hours, {minutes} minutes

++++++++++++++++++++++++++++
""")

    input("Press Enter to Continue")

def mochi_profile():
    os.system("clear")

    print("""
++++++++++++++++++++++++++++
        MOCHI PROFILE
++++++++++++++++++++++++++++
""")

    print(f"Name          : {name}")
    print(f"Level         : {level}")
    print(f"XP            : {xp}/100")
    print(f"Mood          : {mood}")
    print(f"Hunger        : {hunger}/100")
    print(f"Happiness     : {happiness}/100")
    print(f"Energy        : {energy}/100")
    print(f"Evolution     : Stage {evo_stage}")

    print("""
----------------------------
       ACTIVITY STATS
----------------------------
""")

    print(f"Meals         : {meals}")
    print(f"Plays         : {plays}")
    print(f"Sleeps        : {sleeps}")
    print(f"Gifts         : {gifts}")

    print("""
++++++++++++++++++++++++++++
""")

    input("Press Enter to Continue")

while True:
    current_t = time.time()
    elapsed = current_t - last_update

    check_level_up()
    os.system("clear")

    if elapsed >= 5:
      if hunger_decay_enabled:
          hunger_loss = random.randint(1,3)
          hunger = max(0, hunger - hunger_loss)

      last_update = current_t

      if thoughts_enabled:
          mochi_thought()

    get_mood()
    show_screen()
    if thoughts_enabled:
      mochi_thought()

    current_theme = get_theme()

    print(f"""
{current_theme["title"] * 28}
          Mochi
{current_theme["title"] * 28}

1{current_theme["arrow"]} Activities
2{current_theme["arrow"]} Chat with Mochi
3{current_theme["arrow"]} Achievements
4{current_theme["arrow"]} Settings
5{current_theme["arrow"]} Mochi Profile
6{current_theme["arrow"]} Quit

{current_theme["title"] * 28}
""")

    task = input("> ")

    if task == "1":
        activities()

    if task == "2":
        chat_mochi()

    if task == "3":
        show_achievements()

    if task == "4":
        settings_menu()

    if task == "5":
        mochi_profile()

    if task == "6":
        save_game()
        sys.exit()



