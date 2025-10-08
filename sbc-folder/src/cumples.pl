cumples(persona(juan, perez), fecha(21, septiembre, 1975)).
cumples(persona(luis, caceres), fecha(30, septiembre, 1983)).
cumples(persona(alejandro, martinez), fecha(22, septiembre, 1995)).
cumples(persona(ricardo, zuleta), fecha(16, septiembre, 2001)).
cumples(persona(armando, preciado), fecha(5, septiembre, 2002)).

obtener_cumples :-
    cumples(persona(Nombre, Apellido), fecha(D, M, A)),
    format('~w ~w nace el ~w de ~w de ~w.~n',
           [Nombre, Apellido, D, M, A]).

buscar_cumple(Nombre, Apellido) :-
    cumples(persona(Nombre, Apellido), fecha(D, M, A)),
    format('~w ~w nace el ~w de ~w de ~w.~n',
           [Nombre, Apellido, D, M, A]).

