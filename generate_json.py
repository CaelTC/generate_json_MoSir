import csv
import json
from enum import Enum
import os


csv_path = "./carbon_products_2019.2119.csv"
base_dir = "json"
json_path = "./input.json"


class Scenarios(Enum):
    PETP = 1
    PANEL = 2
    BIOMASS = 3


def change_name(row):
    row["SITE_NOM"] = row.pop("\ufeffSITE_NOM")


def change_pulp(row, scenario):
    if scenario == Scenarios.PETP:
        row["Input_PetP"] = row.pop("carbon_pulp_kg.ha")
        row["Input_PetP"] = float(row["Input_PetP"])
    elif scenario == Scenarios.PANEL:
        row["Input_Panneaux"] = row.pop("carbon_pulp_kg.ha")
        row["Input_Panneaux"] = float(row["Input_Panneaux"])
    elif scenario == Scenarios.BIOMASS:
        row["Input_PulpBioenergy"] = row.pop("carbon_pulp_kg.ha")
        row["Input_PulpBioenergy"] = float(row["Input_PulpBioenergy"])


def change_sawtimberFX(row):
    row["Input_Sciage_feuillus"] = row.pop("carbon_sawtimber_kg.ha_FX")
    row["Input_Sciage_feuillus"] = float(row["Input_Sciage_feuillus"])


def change_sawtimberRX(row):
    row["Input_Sciage_resineux"] = row.pop("carbon_sawtimber_kg.ha_RX")
    row["Input_Sciage_resineux"] = float(row["Input_Sciage_resineux"])


def change_biomass(row):
    row["Input_Bioenergy"] = row.pop("carbon_biomass_kg.ha")
    row["Input_Bioenergy"] = float(row["Input_Bioenergy"])


def save_data(scenario, data, json_template):
    for row in data:
        change_name(row)
        change_pulp(row, scenario)
        change_sawtimberFX(row)
        change_sawtimberRX(row)
        change_biomass(row)
        json_data = to_json(row, json_template, scenario)
        file_name = row.get("treatment") + "_" + \
            row.get("SITE_NOM") + "_" + scenario.name + ".json"
        directory_name = os.path.join(base_dir, scenario.name)

        os.makedirs(directory_name, exist_ok=True)

        with open(os.path.join(directory_name, file_name), "w") as json_file:
            json.dump(json_data, json_file)


def to_json(data, json, scenario):
    if scenario == Scenarios.PETP:
        json["Inputs"]["Architecture_OK"]["Input_PetP"]["0"] = data["Input_PetP"]
        json["Inputs"]["Architecture_OK"]["Input_Bioenergy"]["0"] = data["Input_Bioenergy"]
    elif scenario == Scenarios.PANEL:
        json["Inputs"]["Architecture_OK"]["Input_Panneaux"]["0"] = data["Input_Panneaux"]
        json["Inputs"]["Architecture_OK"]["Input_Bioenergy"]["0"] = data["Input_Bioenergy"]
    elif scenario == Scenarios.BIOMASS:
        json["Inputs"]["Architecture_OK"]["Input_Bioenergy"]["0"] = data["Input_Bioenergy"] + \
            data["Input_PulpBioenergy"]
    json["Inputs"]["Architecture_OK"]["Input_Sciage_feuillus"]["0"] = data["Input_Sciage_feuillus"]
    json["Inputs"]["Architecture_OK"]["Input_Sciage_resineux"]["0"] = data["Input_Sciage_resineux"]
    return json


scenarios = [Scenarios.BIOMASS, Scenarios.PANEL, Scenarios.PETP]
for scenario in scenarios:
    with open(csv_path, newline='', mode='r') as csv_file:
        with open(json_path, mode='r') as json_file:
            json_template = json.load(json_file)
            data = csv.DictReader(csv_file, delimiter=',')
            save_data(scenario, data, json_template)
