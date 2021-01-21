from pathlib import Path

from src.mine import load_pdf

from src.classes.zyklus import Zyklus


def load():

    list_triple_lists = load_pdf(Path("./data/data.pdf"))

    for i in range(len(list_triple_lists)):
        new_zyklus = Zyklus(list_triple_lists[i])
        new_zyklus.extract_dates()
        new_zyklus.extract_times()
        new_zyklus.extract_bleeding_values()
        new_zyklus.extract_temps()
        new_zyklus.extract_mukus_values()
        new_zyklus.dataframe.set_index("date", inplace=True)
        new_zyklus.dataframe["temperature.value"].dropna(inplace=True)
        new_zyklus.dataframe["temperature.time"].dropna(inplace=True)
        print(new_zyklus.dataframe.to_csv(header=False))


if __name__ == "__main__":
    load()
