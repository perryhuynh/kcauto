from sikuli import Pattern
from datetime import datetime, timedelta
from random import randint
from kca_globals import Globals
from nav import Nav
from util import Util


class QuestModule(object):
    def __init__(self, config, stats, regions):
        """Initializes the Quest module.

        Args:
            config (Config): kcauto-kai Config instance
            stats (Stats): kcauto-kai Stats instance
            regions (dict): dict of pre-defined kcauto-kai regions
        """
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = self.regions['game']
        self.next_reset_time = datetime.now()
        self.quest_list = []
        self.active_quests = []
        self.active_quest_types = []
        self.inactive_quest_types = ['b', 'c', 'd', 'e']
        self.combat_checkpoints = []
        self.pvp_checkpoints = []
        self.expedition_checkpoints = []
        self.loop_checkpoint = None
        self._define_quest_list()

    def goto_quests(self):
        """Method to navigate to the quest menu.
        """
        Nav.goto(self.regions, 'quests')

    def check_need_to_check_quests(self):
        """Method to check whether or not quests need to be checked.

        Returns:
            bool: True if quests need to be checked, False otherwise
        """
        if self._quests_reset():
            # if daily reset is detected (or is first start), always check
            # quests
            Util.log_msg("Quests reset.")
            return True

        combat_checkpoint = next(iter(self.combat_checkpoints), None)
        pvp_checkpoint = next(iter(self.pvp_checkpoints), None)
        expedition_checkpoint = next(iter(self.expedition_checkpoints), None)
        check_quests = False

        # check against the Stats module to see if a checkpoint has been passed
        if combat_checkpoint and combat_checkpoint <= self.stats.combat_done:
            self.combat_checkpoints = [
                c for c in self.combat_checkpoints
                if c > self.stats.combat_done]
            check_quests = True
        if pvp_checkpoint and pvp_checkpoint <= self.stats.pvp_done:
            self.pvp_checkpoints = [
                c for c in self.pvp_checkpoints
                if c > self.stats.pvp_done]
            check_quests = True
        if (expedition_checkpoint
                and expedition_checkpoint <= self.stats.expeditions_received):
            self.expedition_checkpoints = [
                c for c in self.expedition_checkpoints
                if c > self.stats.expeditions_received]
            check_quests = True

        # check against the loop counts
        if (not combat_checkpoint and not pvp_checkpoint
                and not expedition_checkpoint):
            if (self.loop_checkpoint
                    and self.loop_checkpoint <= self.stats.cycles_completed):
                check_quests = True
            else:
                self.loop_checkpoint = (
                    self.stats.cycles_completed +
                    Globals.QUEST_LOOP_CHECK_RATE)
        else:
            self.loop_checkpoint = None

        return check_quests

    def quests_logic_wrapper(self, context='combat'):
        """Method that fires off the necessary child methods that encapsulates
        the entire action of checking and resolving quests.

        Args:
            context (str, optional): specifies if there is a specific context
                for the quests checking
        """
        self._ooyodo_dismiss()
        self.stats.increment_quests_checked()
        checking = True
        while checking:
            checking = self._finish_quests(context)
        self._run_check_quests_wrapper(context)

    def quests_logic_wrapper_fast(self, context='combat'):
        """Method that fires off the necessary child methods that encapsulates
        the action of checking quests. Additional quests to start are only
        checked if quests were finished.

        Args:
            context (str, optional): specifies if there is a specific context
                for the quests checking
        """
        self._ooyodo_dismiss()
        self.stats.increment_quests_checked()
        pre_check_finished_quests = self.stats.quests_finished + 0
        checking = True
        while checking:
            checking = self._finish_quests(context)
        post_check_finished_quests = self.stats.quests_finished
        if post_check_finished_quests > pre_check_finished_quests:
            self._run_check_quests_wrapper(context)

    def print_status(self):
        """Method to print the next checkpoints for checking quests.
        """
        combat_checkpoint = next(iter(self.combat_checkpoints), None)
        pvp_checkpoint = next(iter(self.pvp_checkpoints), None)
        expedition_checkpoint = next(iter(self.expedition_checkpoints), None)

        msg_array = []
        if combat_checkpoint:
            msg_array.append("sortie #{}".format(combat_checkpoint))
        if pvp_checkpoint:
            msg_array.append("PvP #{}".format(pvp_checkpoint))
        if expedition_checkpoint:
            msg_array.append("expedition #{}".format(expedition_checkpoint))
        if self.loop_checkpoint:
            msg_array.append("loop #{}".format(self.loop_checkpoint))

        if len(msg_array) > 0:
            Util.log_success("Next quest check after {}".format(
                ", or ".join(msg_array)))

    def _quests_reset(self):
        """Method that checks and sets the quest reset time.

        Returns:
            bool: True if a quest reset has been detected, False otherwise
        """
        if datetime.now() > self.next_reset_time:
            jst_time = Util.convert_to_jst(datetime.now(), self.config)
            if jst_time.hour > 4:
                # already past the 5 AM reset time; fast forward next reset
                # time to next day
                jst_time += timedelta(days=1)
            jst_time = jst_time.replace(hour=5, minute=randint(0, 5))
            self.next_reset_time = Util.convert_from_jst(jst_time, self.config)
            return True
        return False

    def _ooyodo_dismiss(self):
        """Method to dismiss the Ooyodo popup.
        """
        Util.kc_sleep()
        Util.click_preset_region(self.regions, 'center')
        Util.kc_sleep(2)

    def _run_check_quests_wrapper(self, context):
        """Method that cycles through the daily, weekly, and monthly quest
        filters and run the quest logic on each.

        Args:
            context (str): specifies if there is a specific context for the
                quests checking
        """
        for cycle in ('daily', 'weekly', 'monthly'):
            self._filter_quests(cycle)
            checking = True
            while checking:
                checking = self._run_check_quests_logic(context)

    def _run_check_quests_logic(self, context):
        """Method that finds the quests on screen, reads their rewards,
        identifies the quest based on the rewards, then resolves it as needed.

        Args:
            context (str): specifies if there is a specific context for the
                quests checking

        Returns:
            bool: True if there was a successful and valid move to the next
                page of quests
        """
        self.active_quests = []
        current_active_quest_types = list(self.active_quest_types)
        # depending on quest check context, remove combat or pvp quests
        if context == 'pvp' and 'b' in current_active_quest_types:
            current_active_quest_types.remove('b')
        elif context == 'combat' and 'c' in current_active_quest_types:
            current_active_quest_types.remove('c')
        for quest_type in current_active_quest_types:
            quests = Util.findAll_wrapper(
                self.regions['left'], '{}.png'.format(quest_type))
            for quest in quests:
                quest_bar = quest.nearby(7).right(580)
                quest_bar_click = quest.right(580)
                quest_rewards = (
                    self._read_reward_number('fuel', quest_bar),
                    self._read_reward_number('ammo', quest_bar),
                    self._read_reward_number('steel', quest_bar),
                    self._read_reward_number('bauxite', quest_bar))
                for valid_quest in self.quest_list:
                    if valid_quest['name'][0] != quest_type:
                        # skip checking for the quest if it doesn't match the
                        # icon that was matched
                        continue
                    if valid_quest['rewards'] == quest_rewards:
                        Util.log_msg("Activating quest {}.".format(
                            valid_quest['name']))
                        if quest_bar.exists('quest_in_progress.png'):
                            # quest is already active
                            self._activate_quest(valid_quest)
                            Util.log_msg("Quest {} already active.".format(
                                valid_quest['name']))
                        else:
                            # attempt to click and active quest
                            Util.click_preset_region(
                                self.regions, quest_bar_click)
                            Util.kc_sleep(3, 0.5)
                            if not quest_bar.exists('quest_in_progress.png'):
                                Util.log_msg("Quest queue full.")
                            else:
                                self.active_quests.extend(valid_quest['name'])
                                self._activate_quest(valid_quest)
                                self.stats.increment_quests_started()
        return self._goto_next_page()

    def _activate_quest(self, quest):
        """Method that is called upon a successful quest activation; updates
        the checkpoints for the next quest check time. Does not interact with
        the game directly.

        Args:
            quest (dict): dict of the activated quest's information
        """
        self.active_quests.extend(quest['name'])
        if quest['wait'][0]:
            self.combat_checkpoints.append(
                self.stats.combat_done + quest['wait'][0])
            self.combat_checkpoints.sort()
        if quest['wait'][1]:
            self.pvp_checkpoints.append(
                self.stats.pvp_done + quest['wait'][1])
            self.pvp_checkpoints.sort()
        if quest['wait'][2]:
            self.expedition_checkpoints.append(
                self.stats.expeditions_received + quest['wait'][2])
            self.expedition_checkpoints.sort()

    def _finish_quests(self, context):
        """Method to finish any completed quests on the current filter and
        click through the rewards. Will switch to the next page if it is
        available.

        Args:
            context (str): specifies if there is a specific context for the
                quests checking

        Returns:
            bool: True if there was a successful and valid move to the next
                page of quests
        """
        self._filter_quests('active')
        while Util.check_and_click(
                self.regions['quest_status'], 'quest_completed.png'):
            self.kc_region.wait('quest_reward_accept.png', 30)
            while Util.check_and_click(
                    self.kc_region, 'quest_reward_accept.png'):
                Util.kc_sleep(1)
            self.stats.increment_quests_finished()
        current_inactive_quest_types = list(self.inactive_quest_types)
        # depending on quest check context, remove combat or pvp quests
        if context == 'pvp':
            current_inactive_quest_types.append('b')
        elif context == 'combat':
            current_inactive_quest_types.append('c')
        for quest_type in current_inactive_quest_types:
            while self.regions['left'].exists('{}.png'.format(quest_type)):
                quest = self.regions['left'].getLastMatch()
                Util.click_preset_region(self.regions, quest.right(580))
                Util.kc_sleep(2, 0.5)
        return self._goto_next_page()

    def _goto_next_page(self):
        """Method to navigate to the next page of quests, if available.

        Returns:
            bool: True if there was a valid and successful move to the next
                page of quests, False otherwise
        """
        if Util.check_and_click(
                self.regions['lower'], 'page_next.png',
                Globals.EXPAND['arrow_navigation']):
            Util.kc_sleep(1)
            return True
        return False

    def _filter_quests(self, filter):
        """Method to filter the quests based on the specified filter (active,
        daily, weekly, or monthly)

        Args:
            filter (str): the filter to filter on
        """
        Util.wait_and_click_and_wait(
            self.regions['left'],
            'filter_tab_{}.png'.format(filter),
            self.regions['left'],
            Pattern('filter_tab_{}_active.png'.format(filter)).exact())

    def _read_reward_number(self, type, region):
        """Method to read the resource reward number next to the resource icon.
        Cannot be multithreaded because of its reliance on OCR/Tesseract
        prohibits this from happening.

        Args:
            type (str): name of resource type to read (fuel, bauxite, etc)
            region (Region): the Region of the quest bar

        Returns:
            int: resource reward count read via OCR
        """
        icon_img = 'icon_{}.png'.format(type)
        return Util.read_number(region, icon_img, 'r', 33, 1)

    def _define_quest_list(self):
        """Defines the valid quests based on the supplied kcauto-kai Config.
        """
        self.active_quest_types.append('e')
        self.inactive_quest_types.remove('e')
        self.quest_list.append(get_quest_info('e4'))
        if self.config.combat['enabled']:
            # define combat quests if combat is enabled
            self.active_quest_types.append('b')
            self.inactive_quest_types.remove('b')
            self.quest_list.extend([
                get_quest_info('bd1'),
                get_quest_info('bd2'),
                get_quest_info('bd3'),
                get_quest_info('bd4'),
                get_quest_info('bd5'),
                get_quest_info('bd6'),
                get_quest_info('bd8'),
                get_quest_info('bw1'),
                get_quest_info('bw2'),
                get_quest_info('bw3'),
                get_quest_info('bw4'),
                get_quest_info('bw4.backup'),  # bw4 has some iffy OCR readings
                get_quest_info('bw10'),
                get_quest_info('e3')])
            # define map-specific combat quests
            if self.config.combat['map'][0] == '4':
                self.quest_list.append(get_quest_info('bd6'))
            if self.config.combat['map'][0] == '2':
                self.quest_list.append(get_quest_info('bd7'))
            if self.config.combat['map'] in ('3-3', '3-4', '3-5'):
                self.quest_list.append(get_quest_info('bw6'))
            if self.config.combat['map'] == '4-4':
                self.quest_list.append(get_quest_info('bw7'))
            if self.config.combat['map'] == '5-2':
                self.quest_list.append(get_quest_info('bw8'))
            if self.config.combat['map'] == '2-5':
                self.quest_list.append(get_quest_info('bm1'))
                self.quest_list.append(get_quest_info('bm7'))
            if self.config.combat['map'] == '6-1':
                self.quest_list.append(get_quest_info('bm2'))
            if self.config.combat['map'] == '1-4':
                self.quest_list.append(get_quest_info('bm3'))
            if self.config.combat['map'] == '5-1':
                self.quest_list.append(get_quest_info('bm4'))
            if self.config.combat['map'] == '1-5':
                self.quest_list.append(get_quest_info('bm5'))
            if self.config.combat['map'] == '4-2':
                self.quest_list.append(get_quest_info('bm6'))
        if self.config.pvp['enabled']:
            # define pvp quests if pvp is enabled
            self.active_quest_types.append('c')
            self.inactive_quest_types.remove('c')
            self.quest_list.extend([
                get_quest_info('c2'),
                get_quest_info('c3'),
                get_quest_info('c4'),
                get_quest_info('c8')])
        if self.config.expeditions['enabled']:
            # define expedition quests if expedition is enabled
            self.active_quest_types.append('d')
            self.inactive_quest_types.remove('d')
            self.quest_list.extend([
                get_quest_info('d2'),
                get_quest_info('d3'),
                get_quest_info('d4')])
            # define expedition-specific quests
            if 5 in self.config.expeditions_all:
                self.quest_list.append(get_quest_info('d22'))
            if (37 in self.config.expeditions_all or
                    38 in self.config.expeditions_all):
                self.quest_list.append(get_quest_info('d9'))
                self.quest_list.append(get_quest_info('d11'))


def get_quest_info(quest):
    """Function to return the relevant information for the specified quest.

    Args:
        quest (str): quest to return information for

    Returns:
        dict: dict with the specified quest's wait intervals and rewards
    """
    if quest == 'bd1':
        return {
            'name': 'bd1', 'wait': (1, 0, 0), 'rewards': (50, 50, 0, 0)}
    elif quest == 'bd2':
        return {
            'name': 'bd2', 'wait': (1, 0, 0), 'rewards': (50, 50, 50, 50)}
    elif quest == 'bd3':
        return {
            'name': 'bd3', 'wait': (3, 0, 0), 'rewards': (150, 150, 200, 100)}
    elif quest == 'bd4':
        return {
            'name': 'bd4', 'wait': (3, 0, 0), 'rewards': (150, 150, 150, 300)}
    elif quest == 'bd5':
        return {
            'name': 'bd5', 'wait': (3, 0, 0), 'rewards': (100, 50, 200, 50)}
    elif quest == 'bd6':
        return {
            'name': 'bd6', 'wait': (2, 0, 0), 'rewards': (0, 200, 0, 0)}
    elif quest == 'bd7':
        return {
            'name': 'bd7', 'wait': (5, 0, 0), 'rewards': (300, 0, 0, 200)}
    elif quest == 'bd8':
        return {
            'name': 'bd8', 'wait': (2, 0, 0), 'rewards': (300, 30, 300, 30)}
    elif quest == 'bw1':
        return {
            'name': 'bw1', 'wait': (12, 0, 0), 'rewards': (300, 300, 300, 100)}
    elif quest == 'bw2':
        return {
            'name': 'bw2', 'wait': (5, 0, 0), 'rewards': (0, 500, 0, 500)}
    elif quest == 'bw3':
        return {
            'name': 'bw3', 'wait': (5, 0, 0), 'rewards': (500, 0, 400, 0)}
    elif quest == 'bw4':
        return {
            'name': 'bw4', 'wait': (12, 0, 0), 'rewards': (400, 0, 800, 0)}
    elif quest == 'bw4.backup':
        return {
            'name': 'bw4', 'wait': (12, 0, 0), 'rewards': (400, 0, 500, 0)}
    elif quest == 'bw5':
        return {
            'name': 'bw5', 'wait': (5, 0, 0), 'rewards': (600, 0, 0, 0)}
    elif quest == 'bw6':
        return {
            'name': 'bw6', 'wait': (12, 0, 0), 'rewards': (400, 0, 0, 700)}
    elif quest == 'bw7':
        return {
            'name': 'bw7', 'wait': (5, 0, 0), 'rewards': (300, 300, 400, 300)}
    elif quest == 'bw8':
        return {
            'name': 'bw8', 'wait': (1, 0, 0), 'rewards': (500, 0, 500, 0)}
    elif quest == 'bw9':
        return {
            'name': 'bw9', 'wait': (2, 0, 0), 'rewards': (0, 300, 0, 800)}
    elif quest == 'bw10':
        return {
            'name': 'bw10', 'wait': (15, 0, 0), 'rewards': (100, 0, 0, 0)}
    elif quest == 'bm1':
        return {
            'name': 'bm1', 'wait': (1, 0, 0), 'rewards': (0, 550, 550, 0)}
    elif quest == 'bm2':
        return {
            'name': 'bm2', 'wait': (3, 0, 0), 'rewards': (0, 600, 0, 0)}
    elif quest == 'bm3':
        return {
            'name': 'bm3', 'wait': (1, 0, 0), 'rewards': (500, 0, 0, 300)}
    elif quest == 'bm4':
        return {
            'name': 'bm4', 'wait': (1, 0, 0), 'rewards': (350, 400, 350, 0)}
    elif quest == 'bm5':
        return {
            'name': 'bm5', 'wait': (10, 0, 0), 'rewards': (800, 0, 0, 0)}
    elif quest == 'bm6':
        return {
            'name': 'bm6', 'wait': (1, 0, 0), 'rewards': (0, 0, 600, 800)}
    elif quest == 'bm7':
        return {
            'name': 'bm7', 'wait': (1, 0, 0), 'rewards': (0, 600, 0, 200)}
    elif quest == 'c2':
        return {
            'name': 'c2', 'wait': (0, 3, 0), 'rewards': (50, 0, 50, 0)}
    elif quest == 'c3':
        return {
            'name': 'c3', 'wait': (0, 5, 0), 'rewards': (0, 50, 0, 50)}
    elif quest == 'c4':
        return {
            'name': 'c4', 'wait': (0, 20, 0), 'rewards': (200, 200, 200, 200)}
    elif quest == 'c8':
        return {
            'name': 'c8', 'wait': (0, 7, 0), 'rewards': (0, 400, 0, 200)}
    elif quest == 'd2':
        return {
            'name': 'd2', 'wait': (0, 0, 1), 'rewards': (100, 100, 100, 100)}
    elif quest == 'd3':
        return {
            'name': 'd3', 'wait': (0, 0, 5), 'rewards': (150, 300, 300, 150)}
    elif quest == 'd4':
        return {
            'name': 'd4', 'wait': (0, 0, 15), 'rewards': (300, 500, 500, 300)}
    elif quest == 'd9':
        return {
            'name': 'd9', 'wait': (0, 0, 1), 'rewards': (150, 0, 0, 0)}
    elif quest == 'd11':
        return {
            'name': 'd11', 'wait': (0, 0, 7), 'rewards': (400, 0, 0, 400)}
    elif quest == 'd22':
        return {
            'name': 'd22', 'wait': (0, 0, 4), 'rewards': (1000, 0, 0, 300)}
    elif quest == 'd24':
        return {
            'name': 'd24', 'wait': (0, 0, 4), 'rewards': (800, 0, 0, 0)}
    elif quest == 'e3':
        return {
            'name': 'e3', 'wait': (0, 2, 0), 'rewards': (30, 30, 30, 30)}
    elif quest == 'e4':
        return {
            'name': 'e4', 'wait': (15, 10, 15), 'rewards': (50, 50, 50, 50)}
