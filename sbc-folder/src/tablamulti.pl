multi(11, _) :- !.

multi(Cont, Fact) :-
    Cont < 11,
    Prod is Fact * Cont,
    format('~w x ~w = ~w~n', [Fact, Cont, Prod]),
    C1 is Cont + 1,
    multi(C1, Fact).

multi_list(Fact) :-
    multi(1, Fact).
