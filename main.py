import streamlit as st
import json
import random
import math
from character_sheet import Charactersheet
from io import StringIO

# Constants
DICE_LIST = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100']
SKILL_LIST = {
    'Athletics': 'Strength', 'Acrobatics': 'Dexterity', 'Stealth': 'Dexterity', 
    'Sleight of Hand': 'Dexterity', 'Arcana': 'Intelligence', 'History': 'Intelligence', 
    'Investigation': 'Intelligence', 'Nature': 'Intelligence', 'Religion': 'Intelligence', 
    'Animal Handling': 'Wisdom', 'Insight': 'Wisdom', 'Medicine': 'Wisdom', 
    'Perception': 'Wisdom', 'Survival': 'Wisdom', 'Deception': 'Charisma', 
    'Intimidation': 'Charisma', 'Performance': 'Charisma', 'Persuasion': 'Charisma'
}
WEAPON_DATABASE = {
'battleaxe'      : {'damage_dice': '1d8',  'attack_type': 'melee',  'gov_proficiency': 'Martial', 'versatile': '1d10'},
'club'           : {'damage_dice': '1d4',  'attack_type': 'melee',  'gov_proficiency': 'Simple'},
'dagger'         : {'damage_dice': '1d4',  'attack_type': 'melee',  'gov_proficiency': 'Simple', 'finesse': True},
'flail'          : {'damage_dice': '1d8',  'attack_type': 'melee',  'gov_proficiency': 'Martial'},
'glaive'         : {'damage_dice': '1d10', 'attack_type': 'melee',  'gov_proficiency': 'Martial'},
'greataxe'       : {'damage_dice': '1d12', 'attack_type': 'melee',  'gov_proficiency': 'Martial'},
'greatclub'      : {'damage_dice': '1d8',  'attack_type': 'melee',  'gov_proficiency': 'Simple'},
'greatsword'     : {'damage_dice': '2d6',  'attack_type': 'melee',  'gov_proficiency': 'Martial'},
'halberd'        : {'damage_dice': '1d10', 'attack_type': 'melee',  'gov_proficiency': 'Martial'},
'handaxe'        : {'damage_dice': '1d6',  'attack_type': 'melee',  'gov_proficiency': 'Simple'},
'javelin'        : {'damage_dice': '1d6',  'attack_type': 'melee',  'gov_proficiency': 'Simple'},
'lance'          : {'damage_dice': '1d12', 'attack_type': 'melee',  'gov_proficiency': 'Martial'},
'light hammer'   : {'damage_dice': '1d4',  'attack_type': 'melee',  'gov_proficiency': 'Simple'},
'longsword'      : {'damage_dice': '1d8',  'attack_type': 'melee',  'gov_proficiency': 'Martial', 'versatile': '1d10'},
'mace'           : {'damage_dice': '1d6',  'attack_type': 'melee',  'gov_proficiency': 'Simple'},
'maul'           : {'damage_dice': '2d6',  'attack_type': 'melee',  'gov_proficiency': 'Martial'},
'morningstar'    : {'damage_dice': '1d8',  'attack_type': 'melee',  'gov_proficiency': 'Martial'},
'pike'           : {'damage_dice': '1d10', 'attack_type': 'melee',  'gov_proficiency': 'Martial'},
'quarterstaff'   : {'damage_dice': '1d6',  'attack_type': 'melee',  'gov_proficiency': 'Simple', 'versatile': '1d8'},
'rapier'         : {'damage_dice': '1d8',  'attack_type': 'melee',  'gov_proficiency': 'Martial', 'finesse': True},
'scimitar'       : {'damage_dice': '1d6',  'attack_type': 'melee',  'gov_proficiency': 'Martial', 'finesse': True},
'shortsword'     : {'damage_dice': '1d6',  'attack_type': 'melee',  'gov_proficiency': 'Martial', 'finesse': True},
'sickle'         : {'damage_dice': '1d4',  'attack_type': 'melee',  'gov_proficiency': 'Simple'},
'spear'          : {'damage_dice': '1d6',  'attack_type': 'melee',  'gov_proficiency': 'Simple', 'versatile': '1d8'},
'trident'        : {'damage_dice': '1d6',  'attack_type': 'melee',  'gov_proficiency': 'Martial', 'versatile': '1d8'},
'war pick'       : {'damage_dice': '1d8',  'attack_type': 'melee',  'gov_proficiency': 'Martial'},
'warhammer'      : {'damage_dice': '1d8',  'attack_type': 'melee',  'gov_proficiency': 'Martial', 'versatile': '1d10'},
'whip'           : {'damage_dice': '1d4',  'attack_type': 'melee',  'gov_proficiency': 'Martial', 'finesse': True},
'blowgun'        : {'damage_dice': '1',    'attack_type': 'ranged', 'gov_proficiency': 'Martial'},
'light crossbow' : {'damage_dice': '1d8',  'attack_type': 'ranged', 'gov_proficiency': 'Simple'},
'dart'           : {'damage_dice': '1d4',  'attack_type': 'ranged', 'gov_proficiency': 'Simple', 'finesse': True},
'shortbow'       : {'damage_dice': '1d6',  'attack_type': 'ranged', 'gov_proficiency': 'Simple'},
'sling'          : {'damage_dice': '1d4',  'attack_type': 'ranged', 'gov_proficiency': 'Simple'},
'hand crossbow'  : {'damage_dice': '1d6',  'attack_type': 'ranged', 'gov_proficiency': 'Martial'},
'heavy crossbow' : {'damage_dice': '1d10', 'attack_type': 'ranged', 'gov_proficiency': 'Martial'},
'longbow'        : {'damage_dice': '1d8',  'attack_type': 'ranged', 'gov_proficiency': 'Martial'}
}
# Page configuration
st.set_page_config(page_title="D&D Roller III", page_icon="🎲", layout="wide")
def st_centered():
    _, col, _ = st.columns([1, 2, 1])
    return col
# Custom CSS for styling
st.markdown("""
    <style>
* {
    font-family: 'Bookman Old Style', 'Georgia', serif !important;
    }
        
    /* Buttons */
    .stButton>button {
        background-color: #121212;
        border: 4px ridge #737272;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Text inputs */
    .stTextInput>div>div>input {
        background-color: #121212;
        border: 5px ridge #737272;
    }
    
    /* Select boxes */
    .stSelectbox>div>div>div {
        background-color: #121212;
        border: 4px ridge #737272;
            padding: 5px;
    }

    /* Multiselect */
    .stMultiSelect>div>div>div {
        background-color: #121212;
        border: 4px ridge #737272;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        text-align: center;
    }
    
    /* Regular text */
    p, span, div {
        color: #C9C9C9;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background-color: #121212;
        color: white;
        border: 4px ridge #737272;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #432f23;
    }
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'character_sheet' not in st.session_state:
        st.session_state.character_sheet = None
    if 'character_name' not in st.session_state:
        st.session_state.character_name = "Demo Character"
    if 'character_level' not in st.session_state:
        st.session_state.character_level = "5"
    if 'result_text' not in st.session_state:
        st.session_state.result_text = "Ready to Roll!"
    if 'character_loaded' not in st.session_state:
        st.session_state.character_loaded = False
    if 'show_creation_form' not in st.session_state:
        st.session_state.show_creation_form = False

def calculate_ability_modifiers(ability_scores):
    """Calculate ability modifiers from scores"""
    def attribute_to_modifier(score):
        if score < 1:
            return 0
        elif score > 30:
            return 10
        else:
            return (score - 10) // 2
    
    return {ability: attribute_to_modifier(score) 
            for ability, score in ability_scores.items()}
    
def parse_character_filename(filename):
    """Parse character name and level from filename"""
    name_part = filename[:-5] if filename.endswith('.json') else filename
    if ' lvl ' in name_part:
        name, level = name_part.split(' lvl ')
        return name, level
    else:
        return name_part, "?"

def create_demo_character():
    """Create a demo character for testing"""
    return Charactersheet(
        ability_scores={
            'Strength': 16,
            'Dexterity': 14,
            'Constitution': 14,
            'Intelligence': 10,
            'Wisdom': 12,
            'Charisma': 8
        },
        proficiency_bonus=3,
        proficient_skills=['Athletics', 'Intimidation', 'Perception'],
        proficient_tools=['Simple'],
        held_weapons=['longsword', 'shortbow', 'dagger'],
        proficient_weapons = ['longsword']
        )

def character_to_json_string(character):
    """Convert character to JSON string for download"""
    data = {
        'held_weapons': character.held_weapons,
        'proficiency_bonus': character.proficiency_bonus,
        'ability_scores': character.ability_scores,
        'proficient_skills': character.proficient_skills,
        'proficient_tools': character.proficient_tools,
        'proficient_weapons': getattr(character, 'proficient_weapons', [])
    }
    return json.dumps(data, indent=2)

def perform_dice_roll(dice_type, multiplier):
    """Perform a dice roll and return result text"""
    dice_sides = int(dice_type[1:])
    dice_results = [random.randint(1, dice_sides) for _ in range(multiplier)]
    total_result = sum(dice_results)
    
    if multiplier == 1 and dice_sides == 20:
        roll = dice_results[0]
        if roll == 20:
            return f'Rolling a {dice_type}...\n\nyou rolled {roll}!\n\nCRITICAL SUCCESS!'
        elif roll == 1:
            return f'Rolling a {dice_type}...\n\nyou rolled {roll}!\n\nCRITICAL FAILURE!'
        else:
            return f'Rolling a {dice_type}...\n\nyou rolled {roll}!'
    else:
        extra = ""
        if all(r == dice_sides for r in dice_results):
            extra = "\n\nALL CRIT SUCCESS!"
        elif all(r == 1 for r in dice_results):
            extra = "\n\nALL CRIT FAILURE!"
        return f'Rolling {multiplier} {dice_type}...\n\nyou rolled {dice_results}\n\ntotal: {total_result}!{extra}'

def perform_skill_check(skill, character_sheet, ability_modifiers):
    """Perform a skill check and return result text"""
    ability_modifier = ability_modifiers[SKILL_LIST[skill]]
    proficiency_bonus = character_sheet.proficiency_bonus
    skill_proficiency = proficiency_bonus if skill in character_sheet.proficient_skills else 0
    skill_check_roll = random.randint(1, 20)
    total_skill_bonus = skill_proficiency + ability_modifier
    total_skill_roll = skill_check_roll + total_skill_bonus
    
    if total_skill_bonus != 0:
        base_text = f"Rolling {skill}...\n\nRoll: {skill_check_roll} + {total_skill_bonus} Total: {total_skill_roll}!"
    else:
        base_text = f"Rolling {skill}...\n\nyou got {total_skill_roll}!"
    
    if skill_check_roll == 20:
        return f"{base_text}\n\nCRITICAL SUCCESS!"
    elif skill_check_roll == 1:
        return f"{base_text}\n\nCRITICAL FAILURE!"
    else:
        return base_text

def perform_weapon_attack(weapon, character_sheet, ability_modifiers, use_finesse, use_versatile):
    """Perform weapon attack and damage roll"""
    weapon_data = WEAPON_DATABASE[weapon]
    
    # Determine ability to use
    if 'finesse' in weapon_data and weapon_data['finesse'] and use_finesse:
        selected_ability = 'Dexterity'
    elif weapon_data['attack_type'] == 'melee':
        selected_ability = 'Strength'
    else:
        selected_ability = 'Dexterity'
    
    ability_modifier = ability_modifiers[selected_ability]
    
    # Determine damage dice
    if 'versatile' in weapon_data and use_versatile:
        damage_dice = weapon_data['versatile']
    else:
        damage_dice = weapon_data['damage_dice']
    
    # Check proficiency
    weapon_proficiency = weapon_data['gov_proficiency']
    prof_weapons = getattr(character_sheet, 'proficient_weapons', [])
    prof_tools = getattr(character_sheet, 'proficient_tools', [])
    proficient = (weapon in prof_weapons) or (weapon_proficiency in prof_tools)
    proficiency_bonus = character_sheet.proficiency_bonus if proficient else 0
    total_bonus = ability_modifier + proficiency_bonus
    
    # Roll attack
    attack_die = random.randint(1, 20)
    attack_total = attack_die + total_bonus
    
    if attack_die == 20:
        attack_result_text = f"Attack Roll: {attack_die} + {total_bonus} = {attack_total}! \n\nCRITICAL HIT!"
    elif attack_die == 1:
        attack_result_text = f"Attack Roll: {attack_die} + {total_bonus} = {attack_total}! \n\nCRITICAL FAILURE!"
    else:
        attack_result_text = f"Attack Roll: {attack_die} + {total_bonus} = {attack_total}!"
    
    # Roll damage
    if isinstance(damage_dice, str) and 'd' in damage_dice:
        damage_dice_count, damage_dice_sides = map(int, damage_dice.split('d'))
        num_rolls = damage_dice_count * 2 if attack_die == 20 else damage_dice_count
        damage_rolls = [random.randint(1, damage_dice_sides) for _ in range(num_rolls)]
        total_damage = sum(damage_rolls) + ability_modifier
        return (f"Rolling {weapon} with {selected_ability}...\n\n"
                f"{attack_result_text}\n\n"
                f"Damage Rolls: {damage_rolls} + {ability_modifier} = {total_damage}!")
    else:
        # flat damage (e.g. '1' for blowgun)
        try:
            flat = int(damage_dice)
        except Exception:
            flat = 0
        total_damage = flat
        return (f"Rolling {weapon} with {selected_ability}...\n\n"
                f"{attack_result_text}\n\n"
                f"Damage = {total_damage}")

def validate_and_create_character(data):
    """
    Validate uploaded JSON dict and return (True, Charactersheet) or (False, error_message).
    """

    import json

    # Required top-level keys (proficient_weapons is optional)
    required_keys = ['held_weapons', 'proficiency_bonus', 'ability_scores',
                     'proficient_skills', 'proficient_tools']

    missing = [k for k in required_keys if k not in data]
    if missing:
        return False, f"Missing keys: {', '.join(missing)}"

    # Validate ability_scores
    abilities = data.get('ability_scores', {})
    expected = {'Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'}
    if not isinstance(abilities, dict) or not expected.issubset(set(abilities.keys())):
        return False, "ability_scores must be a dict containing keys: " + ", ".join(sorted(expected))
    for k, v in abilities.items():
        if not isinstance(v, int) or not (1 <= v <= 30):
            return False, f"Invalid ability score for {k}: must be int 1-30"

    # Validate proficiency bonus
    pb = data.get('proficiency_bonus')
    if not isinstance(pb, int):
        return False, "proficiency_bonus must be an integer"

    # Validate list fields
    for list_key in ('held_weapons', 'proficient_skills', 'proficient_tools'):
        if not isinstance(data.get(list_key, []), list):
            return False, f"{list_key} must be a list"

    # Optional individual weapon proficiencies
    prof_weapons = data.get('proficient_weapons', [])
    if not isinstance(prof_weapons, list):
        return False, "proficient_weapons must be a list if present"

    # Safe defaults
    held_weapons = data.get('held_weapons', [])
    prof_skills = data.get('proficient_skills', [])
    prof_tools = data.get('proficient_tools', [])

    # Create Charactersheet (constructor accepts proficient_weapons optional)
    try:
        char = Charactersheet(
            held_weapons=held_weapons,
            proficiency_bonus=pb,
            ability_scores=abilities,
            proficient_skills=prof_skills,
            proficient_tools=prof_tools,
            proficient_weapons=prof_weapons
        )
    except Exception as e:
        return False, f"Failed to create character object: {e}"

    return True, char

# Main app
init_session_state()

st.title("D&D Roller III")

# Character selection / loading
if not st.session_state.character_loaded:
    
    # Check if we should show creation form
    if st.session_state.show_creation_form:
        st.header("Create New Character")
        
        # Character Name and Level
        col1, col2 = st_centered().columns([3, 1])
        with col1:
            char_name = st.text_input("Character Name", value="", placeholder="Enter character name")
        with col2:
            char_level = st.number_input("Level", min_value=1, max_value=20, value=1)
        
        st_centered().markdown("---")
        
        # Ability Scores
        st.subheader("Ability Scores (1-30)")
        col1, col2, col3 = st_centered().columns(3)
        with col1:
            strength = st.number_input("Strength", min_value=1, max_value=30, value=10)
            dexterity = st.number_input("Dexterity", min_value=1, max_value=30, value=10)
        with col2:
            constitution = st.number_input("Constitution", min_value=1, max_value=30, value=10)
            intelligence = st.number_input("Intelligence", min_value=1, max_value=30, value=10)
        with col3:
            wisdom = st.number_input("Wisdom", min_value=1, max_value=30, value=10)
            charisma = st.number_input("Charisma", min_value=1, max_value=30, value=10)
        
        st_centered().markdown("---")
        
        # Proficiency Bonus
        col1, col2 = st_centered().columns([1,2])
        with col1:
            prof_bonus = math.ceil(char_level / 4) + 1
            st.markdown("####")
            st.subheader(f"Proficiency Bonus")
            with st.container(border=True, width=52):
                st.markdown(f"+{prof_bonus}")
            
        
        with col2:
            st.subheader("Weapon Proficiency")
            weapon_prof_simple = st_centered().checkbox("Simple Weapons", value=False)
            weapon_prof_martial = st_centered().checkbox("Martial Weapons", value=False)
                # Add individual weapon selection
            st.write("**And/Or select individual weapons**")

            # Build available weapon list excluding those covered by checked categories
            weapon_options = sorted(WEAPON_DATABASE.keys())
            excluded = set()
            if weapon_prof_simple:
                excluded |= {w for w, v in WEAPON_DATABASE.items() if v.get('gov_proficiency') == 'Simple'}
            if weapon_prof_martial:
                excluded |= {w for w, v in WEAPON_DATABASE.items() if v.get('gov_proficiency') == 'Martial'}
            available_options = [w for w in weapon_options if w not in excluded]

            # Keep session state consistent and retroactively remove now-excluded weapons
            if "individual_prof" not in st.session_state:
                st.session_state.individual_prof = []
            st.session_state.individual_prof = [w for w in st.session_state.individual_prof if w in available_options]

            individual_weapons = st.multiselect(
                "Proficient Weapons",
                options=available_options,
                key="individual_prof")
        st_centered().markdown("---")
        
        # Proficient Skills
        st.subheader("Proficient Skills")
        skills_list = ['Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception', 
                       'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine', 
                       'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion', 
                       'Sleight of Hand', 'Stealth', 'Survival']
        
        # Display skills in 3 columns
        col1, col2, col3 = st_centered().columns(3)
        selected_skills = []
        for i, skill in enumerate(skills_list):
            with [col1, col2, col3][i % 3]:
                if st.checkbox(skill, key=f"skill_{skill}"):
                    selected_skills.append(skill)
        
        st_centered().markdown("---")
        
        # Held Weapons
        st.subheader("Held Weapons (Select up to 6)")
        weapon_list = sorted(WEAPON_DATABASE.keys())
        selected_weapons = st_centered().multiselect(
            "Select Weapons",
            options=weapon_list,
            default=[],
            max_selections=6
        )

        
        st_centered().markdown("---")
        
        # Action buttons
        col1, col2 = st_centered().columns(2)
        with col1:
            if st.button("Create Character", use_container_width=True):
                if not char_name:
                    st.error("Please enter a character name!")
                elif not selected_weapons:
                    st.error("Please select at least one weapon!")
                else:
                    # Build proficient tools list
                    proficient_tools = []
                    if weapon_prof_simple:
                        proficient_tools.append('Simple')
                    if weapon_prof_martial:
                        proficient_tools.append('Martial')
                    
                    # Create character
                    new_char = Charactersheet(
                        ability_scores={
                            'Strength': strength,
                            'Dexterity': dexterity,
                            'Constitution': constitution,
                            'Intelligence': intelligence,
                            'Wisdom': wisdom,
                            'Charisma': charisma
                        },
                        proficiency_bonus=prof_bonus,
                        proficient_skills=selected_skills,
                        proficient_tools=proficient_tools,
                        held_weapons=selected_weapons
                    )
                    # attach individual weapon proficiencies (safe even if ctor doesn't take it)
                    new_char.proficient_weapons = individual_weapons
                    # Load the character (no file saving)
                    st.session_state.character_sheet = new_char
                    st.session_state.character_name = char_name
                    st.session_state.character_level = str(char_level)
                    st.session_state.character_loaded = True
                    st.session_state.show_creation_form = False
                    st.success(f"Character '{char_name}' created! Don't forget to download it.")
                    st.rerun()
        
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_creation_form = False
                st.rerun()
    
    else:
        # Main character selection screen
        st.header("Character Selection")
        
        st_centered().info("Upload an existing character file, use the demo, or create a new one.")
        
        # Upload character file
        st.subheader("📤 Upload Character")
        uploaded_file = st_centered().file_uploader("Upload a character sheet JSON file", type=['json'])
        if uploaded_file is not None:
            try:
                raw = uploaded_file.getvalue().decode("utf-8")
                data = json.loads(raw)
            except Exception:
                st.error("Uploaded file is not valid JSON.")
            else:
                ok, result = validate_and_create_character(data)
                if not ok:
                    st.error(result)
                else:
                    uploaded_char = result
                    # parse filename for name/level if helper exists, otherwise default
                    upload_filename = uploaded_file.name
                    try:
                        name, level = parse_character_filename(upload_filename)
                    except Exception:
                        name, level = ("Uploaded Character", "1")

                    st.session_state.character_sheet = uploaded_char
                    st.session_state.character_name = name
                    st.session_state.character_level = level
                    st.session_state.character_loaded = True

                    st.success(f"Loaded {name} (Level {level})!")
                    st.rerun()

        st_centered().markdown("---")
        
        col1, col2 = st_centered().columns(2)
        
        with col1:
            if st.button("🎲 Use Demo Character", use_container_width=True):
                st.session_state.character_sheet = create_demo_character()
                st.session_state.character_name = "Demo Fighter"
                st.session_state.character_level = "5"
                st.session_state.character_loaded = True
                st.rerun()
        
        with col2:
            if st.button("✨ Create New Character", use_container_width=True):
                st.session_state.show_creation_form = True
                st.rerun()
    

else:
    # Main interface - character is loaded
    char = st.session_state.character_sheet
    ability_mods = calculate_ability_modifiers(char.ability_scores)
    
    with st.sidebar:
        st.header(f"{st.session_state.character_name}")
        st.subheader(f"Level {st.session_state.character_level}")
        
        st.markdown("---")
        st.subheader("Ability Scores")
        for ability, score in char.ability_scores.items():
            mod = ability_mods[ability]
            st.write(f"**{ability}:** {score} ({mod:+d})")
        
        st.markdown("---")
        st.subheader("Proficiencies")
        st.write(f"*Proficiency Bonus:* +{char.proficiency_bonus}")
        st.write("*Skills:*")
        st.write(", ".join(char.proficient_skills))
        st.write("*Weapons types:*")
        st.write(", ".join(char.proficient_tools))
        st.write("*Individual Weapons:*")
        prof_weapons = getattr(char, 'proficient_weapons', [])
        if prof_weapons:
            st.write(", ".join(prof_weapons))
        else:
            st.write("*None*")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"### {st.session_state.character_name}")
    with col3:
        # Download button
        char_json = character_to_json_string(char)
        download_filename = f"{st.session_state.character_name} lvl {st.session_state.character_level}.json"
        st.download_button(
            label="Download Character",
            data=char_json,
            file_name=download_filename,
            mime="application/json",
            width=131,
        )
    
    # Result display area
    st.markdown(f"""
    <div style='
            background-color: #432f23;
            border: 8px ridge #737272;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            text-align: center;
            width: 800px;
            margin-left: auto;
            margin-right: auto;
            '>
        <pre style='color: #cd1c10; font-family: "Bookman Old Style", "Georgia", serif; 
                    font-size: 16px; margin: 0;'>{st.session_state.result_text}</pre>
    </div>
    """, unsafe_allow_html=True)
    
    # Three column layout for main functions (+ spacing)
    col1, col2, col3, col4, col5 = st.columns([10,6,7,6,10])
    
    # SKILL CHECK COLUMN
    with col2:
        st.markdown("### Skill Check")
        selected_skill = st.selectbox("Select Skill", list(SKILL_LIST.keys()), key="skill_select")
        if st.button("Roll Skill Check", key="skill_button", use_container_width=True):
            st.session_state.result_text = perform_skill_check(selected_skill, char, ability_mods)
            st.rerun()
    
    # WEAPON ATTACK COLUMN
    with col3:
        st.markdown("### Weapon Attack")
        selected_weapon = st.selectbox("Select Weapon", char.held_weapons, key="weapon_select")
        
        weapon_data = WEAPON_DATABASE.get(selected_weapon, {})
        
        # Check weapon properties and only show relevant checkboxes
        has_finesse = 'finesse' in weapon_data and weapon_data.get('finesse', False)
        has_versatile = 'versatile' in weapon_data and weapon_data.get('versatile')
        
        use_finesse = False
        use_versatile = False
        
        if has_finesse:
            use_finesse = st.checkbox("Use Finesse (DEX)", key="finesse_check")
        if has_versatile:
            use_versatile = st.checkbox("Use Versatile", key="versatile_check")
        
        if st.button("Roll Weapon Attack", key="weapon_button", use_container_width=True):
            st.session_state.result_text = perform_weapon_attack(
                selected_weapon, char, ability_mods, use_finesse, use_versatile
            )
            st.rerun()
    
    # DICE ROLL COLUMN
    with col4:
        st.markdown("### Dice Roll")
        selected_dice = st.selectbox("Select Dice", DICE_LIST, key="dice_select", index=5)  # Default to d20
        multiplier = st.selectbox("Number of Dice", list(range(1, 11)), key="multi_select")
        if st.button("Roll Dice", key="dice_button", use_container_width=True):
            st.session_state.result_text = perform_dice_roll(selected_dice, multiplier)
            st.rerun()
    
    # Back button
    st.markdown("#")
    if st.button("← Back to Character Selection"):
        st.session_state.character_loaded = False
        st.session_state.character_name = "Demo Character"
        st.session_state.character_level = "5"
        st.session_state.result_text = "Ready to Roll!"
        st.rerun()