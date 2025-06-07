from csv_diff import compare, load_csv


if __name__ == "__main__":
    diff = compare(
        load_csv("v1.csv"),
        load_csv("v2.csv")
    )
    pass