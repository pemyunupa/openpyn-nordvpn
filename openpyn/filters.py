import operator
import sys
from openpyn import locations


def filter_by_area(area, type_country_filtered):
    remaining_servers = []
    resolved_locations = locations.get_unique_locations(list_of_servers=type_country_filtered)
    for aServer in type_country_filtered:
        for item in resolved_locations:
            if aServer["location"]["lat"] == item[1]["lat"] and \
                    aServer["location"]["long"] == item[1]["long"] and area in item[2]:
                aServer["location_names"] = item[2]  # add location info to server
                # print(aServer)
                remaining_servers.append(aServer)
    return remaining_servers


def filter_by_country(country_code, type_filtered_servers):
    remaining_servers = []
    for aServer in type_filtered_servers:
        if aServer["domain"][:2].lower() == country_code.lower():
            remaining_servers.append(aServer)
            # print(aServer["domain"])
    return remaining_servers


def filter_by_type(json_response, p2p, dedicated, double_vpn, tor_over_vpn, anti_ddos, netflix):
    remaining_servers = []
    serverCount = 0
    netflix_srv = [[707, 710, "us"], [722, 733, "us"], [868, 875, "us"], [884, 887, "us"],
                   [940, 947, "us"], [952, 963, "us"], [980, 987, "us"], [1074, 1153, "us"],
                   [1154, 1195, "us"], [1196, 1287, "us"], [1289, 1292, "us"], [1297, 1312, "us"],
                   [1314, 1317, "us"], [1322, 1353, "us"], [1358, 1365, "us"], [1370, 1385, "us"],
                   [1394, 1421, "us"], [1422, 1457, "us"], [15, 20, "uk"], [30, 34, "uk"],
                   [36, 41, "uk"], [47, 51, "uk"], [53, 101, "uk"], [190, 192, "uk"],
                   [196, 207, "uk"], [228, 239, "uk"], [248, 251, "uk"], [256, 279, "uk"],
                   [300, 323, "uk"], [328, 331, "uk"], [348, 351, "uk"],
                   [30, 44, "fr"], [45, 63, "fr"], [65, 76, "fr"], [77, 80, "fr"],
                   [92, 95, "nl"], [165, 170, "ca"]]

    for eachServer in json_response:
        serverCount += 1
        if netflix:
            for server in netflix_srv:
                for number in range(server[0], server[1] + 1):
                    # print(server[2]+str(number)+".")
                    # print(eachServer["domain"])
                    if server[2] + str(number) + "." in eachServer["domain"]:
                        remaining_servers.append(eachServer)
                        # print(eachServer["domain"])
        for ServerType in eachServer["categories"]:
            # print(eachServer["categories"])
            if p2p and ServerType["name"] == "P2P":
                remaining_servers.append(eachServer)
            if dedicated and ServerType["name"] == "Dedicated IP servers":
                remaining_servers.append(eachServer)
            if double_vpn and ServerType["name"] == "Double VPN":
                remaining_servers.append(eachServer)
            if tor_over_vpn and ServerType["name"] == "Onion Over VPN":
                remaining_servers.append(eachServer)
            if anti_ddos and ServerType["name"] == "Anti DDoS":
                remaining_servers.append(eachServer)
            if p2p is False and dedicated is False and double_vpn is False and \
                    tor_over_vpn is False and anti_ddos is False and netflix is False:
                if ServerType["name"] == "Standard VPN servers":
                    remaining_servers.append(eachServer)
    # print("Total available servers = ", serverCount)
    return remaining_servers


def filter_by_protocol(json_res_list, tcp):
    remaining_servers = []

    for res in json_res_list:
        # when connecting using TCP only append if it supports OpenVPN-TCP
        if tcp is True and res["features"]["openvpn_tcp"] is True:
            remaining_servers.append([res["domain"][:res["domain"].find(".")], res["load"]])
        # when connecting using TCP only append if it supports OpenVPN-TCP
        elif tcp is False and res["features"]["openvpn_udp"] is True:
            remaining_servers.append([res["domain"][:res["domain"].find(".")], res["load"]])
            # print("TCP SERVESR :", res["feature"], res["feature"]["openvpn_tcp"])
    return remaining_servers


# Exclude servers over "max_load" and only keep < "top_servers"
def filter_by_load(server_list, max_load, top_servers):
    remaining_servers = []
    # sort list by the server load
    server_list.sort(key=operator.itemgetter(1))
    # only choose servers with < 70% load then top 10 of them
    for server in server_list:
        server_load = int(server[1])
        # skip if server_load < 4, sometimes they don't work
        if server_load < max_load and len(remaining_servers) < top_servers and server_load > 3:
            remaining_servers.append(server)

    if len(remaining_servers) < 1:    # if no servers under search criteria
        print("There are no servers that satisfy your criteria, please broaden your search.")
        sys.exit()
    return remaining_servers
