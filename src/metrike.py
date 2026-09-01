import random
import time

from aco import aco
from astar import astar, load_koordinate, napravi_heuristiku
from graph import load_graph_from_json


def izmjeri_astar(graph, start, cilj, h):
    pocetak = time.perf_counter()
    if h is not None:
        put, cijena, brojac = astar(graph, start, cilj, h)
    else:
        put, cijena, brojac = astar(graph, start, cilj)
    vrijeme = time.perf_counter() - pocetak

    return put, cijena, brojac, vrijeme


def izmjeri_aco(graph, start, cilj, broj_pokretanja=10, **aco_parametri):
    vremena = []
    cijene = []
    najbolji_put = None
    najbolja_cijena = float("inf")

    for i in range(broj_pokretanja):
        pocetak = time.perf_counter()
        put, cijena, brojac, feromoni = aco(graph, start, cilj, **aco_parametri)
        vrijeme = time.perf_counter() - pocetak

        vremena.append(vrijeme)
        if put is not None:
            cijene.append(cijena)
            if cijena < najbolja_cijena:
                najbolja_cijena = cijena
                najbolji_put = put

        prosjecno_vrijeme = sum(vremena) / len(vremena)
        prosjecna_cijena = sum(cijene) / len(cijene) if cijene else float("inf")

        return najbolji_put, najbolja_cijena, prosjecna_cijena, prosjecno_vrijeme


if __name__ == "__main__":
    random.seed(42)

    g = load_graph_from_json("data/gradovi.json")
    koordinate = load_koordinate("data/koordinate.json")
    start, cilj = "Rome", "Paris"

    print(f"Poredjenje A* vs ACO za rutu: {start} -> {cilj}")
    print()

    h = napravi_heuristiku(koordinate, cilj)
    put_a, cijena_a, brojac_a, vrijeme_a = izmjeri_astar(g, start, cilj, h)

    print("=== A* ===")
    print(f"Put: {' -> '.join(put_a)}")  # type: ignore
    print(f"Cijena: {cijena_a}")
    print(f"Obradjeno cvorova: {brojac_a}")
    print(f"Vrijeme: {vrijeme_a * 1000:.3f} ms")
    print()

    broj_pokretanja = 10
    put_b, najbolja_b, prosjecna_b, vrijeme_b = izmjeri_aco(
        g, start, cilj, broj_pokretanja=broj_pokretanja
    )  # type: ignore

    print(f"=== ACO (prosjek od {broj_pokretanja} pokretanja) ===")
    print(f"Najbolji put: {' -> '.join(put_b) if put_b else 'nije pronadjen'}")
    print(f"Najbolja cijena (od svih pokretanja): {najbolja_b}")
    print(f"Prosjecna cijena: {prosjecna_b:.1f}")
    print(f"Prosjecno vrijeme: {vrijeme_b * 1000:.3f} ms")
    print()

    print("=== Poredjenje ===")
    print(f"{'':<20} {'Cijena':>12} {'Vrijeme':>15}")
    print(f"{'A*':<20} {cijena_a:>12} {vrijeme_a * 1000:>12.3f} ms")
    print(f"{'ACO (najbolji)':<20} {najbolja_b:>12} {vrijeme_b * 1000:>12.3f} ms")
    print()

    if vrijeme_a < vrijeme_b:
        print(f"A* je bio {vrijeme_b / vrijeme_a:.1f}x brzi od ACO (prosjecno).")
    else:
        print(f"ACO je bio {vrijeme_a / vrijeme_b:.1f}x brzi od A* (prosjecno).")

    if najbolja_b < cijena_a:
        print("ACO je pronasao BOLJI (jeftiniji) put od A*.")
    elif najbolja_b > cijena_a:
        print("A* je pronasao BOLJI (jeftiniji) put od ACO.")
    else:
        print("Oba algoritma su pronasla isti (optimalan) put.")
