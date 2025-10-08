factorial(2, 2).

factorial(Num, Fact) :-
    Num > 2,
    Aux1 is Num-1,
    factorial(Aux1, FAux),
    Fact is Num * FAux.
