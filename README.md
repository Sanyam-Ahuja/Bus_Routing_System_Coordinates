# 🚌 Bus Route Optimizer (Coordinates + OR-Tools)

This project demonstrates solving a simplified **School Bus Routing Problem (SBRP)** using 
**Python + Google OR-Tools**, where student locations and school are represented as coordinates.

The program assigns students to buses (respecting bus capacities) and finds optimized routes 
that minimize the **total travel distance of all buses combined**.

---

## 🔹 How It Works

1. **Input Data**
   - `students.csv` contains student IDs, names, and their `(x, y)` coordinates.  
   - `buses.csv` contains bus IDs and their seating capacities.  
   - School is assumed to be at `(0,0)` (can be changed in code).

2. **Distance Matrix**
   - Euclidean distance is used between all points (school + students).  

3. **Optimization (VRP)**
   - OR-Tools `RoutingModel` solves the **Capacitated Vehicle Routing Problem (CVRP)**.  
   - Students are assigned to buses.  
   - Each bus gets an optimized route.  
   - Objective: **minimize total distance across all buses**.  

---

## 🔹 File Formats

### `students.csv`
```csv
id,name,x,y
1,Amit,2,3
2,Simran,5,4
3,Rohit,6,2
4,Meera,4,9
5,Kabir,9,3
6,Sneha,8,6
7,Arjun,3,8
8,Riya,1,7
buses.csv
csv
Copy code
id,capacity
1,4
2,4
🔹 Installation
Clone the repo:

bash
Copy code
git clone https://github.com/YOUR-USERNAME/bus-route-optimizer.git
cd bus-route-optimizer/coordinates_version
Install dependencies:

bash
Copy code
pip install -r requirements.txt
🔹 Run the Optimizer
bash
Copy code
python main.py
🔹 Example Output
less
Copy code
Bus 1 (Capacity 4)
Assigned Students: ['Amit', 'Simran', 'Rohit', 'Kabir']
Route: [(0, 0), (2.0, 3.0), (5.0, 4.0), (6.0, 2.0), (9.0, 3.0), (0, 0)]
Distance: 18.87 km

Bus 2 (Capacity 4)
Assigned Students: ['Meera', 'Sneha', 'Arjun', 'Riya']
Route: [(0, 0), (4.0, 9.0), (8.0, 6.0), (3.0, 8.0), (1.0, 7.0), (0, 0)]
Distance: 20.23 km

Total Distance (all buses): 39.10 km



(Readme Made Using Chatgpt)
