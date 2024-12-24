import heapq

from kryptikkaocutils.Timer import timer


class Node:
    def __init__(self, id: str, neighbor: str):
        self.id = id
        self.neighbors = {neighbor}

    def add_neighbor(self, other):
        self.neighbors.add(other)


class Network:
    def __init__(self, connections: list[str]):
        self.nodes = {}
        self.triplets = set()
        for connection in connections:
            id1, id2 = connection.strip().split("-")
            self.add_nodes(id1, id2)
            self.check_triplets(id1, id2)

    def add_nodes(self, id1, id2):
        if id1 not in self.nodes:
            self.nodes[id1] = Node(id1, id2)
        else:
            self.nodes[id1].add_neighbor(id2)
        if id2 not in self.nodes:
            self.nodes[id2] = Node(id2, id1)
        else:
            self.nodes[id2].add_neighbor(id1)

    def check_triplets(self, id1, id2):
        for neighbor in self.nodes[id1].neighbors:
            if neighbor in self.nodes[id2].neighbors:
                self.triplets.add((id1, id2, neighbor))

    def count_triplets(self, starts):
        count = 0
        for triplet in self.triplets:
            for item in triplet:
                if starts == item[0]:
                    count += 1
                    break
        return count

    def all_connected(self, nodes):
        return all(
            [
                n2 in self.nodes[n1].neighbors
                for n1 in nodes
                for n2 in nodes
                if n1 < n2
            ]
        )

    def password(self):
        neighbor_list = [
            self.nodes[node].neighbors.union({node}) for node in self.nodes
        ]

        queue = [(-len(neighbors), neighbors) for neighbors in neighbor_list]
        while queue:
            priority, nodes = heapq.heappop(queue)
            if self.all_connected(nodes):
                return ",".join(sorted(nodes))
            for node in nodes:
                heapq.heappush(queue, (priority + 1, nodes - {node}))
        return ""


@timer
def part1():
    print(network.count_triplets("t"))


@timer
def part2():
    print(network.password())


if __name__ == "__main__":
    connections = open("i.txt").readlines()
    network = Network(connections)
    part1()
    part2()
