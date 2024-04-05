import csv
import json

csv_path = "./carbon_products_2019.2119.csv"


def change_name(row):
    row["SITE_NOM"] = row.pop("\ufeffSITE_NOM")


def change_pulp(row):
    row["Input_PetP"] = row.pop("carbon_pulp_kg.ha")


def change_sawtimberFX(row):
    row["Input_Sciage_feuillus"] = row.pop("carbon_sawtimber_kg.ha_FX")


def change_sawtimberRX(row):
    row["Input_Sciage_resineux"] = row.pop("carbon_sawtimber_kg.ha_RX")


def change_biomass(row):
    row["Input_Bioenergy"] = row.pop("carbon_biomass_kg.ha")


with open(csv_path, newline='') as csv_file:
    data = csv.DictReader(csv_file, delimiter=',')
    for row in data:
        change_name(row)
        change_pulp(row)
        change_sawtimberFX(row)
        change_sawtimberRX(row)
        change_biomass(row)
        file_name = row.get("treatment") + "_" + row.get("SITE_NOM") + ".json"
        with open(file_name, "w") as json_file:
            json.dump(row, json_file)
