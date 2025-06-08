```markdown
# 🏎️ Track Racing Game (Pygame)

A 2D top-down racing game built with **Python** and **Pygame**, featuring:

- **Player** car with rotation, acceleration, and friction  
- **Computer AI** car that follows a predefined waypoint path  
- **Track boundary** collision (bounce back) for both cars  
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
  6. Computer car
* **Player** input moves and rotates the car.
* **Computer** car:

  1. Computes angle toward its next waypoint.
  2. Rotates up to a fixed amount per frame.
  3. Moves forward.
  4. Advances to the next waypoint when reached.

### 3. Collision & Finish Line

* **Track border collision** now applies to **both** cars:

  * If either car’s mask overlaps the track-border mask, that car bounces back.
* **Finish line** detection:

  * Player bounces or resets depending on crossing direction.
  * Computer always resets its position and waypoint index.

### 4. Computer Path-Following (Custom Feature)

* Defined a custom `PATH` of (x, y) waypoints tracing the track’s center.
* The AI car:

  1. **`calculate_angle()`**: smooth steering toward current waypoint.
  2. **`update_path_point()`**: increments waypoint when the car reaches it.
  3. **`move_computer_car()`**: calls the above and then moves the car each frame.
* When the path index reaches the end, it wraps back to the start.

### 5. Utilities (`utils.py`)

* `resize_image(image, factor)`: scales an image by a given multiplier.
* `rotate_center(win, image, topleft, angle)`: rotates an image about its center and blits to the window.

---

## 🔄 PATH (Computer Car Waypoints)

```python
PATH = [
  (170,110), (65,90), (70,481), (318,731), (404,680),
  (418,521), (518,465), (600,535), (613,715), (730,710),
  (734,399), (611,357), (415,343), (425,257), (695,245),
  (710,95), (320,45), (275,150), (280,380), (176,388),
  (178,280)
]
```

* Traces the center of the track; AI car follows these in a loop.

---

## 📌 Next Steps

* Implement the **Options** submenu.
* Add **sound effects** and **background music**.
* Create a **Game Over/Victory** screen with restart.

---

## 📄 License & Credits

* Inspired by [Tech With Tim’s Pygame Car Racer](https://github.com/techwithtim/Pygame-Car-Racer).
* Custom AI path-following and dual-car collision are original enhancements.

```
