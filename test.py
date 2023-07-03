import json
import random

with open("data/ports.json", encoding="utf8") as f:
    ports = json.load(f)

IndiaPorts = [i for i in ports.keys() if i.startswith("IN")]
for p in IndiaPorts:
    temp = ports[p]
    name = f"{temp['name']}, {temp['province']} ({p})]"

ports_rate = {}
for i in IndiaPorts:
    for j in IndiaPorts:
        if i != j:
            k = f"{i}->{j}"
            v = random.randrange(500, 5000)
            ports_rate[k] = v

freight_rates = {}
freight_rates["fcl_rate"] = {
    "10std": 1000,
    "20std": 2000,
    "40std": 4000,
    "40hcube": 8000,
    "45hcube": 8500,
    "20ref": 3000,
    "40ref": 6000
}
freight_rates["lcl_rate"] = {
    "per_kg": 20,
    "per_vol": 40
}
freight_rates["service_rate"] = ports_rate

with open("data/freight_rates.json", "w") as f:
    json.dump(freight_rates, f)
