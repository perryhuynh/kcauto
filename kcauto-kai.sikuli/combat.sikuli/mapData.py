from sikuli import Location, Button
import json
import os
from random import randint
from util import Util


class MapData(object):
    location = None
    world = None
    subworld = None
    nodes = {}

    def __init__(self, location, regions, config):
        """Initializes a MapData instance. Holds the map and node information
        of the specified map, as well as methods for resolving formation
        and night battle selections based on node data.

        Args:
            location (str): localized map name; should be equivalent to the
                json file name sans extension
            regions (dict): dict of pre-defined kcauto-kai regions
            config (Config): kcauto-kai Config instance
        """
        self.location = location
        self.regions = regions
        self.kc_region = self.regions['game']
        self.config = config

        # load json data for map
        json_path = os.path.join(
            os.getcwd(), 'kcauto-kai.sikuli', 'maps',
            '{}.json'.format(self.location))
        try:
            with open(json_path) as raw_json:
                map_data = json.load(raw_json)
        except:
            Util.log_error(
                "There was an issue opening or loading the specified map file:"
                " {}.json".format(self.location))
            raise

        self.world = map_data['world']
        self.subworld = map_data['subworld']

        # instantiate Node objects for every node
        for node in map_data['nodes']:
            self.nodes[node] = Node(node, map_data['nodes'][node])

    def find_node_by_pos(self, x, y):
        """Method to loop through the nodes on the map and find the node
        matching the provided x and y coordinates.

        Args:
            x (int): x coordinate of where to search
            y (int): y coordinate of where to search

        Returns:
            Node or None: Node object for node that exists at the coordinates,
                otherwise None if no matching Node object was found
        """
        for node in self.nodes:
            if self.nodes[node].coord_match(x, y):
                return self.nodes[node]
        return None

    def resolve_formation(self, node):
        """Method for determining which node to engage the enemy with on the
        specified node.

        Args:
            node (Node): Node object for the node to determine the formation
                for

        Returns:
            tuple: tuple of formations to try in order
        """
        if node:
            if node.formation:
                return (node.formation, )
            elif 'sub' in node.types:
                if self.config.combat['combined_fleet']:
                    return ('combinedfleet_1', )
                else:
                    return ('line_abreast', )
            elif 'air' in node.types:
                if self.config.combat['combined_fleet']:
                    # formation 3 might not be available possibly due to FCF;
                    # provide formation 4 as fallback
                    return ('combinedfleet_3', 'combinedfleet_4')
                else:
                    return ('diamond', )
            elif 'mixed' in node.types:
                if self.config.combat['combined_fleet']:
                    return ('combinedfleet_2', )
                else:
                    return ('double_line', )
            else:
                if self.config.combat['combined_fleet']:
                    return ('combinedfleet_4', )
                else:
                    return ('line_ahead', )
        else:
            # default to line ahead or combinedfleet 4
            if self.config.combat['combined_fleet']:
                return ('combinedfleet_4', )
            else:
                return ('line_ahead', )

    def resolve_night_battle(self, node):
        """Method for determining whether or not to conduct night battle at the
        specified node.

        Args:
            node (Node): Node object for the node to determine the night battle
                status for

        Returns:
            bool: True if night battle should be conducted at the node, False
                otherwise
        """
        if node:
            if node.night_battle is not None:
                return node.night_battle
            elif 'boss' in node.types:
                return True
            elif 'sub' in node.types or 'air' in node.types:
                return False
            else:
                return False
        else:
            return False


class Node(object):
    name = ''
    coords = []
    types = []
    formation = ''
    night_battle = None

    def __init__(self, name, node_data):
        """Initializes a Node instance for a map.

        Args:
            name (TYPE): Description
            node_data (TYPE): Description
        """
        self.name = name
        self.coords.append(node_data['coords'])
        if 'altCoords' in node_data:
            self.coords.extend(node_data['altCoords'])
        self.types = node_data['types'] if 'types' in node_data else []
        self.formation = (
            node_data['formation'] if 'formation' in node_data else '')
        self.night_battle = (
            node_data['nightBattle'] if 'nightBattle' in node_data else None)

    def coord_match(self, x, y):
        node_buffer = 35 if 'boss' in self.types else 20
        for coord in self.coords:
            min_x = coord[0] - node_buffer
            max_x = coord[0] + node_buffer
            min_y = coord[1] - node_buffer
            max_y = coord[1] + node_buffer
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
            return False

    def click_node(self, kc_region):
        rand_x = kc_region.x + randint(self.coords[0] - 5, self.coords[0] + 5)
        rand_y = kc_region.y + randint(self.coords[1] - 5, self.coords[1] + 5)

        kc_region.mouseMove(Location(rand_x, rand_y))
        kc_region.mouseDown(Button.LEFT)
        Util.kc_sleep()
        kc_region.mouseUp(Button.LEFT)

    def __str__(self):
        return self.name
