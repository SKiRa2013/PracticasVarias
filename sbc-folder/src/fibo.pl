fibonacci(0, 0).
fibonacci(1, 1).

fibonacci(Pos, Fibo) :-
    Pos > 1,
    Aux1 is Pos-1,
    Aux2 is Pos-2,
    fibonacci(Aux1, F1),
    fibonacci(Aux2, F2),
    Fibo is F1 + F2.

fibonacci_list(Length, Lista) :-
    findall(F, (between(0, Length, Fibos), fibonacci(Fibos, F)), Lista).
