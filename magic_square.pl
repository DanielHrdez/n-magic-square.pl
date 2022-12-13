% Librería para ayudar en listas
:- use_module(library(clpfd)).

% Función para asignar un dominio a cada variable de una matriz
% Parametros:
% - Min: Valor mínimo del dominio
% - Max: Valor máximo del dominio
% - First: Primer elemento de la lista
% - Rest: Resto de la lista
list_between(_, _, []).
list_between(Min, Max, [First|Rest]) :-
    between(Min, Max, First),
    list_between(Min, Max, Rest).

% Función para crear una matriz de NxN
% Parametros:
% - N: Tamaño de la matriz
% - First: Primer elemento de la lista
% - Rest: Resto de la lista
create_mat(_, []).
create_mat(N, [First|Matrix]) :-
	length(First, N),
	create_mat(N, Matrix).

% Función para sumar cada fila de una matriz
% Parametros:
% - Row: Fila de la matriz
% - Matrix: Matriz a sumar
% - Sum: Suma de cada fila
sum_row([], _).
sum_row([Row|Matrix], Sum) :-
	sum(Row, #=, Sum),
	sum_row(Matrix, Sum).

% Función para extraer los elementos diagonales de una matriz
extract_element(L, L1, [H|L1]):- 
    length(L1, N1), 
    length(L2, N1), 
    append(L2, [H|_], L).

% Función para sumar cada elemento de la diagonal principal de una matriz
% Parametros:
% - Matrix: Matriz a resolver
% - N: Tamaño de la matriz
% - Result: Cada elemento de la diagonal principal
diagonal1(Matrix, N):- 
    foldl(extract_element, Matrix, [], Result),
    sum(Result, #=, N).

% Función para sumar cada elemento de la diagonal secundaria de una matriz
% Parametros:
% - Matrix: Matriz a resolver
% - N: Tamaño de la matriz
% - Result: Cada elemento de la diagonal secundaria
diagonal2(Matrix, N):- 
    reverse(Matrix, M2),
    foldl(extract_element, M2, [], Res),
    sum(Res, #=, N).

% Función principal que devuelve los resultados de los cuadrados NxN
% Parametros:
% - N: Tamaño de la matriz
% - Matrix: Matriz a resolver
magic_square(N, Matrix) :-
    % Se comprueba que el tamaño sea mayor a 0
    N > 0,

    % Se crea una matriz de NxN con dominio NxN
    length(Matrix, N),
	create_mat(N, Matrix),

    % Cada elemento de la matriz es un número entre 1 y NxN y no se repite
	flatten(Matrix, Vars),
	N_sq is N * N,
    Vars ins 1..N_sq,
	all_distinct(Vars),

    % Los elementos de cada fila suman lo mismo
	SumDim is N * (N_sq + 1) / 2,
	sum_row(Matrix, SumDim),

    % Los elementos de cada columna suman lo mismo
	transpose(Matrix, TransMat),
	sum_row(TransMat, SumDim),

    % Los elementos de la diagonal principal y secundaria suman lo mismo
    diagonal1(Matrix, SumDim),
    diagonal2(Matrix, SumDim),

    % Se resuelve el problema
    list_between(1, N_sq, Vars).

% Función principal que resuelve cuadrados mágicos
% Parametros:
% - Matrix: Matriz a resolver
magic_square(Matrix) :-
    length(Matrix, N),
    magic_square(N, Matrix).

/** <examples>
?- magic_square(4, Sol).
?- magic_square([[G, A, E], [F, B, H], [C, 3, D]]).
*/