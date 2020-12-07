class Zyklus:
    def __init__(self, raw_list: list) -> None:
        self.raw_list = raw_list
        self.length = 0
        self.date_range = ""
        self.year = 0
        self.date_list = []
        self.temp_list = []
        self.time_list = []
        self.extract_length()
        self.extract_date_range()
        self.extract_temps()
        self.extract_dates()
        self.extract_times()
        self.print_csv()

    def print_csv(self):
        lines = ""

        for i, date_el in enumerate(self.date_list):
            new_line = ""
            date_result = datetime.strptime(date_el, "%d.%m.%Y")
            final_str = date_result.strftime("%Y-%m-%d")
            new_line = new_line + final_str + ","
            try:
                new_line = new_line + self.temp_list[i] + ",false,"
                new_line = new_line + self.time_list[i]
            except IndexError:
                new_line = new_line + "NONE,false,"
                new_line = new_line + "NONE"
            lines = lines + new_line + "\n"
        print(lines)

    def extract_length(self):
        self.length = int(self.raw_list[2].split(": ")[1])

    def extract_date_range(self):
        critical_part = self.raw_list[3].split("D")[0]
        self.date_range = critical_part.split(": ")[1].split(" ")[0]

        self.year = "." + str(self.date_range.split(".")[2])

    def extract_temps(self):
        str_val = self.raw_list[3].split("Exportiert")[0]
        temps = str_val.split("BT")[1].split("PERIO")[0]

        counties_temps = temps.replace("\n", "")
        for i in range(0, len(counties_temps), 5):
            single_temp = counties_temps[i : i + 5]
            single_temp = single_temp.replace(",", ".")
            self.temp_list.append(single_temp)

    def extract_dates(self):
        date_str = self.raw_list[3].split("DATUM")[1]
        date_str = date_str.split("UHR")[0]
        continuous_date = date_str.replace(".\n", ",")
        date_split = continuous_date.split(".")
        for date_el in date_split:
            final_val = date_el.replace(",", ".")
            if len(final_val) == 5:
                final_val = final_val + self.year
                self.date_list.append(final_val)

    def extract_times(self):
        time_str = self.raw_list[3].split("UHRZEIT")[1].split("37,00")[0]
        continuous_time = time_str.replace("\n", "")
        for i in range(0, len(continuous_time), 5):
            self.time_list.append(continuous_time[i : i + 5])
