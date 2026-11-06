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
Clone the repository:  
`git clone https://github.com/Vitrehac/SignalLost.git`  
`cd SignalLost`

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


SignalLost/  
├── entities/  
|   └── player.py  
├── levels/  
|   ├── maps/  
|   |   ├── level1.txt  
|   |   ├── level2.txt  
|   |   └── level3.txt  
|   └── tilemap.py  
├── puzzles/  
|   ├── keypad_puzzle.py  
|   └── power_puzzle.py       
├── systems/  
|   ├── camera.py  
|   ├── collision.py  
|   ├── game_state.py  
|   └── objectives.py  
├── ui/  
|   ├── ending_screen.py  
|   └── log_viewer.py  
└── main.py  

## Development & AI Usage
SignalLost was developed to practice Python and learn game development (pygame) and was built as part of my Hack Club's Phantom participation.  
AI was used during development for explanations and sometimes debugging. Development mostly involved manually writing the code and testing game functionality.

