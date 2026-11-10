import heapq

INF = float("inf")


# ---------- 1. DIJKSTRA ----------
def dijkstra(grafo, origen):
    dist = {n: INF for n in grafo}
    previo = {n: None for n in grafo}
    dist[origen] = 0
    cola = [(0, origen)]
    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:
            continue
        for v, peso in grafo[u]:
            if d + peso < dist[v]:
                dist[v] = d + peso
                previo[v] = u
                heapq.heappush(cola, (dist[v], v))
    return dist, previo


def reconstruir_camino(previo, destino):
    ruta = []
    while destino is not None:
        ruta.append(destino)
        destino = previo[destino]
    return ruta[::-1]


# ---------- 2. FLOYD ----------
def floyd(matriz):
    n = len(matriz)
    d = [fila[:] for fila in matriz]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


# ---------- 3. WARSHALL ----------
def warshall(adj):
    n = len(adj)
    r = [fila[:] for fila in adj]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                r[i][j] = r[i][j] or (r[i][k] and r[k][j])
    return r


# ---------- 4. KRUSKAL ----------
def kruskal(n, aristas):
    padre = list(range(n))

    def buscar(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    mst, total = [], 0
    for peso, u, v in sorted(aristas):
        ru, rv = buscar(u), buscar(v)
        if ru != rv:
            padre[ru] = rv
            mst.append((u, v, peso))
            total += peso
    return mst, total


def imprimir_matriz(m, etiquetas):
    print("      " + "".join(f"{e:>6}" for e in etiquetas))
    for e, fila in zip(etiquetas, m):
        print(f"{e:>5} " + "".join(f"{('INF' if x == INF else x):>6}" for x in fila))


# ---------- EJEMPLOS Y MENÚ ----------
def caso_dijkstra():
    grafo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("D", 5)],
        "C": [("B", 1), ("D", 8), ("E", 10)],
        "D": [("E", 2)],
        "E": [],
    }
    origen = "A"
    dist, previo = dijkstra(grafo, origen)
    print(f"\nDijkstra desde {origen}:")
    for nodo in grafo:
        print(f"  {nodo}: distancia = {dist[nodo]}, camino = {' -> '.join(reconstruir_camino(previo, nodo))}")


def caso_floyd():
    m = [
        [0, 3, INF, 7],
        [8, 0, 2, INF],
        [5, INF, 0, 1],
        [2, INF, INF, 0],
    ]
    print("\nFloyd - distancias mínimas entre todos los pares:")
    imprimir_matriz(floyd(m), ["0", "1", "2", "3"])


def caso_warshall():
    adj = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]
    print("\nWarshall - clausura transitiva (1 = existe camino):")
    imprimir_matriz(warshall(adj), ["0", "1", "2", "3"])


def caso_kruskal():
    # (peso, u, v)
    aristas = [(7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3), (7, 1, 4),
               (5, 2, 4), (15, 3, 4), (6, 3, 5), (8, 4, 5), (9, 4, 6), (11, 5, 6)]
    mst, total = kruskal(7, aristas)
    print("\nKruskal - árbol de expansión mínima:")
    for u, v, w in mst:
        print(f"  {u} - {v} (peso {w})")
    print(f"  Peso total: {total}")


def main():
    casos = {"1": caso_dijkstra, "2": caso_floyd, "3": caso_warshall, "4": caso_kruskal}
    while True:
        print("\n=== ALGORITMOS DE GRAFOS ===")
        print("1. Dijkstra\n2. Floyd\n3. Warshall\n4. Kruskal\n0. Salir")
        op = input("Elige una opción: ").strip()
        if op == "0":
            print("¡Hasta luego!")
            break
        casos.get(op, lambda: print("Opción no válida."))()


if __name__ == "__main__":
    main()
