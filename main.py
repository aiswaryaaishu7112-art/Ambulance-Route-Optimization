import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

print("=" * 75)
print("                 AMBULANCE ROUTE OPTIMIZATION")
print("              TRAFFIC-AWARE SHORTEST PATH")
print("=" * 75)

# ---------------------------------------------------------
# 1. LOAD ROAD DATA
# ---------------------------------------------------------

data = pd.read_csv("data.csv")

G = nx.Graph()

for _, row in data.iterrows():
    G.add_edge(
        row["From"],
        row["To"],
        distance=row["Distance"],
        time=row["Time"],
        traffic=row["Traffic"]
    )

# ---------------------------------------------------------
# 2. SELECT STARTING LOCATION
# ---------------------------------------------------------

print("\nAvailable Starting Locations:")
print("1. Accident")
print("2. Junction A")
print("3. Junction B")
print("4. Junction C")

choice = input("\nEnter starting location number (1-4): ")

locations = {
    "1": "Accident",
    "2": "Junction A",
    "3": "Junction B",
    "4": "Junction C"
}

if choice not in locations:
    print("\nInvalid choice. Please run the program again.")
    exit()

start = locations[choice]

# ---------------------------------------------------------
# 3. HOSPITALS
# ---------------------------------------------------------

hospitals = [
    "Hospital A",
    "Hospital B",
    "Hospital C"
]

print()
print("=" * 75)
print(f"Starting Location : {start}")
print("=" * 75)

# ---------------------------------------------------------
# 4. FIND SHORTEST ROUTE BY DISTANCE
# ---------------------------------------------------------

distance_results = []

print("\nSHORTEST DISTANCE ANALYSIS")
print("-" * 75)

for hospital in hospitals:

    route = nx.shortest_path(
        G,
        source=start,
        target=hospital,
        weight="distance"
    )

    distance = nx.shortest_path_length(
        G,
        source=start,
        target=hospital,
        weight="distance"
    )

    travel_time = 0

    for i in range(len(route) - 1):
        travel_time += G[route[i]][route[i + 1]]["time"]

    distance_results.append(
        (hospital, distance, travel_time, route)
    )

    print(f"\n{hospital}")
    print(f"Route       : {' -> '.join(route)}")
    print(f"Distance    : {distance} km")
    print(f"Travel Time : {travel_time} minutes")

# ---------------------------------------------------------
# 5. FIND FASTEST ROUTE BY TIME
# ---------------------------------------------------------

time_results = []

print("\n")
print("=" * 75)
print("FASTEST ROUTE ANALYSIS")
print("=" * 75)

for hospital in hospitals:

    route = nx.shortest_path(
        G,
        source=start,
        target=hospital,
        weight="time"
    )

    travel_time = nx.shortest_path_length(
        G,
        source=start,
        target=hospital,
        weight="time"
    )

    distance = 0

    for i in range(len(route) - 1):
        distance += G[route[i]][route[i + 1]]["distance"]

    time_results.append(
        (hospital, distance, travel_time, route)
    )

    print(f"\n{hospital}")
    print(f"Route       : {' -> '.join(route)}")
    print(f"Distance    : {distance} km")
    print(f"Travel Time : {travel_time} minutes")

# ---------------------------------------------------------
# 6. BEST HOSPITAL BASED ON FASTEST TIME
# ---------------------------------------------------------

best_hospital, best_distance, best_time, best_route = min(
    time_results,
    key=lambda x: x[2]
)

# ---------------------------------------------------------
# 7. FINAL DECISION
# ---------------------------------------------------------

print()
print("=" * 75)
print("                       OPTIMAL DECISION")
print("=" * 75)

print(f"Best Hospital    : {best_hospital}")
print(f"Optimal Route    : {' -> '.join(best_route)}")
print(f"Minimum Distance : {best_distance} km")
print(f"Minimum Time     : {best_time} minutes")

print("=" * 75)

# ---------------------------------------------------------
# 8. TRAFFIC INFORMATION FOR SELECTED ROUTE
# ---------------------------------------------------------

print("\nTRAFFIC CONDITIONS ON OPTIMAL ROUTE")
print("-" * 75)

for i in range(len(best_route) - 1):

    u = best_route[i]
    v = best_route[i + 1]

    traffic = G[u][v]["traffic"]

    print(f"{u} -> {v} : {traffic} traffic")

# ---------------------------------------------------------
# 9. DRAW NETWORK GRAPH
# ---------------------------------------------------------

plt.figure(figsize=(14, 9))

pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=2500,
    node_color="lightblue",
    font_size=10,
    font_weight="bold"
)

# Edge labels
edge_labels = {}

for u, v, attributes in G.edges(data=True):

    edge_labels[(u, v)] = (
        f"{attributes['distance']} km\n"
        f"{attributes['time']} min\n"
        f"{attributes['traffic']}"
    )

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_size=8
)

# Highlight optimal route
route_edges = list(zip(best_route, best_route[1:]))

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=route_edges,
    width=4,
    edge_color="red"
)

plt.title(
    f"Optimal Ambulance Route\n"
    f"{best_hospital} | {best_distance} km | {best_time} minutes"
)

plt.show()