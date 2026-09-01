import json
from math import sqrt

from graph import Graph, load_graph_from_json


def null_heuristic(cvor):
    return 0


def load_koordinate(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def vazdusna_udaljenost_km(koord_a, koord_b):
    from math import atan2, cos, radians, sin

    R = 6371.0
    lat1, lon1 = radians(koord_a[0]), radians(koord_a[1])
    lat2, lon2 = radians(koord_b[0]), radians(koord_b[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def napravi_heuristiku(koordinate, cilj):
    if cilj not in koordinate:
        raise ValueError(f"Nema koordinata za ciljni grad '{cilj}'")

    koord_cilja = koordinate[cilj]

    def h(cvor):
        if cvor not in koordinate:
            return 0
        return vazdusna_udaljenost_km(koordinate[cvor], koord_cilja)

    return h


def sljedeci_cvor(opcije, udaljenosti):
    cvor, min_udaljenost = None, float("inf")
    for opcija in opcije:
        if udaljenosti[opcija] < min_udaljenost:
            cvor, min_udaljenost = opcija, udaljenosti[opcija]
    return cvor


def astar(graph: Graph, prvi, trazeni, h=null_heuristic):
    if prvi not in graph.graph:
        raise ValueError(f"Pocetni cvor '{prvi}' ne postoji u grafu.")
    if trazeni not in graph.graph:
        raise ValueError(f"Ciljni cvor '{trazeni}' ne postoji u grafu.")

    opcije = {prvi}

    min_udaljenosti = {v: float("inf") for v in graph.graph}
    min_udaljenosti[prvi] = 0

    heuristik_rekalkulacija = {v: float("inf") for v in graph.graph}
    heuristik_rekalkulacija[prvi] = 0 + h(prvi)

    put = {}

    brojac = 0
    while len(opcije) > 0:
        brojac += 1
        trenutni = sljedeci_cvor(opcije, heuristik_rekalkulacija)

        if trazeni == trenutni:
            break

        opcije.remove(trenutni)

        for cvor, udaljenost in graph.neighbors(trenutni):
            if udaljenost is None:
                continue

            nova_udaljenost = min_udaljenosti[trenutni] + udaljenost

            if nova_udaljenost < min_udaljenosti[cvor]:
                min_udaljenosti[cvor] = nova_udaljenost
                heuristik_rekalkulacija[cvor] = nova_udaljenost + h(cvor)
                put[cvor] = trenutni  # do CVORA stizemo iz TRENUTNOG

                if cvor not in opcije:
                    opcije.add(cvor)

    # ako trazeni nikad nije dosegnut (i nije sam pocetni cvor) -- nema puta
    if trazeni != prvi and trazeni not in put:
        return None, float("inf"), brojac

    rekonstrukcija_puta = [trazeni]
    cvor = trazeni
    while cvor != prvi:
        cvor = put[cvor]
        rekonstrukcija_puta.append(cvor)

    rekonstrukcija_puta.reverse()

    return rekonstrukcija_puta, min_udaljenosti[trazeni], brojac


if __name__ == "__main__":
    g = load_graph_from_json("data/gradovi.json")
    koordinate = load_koordinate("data/koordinate.json")

    start, cilj = "Rome", "Paris"
    h = napravi_heuristiku(koordinate, cilj)

    put, cijena, broj_iteracija = astar(g, start, cilj, h)

    if put is None:
        print(f"Ne postoji put izmedju {start} i {cilj}.")
    else:
        print(f"Broj obradjenih cvorova: {broj_iteracija}")
        print(f"Put: {' -> '.join(put)}")
        print(f"Ukupna cijena: {cijena}")
