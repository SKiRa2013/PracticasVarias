% Comentados los bloques que se requieren para que el programa funcione en Visual Prolog 5.x
/* 
DOMAINS
    producto = string
    tamaño = string
    envase = string
    estado = string
    numero = integer
    lista_productos = producto*

PREDICATES
    % Estados del sistema
    paso(estado)
    sugerencia(numero)
    se_va_a_llevar(producto)
    bolsa(numero, lista_productos)
    
    % Propiedades de productos
    producto(producto, tamaño, envase, string)
    
    % Reglas de reacción
    regla_r1
    regla_r2
    regla_r3
    regla_r4
    regla_grandes_vidrio
    regla_grandes
    regla_cambiar_bolsa_grandes
    regla_transicion_a_medianos
    regla_medianos
    regla_cambiar_bolsa_medianos
    regla_transicion_a_pequenos
    regla_pequenos
    regla_cambiar_bolsa_pequenos
    regla_final
    
    % Acciones del sistema
    ejecutar_sistema
    preguntar(producto)
    empacar(producto)
    mostrar_estado_actual
    manejar_respuesta(string, producto)

CLAUSES
*/

% REGLA R1: Sugerir gaseosa si lleva papas fritas pero no gaseosa
regla_r1 :-
    paso("verificar_pedido"),
    sugerencia(1),
    se_va_a_llevar("papas_fritas"),
    not(se_va_a_llevar("gaseosa")),
    retract(sugerencia(1)),
    assert(sugerencia(2)),
    preguntar("gaseosa").
    
% REGLA R2: Pasar a siguiente sugerencia
regla_r2 :-
    paso("verificar_pedido"),
    sugerencia(1),
    retract(sugerencia(1)),
    assert(sugerencia(2)).
    
% REGLA R3: Sugerir cereal si lleva yogurt pero no cereal
regla_r3 :-
    paso("verificar_pedido"),
    sugerencia(2),
    se_va_a_llevar("yogurt"),
    not(se_va_a_llevar("cereal")),
    retract(sugerencia(2)),
    retract(paso("verificar_pedido")),
    assert(paso("empacar_grandes")),
    preguntar("cereal").
    
% REGLA R4: Pasar a empacar productos grandes
regla_r4 :-
    paso("verificar_pedido"),
    sugerencia(2),
    retract(sugerencia(2)),
    retract(paso("verificar_pedido")),
    assert(paso("empacar_grandes")).

% REGLA R5: Empacar productos grandes con envase de vidrio primero
regla_grandes_vidrio :-
    paso("empacar_grandes"),
    se_va_a_llevar(Producto),
    producto(Producto, "grande", "vidrio", _),
    bolsa(Numero, ListaActual),
    length(ListaActual, Cantidad),
    Cantidad < 4,
    retract(se_va_a_llevar(Producto)),
    retract(bolsa(Numero, ListaActual)),
    NuevaLista = [Producto | ListaActual],
    assert(bolsa(Numero, NuevaLista)),
    empacar(Producto).

% REGLA R6: Empacar otros productos grandes
regla_grandes :-
    paso("empacar_grandes"),
    se_va_a_llevar(Producto),
    producto(Producto, "grande", _, _),
    bolsa(Numero, ListaActual),
    length(ListaActual, Cantidad),
    Cantidad < 4,
    retract(se_va_a_llevar(Producto)),
    retract(bolsa(Numero, ListaActual)),
    NuevaLista = [Producto | ListaActual],
    assert(bolsa(Numero, NuevaLista)),
    empacar(Producto).

% REGLA R7: Cambiar bolsa si está llena con productos grandes
regla_cambiar_bolsa_grandes :-
    paso("empacar_grandes"),
    bolsa(Numero, Lista),
    length(Lista, Cantidad),
    Cantidad >= 4,
    NuevoNumero = Numero + 1,
    assert(bolsa(NuevoNumero, [])),
    write("Cambiando a bolsa "), write(NuevoNumero), write(" para productos grandes"), nl.

% REGLA R8: Transición a productos medianos
regla_transicion_a_medianos :-
    paso("empacar_grandes"),
    not((se_va_a_llevar(Producto), producto(Producto, "grande", _, _))),
    retract(paso("empacar_grandes")),
    assert(paso("empacar_medianos")),
    write("Pasando a empacar productos medianos"), nl.

% REGLA R9: Empacar productos medianos
regla_medianos :-
    paso("empacar_medianos"),
    se_va_a_llevar(Producto),
    producto(Producto, "mediano", _, _),
    bolsa(Numero, ListaActual),
    length(ListaActual, Cantidad),
    Cantidad < 5,
    retract(se_va_a_llevar(Producto)),
    retract(bolsa(Numero, ListaActual)),
    NuevaLista = [Producto | ListaActual],
    assert(bolsa(Numero, NuevaLista)),
    empacar(Producto).

% REGLA R10: Cambiar bolsa para productos medianos
regla_cambiar_bolsa_medianos :-
    paso("empacar_medianos"),
    bolsa(Numero, Lista),
    length(Lista, Cantidad),
    Cantidad >= 5,
    NuevoNumero = Numero + 1,
    assert(bolsa(NuevoNumero, [])),
    write("Cambiando a bolsa "), write(NuevoNumero), write(" para productos medianos"), nl.

% REGLA R11: Transición a productos pequeños
regla_transicion_a_pequenos :-
    paso("empacar_medianos"),
    not((se_va_a_llevar(Producto), producto(Producto, "mediano", _, _))),
    retract(paso("empacar_medianos")),
    assert(paso("empacar_pequenos")),
    write("Pasando a empacar productos pequeños"), nl.

% REGLA R12: Empacar productos pequeños
regla_pequenos :-
    paso("empacar_pequenos"),
    se_va_a_llevar(Producto),
    producto(Producto, "pequeno", _, _),
    bolsa(Numero, ListaActual),
    retract(se_va_a_llevar(Producto)),
    retract(bolsa(Numero, ListaActual)),
    NuevaLista = [Producto | ListaActual],
    assert(bolsa(Numero, NuevaLista)),
    empacar(Producto).

% REGLA R13: Finalización
regla_final :-
    not(se_va_a_llevar(_)),
    write("PROCESO DE EMPACADO COMPLETADO"), nl, !.

% ACCIONES
preguntar(Producto) :-
    write("¿Desea llevar "), write(Producto), write("? (si/no): "),
    read(Respuesta),
    manejar_respuesta(Respuesta, Producto).

manejar_respuesta(Entrada, Producto) :-
    Entrada = si, assert(se_va_a_llevar(Producto)),
    write("Producto "), write(Producto), write(" agregado al pedido"), nl.

manejar_respuesta(_, _).

empacar(Producto) :-
    write("Empacando: "), write(Producto), nl.

mostrar_estado_actual :-
    nl, nl, write("--- ESTADO ACTUAL ---"), nl,
    (paso(E) -> write("Paso: "), write(E), nl ; true),
    (sugerencia(S) -> write("Sugerencia: "), write(S), nl ; true),
    findall(P, se_va_a_llevar(P), Pendientes),
    write("Productos pendientes: "), write(Pendientes), nl,
    findall(B, bolsa(B, _), Bolsas),
    write("Bolsas activas: "), write(Bolsas), nl,
    write("-------------------"), nl, nl.

ejecutar_sistema :-
    (regla_r1; regla_r2; regla_r3; regla_r4;
        regla_grandes_vidrio; regla_grandes; regla_cambiar_bolsa_grandes;
        regla_transicion_a_medianos; regla_medianos; regla_cambiar_bolsa_medianos;
        regla_transicion_a_pequenos; regla_pequenos; regla_final),
    mostrar_estado_actual,
    not(regla_final),
    ejecutar_sistema.

ejecutar_sistema :-
    regla_final.

% BASE DE CONOCIMIENTO DE PRODUCTOS
producto("gaseosa", "grande", "vidrio", "no").
producto("papas_fritas", "grande", "plastico", "no").
producto("helado", "mediano", "carton", "si").
producto("cereal", "grande", "carton", "no").
producto("yogurt", "pequeno", "plastico", "no").

% GOAL: Borrar initialization(main) y main :-, reemplazando por GOAL, para la conversión a VP 5.x
:- initialization(main).

main :-
    write("SISTEMA DE EMPACADO DE SUPERMERCADO"), nl,
    write("==================================="), nl, nl,
    
    % Inicializar estado
    assert(paso("verificar_pedido")),
    assert(sugerencia(1)),
    assert(bolsa(1, [])),
    
    % Productos iniciales del pedido
    assert(se_va_a_llevar("papas_fritas")),
    assert(se_va_a_llevar("yogurt")),
    assert(se_va_a_llevar("helado")),
    
    write("Pedido inicial:"), nl,
    write("- Papas fritas"), nl,
    write("- Yogurt"), nl,  
    write("- Helado"), nl, nl,

    ejecutar_sistema.
