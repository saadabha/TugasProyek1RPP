% Hero berdasarkan Atribut Utama.
is_agility_hero(Hero) :-
    primary_attribute(Hero, agility).

is_intelligence_hero(Hero) :-
    primary_attribute(Hero, intelligence).

is_strength_hero(Hero) :-
    primary_attribute(Hero, strength).

is_universal_hero(Hero) :-
    primary_attribute(Hero, universal).

% Tipe Hero berdasarkan Role
% Aturan untuk memeriksa apakah hero memiliki role tertentu.
is_carry(Hero) :-
    has_role(Hero, carry).

is_support(Hero) :-
    has_role(Hero, support).

is_nuker(Hero) :-
    has_role(Hero, nuker).

is_escape(Hero) :-
    has_role(Hero, escape).

is_disabler(Hero) :-
    has_role(Hero, disabler).

is_durable(Hero) :-
    has_role(Hero, durable).

is_initiator(Hero) :-
    has_role(Hero, initiator).

is_pusher(Hero) :-
    has_role(Hero, pusher).

% Hero by Attack Type
is_melee_hero(Hero) :-
    attack_type(Hero, melee).

is_ranged_hero(Hero) :-
    attack_type(Hero, ranged).

% Aturan untuk memeriksa properti ability yang dimiliki hero.
% Ini adalah building block untuk aturan KBS yang lebih kompleks.

% Apakah hero punya setidaknya satu ability tipe 'passive'?
has_passive_ability(Hero) :-
    has_ability(Hero, Ability),
    ability_type(Ability, passive).

% Apakah hero punya setidaknya satu ability tipe 'aoe' (Area of Effect)?
has_aoe_ability(Hero) :-
    has_ability(Hero, Ability),
    ability_type(Ability, aoe).

% Apakah hero punya setidaknya satu ability (non-passive) yang
% menghasilkan damage tipe 'pure'?
has_pure_damage_ability(Hero) :-
    has_ability(Hero, Ability),
    damage_type(Ability, pure),
    ability_type(Ability, Type),
    Type \= passive.

% Apakah hero punya setidaknya satu ability tipe 'channeled'?
has_channeled_ability(Hero) :-
    has_ability(Hero, Ability),
    ability_type(Ability, channeled).