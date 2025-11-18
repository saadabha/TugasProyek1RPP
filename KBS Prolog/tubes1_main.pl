% MAIN LOADER FILE
% for Dota 2 Knowledge-Based System

:- include('abox_dota2.pl').
:- include('tbox_dota2.pl').
:- include('kbsrules_dota2.pl').

:- initialization(main).

main :-
    write('Dota 2 Knowledge Base loaded successfully!'), nl.