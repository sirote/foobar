"""
Escape Pods
===========
You've blown up the LAMBCHOP doomsday device and relieved the bunnies of their
work duries -- and now you need to escape from the space station as quickly and
as orderly as possible! The bunnies have all gathered in various locations
throughout the station, and need to make their way towards the seemingly
endless amount of escape pods positioned in other parts of the station. You
need to get the numerous bunnies through the various rooms to the escape pods.
Unfortunately, the corridors between the rooms can only fit so many bunnies at
a time. What's more, many of the corridors were resized to accommodate the
LAMBCHOP, so they vary in how many bunnies can move through them at a time.

Given the starting room numbers of the groups of bunnies, the room numbers of
the escape pods, and how many bunnies can fit through at a time in each
direction of every corridor in between, figure out how many bunnies can safely
make it to the escape pods at a time at peak.

Write a function solution(entrances, exits, path) that takes an array of
integers denoting where the groups of gathered bunnies are, an array of
integers denoting where the escape pods are located, and an array of an array
of integers of the corridors, returning the total number of bunnies that can
get through at each time step as an int. The entrances and exits are disjoint
and thus will never overlap. The path element path[A][B] = C describes that the
corridor going from A to B can fit C bunnies at each time step. There are at
most 50 rooms connected by the corridors and at most 2000000 bunnies that will
fit at a time.

For example, if you have:
entrances = [0, 1]
exits = [4, 5]
path = [
[0, 0, 4, 6, 0, 0], # Room 0: Bunnies
[0, 0, 5, 2, 0, 0], # Room 1: Bunnies
[0, 0, 0, 0, 4, 4], # Room 2: Intermediate room
[0, 0, 0, 0, 6, 6], # Room 3: Intermediate room
[0, 0, 0, 0, 0, 0], # Room 4: Escape pods
[0, 0, 0, 0, 0, 0], # Room 5: Escape pods
]

Then in each time step, the following might happen:
0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each
time step. (Note that in this example, room 3 could have sent any variation of
8 bunnies to 4 and 5, such as 2/6 and 6/6, but the final solution remains the
same.)
"""


from collections import defaultdict, deque


INF = float('inf')
SOURCE = object()
SINK = object()


def solution(entrances, exits, path):
    """Find the  maximum bunnies that can escape at each time step."""
    graph = create_graph(entrances, exits, path)
    return max_flow(graph)


def create_graph(entrances, exits, path):
    """Create a weighted graph with a single source and sink."""
    graph = defaultdict(dict)

    for entrance in entrances:
        graph[SOURCE][entrance] = INF

    for exit_ in exits:
        graph[exit_][SINK] = INF

    for i, row in enumerate(path):
        for j, capacity in enumerate(row):
            graph[i][j] = capacity

    return graph


def max_flow(graph):
    """Find the maximum flow from source to sink using Ford-Fulkerson
    algorithm.
    """
    forward = make_forward(graph)
    backward = transpose(forward)
    weights = defaultdict(int)

    def update_state(path, flow):
        node = SINK
        while node != SOURCE:
            node, neighbor = path[node], node
            if neighbor in forward[node]:
                weights[node, neighbor] += flow
            else:
                weights[neighbor, node] -= flow

    while True:
        path, flow = bfs(graph, forward, backward, weights)
        if flow == 0:
            break

        update_state(path, flow)

    return sum(weights[SOURCE, neighbor] for neighbor in forward[SOURCE])


def make_forward(graph):
    """Create a graph with only forward edges."""
    return {
        node: {
            neighbor
            for neighbor, capacity in neighbor_to_capacity.items()
            if capacity
        }
        for node, neighbor_to_capacity in graph.items()
    }


def transpose(graph):
    """Reverse the direction of the edges in the graph."""
    backward = defaultdict(set)
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            backward[neighbor].add(node)
    return backward


def bfs(graph, forward, backward, weights):
    """Find the shortest path and its flow value from source to sink."""
    path = {SOURCE: None}
    flows = {SOURCE: INF}
    queue = deque([SOURCE])

    def update_state(neighbor, weight):
        if neighbor in path or weight == 0:
            return

        path[neighbor] = node
        flows[neighbor] = min(flows[node], weight)
        queue.append(neighbor)

    while queue:
        node = queue.popleft()
        if node == SINK:
            return path, flows[SINK]

        for neighbor in forward[node]:
            update_state(
                neighbor,
                graph[node][neighbor] - weights[node, neighbor],
            )

        for neighbor in backward[node]:
            update_state(
                neighbor,
                weights[neighbor, node],
            )

    return None, 0


if __name__ == '__main__':
    assert solution(
        entrances=[0],
        exits=[3],
        path=[
            [0, 7, 0, 0],
            [0, 0, 6, 0],
            [0, 0, 0, 8],
            [9, 0, 0, 0]
        ],
    ) == 6
    assert solution(
        entrances=[0, 1],
        exits=[4, 5],
        path=[
            [0, 0, 4, 6, 0, 0],
            [0, 0, 5, 2, 0, 0],
            [0, 0, 0, 0, 4, 4],
            [0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ],
    ) == 16
