# D&D Roller III

A web-based dice rolling assistant for D&D 5e built with Streamlit. This is a modernized version of my original Python/Tkinter desktop application, redesigned for browser-based use.

## Features

- **Dice Rolling**: Roll any standard D&D dice (d4, d6, d8, d10, d12, d20, d100) with multipliers
- **Skill Checks**: Automated skill checks with proficiency bonuses and ability modifiers
- **Weapon Attacks**: Calculate attack rolls and damage with support for finesse and versatile weapons
- **Character Management**: Create, save, and load character sheets (JSON format)
- **Complete Weapon Database**: All standard D&D 5e weapons included

## Live Demo

[Link to your deployed app - add after deployment]

## Screenshots

[Add 2-3 screenshots here after deployment]

## Tech Stack

- **Python 3.x**
- **Streamlit** - Web framework
- **JSON** - Character data storage

## Running Locally

1. Clone the repository:
```bash
git clone [your-repo-url]
cd dnd-roller-web
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## Usage

1. **Create a Character**: Click "Create New Character" and fill in stats
2. **Download**: Save your character as a JSON file
3. **Roll Dice**: Select dice type and quantity, then roll
4. **Make Skill Checks**: Choose a skill and roll with automatic modifiers
5. **Attack**: Select a weapon and roll attack + damage

## Character Sheet Format

Characters are stored as JSON files with this structure:
```json
{
  "ability_scores": { "Strength": 16, ... },
  "proficiency_bonus": 3,
  "proficient_skills": ["Athletics", "Perception"],
  "proficient_tools": ["Martial", "Simple"],
  "held_weapons": ["longsword", "shortbow"]
}
```

## Project Evolution

This is Version 2 of my D&D Roller project:
- **V1**: Desktop application using Python + Tkinter
- **V2**: Web application using Python + Streamlit (this version)

Key improvements in V2:
- Browser-based accessibility (no installation needed)
- Modern UI with custom styling
- Upload/download character management
- Responsive design

## Future Enhancements

- [ ] Spell slot tracking
- [ ] Hit point management
- [ ] Initiative tracker
- [ ] Multi-character party management

## License

[Choose a license - MIT is common for portfolio projects]

## Contact

[Your name]
- Portfolio: [link]
- LinkedIn: [link]

- Email: [email]
