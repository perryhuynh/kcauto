import api.api_core as api
import util.kca as kca_u
from constants import NEAR_EXACT
from kca_enums.kcsapi_paths import KCSAPIEnum
from util.logger import Log


class NavNodes(object):
    def __init__(self):
        # define all the NavNodes first
        self.home = NavNode('home')
        self.top_menu = NavNode('top_menu')
        self.side_menu = NavNode('side_menu')

        self.quest = NavNode('quest')

        self.sortie = NavNode('sortie')
        self.combat = NavNode('combat')
        self.pvp = NavNode('pvp')
        self.expedition = NavNode('expedition')

        self.fleetcomp = NavNode('fleetcomp')
        self.resupply = NavNode('resupply')
        self.equipment = NavNode('equipment')
        self.repair = NavNode('repair')
        self.development = NavNode('development')

        # then define all the connections for the nodes
        self.home.define_connection(
            self.quest,
            'top_menu', 'QUEST_MENU',
            'left', 'quest|filter_tab_all_active.png',
            KCSAPIEnum.QUEST_LIST)
        self.home.define_connection(
            self.sortie,
            'home_menu', 'nav|home_menu_sortie.png',
            'side_menu', 'nav|side_menu_fleetcomp.png')
        self.home.define_connection(
            self.fleetcomp,
            'home_menu', 'nav|home_menu_fleetcomp.png',
            'upper', 'shipswitcher|shiplist_button.png',
            KCSAPIEnum.FLEETCOMP_PRESETS)
        self.home.define_connection(
            self.resupply,
            'home_menu', 'nav|home_menu_resupply.png',
            'lower_right', 'resupply|resupply_all_done.png')
        self.home.define_connection(
            self.equipment,
            'home_menu', 'nav|home_menu_equipment.png',
            'lower_right', 'nav|screen_equipment_ready.png')
        self.home.define_connection(
            self.repair,
            'home_menu', 'nav|home_menu_repair.png',
            'upper_left', 'nav|screen_repair_ready.png',
            KCSAPIEnum.REPAIR_DOCKS)
        self.home.define_connection(
            self.development,
            'home_menu', 'nav|home_menu_development.png',
            'upper_left', 'nav|screen_development_ready.png')

        self.top_menu.define_connection(
            self.home,
            'lower_left', 'nav|top_menu_home.png',
            'home_menu', 'nav|home_menu_sortie.png',
            KCSAPIEnum.PORT)

        self.quest.define_connection(
            self.home,
            'lower_left', 'nav|top_menu_home.png',
            'home_menu', 'nav|home_menu_sortie.png',
            KCSAPIEnum.PORT)

        self.sortie.define_connection(
            self.combat,
            'kc', 'nav|sortie_menu_combat.png',
            'top_submenu', 'nav|sortie_top_menu_combat_active.png',
            KCSAPIEnum.SORTIE_MAPS)
        self.sortie.define_connection(
            self.pvp,
            'kc', 'nav|sortie_menu_pvp.png',
            'top_submenu', 'nav|sortie_top_menu_pvp_active.png',
            KCSAPIEnum.PVP_LIST)
        self.sortie.define_connection(
            self.expedition,
            'kc', 'nav|sortie_menu_expedition.png',
            'top_submenu', 'nav|sortie_top_menu_expedition_active.png',
            KCSAPIEnum.EXPEDITION_LIST)

        self.combat.define_connection(
            self.pvp,
            'top_submenu', 'nav|sortie_top_menu_pvp.png',
            'top_submenu', 'nav|sortie_top_menu_pvp_active.png',
            KCSAPIEnum.PVP_LIST)
        self.combat.define_connection(
            self.expedition,
            'top_submenu', 'nav|sortie_top_menu_expedition.png',
            'top_submenu', 'nav|sortie_top_menu_expedition_active.png',
            KCSAPIEnum.EXPEDITION_LIST)
        self.pvp.define_connection(
            self.combat,
            'top_submenu', 'nav|sortie_top_menu_combat.png',
            'top_submenu', 'nav|sortie_top_menu_combat_active.png',
            KCSAPIEnum.SORTIE_MAPS)
        self.pvp.define_connection(
            self.expedition,
            'top_submenu', 'nav|sortie_top_menu_expedition.png',
            'top_submenu', 'nav|sortie_top_menu_expedition_active.png',
            KCSAPIEnum.EXPEDITION_LIST)
        self.expedition.define_connection(
            self.combat,
            'top_submenu', 'nav|sortie_top_menu_combat.png',
            'top_submenu', 'nav|sortie_top_menu_combat_active.png',
            KCSAPIEnum.SORTIE_MAPS)
        self.expedition.define_connection(
            self.pvp,
            'top_submenu', 'nav|sortie_top_menu_pvp.png',
            'top_submenu', 'nav|sortie_top_menu_pvp_active.png',
            KCSAPIEnum.PVP_LIST)

        for node in (
                self.side_menu, self.sortie, self.combat, self.pvp,
                self.expedition, self.fleetcomp, self.resupply,
                self.equipment, self.repair, self.development):
            node.define_connection(
                self.home,
                'side_menu', 'nav|side_menu_home.png',
                'home_menu', 'nav|home_menu_sortie.png',
                KCSAPIEnum.PORT)
            node.define_connection(
                self.fleetcomp,
                'side_menu', 'nav|side_menu_fleetcomp.png',
                'upper', 'shipswitcher|shiplist_button.png',
                KCSAPIEnum.FLEETCOMP_PRESETS)
            node.define_connection(
                self.resupply,
                'side_menu', 'nav|side_menu_resupply.png',
                'lower_right', 'resupply|resupply_all_done.png')
            node.define_connection(
                self.equipment,
                'side_menu', 'nav|side_menu_equipment.png',
                'lower_right', 'nav|screen_equipment_ready.png')
            node.define_connection(
                self.repair,
                'side_menu', 'nav|side_menu_repair.png',
                'upper_left', 'nav|screen_repair_ready.png',
                KCSAPIEnum.REPAIR_DOCKS)
            node.define_connection(
                self.development,
                'side_menu', 'nav|side_menu_development.png',
                'upper_left', 'nav|screen_development_ready.png')
            node.define_connection(
                self.quest,
                'top_menu', 'QUEST_MENU',
                'left', 'quest|filter_tab_all_active.png',
                KCSAPIEnum.QUEST_LIST)


class NavNode(object):
    def __init__(self, name):
        """Initializes a NavNode instance, which represents a node in the
        navigation tree.

        Args:
            name (str): name (in-game location) of the node
        """
        self.name = name
        self.connections = {}

    def define_connection(
            self, connection, click_target_region, click_target,
            wait_target_region, wait_target, api_target=KCSAPIEnum.NONE):
        """Method to define the various out-going direct connections this node
        has to other nodes. A node can have multiple out-going connections.

        Args:
            connection (str): name (in-game location) of the out-going
                connection
            click_target_region (Region): where to search for the click target
                that will move the game from the current node to the
                destination node
            click_target (str): the click target asset name that will move the
                game from the current node to the destination node
            wait_target_region (Region): where to search for the asset that
                will signal a successful and completed transition to the
                destination node
            wait_target (str): the asset name that will signal a successful
                and completed transition to the destination node
        """
        self.connections[connection.name] = {
            'target': connection,
            'click_target_region': click_target_region,
            'click_target': click_target,
            'wait_target_region': wait_target_region,
            'wait_target': wait_target,
            'api_target': api_target
        }

    def navigate_to(self, target, api_update=True):
        """Method that interacts with the game to transition from the current
        node to the destination via the pre-defined connections.

        Args:
            target (str): name of destination node

        Returns:
            NavNode: NavNode instance of the destination
        """
        if target in self.connections:
            c = self.connections[target]
            kca_u.kca.hover('top')
            if c['click_target'] == 'QUEST_MENU':
                kca_u.kca.click('top_menu_quest')
            else:
                kca_u.kca.wait_and_click(
                    kca_u.kca.r[c['click_target_region']], c['click_target'])
            if api_update:
                api.api.update_from_api({c['api_target']})
            kca_u.kca.hover('top')
            kca_u.kca.sleep()
            kca_u.kca.wait(
                kca_u.kca.r[c['wait_target_region']], c['wait_target'], 20,
                NEAR_EXACT)
            return c['target']
        else:
            Log.log_error(
                f"Not possible to navigate to '{target}' from {self.name} "
                "screen.")


nav_nodes = NavNodes()
