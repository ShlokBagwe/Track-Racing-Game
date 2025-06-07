```markdown
# 🏎️ Track Racing Game (Pygame)

A 2D top-down racing game built with **Python** and **Pygame**, featuring:

- **Player** car with rotation, acceleration, and friction  
- **Computer AI** car that follows a predefined waypoint path  
- **Track boundary** collision (bounce back)  
- **Finish-line** detection (reset or bounce)  
- **Main Menu** with Play, Options (placeholder), and Quit  
- **3-2-1 Countdown** before the race starts  
- Utility functions for image scaling and rotation

---

## 📁 Project Structure

```

Track\_Racing/
├── Images/imgs/         # Game assets (grass, track, border, cars, finish line)
├── main.py              # Main game loop (player & AI cars, menu, countdown)
├── utils.py             # Helper functions: resize\_image, rotate\_center
└── README.md            # Project documentation (this file)

````

---

## ▶️ Getting Started

1. **Install dependencies**:
   ```bash
   pip install pygame
````

2. **Run the game**:

   ```bash
   python main.py
   ```

3. **Navigate menus**:

   * **ENTER**: Start the race
   * **SPACE**: Options (not implemented yet)
   * **ESC**: Quit

---

## 🕹️ Controls (Player)

| Key     | Action                    |
| ------- | ------------------------- |
| **W**   | Accelerate forward        |
| **S**   | Accelerate backward/brake |
| **A**   | Rotate left               |
| **D**   | Rotate right              |
| **ESC** | Quit game / exit menu     |

---

## ⚙️ Features & Workflow

### 1. Main Menu & Countdown

* `menu_loop()` shows:

  * “Press ENTER to Play”
  * “Press SPACE for Options”
  * “Press ESC to Quit”
* On **Play**, calls `game_loop()`, which first shows a **3-2-1** countdown (`draw_signals()`), then starts the race.

### 2. Gameplay Loop (`game_loop()`)

* Runs at 60 FPS.
* Draw order:

  1. Grass background
  2. Track image
  3. Finish line
  4. Track border (collision mask)
  5. Player car
  6. Computer car (with visible waypoints for debugging)
* **Player** input moves and rotates the car.
* **Computer** car:

  1. Computes angle toward its next waypoint.
  2. Rotates up to a fixed amount per frame.
  3. Moves forward.
  4. Advances to the next waypoint when reached.

### 3. Collision & Finish Line

* `collide(mask, x, y)` uses Pygame masks for pixel-perfect detection.
* On **track border collision**, cars bounce back.
* On **finish line**:

  * Player bounces if crossing from the wrong side, else resets start position.
  * Computer always resets to its start position and path.

### 4. Utilities (`utils.py`)

* `resize_image(image, factor)`: scales an image.
* `rotate_center(win, image, topleft, angle)`: rotates about center and blits.

---

## 📌 Next Steps

* Implement the **Options** submenu.
* Add a **lap counter** and **timer** display.
* Add **sound effects** and **background music**.
* Create a **Game Over/Victory** screen with restart.

---

## 📄 License & Credits

* Inspired by [Tech With Tim’s Pygame Car Racer](https://github.com/techwithtim/Pygame-Car-Racer).
* Assets and code are for learning and demonstration.

````

