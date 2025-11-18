import json
import os
from owlready2 import *

def create_ontology_structure(onto):
    """
    Defines the entire class hierarchy (TBox), object properties, and data properties
    for the Dota 2 ontology based on the agreed-upon blueprint.
    """
    with onto:
        # 1. CLASS HIERARCHY (TBOX)
        class Dota2Entity(Thing): pass

        class Agent(Dota2Entity): pass
        class GameItem(Dota2Entity): pass
        class AbilityConcept(Dota2Entity): pass
        class GameMechanic(Dota2Entity): pass
        class Structure(Dota2Entity): pass

        class Hero(Agent): pass
        class NonHeroUnit(Agent): pass

        class StrengthHero(Hero): pass
        class AgilityHero(Hero): pass
        class IntelligenceHero(Hero): pass
        class UniversalHero(Hero): pass
        AllDisjoint([StrengthHero, AgilityHero, IntelligenceHero, UniversalHero])

        class Creep(NonHeroUnit): pass
        class SummonedUnit(NonHeroUnit): pass
        class Roshan(NonHeroUnit): pass
        class LaneCreep(Creep): pass
        class NeutralCreep(Creep): pass

        class Item(GameItem): pass
        class ComponentItem(Item): pass
        class CraftedItem(Item): pass
        class ConsumableItem(Item): pass
        class NeutralItem(Item): pass

        class Ability(AbilityConcept): pass
        class BasicAbility(Ability): pass
        class UltimateAbility(Ability): pass
        class Talent(AbilityConcept): pass
        class Facet(AbilityConcept): pass

        class Role(GameMechanic): pass
        class Attribute(GameMechanic): pass
        class PrimaryAttribute(Attribute): pass
        class AttackType(GameMechanic): pass
        class DamageType(GameMechanic): pass
        class Behavior(GameMechanic): pass

        class Building(Structure): pass
        class Fountain(Structure): pass
        class Tower(Building): pass
        class Barracks(Building): pass
        class Ancient(Building): pass
        class Effigy(Building): pass

        # 2. DATA PROPERTIES
        class displayName(DataProperty): range = [str]
        class description(DataProperty): range = [str]
        class imageURL(DataProperty): range = [str]

        class health(DataProperty): domain = [Agent, Structure]; range = [int]
        class mana(DataProperty): domain = [Agent]; range = [int]
        class healthRegen(DataProperty): domain = [Agent, Structure]; range = [float]
        class manaRegen(DataProperty): domain = [Agent]; range = [float]
        class armor(DataProperty): domain = [Agent, Structure]; range = [int]
        class magicResistance(DataProperty): domain = [Agent]; range = [int]
        class movementSpeed(DataProperty): domain = [Agent]; range = [int]
        class experienceBounty(DataProperty): domain = [NonHeroUnit, Structure]; range = [int]

        class localizedName(DataProperty): domain = [Hero]; range = [str]
        class baseMinAttackDamage(DataProperty): domain = [Hero]; range = [int]
        class baseMaxAttackDamage(DataProperty): domain = [Hero]; range = [int]
        class attackRange(DataProperty): domain = [Hero, Structure]; range = [int]
        class attackRate(DataProperty): domain = [Hero, Structure]; range = [float]
        class strengthGain(DataProperty): domain = [Hero]; range = [float]
        class agilityGain(DataProperty): domain = [Hero]; range = [float]
        class intelligenceGain(DataProperty): domain = [Hero]; range = [float]
        class dayVision(DataProperty): domain = [Hero]; range = [int]
        class nightVision(DataProperty): domain = [Hero]; range = [int]

        class cooldown(DataProperty): domain = [AbilityConcept]; range = [float]
        class manaCost(DataProperty): domain = [AbilityConcept]; range = [int]
        class requiredLevel(DataProperty): domain = [Talent]; range = [int]
        class facetTitle(DataProperty): domain = [Facet]; range = [str]
        class facetDescription(DataProperty): domain = [Facet]; range = [str]
        class facetColor(DataProperty): domain = [Facet]; range = [str]

        class cost(DataProperty): domain = [Item]; range = [int]
        class lore(DataProperty): domain = [Item]; range = [str]
        class notes(DataProperty): domain = [Item]; range = [str]
        class tier(DataProperty): domain = [NeutralItem]; range = [int]

        class goldBounty(DataProperty): domain = [Structure]; range = [int]
        class structureTier(DataProperty): domain = [Tower]; range = [int]
        class trueSightRadius(DataProperty): domain = [Tower, Fountain]; range = [int]

        class goldBountyMin(DataProperty): domain = [Creep]; range = [int]
        class goldBountyMax(DataProperty): domain = [Creep]; range = [int]
        class spawnLocation(DataProperty): domain = [NonHeroUnit]; range = [str]

        # 3. OBJECT PROPERTIES
        class hasAbility(ObjectProperty): domain = [Hero]; range = [AbilityConcept]
        class hasTalent(ObjectProperty): domain = [Hero]; range = [Talent]
        class hasFacet(ObjectProperty): domain = [Hero]; range = [Facet]
        class hasRole(ObjectProperty): domain = [Hero]; range = [Role]
        class hasPrimaryAttribute(ObjectProperty): domain = [Hero]; range = [PrimaryAttribute]
        class hasAttackType(ObjectProperty): domain = [Hero]; range = [AttackType]
        class hasBehavior(ObjectProperty): domain = [AbilityConcept, Item]; range = [Behavior]
        class hasDamageType(ObjectProperty): domain = [AbilityConcept]; range = [DamageType]
        class grantsAbility(ObjectProperty): domain = [Item, Facet]; range = [Ability]
        class targetsTeam(ObjectProperty): domain = [Ability]; range = [str]
        class requiresComponent(ObjectProperty): domain = [CraftedItem]; range = [Item]
        class buildsInto(ObjectProperty): inverse_property = requiresComponent
        class counters(ObjectProperty): domain = [Hero]; range = [Hero]
        class synergizesWith(ObjectProperty): domain = [Hero]; range = [Hero]


def populate_from_json(onto, heroes_data, hero_abilities_data, items_data, abilities_data):
    """
    Populates the ontology with individuals (ABox) from the loaded JSON data.
    """
    with onto:
        print("Populating Heroes...")
        created_concepts = set()

        for hero_id, hero_info in heroes_data.items():
            hero_name = hero_info['name']

            primary_attr = hero_info.get('primary_attr')
            hero_class = onto.Hero
            if primary_attr == 'str': hero_class = onto.StrengthHero
            elif primary_attr == 'agi': hero_class = onto.AgilityHero
            elif primary_attr == 'int': hero_class = onto.IntelligenceHero
            elif primary_attr == 'all': hero_class = onto.UniversalHero

            hero = hero_class(hero_name)
            hero.localizedName.append(hero_info['localized_name'])
            if 'img' in hero_info:
                hero.imageURL.append(f"https://api.opendota.com{hero_info['img']}")

            prop_map = {
                "health": "base_health", "healthRegen": "base_health_regen",
                "mana": "base_mana", "manaRegen": "base_mana_regen",
                "armor": "base_armor", "magicResistance": "base_mr",
                "baseMinAttackDamage": "base_attack_min", "baseMaxAttackDamage": "base_attack_max",
                "strengthGain": "str_gain", "agilityGain": "agi_gain", "intelligenceGain": "int_gain",
                "attackRange": "attack_range", "attackRate": "attack_rate",
                "movementSpeed": "move_speed", "dayVision": "day_vision", "nightVision": "night_vision"
            }
            for prop_name, json_key in prop_map.items():
                if json_key in hero_info and hero_info[json_key] is not None:
                    getattr(hero, prop_name).append(hero_info[json_key])

            for role_name in hero_info.get('roles', []):
                hero.hasRole.append(onto.Role(role_name.replace(" ", "_")))

            attr_map = {'str': 'Strength', 'agi': 'Agility', 'int': 'Intelligence', 'all': 'Universal'}
            if primary_attr in attr_map:
                hero.hasPrimaryAttribute.append(onto.PrimaryAttribute(attr_map[primary_attr]))

            if hero_info.get('attack_type'):
                hero.hasAttackType.append(onto.AttackType(hero_info['attack_type'].replace(" ", "_")))

            if hero_name in hero_abilities_data:
                hero_specifics = hero_abilities_data[hero_name]
                for idx, ability_name in enumerate(hero_specifics.get('abilities', [])):
                    if ability_name not in ["generic_hidden", "dota_base_ability"]:
                        if idx <= 3: ability_ind = onto.BasicAbility(ability_name)
                        elif idx == 5: ability_ind = onto.UltimateAbility(ability_name)
                        else: ability_ind = onto.Ability(ability_name)
                        created_concepts.add(ability_name)
                        hero.hasAbility.append(ability_ind)

                for talent_info in hero_specifics.get('talents', []):
                    talent_ind = onto.Talent(talent_info['name']); created_concepts.add(talent_info['name'])
                    if 'level' in talent_info: talent_ind.requiredLevel.append(talent_info['level'])
                    hero.hasTalent.append(talent_ind)

                for facet_info in hero_specifics.get('facets', []):
                    facet_ind = onto.Facet(facet_info['name']); created_concepts.add(facet_info['name'])
                    facet_ind.facetTitle.append(facet_info['title'])
                    facet_ind.facetDescription.append(facet_info['description'])
                    facet_ind.facetColor.append(facet_info['color'])
                    hero.hasFacet.append(facet_ind)

        print("Populating Items...")
        for item_key, item_info in items_data.items():
            item_class = onto.Item
            if 'tier' in item_info and item_info['tier']: item_class = onto.NeutralItem
            item = item_class(item_key)
            if 'dname' in item_info: item.displayName.append(item_info['dname'])
            if item_info.get('created', False): item.is_a.append(onto.CraftedItem)
            if 'component' in item_info.get('qual', ''): item.is_a.append(onto.ComponentItem)
            if 'consumable' in item_info.get('qual', ''): item.is_a.append(onto.ConsumableItem)
            if 'tier' in item_info and item_info['tier']: item.tier.append(item_info['tier'])

            prop_map = {"cost": "cost", "lore": "lore", "notes": "notes"}
            for prop, key in prop_map.items():
                if key in item_info and item_info[key]: getattr(item, prop).append(item_info[key])
            if 'img' in item_info: item.imageURL.append(f"https://api.opendota.com{item_info['img']}")
            if item_info.get('cd') and isinstance(item_info['cd'], (int, float)): item.cooldown.append(item_info['cd'])

            if item_info.get('components'):
                for component_key in item_info['components']:
                    if component_key: item.requiresComponent.append(onto.Item(component_key))

            behaviors = item_info.get('behavior')
            if isinstance(behaviors, str): behaviors = [behaviors]
            if isinstance(behaviors, list):
                for behavior_name in behaviors:
                    item.hasBehavior.append(onto.Behavior(behavior_name.replace(" ", "_")))

        print("Populating Abilities...")
        for ability_key, ability_info in abilities_data.items():
            if ability_key not in ["dota_base_ability", "dota_empty_ability", "special_bonus_attributes", "generic_hidden"]:
                ability = onto.search_one(iri=f"*{ability_key}") or onto.Ability(ability_key)

                if 'dname' in ability_info and ability_info['dname']: ability.displayName.append(ability_info['dname'])
                if 'img' in ability_info: ability.imageURL.append(f"https://api.opendota.com{ability_info['img']}")
                if 'desc' in ability_info: ability.description.append(ability_info['desc'])
                if 'dmg_type' in ability_info and ability_info['dmg_type']:
                    ability.hasDamageType.append(onto.DamageType(ability_info['dmg_type']))

                try:
                    if 'mc' in ability_info and ability_info['mc']: ability.manaCost.append(int(ability_info['mc']))
                    if 'cd' in ability_info and ability_info['cd']: ability.cooldown.append(float(ability_info['cd']))
                except (ValueError, TypeError): pass

                behaviors = ability_info.get('behavior')
                if isinstance(behaviors, str): behaviors = [behaviors]
                if isinstance(behaviors, list):
                    for behavior_name in behaviors:
                        ability.hasBehavior.append(onto.Behavior(behavior_name.replace(" ", "_")))


def populate_non_hero_units(onto):
    """
    Populates the ontology with static data for non-hero units.
    """
    print("Populating Non-Hero Units...")
    with onto:
        # Roshan
        roshan = onto.Roshan("roshan_boss")
        roshan.displayName.append("Roshan")
        roshan.health.append(7500)
        roshan.armor.append(20)
        roshan.movementSpeed.append(270)
        roshan.experienceBounty.append(225)
        roshan.spawnLocation.append("Roshan Pit")

        # Lane Creeps
        creep_data = [
            ("radiant_melee_creep", onto.LaneCreep, "Radiant Melee Creep", 550, 0, 325, 40, 18, 23, "Radiant Lanes"),
            ("radiant_ranged_creep", onto.LaneCreep, "Radiant Ranged Creep", 300, 0, 325, 60, 28, 33, "Radiant Lanes"),
            ("dire_melee_creep", onto.LaneCreep, "Dire Melee Creep", 550, 0, 325, 40, 18, 23, "Dire Lanes"),
            ("dire_ranged_creep", onto.LaneCreep, "Dire Ranged Creep", 300, 0, 325, 60, 28, 33, "Dire Lanes")
        ]
        for name, cls, dname, hp, arm, ms, exp, gmin, gmax, loc in creep_data:
            c = cls(name)
            c.displayName.append(dname)
            c.health.append(hp)
            c.armor.append(arm)
            c.movementSpeed.append(ms)
            c.experienceBounty.append(exp)
            c.goldBountyMin.append(gmin)
            c.goldBountyMax.append(gmax)
            c.spawnLocation.append(loc)

        # Neutral Creeps (Sample)
        neutrals = [
            ("kobold_soldier", "Kobold Soldier", 300, 0, 315, 22, 14, 17, "Small Neutral Camp"),
            ("satyr_mindstealer", "Satyr Mindstealer", 600, 0, 300, 42, 22, 26, "Medium Neutral Camp"),
            ("centaur_conqueror", "Centaur Conqueror", 950, 2, 325, 62, 58, 68, "Large Neutral Camp"),
            ("ancient_black_dragon", "Ancient Black Dragon", 2000, 4, 300, 180, 77, 91, "Ancient Neutral Camp")
        ]
        for name, dname, hp, arm, ms, exp, gmin, gmax, loc in neutrals:
            n = onto.NeutralCreep(name)
            n.displayName.append(dname)
            n.health.append(hp)
            n.armor.append(arm)
            n.movementSpeed.append(ms)
            n.experienceBounty.append(exp)
            n.goldBountyMin.append(gmin)
            n.goldBountyMax.append(gmax)
            n.spawnLocation.append(loc)

def populate_structures(onto):
    """
    Populates the ontology with static data for structures.
    """
    print("Populating Structures...")
    with onto:
        # Towers
        tower_data = [
            # Tier, Health, Armor, Dmg, Range, Gold, Exp
            (1, 1800, 12, 100, 700, 125, 0),
            (2, 2000, 14, 120, 700, 150, 0),
            (3, 2000, 14, 120, 700, 175, 0),
            (4, 2000, 20, 150, 700, 200, 0)
        ]
        for faction in ["radiant", "dire"]:
            for tier, hp, arm, dmg, rng, gold, exp in tower_data:
                t = onto.Tower(f"{faction}_tier_{tier}_tower")
                t.displayName.append(f"{faction.capitalize()} Tier {tier} Tower")
                t.health.append(hp)
                t.armor.append(arm)
                t.attackRate.append(1.0)
                t.attackRange.append(rng)
                t.structureTier.append(tier)
                t.goldBounty.append(gold)
                t.experienceBounty.append(exp)
                t.trueSightRadius.append(700)

        # Barracks
        for faction in ["radiant", "dire"]:
            for btype in ["melee", "ranged"]:
                b = onto.Barracks(f"{faction}_{btype}_barracks")
                b.displayName.append(f"{faction.capitalize()} {btype.capitalize()} Barracks")
                b.health.append(2200 if btype == "Melee" else 1300)
                b.armor.append(12)
                b.healthRegen.append(5.0)
                b.goldBounty.append(150)

        # Ancients
        rad_ancient = onto.Ancient("radiant_ancient")
        rad_ancient.displayName.append("Radiant Ancient")
        rad_ancient.health.append(4250)
        rad_ancient.armor.append(18)
        rad_ancient.healthRegen.append(12.0)

        dire_ancient = onto.Ancient("dire_ancient")
        dire_ancient.displayName.append("Dire Ancient")
        dire_ancient.health.append(4250)
        dire_ancient.armor.append(18)
        dire_ancient.healthRegen.append(12.0)

        # Fountains
        rad_fountain = onto.Fountain("radiant_fountain")
        rad_fountain.displayName.append("Radiant Fountain")
        rad_fountain.health.append(200000)
        rad_fountain.armor.append(200)
        rad_fountain.attackRange.append(1200)
        rad_fountain.trueSightRadius.append(1200)

        dire_fountain = onto.Fountain("dire_fountain")
        dire_fountain.displayName.append("Dire Fountain")
        dire_fountain.health.append(200000)
        dire_fountain.armor.append(200)
        dire_fountain.attackRange.append(1200)
        dire_fountain.trueSightRadius.append(1200)


if __name__ == '__main__':
    HEROES_FILE = 'heroes.json'
    HERO_ABILITIES_FILE = 'hero_abilities.json'
    ITEMS_FILE = 'items.json'
    ABILITIES_FILE = 'abilities.json'
    OUTPUT_ONTOLOGY_FILE = 'dota2_ontology.owl'

    required_files = [HEROES_FILE, HERO_ABILITIES_FILE, ITEMS_FILE, ABILITIES_FILE]
    if not all(os.path.exists(f) for f in required_files):
        print("Error: One or more required JSON files are not found.")
        print(f"Please ensure {', '.join(required_files)} are present in the same directory as the script.")
        exit()

    onto = get_ontology("http://www.semanticweb.org/dota2-ontology#")

    create_ontology_structure(onto)
    print("Structure created.")

    print("\nStep 2: Loading JSON data...")
    try:
        with open(HEROES_FILE, 'r', encoding='utf-8') as f: heroes_data = json.load(f)
        with open(HERO_ABILITIES_FILE, 'r', encoding='utf-8') as f: hero_abilities_data = json.load(f)
        with open(ITEMS_FILE, 'r', encoding='utf-8') as f: items_data = json.load(f)
        with open(ABILITIES_FILE, 'r', encoding='utf-8') as f: abilities_data = json.load(f)
        print("JSON data loaded successfully.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit()

    print("\nStep 3: Populating ontology with data...")
    populate_from_json(onto, heroes_data, hero_abilities_data, items_data, abilities_data)
    populate_non_hero_units(onto)
    populate_structures(onto)
    print("Population complete.")

    print(f"\nStep 4: Saving ontology to '{OUTPUT_ONTOLOGY_FILE}'...")
    onto.save(file=OUTPUT_ONTOLOGY_FILE, format="rdfxml")
    print("Ontology saved successfully.")
    print(f"\nYou can now open the '{OUTPUT_ONTOLOGY_FILE}' file in Protégé.")
