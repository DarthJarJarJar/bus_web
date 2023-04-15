import requests
import xmltodict


# https://retro.umoiq.com/service/publicXMLFeed?command=routeList&a=ttc

def get_routes():
    url = fr"https://retro.umoiq.com/service/publicXMLFeed?command=routeList&a=ttc"

    response = requests.get(url)

    data = xmltodict.parse(response.content)

    d = data["body"]["route"]

    final = []

    for route in d:
        r = {"tag": route["@tag"], "title": route["@title"], "showing": False, "id": int(route["@tag"])}

        final.append(r)

    return final




def get_data(timeobject, route):
    t = int(timeobject.time())

    if route[-1] == ',':
        route = route[0:len(route)-1]

    #route = 102,7,129

    routeList = route.split(",")
    final = []
    print(routeList)
    for r in routeList:


        url = fr"https://retro.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&r={r}&t={t}"

        response = requests.get(url)
        data = xmltodict.parse(response.content)

        d = data["body"]["vehicle"]

        for vehicle in d:
            a = {
                "heading": vehicle["@heading"],
                "id": vehicle["@id"],
                "lat": vehicle["@lat"],
                "lon": vehicle["@lon"],
                "predictable": vehicle["@predictable"],
                "routeTag": vehicle["@routeTag"],
                "secsSinceReport": vehicle["@secsSinceReport"],
                "speed": vehicle["@speedKmHr"]
            }

            if "@dirTag" in vehicle:
                a["dirTag"] = vehicle["@dirTag"]
                x = vehicle["@dirTag"].split("_")
                a["route"] = x[2]
                if x[1] == "0":
                    a["direction"] = "S"
                else:
                    a["direction"] = "N"

            else:
                a["dirTag"] = ""
                a["direction"] = ""
                a["route"] = vehicle["@routeTag"]

            final.append(a)

    return final


