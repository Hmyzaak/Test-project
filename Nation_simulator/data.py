from enum import Enum
from base import DefinitionOption, DefinitionCategory, definition_categories

class Trait(str, Enum):
    """Enum for traits that can be assigned to a nation."""
    HIERARCHICAL = "Hierarchický"
    COLLECTIVIST = "Kolektivistický"
    INDIVIDUALIST = "Individualistický"
    SPIRITUAL = "Spirituální-mystický"
    MATERIALIST = "Materialistický-pragmatický"
    ISOLATIONIST = "Izolacionistický-xenofobní"
    ADAPTIVE = "Adaptivní-synkretický"
    TRADITIONAL = "Tradiční-konzervativní"
    EXPANSIVE = "Expanzivní"
    ECO_SETTLED = "Ekologicky vázaný-usedlý"
    NOMADIC = "Nomádský-mobilní"
    TECHNOCRATIC = "Technokratický"

class StateType(str, Enum):
    """Enum for different types of states."""
    MULTICULTURAL = "Multikulturní"
    NATIONAL = "Národnostní"
    PROTECTORATE = "Protektorát"
    FRAGMENTED = "Decentralizované ministáty"

class Trend(str, Enum):
    """Enum for mood trends that can be assigned to a nation."""



# 1. Struktura autority
definition_categories["Struktura autority"] = DefinitionCategory(
    name="Struktura autority",
    options=[
        DefinitionOption(
            value_name="Despotie",
            trait= HIERARCHICAL,
            trait_weight=1,
            description="Panovník nebo centrální kasta s absolutní mocí",
            env_flex=0,
            stability=5,
            economy=4,
            cultural_influence=1,
            historic_dynamics=1,
            militarization=5
        ),
        DefinitionOption(
            value_name="Rada rovnosti",
            trait= COLLECTIVIST,
            trait_weight=1,
            description="Rovnostářské rady nebo kruhy s kolektivním rozhodováním",
            env_flex=1,
            stability=4,
            economy=3,
            cultural_influence=3,
            historic_dynamics=2,
            militarization=3
        ),
        DefinitionOption(
            value_name="Volné klany",
            trait= INDIVIDUALIST,
            trait_weight=1,
            description="Volné klany či samostatné domácnosti bez vyšší moci",
            env_flex=2,
            stability=1,
            economy=1,
            cultural_influence=4,
            historic_dynamics=4,
            militarization=1
        )
    ]
)

# 2. Způsob výběru vůdců / správy
definition_categories["Způsob výběru vůdců / správy"] = DefinitionCategory(
    name="Způsob výběru vůdců / správy",
    options=[
        DefinitionOption(
            value_name="Vyvolení",
            trait= SPIRITUAL,
            trait_weight=2,
            description="Zrození, znamení či osvícení jako důkaz vůdcovství",
            env_flex=1,
            stability=3,
            economy=1,
            cultural_influence=4,
            historic_dynamics=3,
            militarization=1
        ),
        DefinitionOption(
            value_name="Meritokracie",
            trait= MATERIALIST,
            trait_weight=2,
            description="Volba na základě odbornosti, schopností nebo soutěže",
            env_flex=2,
            stability=4,
            economy=4,
            cultural_influence=2,
            historic_dynamics=3,
            militarization=3
        ),
        DefinitionOption(
            value_name="Dědičnost",
            trait= TRADITIONAL,
            trait_weight=2,
            description="Uzavřený výběr uvnitř tradice nebo rodu",
            env_flex=0,
            stability=4,
            economy=2,
            cultural_influence=1,
            historic_dynamics=1,
            militarization=1
        )
    ]
)

# 3. Společenské hodnoty
definition_categories["Společenské hodnoty"] = DefinitionCategory(
    name="Společenské hodnoty",
    options=[
        DefinitionOption(
            value_name="Efektivita",
            trait= TECHNOCRATIC,
            trait_weight=2,
            description="Přesnost, efektivita a inovace",
            env_flex=1,
            stability=4,
            economy=5,
            cultural_influence=3,
            historic_dynamics=4,
            militarization=1
        ),
        DefinitionOption(
            value_name="Uctění předků",
            trait= TRADITIONAL,
            trait_weight=2,
            description="Spojení s předky, úcta k tradici a rituálům",
            env_flex=0,
            stability=4,
            economy=2,
            cultural_influence=1,
            historic_dynamics=1,
            militarization=1
        ),
        DefinitionOption(
            value_name="Osobní svoboda",
            trait= INDIVIDUALIST,
            trait_weight=2,
            description="Osobní svoboda, odvaha, samostatnost",
            env_flex=2,
            stability=1,
            economy=3,
            cultural_influence=4,
            historic_dynamics=4,
            militarization=3
        )
    ]
)

