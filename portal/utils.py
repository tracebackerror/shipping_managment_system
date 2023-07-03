import json

ports, freight_rates = "", ""
with open("data/ports.json", encoding="utf8") as f:
    ports = json.load(f)
with open("data/freight_rates.json") as f:
    freight_rates = json.load(f)


def getIndianPortsList():
    port_list = []
    IndiaPorts = [i for i in ports.keys() if i.startswith("IN")]
    for p in IndiaPorts:
        temp = ports[p]
        name = f"{temp['name']}, {temp['province']} [{p}]"
        port_list.append((p, name))
    return port_list

def getPortFullName(port_code):
    port = ports[port_code]
    return f"{port['name']}, {port['province']} [{port_code}]"

def getFreightRates(kwargs):
    res = {}
    key = f"{kwargs['source_port']}->{kwargs['dest_port']}"
    service_charge = freight_rates["service_rate"][key]
    if kwargs['transportation_by'] == "fcl":
        container_charge = freight_rates["fcl_rate"][kwargs['container_type']]
    else:
        per_kg_rate = freight_rates["lcl_rate"]["per_kg"]
        per_vol_rate = freight_rates["lcl_rate"]["per_vol"]
        weight = float(kwargs['weight'])
        volume = float(kwargs['volume'])
        container_charge = (weight*per_kg_rate) + (volume*per_vol_rate)
    res["service_charge"] = round(service_charge, 2)
    res["container_charge"] = round(container_charge, 2)
    res["total"] = res["service_charge"] + res["container_charge"]
    return res


def getServiceCharge(source_port, dest_port):
    try:
        key = f"{source_port}->{dest_port}"
        service_charge = freight_rates["service_rate"][key]
    except:
        service_charge = 0
    return service_charge


def getContainerCharge(transportation_by, container_type, weight, volume, quantity):
    if transportation_by == "fcl":
        container_charge = freight_rates["fcl_rate"][container_type]
    else:
        per_kg_rate = freight_rates["lcl_rate"]["per_kg"]
        per_vol_rate = freight_rates["lcl_rate"]["per_vol"]
        weight = float(weight)
        volume = float(volume)
        container_charge = (weight*per_kg_rate) + (volume*per_vol_rate)
    return container_charge,round(container_charge*quantity,2)
