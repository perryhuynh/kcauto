from sikuli import Region, Pattern, FOREVER
from datetime import datetime, timedelta
from threading import Thread
from kca_globals import Globals
from fleet import Fleet
from lbas import LBAS
from map_data import MapData, Node, UnknownNode
from event_reset import EventReset
from nav import Nav
from util import Util


class CombatModule(object):
    def __init__(self, config, stats, regions, fleets):
        """Initializes the Combat module.

        Args:
            config (Config): kcauto Config instance
            stats (Stats): kcauto Stats instance
            regions (dict): dict of pre-defined kcauto regions
            fleets (dict): dict of active CombatFleet instances
        """
        self.enabled = True
        self.disabled_time = None
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = regions['game']
        self.fast_kc_region = Region(self.kc_region)
        self.fast_kc_region.setAutoWaitTimeout(0)
        self.fleets = fleets
        self.next_combat_time = datetime.now()

        self.combined_fleet = self.config.combat['combined_fleet']
        self.striking_fleet = self.config.combat['striking_fleet']

        self.primary_fleet = fleets[3] if self.striking_fleet else fleets[1]
        self.fleet_icon = 'fleet_icon_standard.png'
        if self.combined_fleet:
            self.fleet_icon = 'fleet_icon_{}.png'.format(
                self.config.combat['fleet_mode'])
        self.dmg = {}

        self.map = MapData(
            self.config, self.regions, self.config.combat['map'])
        self.current_position = [0, 0]
        self.current_node = self.map.unknown_node
        self.current_node_backup = None
        self.nodes_run = []

        self.lbas = (
            LBAS(self.config, self.regions, self.map)
            if self.config.combat['lbas_enabled'] else None)

        self.event_reset = (
            EventReset(self.config, self.stats, self.regions, self.map)
            if self.config.event_reset['enabled'] else None)

        # combat-related regions
        x = self.kc_region.x
        y = self.kc_region.y
        self.module_regions = {
            'game': self.kc_region,
            'check_fatigue': Region(x + 742, y + 196, 35, 440),
            'check_damage': Region(x + 710, y + 195, 20, 440),
            'check_damage_7th': Region(x + 710, y + 570, 20, 64),
            'check_damage_flagship': Region(x + 470, y + 280, 42, 70),
            'check_damage_combat': Region(x + 470, y + 215, 50, 475),
            'observe_region': Region(x + 110, y + 95, 986, 478),
            'event_next': Region(x + 1090, y + 525, 110, 75)
        }

    def goto_combat(self):
        """Method to navigate to the combat menu.
        """
        Nav.goto(self.regions, 'combat')

    def check_need_to_sortie(self):
        """Method to check whether the combat fleets need to sortie based on
        the stored next combat time.

        Returns:
            bool: True if the combat fleets need to sortie, False otherwise
        """
        if not self.enabled:
            return False
        if self.next_combat_time < datetime.now():
            return True
        return False

    def set_next_combat_time(self, delta={}):
        """Method to set the next combat time based on the provided hours,
        minutes, and seconds delta.

        Args:
            delta (dict, optional): dict containing the hours, minutes, and
                seconds delta
        """
        self.next_combat_time = datetime.now() + timedelta(
            hours=delta['hours'] if 'hours' in delta else 0,
            minutes=delta['minutes'] if 'minutes' in delta
            else Globals.COMBAT_BUFFER_MINUTES,
            seconds=delta['seconds'] if 'seconds' in delta else 0)

    def combat_logic_wrapper(self):
        """Method that fires off the necessary child methods that encapsulates
        the entire action of sortieing combat fleets and resolving combat.

        Returns:
            bool: False if the combat fleets could not be sortied
        """
        self.stats.increment_combat_attempted()

        if not self._select_combat_map():
            # Port check or LBAS fatigue check failed; cancel sortie
            return False

        if self._conduct_pre_sortie_checks():
            start_button = 'combat_start.png'
            if (self.lbas and (
                    self.config.combat['lbas_group_1_nodes']
                    or self.config.combat['lbas_group_2_nodes']
                    or self.config.combat['lbas_group_3_nodes'])):
                start_button = 'combat_start_lbas.png'
            # attempt to click sortie start button
            if Util.check_and_click(self.regions['lower_right'], start_button):
                Util.log_msg("Beginning combat sortie.")
            else:
                # generic sortie fail catch
                Util.log_warning("Could not begin sortie for some reason!")
                self.set_next_combat_time({'minutes': 5})
                return False
        else:
            # fleet fatigue/damage check failed; cancel sortie
            return False

        # reset FCF retreat counters for combined and striking fleets
        if self.combined_fleet:
            self.fleets[1].reset_fcf_retreat_counts()
            self.fleets[2].reset_fcf_retreat_counts()
        if self.striking_fleet:
            self.fleets[3].reset_fcf_retreat_counts()

        self._run_combat_logic()
        self.set_next_combat_time()

        # after combat, resolve the FCF retreat counters for combined and
        # striking fleets and add them back to their damage counters
        if self.combined_fleet:
            self.fleets[1].resolve_fcf_retreat_counts()
            self.fleets[2].resolve_fcf_retreat_counts()
            self.fleets[2].damage_counts['repair'] = 0
        if self.striking_fleet:
            self.fleets[3].resolve_fcf_retreat_counts()
            self.fleets[3].damage_counts['repair'] = 0
        else:
            self.fleets[1].damage_counts['repair'] = 0

        return True

    def _select_combat_map(self):
        """Method that goes through the menu and chooses the specified map to
        sortie to. Non-event port checks and LBAS checks are also resolved at
        this point.

        Returns:
            bool: True if the combat map is successfully chosen and started,
                False if a port or LBAS check failed
        """
        Util.rejigger_mouse(self.regions, 'top')

        if self.map.world == 'event':
            Util.wait_and_click(self.regions['lower'], '_event_world.png')
        else:
            Util.wait_and_click_and_wait(
                self.regions['lower'],
                'c_world_{}.png'.format(self.map.world),
                self.kc_region,
                'c_world_{}-1.png'.format(self.map.world))
        Util.rejigger_mouse(self.regions, 'top')

        if self.lbas:
            # resupply and delay sortie time if LBAS fails fatigue check
            lbas_check_fatigue = (
                'CheckFatigue' in self.config.combat['misc_options'])
            pass_lbas_check, delay_time = (
                self.lbas.resupply_groups(lbas_check_fatigue))
            if not pass_lbas_check:
                self.set_next_combat_time({'minutes': delay_time})
                return False

        if self.map.world == 'event':
            for page in range(1, int(self.map.subworld[0])):
                Util.check_and_click(
                    self.kc_region, '_event_next_page_{}.png'.format(page))
                Util.rejigger_mouse(self.regions, 'top')
                Util.kc_sleep(2)
            Util.wait_and_click(
                self.kc_region,
                '_event_world_{}.png'.format(self.map.subworld))
            # dismiss Ooyodo chalkboards
            self.regions['lower'].wait('event_chalkboard.png', 10)
            if self.event_reset and self.event_reset.check_need_to_reset():
                self.event_reset.reset_event_map_progress()
            else:
                while self.regions['lower'].exists('event_chalkboard'):
                    Util.kc_sleep(1)
                    Util.click_preset_region(self.regions, 'center')
                    Util.kc_sleep(1)
                    if self.regions['lower_right'].exists('sortie_select.png'):
                        break
        else:
            if int(self.map.subworld) > 4:
                Util.wait_and_click(
                    self.regions['right'], 'c_world_eo_arrow.png')
                Util.rejigger_mouse(self.regions, 'top')
                Util.kc_sleep(2)
            Util.wait_and_click(self.kc_region, 'c_world_{}-{}.png'.format(
                self.map.world, self.map.subworld))
        self.regions['lower_right'].wait('sortie_select.png')
        if self._delay_from_port_check('select'):
            return False
        Util.check_and_click(self.regions['lower_right'], 'sortie_select.png')
        Util.rejigger_mouse(self.regions, 'top')
        return True

    def _conduct_pre_sortie_checks(self):
        """Method to conduct pre-sortie fatigue and supply checks on the
        combat fleets as needed.

        Returns:
            bool: True if the fleet passes the pre-sortie checks, False
                otherwise
        """
        cancel_sortie = False

        if self.config.combat['fleet_mode'] == 'striking':
            # switch fleet to 3rd fleet if striking fleet
            Util.kc_sleep(1)
            Fleet.switch(self.regions['top_submenu'], 3)

        needs_resupply, self.dmg, fleet_fatigue = (
            self._run_pre_sortie_fleet_check_logic(self.primary_fleet))

        if self.combined_fleet:
            # additional combined fleet checks
            Fleet.switch(self.regions['top_submenu'], 2)
            two_needs_resupply, fleet_two_damages, fleet_two_fatigue = (
                self._run_pre_sortie_fleet_check_logic(self.fleets[2]))
            Fleet.switch(self.regions['top_submenu'], 1)

            self.dmg = self._combine_fleet_damages(self.dmg, fleet_two_damages)
            for key in fleet_fatigue:
                fleet_fatigue[key] = (
                    fleet_fatigue[key] or fleet_two_fatigue[key])

        if needs_resupply:
            Util.log_warning("Canceling combat sortie: resupply required.")
            self.set_next_combat_time()
            cancel_sortie = True

        if 'CheckFatigue' in self.config.combat['misc_options']:
            if fleet_fatigue['high']:
                Util.log_warning(
                    "Canceling combat sortie: fleet has high fatigue.")
                self.set_next_combat_time({'minutes': 25})
                cancel_sortie = True
            elif fleet_fatigue['medium']:
                Util.log_warning(
                    "Canceling combat sortie: fleet has medium fatigue.")
                self.set_next_combat_time({'minutes': 15})
                cancel_sortie = True

        # just use fleet 1's method
        damage_counts_at_threshold = (
            self.primary_fleet.get_damage_counts_at_threshold(
                self.config.combat['repair_limit'], self.dmg))

        if damage_counts_at_threshold > 0:
            Util.log_warning(
                "Canceling combat sortie: {:d} ships above damage threshold."
                .format(damage_counts_at_threshold))
            self.set_next_combat_time()
            cancel_sortie = True

        if self.dmg['repair'] > 0:
            Util.log_warning(
                "Canceling combat sortie: {:d} ships are being repaired."
                .format(self.dmg['repair']))
            self.set_next_combat_time()
            self.primary_fleet.force_check_repair = True
            cancel_sortie = True

        if self._delay_from_port_check('sortie'):
            cancel_sortie = True

        if cancel_sortie:
            return False
        return True

    def _run_pre_sortie_fleet_check_logic(self, fleet):
        """Method that actually does the checking of supplies and damages of
        the fleet during the pre-sortie fleet check. Also includes special
        handling of the 7th ship in striking fleets.

        Args:
            fleet (CombatFleet): CombatFleet instance of fleet being checked

        Returns:
            bool: indicates whether or not the fleed requires resupply
            dict: dict of combat damages
            dict: dict of fleet fatigue
        """
        needs_resupply = False
        if not fleet.check_supplies(self.regions['check_supply']):
            fleet.needs_resupply = True
            needs_resupply = True
        fleet_damages = (
            fleet.check_damages_7th(self.module_regions)
            if self.config.combat['fleet_mode'] == 'striking'
            else fleet.check_damages(self.module_regions['check_damage']))
        fleet.print_damage_counts(repair=True)

        if 'CheckFatigue' in self.config.combat['misc_options']:
            fleet_fatigue = fleet.check_fatigue(
                self.module_regions['check_fatigue'])
            fleet.print_fatigue_states()
            return (needs_resupply, fleet_damages, fleet_fatigue)
        return (needs_resupply, fleet_damages, {})

    def _delay_from_port_check(self, context):
        """Checks to see if the sortie needs to be delayed due to a full port
        and the config that checks for this, or the map being an event map.

        Args:
            context (str): 'select' or 'sortie', depending on which screen the
                warning messages are being checked at

        Returns:
            bool: True if the sortie needs to be cancelled and delayed, False
                otherwise
        """
        full_port = False
        if ('PortCheck' in self.config.combat['misc_options']
                or self.map.world == 'event'):
            # this logic may need to be reworked; the event-time messaging
            # is a bit uncertain at the moment, since this is being revised not
            # during an event
            if context == 'select' and self.map.world != 'event':
                if self.regions['right'].exists('warning_port_full.png'):
                    full_port = True
            elif context == 'sortie' and self.map.world == 'event':
                if self.regions['lower'].exists('warning_port_full_event.png'):
                    full_port = True
        if full_port:
            Util.log_warning("Canceling combat sortie: port is full.")
            self.set_next_combat_time({'minutes': 15})
            return True
        else:
            return False

    def _run_combat_logic(self):
        """Method that contains the logic and fires off necessary child methods
        for resolving anything combat-related. Includes LBAS node assignment,
        compass spins, formation selects, night battle selects, FCF retreats
        for combined fleet, flagship retreats, mid-battle damage checks, and
        resource node ends.
        """
        self.stats.increment_combat_done()

        if self.lbas:
            self.lbas.assign_groups()

        self.primary_fleet.needs_resupply = True
        if self.combined_fleet:
            self.fleets[2].needs_resupply = True

        # primary combat loop
        sortieing = True
        self.current_position = [0, 0]
        self.current_node = self.map.unknown_node
        self.current_node.reset_unknown_node()
        self.nodes_run = []
        disable_combat = False
        post_combat_screens = []
        while sortieing:
            at_node, dialogue_click = self._run_loop_between_nodes()

            if at_node:
                # arrived at combat node
                self._increment_nodes_run()

                # reset ClearStop temp variables
                if 'ClearStop' in self.config.combat['misc_options']:
                    disable_combat = False
                    post_combat_screens = []

                if dialogue_click:
                    # click to get rid of initial boss dialogue in case it
                    # exists
                    Util.kc_sleep(5)
                    Util.click_preset_region(self.regions, 'center')
                    Util.kc_sleep()
                    Util.click_preset_region(self.regions, 'center')
                    Util.rejigger_mouse(self.regions, 'lbas')

                combat_result = self._run_loop_during_battle()

                # resolve night battle
                if combat_result == 'night_battle':
                    if self._select_night_battle(self._resolve_night_battle()):
                        self._run_loop_during_battle()

                self.regions['lower_right_corner'].wait('next.png', 30)

                # battle complete; resolve combat results
                Util.click_preset_region(self.regions, 'center')
                self.regions['game'].wait('mvp_marker.png', 30)
                self.dmg = self.primary_fleet.check_damages(
                    self.module_regions['check_damage_combat'])
                self.primary_fleet.print_damage_counts()
                if 'ClearStop' in self.config.combat['misc_options']:
                    # check for a medal drop here if ClearStop is enabled
                    self.regions['lower_right_corner'].wait('next.png', 30)
                    if self.regions['right'].exists('medal_marker.png'):
                        disable_combat = True
                if self.combined_fleet:
                    self.regions['lower_right_corner'].wait('next.png', 30)
                    Util.click_preset_region(self.regions, 'center')
                    Util.kc_sleep(2)
                    self.regions['game'].wait('mvp_marker.png', 30)
                    fleet_two_damages = self.fleets[2].check_damages(
                        self.module_regions['check_damage_combat'])
                    self.fleets[2].print_damage_counts()
                    self.dmg = self._combine_fleet_damages(
                        self.dmg, fleet_two_damages)
                    # ascertain whether or not the escort fleet's flagship is
                    # damaged if necessary
                    if (fleet_two_damages['heavy'] == 1
                            and not self.fleets[2].flagship_damaged):
                        self.fleets[2].check_damage_flagship(
                            self.module_regions)
                Util.rejigger_mouse(self.regions, 'lbas')
                # click through while not next battle or home
                while not (
                        self.fast_kc_region.exists('home_menu_sortie.png')
                        or self.fast_kc_region.exists(
                            'combat_flagship_dmg.png')
                        or self.fast_kc_region.exists('combat_retreat.png')):
                    if self.regions['lower_right_corner'].exists('next.png'):
                        Util.click_preset_region(self.regions, 'shipgirl')
                        Util.rejigger_mouse(self.regions, 'top')
                        if 'ClearStop' in self.config.combat['misc_options']:
                            post_combat_screens.append('next')
                    elif self.regions['lower_right_corner'].exists(
                            'next_alt.png'):
                        Util.click_preset_region(self.regions, 'shipgirl')
                        Util.rejigger_mouse(self.regions, 'top')
                        if 'ClearStop' in self.config.combat['misc_options']:
                            post_combat_screens.append('next_alt')
                    if self.map.world == 'event':
                        # if the 'next' asset exists in this region during an
                        # event map sortie, the map is cleared. This 'next' is
                        # for the screen indicating the opening of EOs.
                        if self.module_regions['event_next'].exists(
                                'next.png'):
                            Util.click_preset_region(self.regions, 'shipgirl')
                            Util.rejigger_mouse(self.regions, 'top')
                            if ('ClearStop' in self.config.combat[
                                    'misc_options']):
                                disable_combat = True
                    if self.combined_fleet or self.striking_fleet:
                        self._resolve_fcf()
                        Util.rejigger_mouse(self.regions, 'top')

            if self.regions['left'].exists('home_menu_sortie.png'):
                # arrived at home; sortie complete
                self._print_sortie_complete_msg(self.nodes_run)
                sortieing = False
                break

            if self.regions['lower_right'].exists(
                    'combat_flagship_dmg.png'):
                # flagship retreat; sortie complete
                Util.log_msg("Flagship damaged. Automatic retreat.")
                Util.click_preset_region(self.regions, 'shipgirl')
                self.regions['left'].wait('home_menu_sortie.png', 30)
                self._print_sortie_complete_msg(self.nodes_run)
                sortieing = False
                break

            if self.regions['lower_right_corner'].exists('next_alt.png'):
                # resource node end; sortie complete
                while not self.regions['left'].exists('home_menu_sortie.png'):
                    if self.regions['lower_right_corner'].exists('next.png'):
                        Util.click_preset_region(self.regions, 'shipgirl')
                        Util.rejigger_mouse(self.regions, 'top')
                    elif self.regions['lower_right_corner'].exists(
                            'next_alt.png'):
                        Util.click_preset_region(self.regions, 'shipgirl')
                        Util.rejigger_mouse(self.regions, 'top')
                self._print_sortie_complete_msg(self.nodes_run)
                sortieing = False
                break

            if self.kc_region.exists('combat_retreat.png'):
                continue_sortie = self._resolve_continue_sortie()

                # resolve retreat/continue
                if continue_sortie:
                    self._select_continue_sortie(True)
                else:
                    self._select_continue_sortie(False)
                    self.regions['left'].wait('home_menu_sortie.png', 30)
                    self._print_sortie_complete_msg(self.nodes_run)
                    sortieing = False
                    break
        # after sortie is complete, check the dismissed post-combat screens to
        # see if combat should be disabled
        if ('ClearStop' in self.config.combat['misc_options']
                and not disable_combat):
            # TODO: additional logic needed to resolve end of 1-6
            if self.map.world == 'event' and len(post_combat_screens) > 2:
                # event map and more than 2 post-combat screens dismissed;
                # assume that it means that event map is cleared
                disable_combat = True

        # if the disable combat flag is set, disable the combat module
        if disable_combat:
            self.disable_module()

    def _print_sortie_complete_msg(self, nodes_run):
        """Method that prints the post-sortie status report indicating number
        of nodes run and nodes run.

        Args:
            nodes_run (list): list of combat node numbers (legacy mode) or
                Nodes instances (live mode) run in the primary combat logic
        """
        Util.log_success(
            "Sortie complete. Encountered {} combat nodes (nodes {}).".format(
                len(nodes_run), ', '.join(str(node) for node in nodes_run)))

    def _run_loop_between_nodes(self):
        """Method that continuously checks for the next update between combat
        nodes. Resolves compass spins, formation selects, node selects, and
        resource node ends.

        Returns:
            bool: True if the method ends on a combat node, False otherwise
            bool: True if the click to remove boss dialogue should be done,
                False otherwise (only applicable if first bool is True)
        """
        at_node = False

        # if in live engine mode, begin the background observer to track and
        # update the fleet position
        if self.config.combat['engine'] == 'live':
            # reset the current node backup variable every time the observer is
            # started
            self.current_node_backup = None
            self._start_fleet_observer()

        while not at_node:
            if self.fast_kc_region.exists('compass.png'):
                # spin compass
                while (self.kc_region.exists('compass.png')):
                    Util.click_preset_region(self.regions, 'center')
                    Util.rejigger_mouse(self.regions, 'lbas')
                    Util.kc_sleep(3)
            elif (
                    self.regions['formation_line_ahead'].exists(
                        'formation_line_ahead.png')
                    or self.regions['formation_combinedfleet_1'].exists(
                        'formation_combinedfleet_1.png')):
                # check for both single fleet and combined fleet formations
                # since combined fleets can have single fleet battles
                self._stop_fleet_observer()
                self._print_current_node()
                formations = self._resolve_formation()
                for formation in formations:
                    if self._select_formation(formation):
                        break
                Util.rejigger_mouse(self.regions, 'lbas')
                at_node = True
                return (True, True)
            elif self.fast_kc_region.exists('combat_node_select.png'):
                # node select dialog option exists; resolve fleet location and
                # select node
                if self.config.combat['engine'] == 'legacy':
                    # only need to manually update self.current_node if in
                    # legacy engine mode
                    self._update_fleet_position_once()
                if (self.current_node.name
                        in self.config.combat['node_selects']):
                    next_node = self.config.combat['node_selects'][
                        self.current_node.name]
                    Util.log_msg("Selecting Node {} from Node {}.".format(
                        next_node, self.current_node))
                    self.map.nodes[next_node].click_node(self.regions['game'])
                    Util.rejigger_mouse(self.regions, 'lbas')
            elif (self.regions['lower_right_corner'].exists('next.png')
                    or self.fast_kc_region.exists('combat_nb_fight.png')):
                # post-combat or night battle select without selecting a
                # formation
                self._stop_fleet_observer()
                self._print_current_node()
                Util.rejigger_mouse(self.regions, 'lbas')
                at_node = True
                return (True, False)
            elif self.regions['lower_right'].exists(
                    'combat_flagship_dmg.png'):
                # flagship retreat
                self._stop_fleet_observer()
                return (False, False)
            elif self.regions['lower_right_corner'].exists('next_alt.png'):
                # resource node end
                self._stop_fleet_observer()
                return (False, False)

    def _run_loop_during_battle(self):
        """Method that continuously runs during combat for the night battle
        prompt or battle end screen.

        Returns:
            str: 'night_battle' if combat ends on the night battle prompt,
                'results' if otherwise
        """
        while True:
            if self.kc_region.exists('combat_nb_fight.png'):
                return 'night_battle'
            elif self.regions['lower_right_corner'].exists('next.png'):
                return 'results'
            else:
                pass

    def _start_fleet_observer(self):
        """Method that starts the observeRegion/observeInBackground methods
        that tracks the fleet position icon in real-time in the live engine
        mode.
        """
        self.module_regions['observe_region'].onAppear(
            Pattern(self.fleet_icon).similar(Globals.FLEET_ICON_SIMILARITY),
            self._update_fleet_position)
        self.module_regions['observe_region'].observeInBackground(FOREVER)

    def _stop_fleet_observer(self):
        """Stops the observer started by the _start_fleet_observer() method.
        """
        self.module_regions['observe_region'].stopObserver()
        # add sleep to account for async nature of observer overwriting backup
        # node logic
        Util.kc_sleep(1)
        if (type(self.current_node) is UnknownNode
                and type(self.current_node_backup) is Node):
            # on observer stop, if the current node is an UnknowNode but the
            # backup is a valid Node, fallback to the backup since the current
            # node variable was overridden in the last stages before formation
            # select
            self.current_node = self.current_node_backup

    def _update_fleet_position(self, event):
        """Method that is run by the fleet observer to continuously update the
        fleet's status.

        Args:
            event (event): sikuli observer event
        """
        fleet_match = event.getMatch()
        # lastMatch is based off of screen positions, so subtract game region
        # x and y to get in-game positions
        self.current_position = [
            fleet_match.x + (fleet_match.w / 2) - self.kc_region.x,
            fleet_match.y + fleet_match.h - self.kc_region.y
        ]

        self.current_node = self.map.find_node_by_pos(*self.current_position)
        self.current_node_backup = (
            self.current_node
            if type(self.current_node) is not UnknownNode
            and self.current_node != self.current_node_backup
            else self.current_node_backup)
        # debug console print for the observer's found position of the fleet
        # print("{} {} ({})".format(
        #     self.current_position, self.current_node,
        #     self.current_node_backup))
        event.repeat()

    def _update_fleet_position_once(self):
        """Method that can be called to find and update the fleet's position
        on-demand.
        """
        fleet_match = self.kc_region.find(
            Pattern(self.fleet_icon).similar(Globals.FLEET_ICON_SIMILARITY))
        # lastMatch is based off of screen positions, so subtract game region
        # x and y to get in-game positions
        self.current_position = [
            fleet_match.x + (fleet_match.w / 2) - self.kc_region.x,
            fleet_match.y + fleet_match.h - self.kc_region.y
        ]

        self.current_node = self.map.find_node_by_pos(*self.current_position)
        # debug console print for the method's found position of the fleet
        # print("{} {}".format(self.current_position, self.current_node))
        Util.log_msg("Fleet at node {}.".format(self.current_node))

    def _increment_nodes_run(self):
        """Method to properly append to the nodes_run attribute; the combat
        node number if the engine is in legacy mode, otherwise with the Node
        instance of the encountered node if in live mode
        """
        if self.config.combat['engine'] == 'legacy':
            self.nodes_run.append(len(self.nodes_run) + 1)
        elif self.config.combat['engine'] == 'live':
            self.nodes_run.append(self.current_node)

    def _print_current_node(self):
        """Method to print out which node the fleet is at. Behavior differs
        depending on the combat engine mode.
        """
        if self.config.combat['engine'] == 'legacy':
            Util.log_msg("Fleet at Node #{}".format(len(self.nodes_run) + 1))
        if self.config.combat['engine'] == 'live':
            Util.log_msg("Fleet at Node {}".format(self.current_node))

    def _resolve_formation(self):
        """Method to resolve which formation to select depending on the combat
        engine mode and any custom specified formations.

        Returns:
            tuple: tuple of formations to try in order
        """
        # +1 since this happens before entering a node
        next_node_count = len(self.nodes_run) + 1
        custom_formations = self.config.combat['formations']

        # fall back to combinedfleet 4, then combinedfleet2 for CFs;
        # fall back to vanguard, then double_line for non-CFs
        fallback_formations = (
            ('combinedfleet_4', 'combinedfleet_2')
            if self.combined_fleet
            else ('vanguard', 'double_line'))

        if self.config.combat['engine'] == 'legacy':
            # if legacy engine, custom formation can only be applied on a node
            # count basis; if a custom formation is not defined, default to
            # combinedfleet_4, line_ahead, or vanguard formation if striking
            # fleet
            if next_node_count in custom_formations:
                Util.log_msg(
                    "Custom formation specified for node #{}.".format(
                        next_node_count))
                return (
                    (custom_formations[next_node_count], )
                    + fallback_formations)
            else:
                Util.log_msg(
                    "No custom formation specified for node #{}.".format(
                        next_node_count))
                default_formation = ('line_ahead', )
                if self.combined_fleet:
                    default_formation = ('combinedfleet_4', 'combinedfleet_2')
                elif self.striking_fleet:
                    default_formation = ('vanguard', )
                return default_formation
        elif self.config.combat['engine'] == 'live':
            # if live engine, custom formation can be applied by node name or
            # node count; if a custom formation is not defined, defer to the
            # mapData instance's resolve_formation method
            if (self.current_node and
                    self.current_node.name in custom_formations):
                Util.log_msg(
                    "Custom formation specified for node {}.".format(
                        self.current_node.name))
                return (
                    (custom_formations[self.current_node.name], )
                    + fallback_formations)
            elif next_node_count in custom_formations:
                Util.log_msg(
                    "Custom formation specified for node #{}.".format(
                        next_node_count))
                return (
                    (custom_formations[next_node_count], )
                    + fallback_formations)
            else:
                Util.log_msg(
                    "Formation specified for node {} via map data.".format(
                        self.current_node.name))
                return self.map.resolve_formation(self.current_node)

    def _resolve_night_battle(self):
        """Method to resolve whether or not to conduct night battle depending
        on the combat engine mode and any custom specified night battle modes.

        Returns:
            bool: True if night battle should be conducted, False otherwise
        """
        # no +1 since this happens after entering a node
        next_node_count = len(self.nodes_run)
        custom_night_battles = self.config.combat['night_battles']

        if self.config.combat['engine'] == 'legacy':
            # if legacy engine, custom night battle modes can only be applied
            # on a node count basis; if a custom night battle mode is not
            # defined, default to True
            if next_node_count in custom_night_battles:
                Util.log_msg(
                    "Custom night battle specified for node #{}.".format(
                        next_node_count))
                return custom_night_battles[next_node_count]
            else:
                Util.log_msg(
                    "No night battle specified for node #{}.".format(
                        next_node_count))
                return False
        elif self.config.combat['engine'] == 'live':
            # if live engine, custom night battle modes can be applied by node
            # name or node count; if a custom night battle mode is not defined,
            # defer to the mapData instance's resolve_night_battle method
            if (self.current_node and
                    self.current_node.name in custom_night_battles):
                Util.log_msg(
                    "Custom night battle specified for node {}.".format(
                        self.current_node.name))
                return custom_night_battles[self.current_node.name]
            elif next_node_count in custom_night_battles:
                Util.log_msg(
                    "Custom night battle specified for node #{}.".format(
                        next_node_count))
                return custom_night_battles[next_node_count]
            else:
                Util.log_msg(
                    "Night battle specified for node {} via map data.".format(
                        self.current_node.name))
                return self.map.resolve_night_battle(self.current_node)

    def _resolve_continue_sortie(self):
        """Method to resolve whether or not to continue the sortie based on
        number of nodes run, map data (if applicable), and damage counts.

        Returns:
            bool: True if sortie should be continued, False otherwise
        """
        # check whether to retreat against combat nodes count
        if len(self.nodes_run) >= self.config.combat['combat_nodes']:
            Util.log_msg("Ran the necessary number of nodes. Retreating.")
            return False

        # if on live engine mode, check if the current node is a retreat node
        if self.config.combat['engine'] == 'live':
            if not self.map.resolve_continue_sortie(self.current_node):
                Util.log_msg("Node {} is a retreat node. Retreating.".format(
                    self.current_node))
                return False

        # check whether to retreat against fleet damage state
        threshold_dmg_count = (
            self.primary_fleet.get_damage_counts_at_threshold(
                self.config.combat['retreat_limit'], self.dmg))
        if threshold_dmg_count > 0:
            continue_override = False
            if self.combined_fleet and threshold_dmg_count == 1:
                # if there is only one heavily damaged ship and it is
                # the flagship of the escort fleet, do not retreat
                if (self.fleets[2].damage_counts['heavy'] == 1
                        and self.fleets[2].flagship_damaged):
                    continue_override = True
                    Util.log_msg(
                        "The 1 ship damaged beyond threshold is the escort "
                        "fleet's flagship (unsinkable). Continuing sortie.")
            if not continue_override:
                Util.log_warning(
                    "{} ship(s) damaged above threshold. Retreating.".format(
                        threshold_dmg_count))
                return False
        return True

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

        Returns:
            bool: True if night battle was initiated, False otherwise
        """
        if nb:
            Util.log_msg("Commencing night battle.")
            Util.check_and_click(self.kc_region, 'combat_nb_fight.png')
            self.kc_region.waitVanish('combat_nb_fight.png')
            Util.kc_sleep()
            return True
        else:
            Util.log_msg("Declining night battle.")
            Util.check_and_click(self.kc_region, 'combat_nb_retreat.png')
            self.kc_region.waitVanish('combat_nb_retreat.png')
            Util.kc_sleep()
            return False

    def _select_continue_sortie(self, continue_sortie):
        """Method that selects the sortie continue or retreat button.

        Args:
            continue_sortie (bool): True if the the sortie continue button
            should be pressed, False otherwise
        """
        if continue_sortie:
            Util.log_msg("Continuing sortie.")
            Util.check_and_click(self.kc_region, 'combat_continue.png')
            self.kc_region.waitVanish('combat_continue.png')
            Util.kc_sleep()
        else:
            Util.log_msg("Retreating from sortie.")
            Util.check_and_click(self.kc_region, 'combat_retreat.png')
            self.kc_region.waitVanish('combat_retreat.png')
            Util.kc_sleep()

    def _resolve_fcf(self):
        """Method that resolves the FCF prompt. Does not use FCF if there are
        more than one ship in a heavily damaged state. Supports both combined
        fleet FCF and striking force FCF
        """
        if self.regions['lower_left'].exists('fcf_retreat_ship.png'):
            fcf_retreat = False
            if self.combined_fleet:
                # for combined fleets, check the heavy damage counts of both
                # fleets 1 and 2
                fleet_1_heavy_damage = self.fleets[1].damage_counts['heavy']
                fleet_2_heavy_damage = self.fleets[2].damage_counts['heavy']
                if fleet_1_heavy_damage + fleet_2_heavy_damage == 1:
                    fcf_retreat = True
                    self.fleets[1].increment_fcf_retreat_count()
                    self.fleets[2].increment_fcf_retreat_count()
            elif self.striking_fleet:
                # for striking fleets, check the heavy damage counts of the
                # 3rd fleet
                if self.fleets[3].damage_counts['heavy'] == 1:
                    fcf_retreat = True
                    self.fleets[3].increment_fcf_retreat_count()

            if fcf_retreat:
                if (Util.check_and_click(
                        self.regions['lower'], 'fcf_retreat_ship.png')):
                    # decrement the Combat module's internal dmg count so it
                    # knows to continue sortie to the next node
                    self.dmg['heavy'] -= 1
            else:
                Util.log_warning("Declining to retreat ship with FCF.")
                Util.check_and_click(
                    self.regions['lower'], 'fcf_continue_fleet.png')

    def _combine_fleet_damages(self, main, escort):
        """Method for conveniently combining two damage dicts for combined
        fleets.

        Args:
            main (dict): damage dict of main fleet
            escort (dict): damage dict of escort fleet

        Returns:
            dict: damage dict aggregating all damage counts for both main and
                escort fleets
        """
        combined = {}  # create new to not update by reference
        for key in main:
            combined[key] = main[key] + escort[key]
        return combined

    def disable_module(self):
        Util.log_success("De-activating the combat module.")
        self.enabled = False
        self.disabled_time = datetime.now()

    def enable_module(self):
        Util.log_success("Re-activating the combat module.")
        self.enabled = True
        self.disabled_time = None

    def print_status(self):
        """Method that prints the next sortie time status of the Combat module.
        """
        if self.enabled:
            Util.log_success("Next combat sortie at {}".format(
                self.next_combat_time.strftime('%Y-%m-%d %H:%M:%S')))
        else:
            Util.log_success("Combat module disabled as of {}".format(
                self.disabled_time.strftime('%Y-%m-%d %H:%M:%S')))


class CombatFleet(Fleet):
    def __init__(self, fleet_id):
        """Initializes the CombatFleet object, an extension of the Fleet class.

        Args:
            fleet_id (int): id of the fleet
        """
        self.fleet_id = fleet_id
        self.fleet_type = 'combat'
        self.flagship_damaged = False
        self.damage_counts = {
            'heavy': 0,
            'moderate': 0,
            'minor': 0,
            'repair': 0
        }
        self.force_check_repair = False
        self.damaged_fcf_retreat_count = 0
        self.fatigue = {}

    def reset_fcf_retreat_counts(self):
        """Method for setting the fleet's damaged FCF retreat counter.
        """
        self.damaged_fcf_retreat_count = 0

    def resolve_fcf_retreat_counts(self):
        """Method for resolving the fleet's damaged FCF retreat counter by
        adding it back to the damage counter at the end of a sortie.
        """
        self.damage_counts['heavy'] += self.damaged_fcf_retreat_count
        self.reset_fcf_retreat_counts()

    def increment_fcf_retreat_count(self):
        """Method to increment the FCF retreat count if there is only one
        heavily damaged ship in the fleet, and decrement the heavy damage from
        the damage counter.
        """
        if 'heavy' in self.damage_counts and self.damage_counts['heavy'] == 1:
            Util.log_msg(
                "Retreating damaged ship via FCF from fleet {}."
                .format(self.fleet_id))
            self.damaged_fcf_retreat_count += 1
            self.damage_counts['heavy'] -= 1

    def print_damage_counts(self, repair=False):
        """Method to report the fleet's damage counts in a more human-readable
        format
        """
        if repair:
            Util.log_msg(
                (
                    "Fleet {} damage counts: {} heavy / {} moderate / "
                    "{} minor / {} under repair")
                .format(
                    self.fleet_id, self.damage_counts['heavy'],
                    self.damage_counts['moderate'],
                    self.damage_counts['minor'], self.damage_counts['repair']))
        else:
            Util.log_msg(
                "Fleet {} damage counts: {} heavy / {} moderate / {} minor"
                .format(
                    self.fleet_id, self.damage_counts['heavy'],
                    self.damage_counts['moderate'],
                    self.damage_counts['minor']))

    def print_fatigue_states(self):
        """Method to report the fleet's fatigue state in a more human-readable
        format
        """
        fatigue = 'Rested'
        if self.fatigue['high']:
            fatigue = 'High'
        elif self.fatigue['medium']:
            fatigue = 'Medium'
        Util.log_msg(
            "Fleet {} fatigue state: {}".format(self.fleet_id, fatigue))

    def get_damage_counts_at_threshold(self, threshold, counts={}):
        """Method for returning the number of ships at and below the specified
        damage threshold

        Args:
            threshold (str): the cutoff damage threshold
            counts (dict, optional): optionally passed in damage counts; if not
                specified, the fleet's internally stored damage counter is used
                to calculate the number

        Returns:
            int: the number of ships at or below the damage threshold
        """
        counts = counts if counts else self.damage_counts
        if not counts:
            # counts not initialized; return 0
            return 0

        valid_damages = self.get_damages_at_threshold(threshold)

        count = 0
        for damage in valid_damages:
            count += counts[damage]

        return count

    def check_damages(self, region, reset=True):
        """Method to multithread the detection of damage states of the fleet.

        Args:
            region (Region): Region in which to search for the damage states
            reset (bool, optional): specifies whether or not the damage count
                should be reset to 0

        Returns:
            dict: dict of counts of the different damage states
        """
        thread_check_damages_heavy = Thread(
            target=self._check_damages_func, args=('heavy', region, reset))
        thread_check_damages_moderate = Thread(
            target=self._check_damages_func, args=('moderate', region, reset))
        thread_check_damages_minor = Thread(
            target=self._check_damages_func, args=('minor', region, reset))
        thread_check_damages_repair = Thread(
            target=self._check_damages_func, args=('repair', region, reset))
        Util.multithreader([
            thread_check_damages_heavy, thread_check_damages_moderate,
            thread_check_damages_minor, thread_check_damages_repair])
        return self.damage_counts

    def _check_damages_func(self, type, region, reset):
        """Child multithreaded method for checking damage states.

        Args:
            type (str): which damage state to check for
            region (Region): Region in which to search for the damage state
            reset (bool): specifies whether or not the damage count should be
                reset to 0
        """
        if reset:
            self.damage_counts[type] = 0

        dmg_img = 'ship_state_dmg_{}.png'.format(type)
        count = Util.findAll_wrapper(
            region, Pattern(dmg_img).similar(Globals.DAMAGE_SIMILARITY))

        for i in count:
            self.damage_counts[type] += 1

    def check_damages_7th(self, regions):
        """Method that specifically checks the damage in the 7th ship spot
        of the fleet during the pre-sortie damage check.

        Args:
            regions (dict): dict of pre-defined kcauto regions

        Returns:
            dict: dict of counts of the different damage states, including that
                of the 7th ship
        """
        self.check_damages(regions['check_damage'])
        Util.click_preset_region(regions, '7th_next')
        return self.check_damages(regions['check_damage_7th'], reset=False)

    def check_damage_flagship(self, regions):
        """Method that checks whether or not the flagship of the fleet is
        damaged in the post-combat results screen. Important for ascertaining
        whether or not the flagship of the escort fleet is the ship with heavy
        damage as it is not sinkable.

        Args:
            regions (dict): dict of pre-defined kcauto regions
        """
        if (regions['check_damage_flagship'].exists(Pattern(
                'ship_state_dmg_heavy.png').similar(
                    Globals.FATIGUE_SIMILARITY))):
            self.flagship_damaged = True
        else:
            self.flagship_damaged = False

    def check_fatigue(self, region):
        """Method to multithread the detection of fatigue states of the fleet.

        Args:
            region (Region): Region in which to search for the fatigue states

        Returns:
            dict: dict of bools of the different fatigue states
        """
        thread_check_low_fatigue = Thread(
            target=self._check_fatigue_func, args=('medium', region))
        thread_check_high_fatigue = Thread(
            target=self._check_fatigue_func, args=('high', region))
        Util.multithreader([
            thread_check_low_fatigue, thread_check_high_fatigue])
        return self.fatigue

    def _check_fatigue_func(self, mode, region):
        """Child multithreaded method for checking fatigue states.

        Args:
            type (str): which fatigue state to check for
            region (Region): Region in which to search for the fatigue state
        """
        self.fatigue[mode] = (
            True
            if (region.exists(
                Pattern('ship_state_fatigue_{}.png'.format(mode)).similar(
                    Globals.FATIGUE_SIMILARITY
                ), 1.5))
            else False)

    @staticmethod
    def get_damages_at_threshold(threshold):
        """Method for returning the list of valid damages given a threshold.

        Args:
            threshold (str): the cutoff damage threshold

        Returns:
            list: list of valid damages (heavy, moderate, minor)
        """
        valid_damages = ('heavy', 'moderate', 'minor')
        return valid_damages[:valid_damages.index(threshold) + 1]
