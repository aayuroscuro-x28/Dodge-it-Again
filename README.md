# Dodge Fall

A cute arcade game built with Python and Pygame.

Guide a cartoon cat along a seaside beach while dodging falling sushi and wine obstacles.

## Features

- **Ocean-side background** with sky, waves, and sand
- **Cartoon cat player** with animated eyes and body
- **Sushi obstacles** for normal blocks
- **Wine obstacles** for fast blocks
- **Cherry blossom power-ups** that randomly grant one of three effects
  - `Shield` — immune to obstacles for a short time
  - `Speed` — obstacles fall faster
  - `Slow` — obstacles fall much slower for easy dodging

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

## Controls

- **Left / A** — move left
- **Right / D** — move right
- **Esc** — quit

## Gameplay

- Avoid falling sushi and wine
- Collect cherry blossom power-ups to gain temporary advantages
- The score increases over time and with dodged obstacles
- Try to beat your high score!
