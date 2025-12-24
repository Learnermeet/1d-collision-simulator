# 1D Collision Simulator (Pygame)

A simple and interactive **1D physics collision simulator** built using **Python** and **Pygame**.  
This project demonstrates **elastic collisions** between two objects with customizable mass and velocity.

---

## 🚀 Features

- 🔹 Real‑time simulation of elastic collisions in one dimension
- 🔹 Customizable:
  - Mass of both objects
  - Initial velocities
- 🔹 Collision reaction with walls
- 🔹 Simple interactive UI using Pygame
- 🔹 Plays sound effects on collisions

---

## 📦 Requirements

Make sure you have the following installed:

- Python **3.8+**
- Pygame

---

## 🛠️ Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Learnermeet/1d-collision-simulator.git
    cd 1d-collision-simulator
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the simulator:**

    ```bash
    python main.py
    ```

---

## 🎮 Usage

When the simulation starts:

1. **Enter mass and velocity** for both objects via the input interface.
2. Press **Start/Run** to begin the simulation.
3. Watch how the objects collide and change velocities according to one‑dimensional elastic collision physics.
4. Use the **UI controls** (if provided) to pause/reset.

---

## 🧠 How It Works (Physics Overview)

This simulator uses **1D elastic collision equations**:

For two bodies with:
- masses: `m₁`, `m₂`
- initial velocities: `u₁`, `u₂`
- final velocities: `v₁`, `v₂`

The final velocities after collision are:

```text
v₁ = ((m₁ - m₂) / (m₁ + m₂)) * u₁ + (2 * m₂ / (m₁ + m₂)) * u₂
v₂ = (2 * m₁ / (m₁ + m₂)) * u₁ + ((m₂ - m₁) / (m₁ + m₂)) * u₂
