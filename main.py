from pathlib import Path

from src.pdfminer.mine import load_pdf

from src.zyklus import Zyklus


def load():


    list_triple_lists = load_pdf(Path("./data/data.pdf"))


  #  test_zyklus = Zyklus(list_triple_lists[23])
   # test_zyklus.extract_dates()
   # test_zyklus.extract_temps()
  #  print(test_zyklus.dataframe.to_csv())
  #  exit(-1)
    for i in range(len(list_triple_lists)):
        new_zyklus = Zyklus(list_triple_lists[i])
        new_zyklus.extract_dates()
        new_zyklus.extract_times()
        new_zyklus.extract_bleeding_values()
        new_zyklus.extract_temps()
        new_zyklus.dataframe.set_index('date', inplace=True)
        new_zyklus.dataframe["temperature.value"].dropna(inplace=True)
        new_zyklus.dataframe["temperature.time"].dropna(inplace=True)
        print(new_zyklus.dataframe.to_csv(header=False))
    # new_zyklus.print_csv()

if __name__ == "__main__":
    load()
