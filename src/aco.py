import random

from graph import Graph, load_graph_from_json


def inicijalizuj_feromone(graph: Graph, pocetna_vrijednost=1.0):
    feromoni = {}
    for cvor in graph.nodes():
        for susjed, _ in graph.neighbors(cvor):
            feromoni[(cvor, susjed)] = pocetna_vrijednost
    return feromoni


def izaberi_sledeci_cvor(graph: Graph, feromoni, trenutni, posjeceni, alfa, beta):
    kandidati = [
        (susjed, tezina)
        for susjed, tezina in graph.neighbors(trenutni)
        if susjed not in posjeceni and tezina is not None and tezina > 0
    ]

    if not kandidati:
        return None

    tezine_izbora = []
    for susjed, tezina in kandidati:
        feromon = feromoni.get((trenutni, susjed), 1.0)
        heuristika = 1 / tezina
        tezine_izbora.append((feromon**alfa) * (heuristika**beta))

    ukupno = sum(tezine_izbora)
    if ukupno == 0:
        probs = [1 / len(kandidati)] * len(kandidati)
    else:
        probs = [t / ukupno for t in tezine_izbora]

    izabrani = random.choices([s for s, _ in kandidati], weights=probs, k=1)[0]
    return izabrani


def izgradi_rutu(
    graph: Graph, feromoni, start, cilj, alfa, beta, max_koraka=100
) -> tuple[list, float] | None:
    put = [start]
    posjeceni = {start}
    trenutni = start
    cijena = 0
    koraci = 0

    while trenutni != cilj and koraci < max_koraka:
        sledeci = izaberi_sledeci_cvor(graph, feromoni, trenutni, posjeceni, alfa, beta)

        tezina_grane = graph.weight(trenutni, sledeci)
        if tezina_grane is None:
            return None

        cijena += tezina_grane
        put.append(sledeci)
        posjeceni.add(sledeci)
        trenutni = sledeci
        koraci += 1

    if trenutni != cilj:
        return None  # nije stigao do cilja u dozvoljenom broju koraka

    return put, cijena


def azuriraj_feromone(feromoni, uspjesne_rute, rho, Q):
    for grana in feromoni:
        feromoni[grana] *= 1 - rho

    for put, cijena in uspjesne_rute:
        for i in range(len(put) - 1):
            a, b = put[i], put[i + 1]
            dodatak = Q / cijena
            feromoni[(a, b)] = feromoni.get((a, b), 0) + dodatak
            feromoni[(b, a)] = feromoni.get((b, a), 0) + dodatak  # neusmjeren graf


def aco(
    graph: Graph,
    start,
    cilj,
    broj_mrava=10,
    broj_iteracija=50,
    alfa=1.0,
    beta=2.0,
    rho=0.5,
    Q=100,
    max_koraka=100,
    pocetni_feromoni=None,
):
    if start not in graph.graph:
        raise ValueError(f"Pocetni cvor '{start}' ne postoji u grafu.")
    if cilj not in graph.graph:
        raise ValueError(f"Ciljni cvor '{cilj}' ne postoji u grafu.")

    if pocetni_feromoni is not None:
        feromoni = pocetni_feromoni
    else:
        feromoni = inicijalizuj_feromone(graph)

    najbolji_put = None
    najbolja_cijena = float("inf")

    for iteracija in range(broj_iteracija):
        uspjesne_rute = []

        for mrav in range(broj_mrava):
            rezultat = izgradi_rutu(
                graph, feromoni, start, cilj, alfa, beta, max_koraka
            )

            if rezultat is not None:
                put, cijena = rezultat
                uspjesne_rute.append((put, cijena))
                if cijena < najbolja_cijena:
                    najbolja_cijena = cijena
                    najbolji_put = put

        if uspjesne_rute:
            azuriraj_feromone(feromoni, uspjesne_rute, rho, Q)
        else:
            # nijedan mrav nije uspio ove iteracije -- samo isparavanje
            for grana in feromoni:
                feromoni[grana] *= 1 - rho

    return najbolji_put, najbolja_cijena, broj_iteracija, feromoni


if __name__ == "__main__":
    random.seed(42)  # radi ponovljivosti rezultata

    g = load_graph_from_json("data/bih.json")

    start, cilj = "Banja Luka", "Doboj"
    put, cijena, broj_iteracija, feromoni = aco(g, start, cilj)

    if put is None:
        print(f"ACO nije pronasao put izmedju {start} i {cilj}.")
    else:
        print(f"Broj iteracija: {broj_iteracija}")
        print(f"Put: {' -> '.join(put)}")
        print(f"Ukupna cijena: {cijena}")
