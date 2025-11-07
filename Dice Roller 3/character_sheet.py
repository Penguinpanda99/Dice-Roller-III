import json

class Charactersheet:
    def __init__(self, held_weapons, proficiency_bonus, ability_scores, proficient_skills, proficient_tools, proficient_weapons=None):
        self.held_weapons = held_weapons
        self.proficiency_bonus = proficiency_bonus
        self.ability_scores = ability_scores
        self.proficient_skills = proficient_skills
        self.proficient_tools = proficient_tools
        self.proficient_weapons = proficient_weapons if proficient_weapons is not None else []

    @classmethod
    def from_json(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return cls(**data)

    def to_json(self, filename):
        data = {
            'held_weapons': self.held_weapons,
            'proficiency_bonus': self.proficiency_bonus,
            'ability_scores': self.ability_scores,
            'proficient_skills': self.proficient_skills,
            'proficient_tools': self.proficient_tools,
            'proficient_weapons': self.proficient_weapons
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
