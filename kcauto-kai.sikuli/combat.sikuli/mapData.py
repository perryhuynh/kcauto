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
        with open(json_path) as raw_json:
            map_data = json.load(raw_json)

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
        """
        if node:
            if node.formation:
                self._select_formation(node.formation)
            elif 'sub' in node.types:
                if self.config.combat['combined_fleet']:
                    self._select_formation('combinedfleet_1')
                else:
                    self._select_formation('line_abreast')
            elif 'air' in node.types:
                if self.config.combat['combined_fleet']:
                    if not self._select_formation('combinedfleet_3'):
                        # formation 3 not available; possibly due to FCF; fall
                        # back to formation 4
                        self._select_formation('combinedfleet_4')
                else:
                    self._select_formation('diamond')
            else:
                if self.config.combat['combined_fleet']:
                    self._select_formation('combinedfleet_4')
                else:
                    self._select_formation('line_ahead')
        else:
            # default to line ahead or combinedfleet 4
            if self.config.combat['combined_fleet']:
                self._select_formation('combinedfleet_4')
            else:
                self._select_formation('line_ahead')

    def resolve_night_battle(self, node):
        """Method for determining whether or not to conduct night battle at the
        specified node.

        Args:
            node (Node): Node object for the node to determine the night battle
                status for

        Returns:
            bool: True if night battle is conducted at the node, False
                otherwise
        """
        night_battle = False
        if node:
            if node.night_battle is not None:
                self._select_night_battle(node.night_battle)
                night_battle = node.night_battle
            elif 'boss' in node.types:
                self._select_night_battle(True)
                night_battle = True
            elif 'sub' in node.types or 'air' in node.types:
                self._select_night_battle(False)
            else:
                self._select_night_battle(False)
        else:
            self._select_night_battle(False)

        return night_battle

    def select_sortie_continue_retreat(self, retreat):
        """Method that selects the sortie continue or retreat button.

        Args:
            retreat (bool): True if the retreat button should be pressed,
                False otherwise
        """
        if retreat:
            Util.log_msg("Retreating from sortie.")
            Util.check_and_click(self.kc_region, 'combat_retreat.png')
        else:
            Util.log_msg("Continuing sortie.")
            Util.check_and_click(self.kc_region, 'combat_continue.png')

    def _select_formation(self, formation):
        """Method that selects the specified formation on-screen.

        Args:
            formation (str): formation to select

        Returns:
            bool: True if the formation was clicked, False if its button could
                not be found
        """
        Util.log_msg("Engaging the enemy in {} formation.".format(
            formation.replace('_', ' ')))
        return Util.check_and_click(
            self.regions['formation_{}'.format(formation)],
            'formation_{}.png'.format(formation))

    def _select_night_battle(self, nb):
        """Method that selects the night battle sortie button or retreats
        from it.

        Args:
            nb (bool): indicates whether or not night battle should be done or
                not
        """
        if nb:
            Util.log_msg("Commencing night battle.")
            Util.check_and_click(self.kc_region, 'combat_nb_fight.png')
        else:
            Util.log_msg("Declining night battle.")
            Util.check_and_click(self.kc_region, 'combat_nb_retreat.png')


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
        self.coords = node_data['coords']
        self.types = node_data['types'] if 'types' in node_data else []
        self.formation = (
            node_data['formation'] if 'formation' in node_data else '')
        self.night_battle = (
            node_data['nightBattle'] if 'nightBattle' in node_data else None)

    def coord_match(self, x, y):
        node_buffer = 35 if 'boss' in self.types else 20
        min_x = self.coords[0] - node_buffer
        max_x = self.coords[0] + node_buffer
        min_y = self.coords[1] - node_buffer
        max_y = self.coords[1] + node_buffer
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
