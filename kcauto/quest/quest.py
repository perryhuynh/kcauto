from kca_enums.expeditions import ExpeditionEnum
from kca_enums.maps import MapEnum


class Quest(object):
    name = None
    quest_id = None
    interval = ()
    enemy_context = ()
    map_context = ()
    expedition_context = ()

    def __init__(self, name, data):
        self.name = name
        self.quest_id = data['id']
        self.quest_type = data['type']
        self.intervals = tuple(data.get('intervals', (0, 0, 0)))
        self.enemy_context = tuple(data.get('enemy_context', ()))
        map_context = data.get('map_context', ())
        self.map_context = tuple([MapEnum(m) for m in map_context])
        exp_context = data.get('expedition_context', ())
        self.expedition_context = tuple(
            [ExpeditionEnum(e) for e in exp_context])

    def __repr__(self):
        return f"{self.name} (#{self.quest_id})"
