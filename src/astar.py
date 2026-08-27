from graph import Graph, load_graph_from_json


def null_heuristic(cvor):
    return 0


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

    opcije = set([prvi])

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
    g = load_graph_from_json("data/bih.json")

    start, cilj = "Banja Luka", "Tuzla"
    put, cijena, broj_iteracija = astar(g, start, cilj)

    if put is None:
        print(f"Ne postoji put izmedju {start} i {cilj}.")
    else:
        print(f"Broj obradjenih cvorova: {broj_iteracija}")
        print(f"Put: {' -> '.join(put)}")
        print(f"Ukupna cijena: {cijena}")
