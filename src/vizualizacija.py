import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from astar import load_koordinate
from graph import Graph, load_graph_from_json


def crtaj_graf(
    graph: Graph,
    koordinate: dict,
    istaknuti_put=None,
    naslov="Graf gradova",
    prikazi_sve_tezine=False,
    sacuvaj_u="graf.png",
):

    fig, ax = plt.subplots(figsize=(12, 9))

    put_grane = set()
    if istaknuti_put:
        for i in range(len(istaknuti_put) - 1):
            a, b = istaknuti_put[i], istaknuti_put[i + 1]
            put_grane.add(frozenset([a, b]))

    iscrtano = set()
    for cvor_a in graph.nodes():
        if cvor_a not in koordinate:
            continue
        for cvor_b, tezina in graph.neighbors(cvor_a):
            if cvor_b not in koordinate or tezina is None:
                continue
            par = frozenset([cvor_a, cvor_b])
            if par in iscrtano:
                continue
            iscrtano.add(par)

            x1, y1 = koordinate[cvor_a]
            x2, y2 = koordinate[cvor_b]

            if par in put_grane:
                continue

            ax.plot([x1, x2], [y1, y2], color="lightgray", linewidth=0.6, zorder=1)
            if prikazi_sve_tezine:
                ax.text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    str(tezina),
                    fontsize=6,
                    color="gray",
                    ha="center",
                    va="center",
                )

    if istaknuti_put:
        for i in range(len(istaknuti_put) - 1):
            a, b = istaknuti_put[i], istaknuti_put[i + 1]
            if a not in koordinate or b not in koordinate:
                continue
            x1, y1 = koordinate[a]
            x2, y2 = koordinate[b]
            ax.plot([x1, x2], [y1, y2], color="crimson", linewidth=2.5, zorder=2)

            tezina = graph.weight(a, b)
            if tezina is not None:
                ax.text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    str(tezina),
                    fontsize=8,
                    color="crimson",
                    ha="center",
                    va="center",
                    fontweight="bold",
                    bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.5},
                )

    put_cvorovi = set(istaknuti_put) if istaknuti_put else set()
    for grad, (x, y) in koordinate.items():
        if grad not in graph.graph:
            continue
        if grad in put_cvorovi:
            ax.scatter(x, y, color="crimson", s=60, zorder=3)
        else:
            ax.scatter(x, y, color="steelblue", s=25, zorder=3)
        ax.annotate(grad, (x, y), fontsize=7, xytext=(4, 4), textcoords="offset points")

    ax.set_title(naslov)
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(sacuvaj_u, dpi=150)
    print(f"Graf sacuvan u '{sacuvaj_u}'.")
    plt.close(fig)


if __name__ == "__main__":
    from aco import aco
    from astar import astar, napravi_heuristiku

    g = load_graph_from_json("data/gradovi.json")
    koordinate = load_koordinate("data/koordinate.json")
    koordinate_xy = {grad: [lon, lat] for grad, (lat, lon) in koordinate.items()}

    start, cilj = "Rome", "Paris"
    h = napravi_heuristiku(koordinate, cilj)
    put, cijena, brojac = astar(g, start, cilj, h)

    putAco, cijenaAco, broj, feromoni = aco(
        g, start, cilj, broj_mrava=10, broj_iteracija=20
    )

    print(f"Put: {' -> '.join(put)}")  # type: ignore

    crtaj_graf(
        g,
        koordinate_xy,
        istaknuti_put=put,
        naslov=f"ACO put: {start} -> {cilj} (cijena {cijena})",
    )
