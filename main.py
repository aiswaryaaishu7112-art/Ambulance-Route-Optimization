
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

    adjusted_time = row["Time"] + row["Traffic_Delay"]

    G.add_edge(
        row["From"],
        row["To"],
        distance=row["Distance"],
        time=row["Time"],
        traffic=row["Traffic"],
        traffic_delay=row["Traffic_Delay"],
        adjusted_time=adjusted_time
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
    print("\nInvalid choice. Please run again.")
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

print("\n" + "=" * 75)
print(f"Starting Location : {start}")
print("=" * 75)

# ---------------------------------------------------------
# 4. SHORTEST ROUTE BY DISTANCE
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

    original_time = 0
    traffic_delay = 0

    for i in range(len(route) - 1):

        edge = G[route[i]][route[i + 1]]

        original_time += edge["time"]
        traffic_delay += edge["traffic_delay"]

    adjusted_time = original_time + traffic_delay

    distance_results.append(
        (hospital, distance, adjusted_time, route)
    )

    print(f"\n{hospital}")
    print(f"Route              : {' -> '.join(route)}")
    print(f"Distance           : {distance} km")
    print(f"Original Time      : {original_time} minutes")
    print(f"Traffic Delay      : {traffic_delay} minutes")
    print(f"Adjusted Time      : {adjusted_time} minutes")

# ---------------------------------------------------------
# 5. FASTEST ROUTE USING TRAFFIC-AWARE TIME
# ---------------------------------------------------------

time_results = []

print("\n" + "=" * 75)
print("FASTEST ROUTE ANALYSIS (INCLUDING TRAFFIC)")
print("=" * 75)

for hospital in hospitals:

    route = nx.shortest_path(
        G,
        source=start,
        target=hospital,
        weight="adjusted_time"
    )

    adjusted_time = nx.shortest_path_length(
        G,
        source=start,
        target=hospital,
        weight="adjusted_time"
    )

    distance = 0
    original_time = 0
    traffic_delay = 0

    for i in range(len(route) - 1):

        edge = G[route[i]][route[i + 1]]

        distance += edge["distance"]
        original_time += edge["time"]
        traffic_delay += edge["traffic_delay"]

    time_results.append(
        (hospital, distance, adjusted_time, route)
    )

    print(f"\n{hospital}")
    print(f"Route              : {' -> '.join(route)}")
    print(f"Distance           : {distance} km")
    print(f"Original Time      : {original_time} minutes")
    print(f"Traffic Delay      : {traffic_delay} minutes")
    print(f"Adjusted Time      : {adjusted_time} minutes")

# ---------------------------------------------------------
# 6. SELECT BEST HOSPITAL
# ---------------------------------------------------------

best_hospital, best_distance, best_time, best_route = min(
    time_results,
    key=lambda x: x[2]
)

# ---------------------------------------------------------
# 7. FINAL OPTIMAL DECISION
# ---------------------------------------------------------

print("\n" + "=" * 75)
print("                    OPTIMAL DECISION")
print("=" * 75)

print(f"Best Hospital    : {best_hospital}")
print(f"Optimal Route    : {' -> '.join(best_route)}")
print(f"Minimum Distance : {best_distance} km")
print(f"Minimum Time     : {best_time} minutes")

print("=" * 75)

# ---------------------------------------------------------
# 8. TRAFFIC INFORMATION ON OPTIMAL ROUTE
# ---------------------------------------------------------

print("\nTRAFFIC CONDITIONS ON OPTIMAL ROUTE")
print("-" * 75)

for i in range(len(best_route) - 1):

    u = best_route[i]
    v = best_route[i + 1]

    edge = G[u][v]

    print(f"\n{u} -> {v}")
    print(f"Traffic Condition : {edge['traffic']}")
    print(f"Original Time     : {edge['time']} minutes")
    print(f"Traffic Delay     : {edge['traffic_delay']} minutes")
    print(f"Adjusted Time     : {edge['adjusted_time']} minutes")

# ---------------------------------------------------------
# 9. DRAW ROAD NETWORK GRAPH
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

# Display road information

edge_labels = {}

for u, v, attributes in G.edges(data=True):

    edge_labels[(u, v)] = (
        f"{attributes['distance']} km\n"
        f"{attributes['adjusted_time']} min\n"
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
    f"Traffic-Aware Optimal Ambulance Route\n"
    f"{best_hospital} | {best_distance} km | "
    f"{best_time} minutes"
)

plt.show()
