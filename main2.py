import csv
from BTrees.OOBTree import OOBTree
import timeit


def load_data(filename: str):
    items = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(
                {
                    "ID": int(row["ID"]),
                    "Name": row["Name"],
                    "Category": row["Category"],
                    "Price": float(row["Price"]),
                }
            )
    return items


tree = OOBTree()
dictionary = {}


def add_item_to_tree(item):
    tree[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"],
    }


def add_item_to_dict(item):
    dictionary[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"],
    }


def range_query_tree(min_price, max_price):
    return [
        (id_, data)
        for id_, data in tree.items()
        if min_price <= data["Price"] <= max_price
    ]


def range_query_dict(min_price, max_price):
    return [
        (id_, data)
        for id_, data in dictionary.items()
        if min_price <= data["Price"] <= max_price
    ]


def benchmark(min_price, max_price, number=100):
    tree_time = timeit.timeit(
        stmt=lambda: range_query_tree(min_price, max_price), number=number
    )
    dict_time = timeit.timeit(
        stmt=lambda: range_query_dict(min_price, max_price), number=number
    )

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict:    {dict_time:.6f} seconds")


if __name__ == "__main__":
    data = load_data("data/generated_items_data.csv")

    for item in data:
        add_item_to_tree(item)
        add_item_to_dict(item)

    benchmark(100, 500, number=100)
