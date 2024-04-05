import csv
import json
from enum import Enum
import os


csv_path = "./carbon_products_2019.2119.csv"
directory_name = "json"


class Scenarios(Enum):
    PETP = 1
    PANEL = 2


def change_name(row):
    row["SITE_NOM"] = row.pop("\ufeffSITE_NOM")


def change_pulp(row, scenario):
    if scenario == Scenarios.PETP:
        row["Input_PetP"] = row.pop("carbon_pulp_kg.ha")
        row["Input_PetP"] = float(row["Input_PetP"])
    elif scenario == Scenarios.PANEL:
        row["Input_Panneaux"] = row.pop("carbon_pulp_kg.ha")
        row["Input_Panneaux"] = float(row["Input_Panneaux"])


def change_sawtimberFX(row):
    row["Input_Sciage_feuillus"] = row.pop("carbon_sawtimber_kg.ha_FX")
    row["Input_Sciage_feuillus"] = float(row["Input_Sciage_feuillus"])


def change_sawtimberRX(row):
    row["Input_Sciage_resineux"] = row.pop("carbon_sawtimber_kg.ha_RX")
    row["Input_Sciage_resineux"] = float(row["Input_Sciage_resineux"])


def change_biomass(row):
    row["Input_Bioenergy"] = row.pop("carbon_biomass_kg.ha")
    row["Input_Bioenergy"] = float(row["Input_Bioenergy"])


with open(csv_path, newline='') as csv_file:
    data = csv.DictReader(csv_file, delimiter=',')
    scenarios = [Scenarios.PANEL, Scenarios.PETP]
    os.makedirs(directory_name)
    for scenario in scenarios:
        for row in data:
            change_name(row)
            change_pulp(row, scenario)
            change_sawtimberFX(row)
            change_sawtimberRX(row)
            change_biomass(row)
            file_name = row.get("treatment") + "_" + \
                row.get("SITE_NOM") + "_" + scenario.name + ".json"
            with open(os.path.join(directory_name, file_name), "w") as json_file:
                json.dump(row, json_file)
