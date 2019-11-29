from combat.node import MapNode, EmptyNode


class MapData(object):
    name = None
    world = None
    subworld = None
    panel = None
    page = None
    enemy_context = []
    nodes = {}
    edges = {}

    def __init__(self, enum, data):
        self.name = enum.value
        self.world = data['world']
        self.subworld = data['subworld']
        self.panel = data.get('panel', data['subworld'])
        self.page = data.get('page', 1)
        self.enemy_context = data.get('enemy_context', [])
        for node in data['nodes']:
            node_instance = MapNode(node, data['nodes'][node])
            self.nodes[node_instance.name] = node_instance
        for edge in data['edges']:
            node_a = data['edges'][edge][0]
            node_b = data['edges'][edge][1]
            self.edges[int(edge)] = (
                self.nodes.get(node_a, EmptyNode(node_a)),
                self.nodes.get(node_b, EmptyNode(node_b)))
