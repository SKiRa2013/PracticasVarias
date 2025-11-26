% Comentados los bloques que se requieren para que el programa funcione en Visual Prolog 5.x
/*
DOMAINS
    animal = string
    caracteristica = string

PREDICATES
*/
    % Reglas de deducción
    :- dynamic mamifero/1.
    :- dynamic ave/1.
    :- dynamic carnivoro/1.
    :- dynamic herbivoro/1.
    :- dynamic ungulado/1.
    
    % Animales específicos
    :- dynamic pinguino/1.
    :- dynamic avestruz/1.
    :- dynamic cebra/1.
    :- dynamic jirafa/1.
    :- dynamic leopardo/1.
    :- dynamic tigre/1.
    
    % Hechos básicos
    :- dynamic tiene_pelo/1.
    :- dynamic da_leche/1.
    :- dynamic tiene_plumas/1.
    :- dynamic pone_huevos/1.
    :- dynamic vuela/1.
    :- dynamic come_carne/1.
    :- dynamic tiene_ojos_adelante/1.
    :- dynamic tiene_dientes_agudos/1.
    :- dynamic tiene_garras/1.
    :- dynamic rumia/1.
    :- dynamic tiene_pesuna/1.
    :- dynamic tiene_cuello_largo/1.
    :- dynamic nada/1.
    :- dynamic es_negro_blanco/1.
    :- dynamic tiene_franjas_negras/1.
    :- dynamic es_color_leonado/1.
    :- dynamic tiene_pintas_negras/1.
/*  
    % Sistema de inferencia
    identificar_animal(animal)
    mostrar_resultado

CLAUSES
*/

% REGLA 1: Si da leche entonces es mamífero
mamifero(X) :- da_leche(X).

% REGLA 2: Si tiene pelo entonces es mamífero
mamifero(X) :- tiene_pelo(X).

% REGLA 3: Si tiene plumas entonces es ave
ave(X) :- tiene_plumas(X).

% REGLA 4: Si pone huevos y vuela entonces es ave
ave(X) :- pone_huevos(X), vuela(X).

% REGLA 5: Si es mamífero y come carne entonces es carnívoro
carnivoro(X) :- mamifero(X), come_carne(X).

% REGLA 6: Si es mamífero y tiene características de depredador entonces es carnívoro
carnivoro(X) :- 
    mamifero(X), 
    tiene_ojos_adelante(X),
    tiene_dientes_agudos(X),
    tiene_garras(X).

% REGLA 7: Si es mamífero y rumia entonces es herbívoro
herbivoro(X) :- mamifero(X), rumia(X).

% REGLA 8: Si es mamífero y es ungulado entonces es herbívoro
herbivoro(X) :- mamifero(X), ungulado(X).

% REGLA 9: Si es ungulado y tiene pesuña entonces es ungulado
ungulado(X) :- tiene_pesuna(X).

% REGLA 10: Si es mamífero y rumia entonces es ungulado
ungulado(X) :- mamifero(X), rumia(X).
    
% ANIMALES ESPECÍFICOS

% Pingüino: Ave que no vuela, nada y es negro y blanco
pinguino(X) :-
    ave(X),
    \+ vuela(X),
    nada(X),
    es_negro_blanco(X).

% Avestruz: Ave con cuello largo que no vuela y es negro y blanco
avestruz(X) :-
    ave(X),
    tiene_cuello_largo(X),
    \+ vuela(X),
    es_negro_blanco(X).

% Cebra: Ungulado con franjas negras y blancas
cebra(X) :-
    ungulado(X),
    tiene_franjas_negras(X),
    es_negro_blanco(X).


% Jirafa: Ungulado con cuello largo
jirafa(X) :-
    ungulado(X),
    tiene_cuello_largo(X).

% Leopardo: Carnívoro con pintas negras y color leonado
leopardo(X) :-
    carnivoro(X),
    tiene_pintas_negras(X),
    es_color_leonado(X).

% Tigre: Carnívoro con franjas negras y color leonado
tigre(X) :-
    carnivoro(X),
    tiene_franjas_negras(X),
    es_color_leonado(X).

% IDENTIFICACIÓN DE ANIMALES
identificar_animal(Animal) :-
    ( pinguino(tilin)  -> Animal = pinguino
    ; avestruz(tilin)  -> Animal = avestruz
    ; cebra(tilin)     -> Animal = cebra
    ; jirafa(tilin)    -> Animal = jirafa
    ; leopardo(tilin)  -> Animal = leopardo
    ; tigre(tilin)     -> Animal = tigre
    ; Animal = desconocido
    ).
    
mostrar_resultado :-
    identificar_animal(Animal),
    write("El animal Tilin es un: "), write(Animal), nl.

% HECHOS BASE PARA TILÍN: ESTO SE DEBE CAMBIAR SEGÚN LO QUE SE QUIERA REVISAR
tiene_plumas(tilin).
tiene_cuello_largo(tilin).
es_negro_blanco(tilin).

% No vuela
vuela(tilin) :- fail.

% GOAL: Borrar initialization(main) y main :-, reemplazando por GOAL, para la conversión a VP 5.x
:- initialization(main).

main :-
    write("SISTEMA DE IDENTIFICACIÓN DE ANIMALES"), nl,
    write("====================================="), nl, nl,
    % Características para el ejemplo de Tilín, podría cambiarse según el caso 
    write("Características de Tilín:"), nl,
    write("- Tiene plumas"), nl,
    write("- Tiene cuello largo"), nl,  
    write("- Es negro y blanco"), nl,
    write("- No vuela"), nl, nl,
    mostrar_resultado, halt.
