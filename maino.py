import csv
import math
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
def euclidean_distance(coord1, coord2):
    return math.hypot(coord1[0] - coord2[0], coord1[1] - coord2[1])


def create_data_model(students, buses, school=(0, 0)):
    data = {}

    # Locations: first node = school, then all students
    locations = [school] + [s['coords'] for s in students]
    data['locations'] = locations

    # Distance matrix
    size = len(locations)
    distance_matrix = {}
    for i in range(size):
        distance_matrix[i] = {}
        for j in range(size):
            distance_matrix[i][j] = int(euclidean_distance(locations[i], locations[j]) * 1000)  # integer
    data['distance_matrix'] = distance_matrix

    # Demands: school=0, each student=1 seat
    data['demands'] = [0] + [1] * len(students)

    # Vehicle capacities
    data['vehicle_capacities'] = [bus['capacity'] for bus in buses]

    data['num_vehicles'] = len(buses)
    data['depot'] = 0  # school index
    return data


def print_solution(data, manager, routing, solution, students, buses):
    total_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = f"\nBus {buses[vehicle_id]['id']} (Capacity {buses[vehicle_id]['capacity']})\n"
        route_students = []
        route = []
        route_distance = 0

        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            if node_index != 0:  # skip school
                student = students[node_index - 1]
                route_students.append(student['name'])
            route.append(data['locations'][node_index])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

        # back to school
        route.append(data['locations'][0])
        plan_output += f"Assigned Students: {route_students}\n"
        plan_output += f"Route: {route}\n"
        plan_output += f"Distance: {route_distance/1000:.2f}\n"
        print(plan_output)
        total_distance += route_distance
    print(f"Total Distance of all buses: {total_distance/1000:.2f}")

def load_students(csv_file):
    students = []
    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({
                "id": int(row['id']),
                "name": row['name'],
                "coords": (float(row['x']), float(row['y']))
            })
    return students


def load_buses(csv_file):
    buses = []
    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            buses.append({
                "id": int(row['id']),
                "capacity": int(row['capacity'])
            })
    return buses

def main():
    students = load_students("students.csv")
    buses = load_buses("buses.csv")

    data = create_data_model(students, buses)

    # Routing Mananging Index
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Routing model
    routing = pywrapcp.RoutingModel(manager)

    # Distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Capacity constraint
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        data['vehicle_capacities'],
        True,
        'Capacity'
    )

    # Search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters.time_limit.seconds = 5  # optimization time

    # Solve
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        print_solution(data, manager, routing, solution, students, buses)


if __name__ == '__main__':
    main()
