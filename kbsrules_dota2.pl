% KLASIFIKASI Hard Carry
% Definisi: Kita mengklasifikasikan seorang hero sebagai 'Hard Carry'
% jika dia memiliki role 'Carry' DAN atribut utamanya adalah 'Agility'.
% (Contoh: Anti-Mage, Phantom Assassin)
is_hard_carry(Hero) :-
    hero(Hero),             % Pastikan itu adalah hero (dari ABox)
    is_carry(Hero),         % Cek apakah dia 'Carry' (dari TBox)
    is_agility_hero(Hero).  % Cek apakah dia 'Agility Hero' (dari TBox)

% KLASIFIKASI Magic Nuker
% Definisi: Kita mengklasifikasikan hero sebagai 'Magic Nuker'
% jika dia memiliki role 'Nuker' DAN memiliki setidaknya satu
% ability yang menghasilkan damage 'Magical' DAN ability itu BUKAN 'Passive'.
% (Contoh: Zeus, Lina)
is_magic_nuker(Hero) :-
    hero(Hero),
    is_nuker(Hero),                 % Cek role 'Nuker' (dari TBox)
    has_ability(Hero, Ability),     % Temukan ability yang dia miliki (dari ABox)
    damage_type(Ability, magical),  % Cek apakah damage-nya 'Magical' (dari ABox)
    ability_type(Ability, Tipe),    % Cek tipe ability-nya (dari ABox)
    Tipe \= passive.                % \= artinya 'tidak sama dengan'

% KLASIFIKASI Tank Murni (Pure Tank)
% Definisi: Hero yang atributnya 'Strength' DAN punya role 'Durable'.
% (Contoh: Axe, Centaur Warrunner)
is_pure_tank(Hero) :-
    hero(Hero),
    is_strength_hero(Hero),         % Cek TBox
    is_durable(Hero).               % Cek TBox

% KLASIFIKASI Glass Cannon
% Definisi: Hero yang role-nya 'Nuker' ATAU 'Carry',
% TAPI dia BUKAN 'Durable'.
% (Contoh: Sniper, Zeus)
is_glass_cannon(Hero) :-
    hero(Hero),
    (is_nuker(Hero) ; is_carry(Hero)),
    \+ is_durable(Hero).              

% KLASIFIKASI Utility Support
% Definisi: Hero yang role-nya 'Support' DAN juga 'Disabler'.
% (Contoh: Lion, Shadow Shaman)
is_utility_support(Hero) :-
    hero(Hero),
    is_support(Hero),
    is_disabler(Hero).

% KLASIFIKASI Teamfight Controller
% Definisi: Hero 'Initiator' yang memiliki setidaknya satu
% ability dengan tipe 'Area of Effect' (AoE).
% (Contoh: Tidehunter, Magnus, Enigma)
is_teamfight_controller(Hero) :-
    hero(Hero),
    is_initiator(Hero),
    has_aoe_ability(Hero).      % Cek TBox baru

% KLASIFIKASI Ganker
% Definisi: Hero yang merupakan 'Disabler' dan 'Nuker', tapi BUKAN 'Carry'.
% Peran utamanya adalah membunuh hero musuh secara tiba-tiba, bukan farming.
% (Contoh: Nyx Assassin, Spirit Breaker, Pudge)
is_ganker(Hero) :-
    hero(Hero),
    is_disabler(Hero),
    is_nuker(Hero),
    \+ is_carry(Hero).           % Negasi untuk menyaring carry

% KLASIFIKASI Elusive Escape Artist
% Definisi: Hero dengan role 'Escape', tetapi BUKAN 'Durable'.
% Mereka sangat lincah dan sulit ditangkap, tapi rapuh.
% (Contoh: Puck, Weaver, Slark)
is_elusive_escape_artist(Hero) :-
    hero(Hero),
    is_escape(Hero),
    \+ is_durable(Hero).         % Bukan tipe tank

% KLASIFIKASI Right-Click Carry
% Definisi: Hero 'Carry' yang memiliki setidaknya satu ability 'Passive'.
% Ini mengindikasikan mereka mengandalkan serangan dasar yang diperkuat skill pasif.
% (Contoh: Juggernaut, Phantom Assassin, Sniper)
is_right_click_carry(Hero) :-
    hero(Hero),
    is_carry(Hero),
    has_passive_ability(Hero).  % Cek TBox baru

% KLASIFIKASI Pure Damage Specialist
% Definisi: Hero yang memiliki setidaknya satu ability (non-passive)
% yang menghasilkan damage tipe 'Pure'.
% (Contoh: Axe (Culling Blade), Bane (Brain Sap), Queen of Pain (Sonic Wave))
is_pure_damage_specialist(Hero) :-
    hero(Hero),
    has_pure_damage_ability(Hero). % Cek TBox baru

% KLASIFIKASI Annoying Split Pusher
% Definisi: Hero yang memiliki role 'Pusher' DAN 'Escape'.
% Mereka bisa menghancurkan tower dengan cepat lalu kabur.
% (Contoh: Broodmother, Nature's Prophet)
is_split_pusher(Hero) :-
    hero(Hero),
    is_pusher(Hero),
    is_escape(Hero).