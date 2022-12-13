# Magic Square

## Descripción
---
Un **magic square** es una matriz cuadrada de números enteros de tamaño n, donde la suma de los números en cada fila, cada columna y la diagonal principal es la misma.[1]

Por ejemplo, el siguiente es un magic square de tamaño 3:

```
2 7 6
9 5 1
4 3 8
```

El siguiente es un magic square de tamaño 4:

```
 1   2  15  16
12  14   3   5
13   7  10   4
 8  11   6   9
```
---
## Uso Básico
---
### En Prolog `magic_square.pl`

```
?- magic_square(4, Sol).
?- magic_square([[G, A, E], [F, B, H], [C, 3, D]]).
```

- El predicado `magic_square/2` es un predicado de consulta que recibe un tamaño n y una lista de listas de números enteros de tamaño n, devuelve una lista de listas de números enteros que representa un magic square de tamaño n. 
- El predicado `magic_square/1` es un predicado de consulta que recibe una lista de listas de números enteros de tamaño n, devuelve cada valor en la que sería solución, cada posición.

---
### En el ejecutable `magic_square.exe`

Para utilizar el ejecutable, se debe ejecutar el archivo `magic_square.exe` en un sistema operativo Windows y luego ejecutar eestablecer el tamaño del magic square con el teclado numérico en el cuadrado inferior izquierda y luego presionar la tecla `Enter` o el Botón *Submit*.


---
### En Python `magic_square.py`

```
>>> import magic_square
>>> ms.Magic_Square(prolog_file="magic_square.pl", query="magic_square({n}, Result)")
>>> ms.mainloop()
```

[1]: https://en.wikipedia.org/wiki/Magic_square