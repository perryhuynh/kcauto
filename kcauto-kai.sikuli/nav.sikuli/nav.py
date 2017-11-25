from sikuli import Pattern
from random import randint, choice
from util import Util


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
            wait_target_region, wait_target):
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
            'wait_target': wait_target
        }

    def navigate_to(self, regions, target):
        """Method that interacts with the game to transition from the current
        node to the destination via the pre-defined connections.

        Args:
            regions (dict): dict of pre-defined kcauto-kai regions
            target (str): name of destination node

        Returns:
            NavNode: NavNode instance of the destination
        """
        if target in self.connections:
            c = self.connections[target]
            Util.rejigger_mouse(regions, 'top')
            Util.wait_and_click(
                regions[c['click_target_region']], c['click_target'])
            Util.rejigger_mouse(regions, 'top')
            regions[c['wait_target_region']].wait(
                Pattern(c['wait_target']).exact(), 60)
            return c['target']
        else:
            Util.log_error(
                "Not possible to navigate to '{}' from {} screen.".format(
                    target, self.name))


class Nav(object):
    """The Nav module which enables navigation and navigation side-stepping.
    All methods are class and static methods; Nav should not be directly
    instantiated.
    """

    # define all the NavNodes first
    home = NavNode('home')
    top_menu = NavNode('top_menu')
    side_menu = NavNode('side_menu')

    quests = NavNode('quests')
    # inventory = NavNode('inventory')

    sortie = NavNode('sortie')
    combat = NavNode('combat')
    pvp = NavNode('pvp')
    expedition = NavNode('expedition')

    fleetcomp = NavNode('fleetcomp')
    resupply = NavNode('resupply')
    equipment = NavNode('equipment')
    repair = NavNode('repair')
    development = NavNode('development')

    # then define all the connections for the nodes
    home.define_connection(
        quests,
        'top_menu', 'top_menu_quests.png',
        'left', 'filter_tab_all_active.png')
    home.define_connection(
        sortie,
        'home_menu', 'home_menu_sortie.png',
        'side_menu', 'side_menu_fleetcomp.png')
    home.define_connection(
        fleetcomp,
        'home_menu', 'home_menu_fleetcomp.png',
        'side_menu', 'side_menu_fleetcomp_active.png')
    home.define_connection(
        resupply,
        'home_menu', 'home_menu_resupply.png',
        'side_menu', 'side_menu_resupply_active.png')
    home.define_connection(
        equipment,
        'home_menu', 'home_menu_equipment.png',
        'side_menu', 'side_menu_equipment_active.png')
    home.define_connection(
        repair,
        'home_menu', 'home_menu_repair.png',
        'side_menu', 'side_menu_repair_active.png')
    home.define_connection(
        development,
        'home_menu', 'home_menu_development.png',
        'side_menu', 'side_menu_development_active.png')

    top_menu.define_connection(
        home,
        'lower_left', 'top_menu_home.png',
        'home_menu', 'home_menu_sortie.png')

    quests.define_connection(
        home,
        'lower_left', 'top_menu_home.png',
        'home_menu', 'home_menu_sortie.png')

    sortie.define_connection(
        combat,
        'game', 'sortie_menu_combat.png',
        'top_submenu', 'sortie_top_menu_combat_active.png')
    sortie.define_connection(
        pvp,
        'game', 'sortie_menu_pvp.png',
        'top_submenu', 'sortie_top_menu_pvp_active.png')
    sortie.define_connection(
        expedition,
        'game', 'sortie_menu_expedition.png',
        'top_submenu', 'sortie_top_menu_expedition_active.png')

    combat.define_connection(
        pvp,
        'top_submenu', 'sortie_top_menu_pvp.png',
        'top_submenu', 'sortie_top_menu_pvp_active.png')
    combat.define_connection(
        expedition,
        'top_submenu', 'sortie_top_menu_expedition.png',
        'top_submenu', 'sortie_top_menu_expedition_active.png')
    pvp.define_connection(
        combat,
        'top_submenu', 'sortie_top_menu_combat.png',
        'top_submenu', 'sortie_top_menu_combat_active.png')
    pvp.define_connection(
        expedition,
        'top_submenu', 'sortie_top_menu_expedition.png',
        'top_submenu', 'sortie_top_menu_expedition_active.png')
    expedition.define_connection(
        combat,
        'top_submenu', 'sortie_top_menu_combat.png',
        'top_submenu', 'sortie_top_menu_combat_active.png')
    expedition.define_connection(
        pvp,
        'top_submenu', 'sortie_top_menu_pvp.png',
        'top_submenu', 'sortie_top_menu_pvp_active.png')

    for node in (
            side_menu, sortie, combat, pvp, expedition, fleetcomp, resupply,
            equipment, repair, development):
        node.define_connection(
            home,
            'side_menu', 'side_menu_home.png',
            'home_menu', 'home_menu_sortie.png')
        node.define_connection(
            fleetcomp,
            'side_menu', 'side_menu_fleetcomp.png',
            'side_menu', 'side_menu_fleetcomp_active.png')
        node.define_connection(
            resupply,
            'side_menu', 'side_menu_resupply.png',
            'side_menu', 'side_menu_resupply_active.png')
        node.define_connection(
            equipment,
            'side_menu', 'side_menu_equipment.png',
            'side_menu', 'side_menu_equipment_active.png')
        node.define_connection(
            repair,
            'side_menu', 'side_menu_repair.png',
            'side_menu', 'side_menu_repair_active.png')
        node.define_connection(
            development,
            'side_menu', 'side_menu_development.png',
            'side_menu', 'side_menu_development_active.png')
        node.define_connection(
            quests,
            'top_menu', 'top_menu_quests.png',
            'left', 'filter_tab_all_active.png')

    @classmethod
    def goto(cls, regions, destination, max_sidestep=1):
        """Method to call to detect the current location and move to the
        specified destination, with or without sidesteps.

        Args:
            regions (dict): dict of pre-defined kcauto-kai regions
            destination (str): name of the destination
            max_sidestep (int, optional): the max number of sidesteps to take;
                in the current implementation the name and type is a misnomer:
                if it is a non-zero number the code will sidestep once,
                otherwise never sidestep (should be renamed to 'sidestep' with
                bool type)

        Returns:
            bool: True if navigation was successful, False if no actions were
                taken
        """
        sidestep = bool(randint(0, max_sidestep))
        Util.rejigger_mouse(regions, 'top')
        Util.kc_sleep()
        # Figure out where we are
        current_location = None
        if regions['home_menu'].exists('home_menu_sortie.png'):
            Util.log_msg("At home")
            current_location = cls.home
        elif regions['side_menu'].exists('side_menu_home.png'):
            Util.log_msg("At side menu")
            current_location = cls.side_menu
        elif regions['lower_left'].exists('top_menu_home.png'):
            Util.log_msg("At top menu")
            current_location = cls.top_menu

        if current_location.name == 'home':
            # Starting from home screen
            if destination == 'home':
                # Already at home
                # Util.log_msg('Already at home.')
                return False
            elif destination == 'refresh_home':
                # Refresh home
                Util.log_msg("Refreshing home.")
                destination = 'home'
                current_location = current_location.navigate_to(
                    regions, cls._choose_sidestep(destination))
            else:
                # Go to and side menu sub screen
                Util.log_msg(
                    "Navigating to {} screen.".format(destination))
                if destination in ('combat', 'pvp', 'expedition'):
                    current_location = current_location.navigate_to(
                        regions, 'sortie')
                else:
                    if sidestep:
                        current_location = current_location.navigate_to(
                            regions, cls._choose_sidestep(destination))
        elif current_location.name == 'side_menu':
            # Starting from a main menu item screen
            if destination in ('home', 'refresh_home'):
                # Go or refresh home
                Util.log_msg('Going home.')
                destination = 'home'
            if sidestep:
                current_location = current_location.navigate_to(
                    regions, cls._choose_sidestep(destination))
        elif current_location.name == 'top_menu':
            # Starting from top menu item. Theoretically, the script should
            # never attempt to go anywhere but home from here
            if destination in ('home', 'refresh_home'):
                Util.log_msg('Going home.')
                destination = 'home'

        current_location.navigate_to(regions, destination)
        return True

    @staticmethod
    def _choose_sidestep(exclude):
        """Method to choose the sidestep destination, excluding the defined
        exclusion choices (typical the destination itself).

        Args:
            exclude (list): list of all destinations that should be excluded
                from the list of available sidestep destinations

        Returns:
            str: sidestep destination
        """
        choices = [
            'fleetcomp', 'resupply', 'equipment', 'repair', 'development']
        if exclude in choices:
            choices.remove(exclude)
        sidestep_destination = choice(choices)
        return sidestep_destination
