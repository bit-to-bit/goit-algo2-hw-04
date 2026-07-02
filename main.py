import networkx as nx
import matplotlib.pyplot as plt
from src.edmonds_karp import edmonds_karp


def test_edmonds_karp():
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]

    terminals = ["Термінал 1", "Термінал 2"]
    shops = [f"Магазин {i}" for i in range(1, 15)]

    for terminal in terminals:
        edges.append(("Super Source", terminal, float("inf")))
    for shop in shops:
        edges.append((shop, "Super Sink", float("inf")))

    vertexs = set()
    for u, v, w in edges:
        vertexs.add(u)
        vertexs.add(v)

    vertexs = sorted(list(vertexs))
    v_to_idx = {v: i for i, v in enumerate(vertexs)}
    idx_to_v = {i: v for i, v in enumerate(vertexs)}

    n = len(vertexs)
    capacity_matrix = [[0] * n for _ in range(n)]

    for u, v, w in edges:
        capacity_matrix[v_to_idx[u]][v_to_idx[v]] = w if w != float("inf") else 999999

    source_idx = v_to_idx["Super Source"]
    sink_idx = v_to_idx["Super Sink"]

    max_flow, flow_matrix = edmonds_karp(capacity_matrix, source_idx, sink_idx)

    print(f"Total Max Flow: {max_flow}")
    print("-" * 55)
    print("{:<15} | {:<15} | {:<15}".format("Термінал", "Магазин", "Фактичний Потік"))
    print("-" * 55)

    warehouse_contributions = {}
    for w in ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]:
        total_in = 0
        t1_in = 0
        t2_in = 0
        if flow_matrix[v_to_idx["Термінал 1"]][v_to_idx[w]] > 0:
            t1_in += flow_matrix[v_to_idx["Термінал 1"]][v_to_idx[w]]
        if flow_matrix[v_to_idx["Термінал 2"]][v_to_idx[w]] > 0:
            t2_in += flow_matrix[v_to_idx["Термінал 2"]][v_to_idx[w]]

        total_in = t1_in + t2_in
        warehouse_contributions[w] = {
            "Total": total_in,
            "Термінал 1": t1_in / total_in if total_in > 0 else 0,
            "Термінал 2": t2_in / total_in if total_in > 0 else 0,
        }

    shop_to_warehouse = {
        "Магазин 1": "Склад 1",
        "Магазин 2": "Склад 1",
        "Магазин 3": "Склад 1",
        "Магазин 4": "Склад 2",
        "Магазин 5": "Склад 2",
        "Магазин 6": "Склад 2",
        "Магазин 7": "Склад 3",
        "Магазин 8": "Склад 3",
        "Магазин 9": "Склад 3",
        "Магазин 10": "Склад 4",
        "Магазин 11": "Склад 4",
        "Магазин 12": "Склад 4",
        "Магазин 13": "Склад 4",
        "Магазин 14": "Склад 4",
    }

    for t in terminals:
        for shop in shops:
            flow_to_shop = 0
            for u in range(n):
                if flow_matrix[u][v_to_idx[shop]] > 0:
                    flow_to_shop += flow_matrix[u][v_to_idx[shop]]

            w = shop_to_warehouse[shop]
            t_fraction = warehouse_contributions[w][t]
            t_flow = flow_to_shop * t_fraction

            if t_flow > 0:
                print("{:<15} | {:<15} | {:<15.2f}".format(t, shop, t_flow))
            else:
                print("{:<15} | {:<15} | {:<15}".format(t, shop, 0))

    # Візуалізація графа
    G = nx.DiGraph()

    for u, v, w in edges[:20]:  # Беремо перші 20 ребер (без Super Source / Sink)
        actual_flow = flow_matrix[v_to_idx[u]][v_to_idx[v]]
        G.add_edge(u, v, capacity=w, flow=actual_flow)

    pos = {}

    pos["Термінал 1"] = (0, 10)
    pos["Термінал 2"] = (0, -10)

    pos["Склад 1"] = (-1.5, 10)
    pos["Склад 2"] = (-1.5, -10)
    pos["Склад 3"] = (1.5, 10)
    pos["Склад 4"] = (1.5, -10)

    for i in range(1, 7):
        pos[f"Магазин {i}"] = (-3, 25 - (i - 1) * 10)

    for i in range(7, 15):
        pos[f"Магазин {i}"] = (3, 35 - (i - 7) * 10)

    color_map = []
    for node in G.nodes():
        if "Термінал" in node:
            color_map.append("lightblue")
        elif "Склад" in node:
            color_map.append("lightgreen")
        else:
            color_map.append("orange")

    edge_colors = []
    edge_widths = []
    for u, v, d in G.edges(data=True):
        if d["flow"] > 0:
            edge_colors.append("blue")
            edge_widths.append(2.0 + (d["flow"] / 10.0))
        else:
            edge_colors.append("lightgray")
            edge_widths.append(1.0)

    plt.figure(figsize=(16, 10))
    nx.draw_networkx_nodes(
        G, pos, node_color=color_map, node_size=3000, edgecolors="black"
    )
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

    nx.draw_networkx_edges(
        G, pos, arrowstyle="->", arrowsize=15, edge_color=edge_colors, width=edge_widths
    )

    edge_labels = {
        (u, v): f"{d['flow']}/{d['capacity']}" for u, v, d in G.edges(data=True)
    }

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=9,
        font_color="darkred",
        label_pos=0.4,
    )

    plt.title(
        "Візуалізація потоків логістичної мережі (Фактичний потік / Пропускна здатність)",
        fontsize=16,
        fontweight="bold",
    )
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    test_edmonds_karp()
