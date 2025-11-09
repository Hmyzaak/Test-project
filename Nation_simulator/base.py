from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DefinitionOption:
    value_name: str
    trait: Trait
    trait_weight: int
    description: str
    env_flexibility: int
    stability: int
    economy: int
    cultural_influence: int
    historical_dynamics: int
    militarization: int

@dataclass
class DefinitionCategory:
    name: str
    options: List[DefinitionOption]

# Slovník pro všechny kategorie
definition_categories: Dict[str, DefinitionCategory] = {}