import random

from aco import aco
from astar import astar, load_koordinate, napravi_heuristiku
from graph import load_graph_from_json
from promjene import *

if __name__ == "__main__":
    random.seed(42)

    g = load_graph_from_json("data/bih.json")
    koordinate = load_koordinate("data/koordinate.json")
    start, cilj = "Banja Luka", "Tuzla"

    print("=== Korak 1: A* ===")
    h = napravi_heuristiku(koordinate, cilj)
    pocetni_put, pocetna_cijena, brojac = astar(g, start, cilj, h)
    print(f"Put: {' -> '.join(pocetni_put)}")  # type: ignore
    print(f"Cijena: {pocetna_cijena}")
    print()

    print("=== Korak 2: ACO nepromijenjen ===")
    random.seed(42)
    _, _, _, feromoni_prije = aco(g, start, cilj)
    print()

    print("=== Korak 3: Simuliramo zatvorenu ulicu Kotor Varos - Teslic ===")
    zatvori_ulicu(g, "Kotor Varos", "Teslic")
    print()

    print("=== Korak 4a: ACO sa SVJEZIM feromonima ===")
    random.seed(42)
    put_svjez, cijena_svjez, _, _ = aco(g, start, cilj)
    print(f"Put: {' -> '.join(put_svjez) if put_svjez else 'nije pronadjen'}")
    print(f"Cijena: {cijena_svjez}")
    print()

    print("=== Korak 4b: ACO NASTAVLJA sa postojecim feromonima ===")
    random.seed(42)
    put_nastavak, cijena_nastavak, _, _ = aco(
        g, start, cilj, pocetni_feromoni=feromoni_prije
    )
    print(f"Put: {' -> '.join(put_nastavak) if put_nastavak else 'nije pronadjen'}")
    print(f"Cijena: {cijena_nastavak}")
    print()

    print("=== Poredjenje ===")
    print(f"{'Scenario':<35} {'Cijena':>10}")
    print(f"{'A* prije promjene':<35} {pocetna_cijena:>10}")
    print(f"{'ACO poslije, svjezi feromoni':<35} {cijena_svjez:>10}")
    print(f"{'ACO poslije, nastavak feromona':<35} {cijena_nastavak:>10}")
    print()
