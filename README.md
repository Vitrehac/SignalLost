# SignalLost
You spawn inside a research facility that has lost power. Explore the facility, restore power, decode corrupted messages, and uncover the truth behind the blackout.

## Gameplay
The game is a short, story driven experience featuring 3 connected levels.
1. Power restoration: Solve a circuit rotation puzzle to reactivate the facility.
2. Security access: Investigate computer logs, discover a hidden access code, and unlock restricted areas
3. Containment sector: Navigate through dangerous security lasers and disable the emergency defense system.

## Controls
**Move** `W / S / A / D / Arrows`  
**Interact with objects:** `E`  
**Rotate circuit tiles:** `Mouse buttons`  
**Enter keypad codes:** `Number keys`  
**Delete keypad input:** `Backspace`  
**Submit keypad code:** `Enter`  
**Close puzzles / ending screen:** `Esc`  

## Installation
Download the latest Windows version from:  
```text  
[(https://github.com/Vitrehac/SignalLost/releases/latest)]
```

Install Pygame:  
`python -m pip install pygame`

Run the game:  
`python main.py`

## Technologies
- Python
- Pygame
- Git & GitHub
- Google Fonts

## Project structure

```text
|-- .gitignore
|-- assets
|   |-- fonts
|   |-- sounds
|   |-- sprites
|-- data
|-- entities
|   |-- player.py
|-- levels
|   |-- level.py
|   |-- maps
|   |   |-- level1.txt
|   |   |-- level2.txt
|   |   |-- level3.txt
|   |-- tilemap.py
|-- main.py
|-- Plus_Jakarta_Sans
|   |-- OFL.txt
|   |-- PlusJakartaSans-Italic-VariableFont_wght.ttf
|   |-- PlusJakartaSans-VariableFont_wght.ttf
|   |-- README.txt
|   |-- static
|   |   |-- PlusJakartaSans-Bold.ttf
|   |   |-- PlusJakartaSans-BoldItalic.ttf
|   |   |-- PlusJakartaSans-ExtraBold.ttf
|   |   |-- PlusJakartaSans-ExtraBoldItalic.ttf
|   |   |-- PlusJakartaSans-ExtraLight.ttf
|   |   |-- PlusJakartaSans-ExtraLightItalic.ttf
|   |   |-- PlusJakartaSans-Italic.ttf
|   |   |-- PlusJakartaSans-Light.ttf
|   |   |-- PlusJakartaSans-LightItalic.ttf
|   |   |-- PlusJakartaSans-Medium.ttf
|   |   |-- PlusJakartaSans-MediumItalic.ttf
|   |   |-- PlusJakartaSans-Regular.ttf
|   |   |-- PlusJakartaSans-SemiBold.ttf
|   |   |-- PlusJakartaSans-SemiBoldItalic.ttf
|-- puzzles
|   |-- __init__.py
|   |-- keypad_puzzle.py
|   |-- power_puzzle.py
|-- README.md
|-- requirements.txt
|-- settings.py
|-- systems
|   |-- camera.py
|   |-- collision.py
|   |-- game_state.py
|   |-- objectives.py
|-- ui
|   |-- ending_screen.py
|   |-- log_viewer.py
```

## Development & AI Usage
SignalLost was developed to practice Python and learn game development (pygame) and was built as part of my Hack Club's Phantom participation.  
AI was used during development for explanations and sometimes debugging. Development mostly involved manually writing the code and testing game functionality.

