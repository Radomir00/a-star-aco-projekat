from graph import Graph


def zatvori_ulicu(graph: Graph, cvor_a, cvor_b):
    graph.set_weight(cvor_a, cvor_b, None)


def promjeni_saobracaj(graph: Graph, cvor_a, cvor_b, faktor):
    trenutna = graph.weight(cvor_a, cvor_b)
    if trenutna is not None:
        graph.set_weight(cvor_a, cvor_b, trenutna * faktor)


def dodaj_prepreku(graph: Graph, cvor_a, cvor_b, dodatna_tezina):
    trenuna = graph.weight(cvor_a, cvor_b)
    if trenuna is not None:
        graph.set_weight(cvor_a, cvor_b, trenuna + dodatna_tezina)
