import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random

class DataCenterNetwork:
    def __init__(self, num_spines, num_leaves, servers_per_leaf):
        self.num_spines = num_spines
        self.num_leaves = num_leaves
        self.servers_per_leaf = servers_per_leaf
        self.graph = nx.Graph()
        self.links = []
        
        # Costs (Arbitrary values for "Resource Stewardship")
        self.cost_spine = 5000  # Cost per spine switch
        self.cost_leaf = 2500   # Cost per leaf switch
        self.cost_fiber = 50    # Cost per cable
        
    def build_topology(self):
        """Constructs the Leaf-Spine Architecture"""
        print(f"Building Topology: {self.num_spines} Spines, {self.num_leaves} Leaves...")
        
        # 1. Add Spine Switches
        spines = [f"Spine_{i}" for i in range(self.num_spines)]
        self.graph.add_nodes_from(spines, type='spine')
        
        # 2. Add Leaf Switches
        leaves = [f"Leaf_{i}" for i in range(self.num_leaves)]
        self.graph.add_nodes_from(leaves, type='leaf')
        
        # 3. Connect Every Leaf to Every Spine (The "Fabric")
        for spine in spines:
            for leaf in leaves:
                self.graph.add_edge(spine, leaf, bandwidth=100, latency=1) # 100Gbps link
                self.links.append({"source": spine, "target": leaf, "type": "Inter-Switch"})

        # 4. Add Servers and connect to Leaves
        for leaf in leaves:
            for i in range(self.servers_per_leaf):
                server_name = f"Server_{leaf}_{i}"
                self.graph.add_node(server_name, type='server')
                self.graph.add_edge(leaf, server_name, bandwidth=10, latency=2) # 10Gbps link
                self.links.append({"source": leaf, "target": server_name, "type": "Downlink"})

    def calculate_capex(self):
        """Generates the 'Resource Stewardship' Financial Report"""
        num_spines = self.num_spines
        num_leaves = self.num_leaves
        num_servers = num_leaves * self.servers_per_leaf
        num_cables = len(self.links)
        
        total_cost = (num_spines * self.cost_spine) + \
                     (num_leaves * self.cost_leaf) + \
                     (num_cables * self.cost_fiber)
                     
        report = {
            "Total Spines": num_spines,
            "Total Leaves": num_leaves,
            "Total Servers Supported": num_servers,
            "Total Cabling (Links)": num_cables,
            "Estimated CAPEX ($)": f"${total_cost:,}"
        }
        return pd.Series(report)

    def simulate_traffic(self, src_server, dst_server):
        """Simulates a packet moving from Server A to Server B using Dijkstra's Algorithm"""
        try:
            # Dijkstra finds the "shortest path" (lowest latency)
            path = nx.shortest_path(self.graph, source=src_server, target=dst_server, weight='latency')
            latency = nx.shortest_path_length(self.graph, source=src_server, target=dst_server, weight='latency')
            return path, latency
        except nx.NetworkXNoPath:
            return None, -1

    def visualize(self):
        """Draws the network"""
        pos = {}
        # Layered layout: Spines on top, Leaves middle, Servers bottom
        for i, node in enumerate([n for n, d in self.graph.nodes(data=True) if d['type']=='spine']):
            pos[node] = (i * 2, 10)
        for i, node in enumerate([n for n, d in self.graph.nodes(data=True) if d['type']=='leaf']):
            pos[node] = (i * 2, 5)
        for i, node in enumerate([n for n, d in self.graph.nodes(data=True) if d['type']=='server']):
            pos[node] = (i * 0.5, 0)
            
        nx.draw(self.graph, pos, with_labels=False, node_size=50, node_color="skyblue")
        plt.title("Leaf-Spine Data Center Topology")
        plt.show()

# --- EXECUTION ---

# Initialize Data Center: 2 Spines, 4 Leaves, 2 Servers per Leaf
dc = DataCenterNetwork(num_spines=2, num_leaves=4, servers_per_leaf=5)
dc.build_topology()

# 1. Generate Executive Report (The "TPM" Part)
print("--- Executive Capacity Report ---")
print(dc.calculate_capex())

# 2. Run Network Simulation (The "Engineering" Part)
# Pick two random servers
servers = [n for n, d in dc.graph.nodes(data=True) if d['type']=='server']
src, dst = random.sample(servers, 2)
path, latency = dc.simulate_traffic(src, dst)

print("\n--- Network Simulation Results ---")
print(f"Packet Trace: {src} -> {dst}")
print(f"Optimal Path: {path}")
print(f"Total Latency Hops: {latency}")

# 3. Visualize
dc.visualize()