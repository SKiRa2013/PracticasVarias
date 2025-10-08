potencia(_, 0, 1) :- !.

potencia(Base, Exp, Power) :-
    Exp > 0,
    E1 is Exp-1,
    potencia(Base, E1, PAcum),
    Power is PAcum * Base, !.
