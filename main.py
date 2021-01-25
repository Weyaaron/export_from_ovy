from datetime import date
from pathlib import Path

from src.mine import load_pdf

from src.classes.zyklus import Zyklus
from src.utils import read_template


def main():


    result = read_template()
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
        result +=new_zyklus.dataframe.to_csv(header=False)

    today = date.today()

    outpath = f'result_{today}.csv'
    if Path(outpath).is_file():
        print("The target file already exists, please move/remove it first")
        exit(-1)
    with open(outpath,'w') as file:
        file.write(result)



if __name__ == "__main__":
    main()
