# 🏎️ Track Racing Game (Pygame)

A 2D top‐down racing game built with **Python** and **Pygame**, featuring:

* Player‐controlled car with rotation, acceleration, and friction
* Track boundary collision (bounce back)
* Finish‐line detection (reset or bounce)
* **Computer car** that follows a predefined path of waypoints
* Utility functions for image scaling and rotation

---

## 🔄 Project Structure

```
Track_Racing/
├── main.py            # Main game loop, player & computer car logic
├── utils.py           # Helper functions: resize_image, rotate_center
├── Images/
│   └── imgs/          # All image assets
│       ├── grass.jpg
│       ├── track.png
│       ├── track-border.png
│       ├── red-car.png
│       ├── purple-car.png
│       └── finish.png
└── README.md          # This file
```

---

## 🎮 How to Run

1. Install **Pygame** (if not already):

   ```bash
   pip install pygame
   ```
2. In `main.py`, ensure all image paths point to your `Images/imgs/` folder.
3. Run:

   ```bash
   python main.py
   ```

---

## 🕹️ Controls (Player)

* **W** → Accelerate forward
* **S** → Accelerate backward (reverse/brake)
* **A** → Rotate left
* **D** → Rotate right

---

## ⚙️ Current Features

1. **Player Car (`Player_Car`)**

   * Rotates left/right via `A` and `D`
   * Accelerates forward/backward via `W` and `S`
   * Friction when no key is pressed (gradual slowdown)
   * Bounces back on colliding with track border
   * Finish‐line detection:

     * If crossing from the wrong side (y‐offset = 0), bounce back
     * Otherwise (crossing from below), reset to start

2. **Computer Car (`Computer_Car`)**

   * Loads a distinct sprite (`purple‐car.png`)
   * Follows a fixed list of waypoints (`PATH`) around the track
   * Each frame:

     1. **calculate\_angle()** – computes the signed angular difference between its current facing and the vector to the next waypoint, then rotates by up to `rotating_velocity` degrees
     2. **update\_path\_point()** – when its bounding rectangle collides with the waypoint’s coordinates, increments `current_point`
     3. **move()** – moves forward by its current velocity vector (based on `angle` and `starting_vel`)
   * If it reaches the end of `PATH`, it wraps around to the first waypoint
   * Resets to its start position when it crosses the finish line

3. **Collision & Reset**

   * **Track border mask** – if either car’s sprite mask overlaps the border‐mask, that car will “bounce” (reverse)
   * **Finish line mask** – if a car overlaps the finish‐line mask at `(130,250)`:

     * Player: bounce if crossing from the front; otherwise, reset to starting position
     * Computer: always reset to its starting position

4. **Rendering**

   * Draw order each frame:

     1. Grass background
     2. Static track image
     3. Finish‐line image
     4. Track border (with its mask)
     5. Player car (rotated at its `(x,y)` and `angle`)
     6. Computer car (rotated at its `(x,y)` and `angle`)
   * Optional: `draw_points()` for the computer car can draw small circles at each waypoint (useful for debugging).

5. **Utility Functions (`utils.py`)**

   * `resize_image(image, factor)` – uniformly scales an image by `factor`
   * `rotate_center(win, image, top_left, angle)` – rotates `image` about its center and blits it onto `win` at `(top_left)`

---


## 🔄 PATH (Computer Car Waypoints)

```python
PATH = [
    (161, 105), (117, 68), (67, 100), (61, 351), (70, 477),
    (177, 595), (309, 723), (405, 706), (429, 501), (514, 462),
    (605, 536), (613, 708), (731, 717), (747, 426), (650, 365),
    (414, 353), (428, 258), (709, 254), (748, 160), (704, 73),
    (331, 75), (277, 143), (281, 330), (240, 411), (172, 360),
    (171, 280)
]
```

* These `(x,y)` coordinates trace the center‐line of your track.
* The computer car rotates toward each point in turn and moves until it “touches” that point, then proceeds to the next.

---

## 📌 Next Steps & To-Do

* **Lap Counter & Timer** – display how many laps the player has completed and elapsed time
* **Collision Between Cars** – prevent overlapping or bouncing when player and computer collide
* **User Interface** – display speed, lap count, and a “Game Over” or “Victory” screen
* **Sound Effects** – add engine sound, collision SFX, and background music
* **Main Menu & Restart** – allow starting a new race without restarting the script
* **Multiple Tracks or Difficulty Levels** – load different track layouts or increase computer car speed for harder difficulty

