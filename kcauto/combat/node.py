from pyvisauto import Region
import util.kca as kca_u


class MapNode(object):
    name = None
    types = []
    x = None
    y = None

    def __init__(self, name, data):
        self.name = name
        self.types = data.get('types', [])
        self.x = data['coords'][0]
        self.y = data['coords'][1]

    @property
    def boss_node(self):
        if 'boss' in self.types:
            return True
        return False

    @property
    def sub_node(self):
        if 'sub' in self.types:
            return True
        return False

    @property
    def air_node(self):
        if 'air' in self.types:
            return True
        return False

    @property
    def selection_node(self):
        if 'select' in self.types:
            return True
        return False

    @property
    def coords(self):
        return (self.x, self.y)

    def select(self):
        kca_u.kca.click(Region(
            kca_u.kca.game_x + self.x - 3,
            kca_u.kca.game_y + self.y - 3,
            7, 7))

    def __str__(self):
        return self.name


class EmptyNode(MapNode):
    def __init__(self, name):
        self.name = name
