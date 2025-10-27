% Profesión

carrera(Persona, Profesion).
% carrera(julian, ingeniero_sistemas).
% carrera(jairo, artesano).
% carrera(pedro, ingeniero_electronico).

% Nacionalidad

nacionalidad(Persona, Nacionalidad).
% nacionalidad(juan, colombia).
% nacionalidad(julian, colombia).
% nacionalidad(richard, eeuu).

% Reglas de guardado y cargado

save(Path, Pred, Facts) :-
    tell(Path), 
    write_facts(Pred, Facts),
    told, !.

write_facts(_, []) :- !.
write_facts(Pred, [Fact | Rest] ) :-
    write(Pred), write("("), write(Fact), write(")."), nl,
    write_facts(Pred, Rest).


% Reglas:
tipo_trabajo(Persona) :-
    carrera(Persona, Aux_Carrera),
    Aux_Carrera = ingeniero_sistemas,
    nacionalidad(Persona, Aux_Nacionalidad),
    Aux_Nacionalidad = eeuu,
    format("El salario de ~w es bueno.~n", [Persona]),
    asserta(salario(Persona, bueno)), !;
    
    carrera(Persona, Aux_Carrera),
    Aux_Carrera = ingeniero_sistemas,
    nacionalidad(Persona, Aux_Nacionalidad),
    Aux_Nacionalidad = colombia,
    format("El salario de ~w es regular.~n", [Persona]),
    asserta(salario(Persona, regular)), !;

    format("No puedo opinar sobre el salario de ~w", [Persona]), !.

empleado(Persona) :-
    tipo_trabajo(Persona), !.

guardar_hechos :-
    findall((Persona, Carrera), carrera(Persona, Carrera), ListCarrera),
    findall((Persona, Nacionalidad), nacionalidad(Persona, Nacionalidad), ListNacionalidad),
    save('./src/backup/profesiones.txt', carrera, ListCarrera),
    save('./src/backup/nacionalidades.txt', nacionalidad, ListNacionalidad), !.
    