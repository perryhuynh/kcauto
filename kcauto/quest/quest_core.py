import math
from datetime import datetime, timedelta
from pyvisauto import Region
from random import randint

import api.api_core as api
import combat.combat_core as com
import config.config_core as cfg
import stats.stats_core as sts
import util.kca as kca_u
from constants import NEAR_EXACT, PAGE_NAV
from kca_enums.kcsapi_paths import KCSAPIEnum
from quest.quest import Quest
from util.core_base import CoreBase
from util.json_data import JsonData
from util.kc_time import KCTime
from util.logger import Log


class QuestCore(CoreBase):
    QUEST_TYPE_WEIGHTS = {'daily': 1, 'weekly': 2, 'monthly': 3, 'other': 4}
    module_name = 'quest'
    module_display_name = 'Quest'
    quest_reset_time = datetime.now()
    max_quests = None
    quest_id_to_name = {}
    quest_library = {}
    last_checked_context = 'reset'
    next_check_intervals = {}
    cur_page = None
    tot_page = None
    visible_quests = None

    def __init__(self):
        super().__init__()
        self._load_quest_data()

    def _load_quest_data(self):
        Log.log_debug("Loading Quest data.")
        quest_data = JsonData.load_json('data|quests|quests.json')
        for quest_name in quest_data:
            quest = Quest(quest_name, quest_data[quest_name])
            self.quest_library[quest_name] = quest
            self.quest_library[quest.quest_id] = quest
            self.quest_id_to_name[quest_data[quest_name]['id']] = quest_name

    def need_to_check(self, context):
        if datetime.now() > self.quest_reset_time:
            Log.log_debug("Quest check triggered by time.")
            self._reset_next_quest_reset_time()
            return True
        if self._get_quests_to_check_by_interval():
            Log.log_debug("Quest check triggered by interval.")
            return True
        if context is not None and context != self.last_checked_context:
            Log.log_debug("Quest check triggered by context change.")
            return True

    def update_quest_data(self, data):
        self.cur_page = data.get('api_disp_page', 0)
        self.tot_page = data.get('api_page_count', 0)
        self.visible_quests = data['api_list'] if data['api_list'] else []
        Log.log_debug(self.visible_quests_str)

    def manage_quests(self, context=None, fast_check=True):
        # dismiss Ooyodo
        kca_u.kca.r['center'].click()
        kca_u.kca.sleep(1)
        if context and context != self.last_checked_context:
            fast_check = False
            self.last_checked_context = context
        if not context and self.last_checked_context:
            context = self.last_checked_context
        if fast_check:
            if self._turn_in_quests(context):
                self._toggle_quests(context)
        else:
            self._turn_in_quests(context)
            self._toggle_quests(context)
        Log.log_debug(
            f"Tracked quests: {list(self.next_check_intervals.keys())}")

    @property
    def visible_quests_str(self):
        return_string = f"Visible quests: pg{self.cur_page}/{self.tot_page}"
        for q in self.visible_quests:
            if q == -1:
                break
            return_string += f", {q['api_no']} (state:{q['api_state']})"
        return return_string

    def _turn_in_quests(self, context):
        Log.log_debug(
            f"Checking for quests to turn in and deactivate with {context} "
            "context.")
        quest_turned_in = False
        relevant_quests = self._filter_quest_by_context(context)
        interval_check_quests = self._get_quests_to_check_by_interval()
        Log.log_debug(f"Relevant quests: {relevant_quests}")
        Log.log_debug(f"Quests to check: {interval_check_quests}")
        Log.log_debug("Navigating to active quests tab.")
        kca_u.kca.click_existing('left', 'quest|filter_tab_active.png')
        api.api.update_from_api({KCSAPIEnum.QUEST_LIST})
        kca_u.kca.wait(
            'left', 'quest|filter_tab_active_active.png', NEAR_EXACT)
        no_action_taken = False
        while not no_action_taken:
            page_processed = False
            while not page_processed:
                for idx, quest in enumerate(self.visible_quests):
                    if quest == -1:
                        page_processed = True
                        no_action_taken = True
                        break

                    if quest['api_no'] not in self.quest_library:
                        if quest['api_state'] == 3:
                            self._turn_in_quest_idx(idx)
                            quest_turned_in = True
                        else:
                            continue

                    quest_i = self.quest_library[quest['api_no']]
                    if quest['api_state'] == 2 and quest_i in relevant_quests:
                        Log.log_debug(f"Quest {quest_i.name} already active.")
                        if quest_i.name not in self.next_check_intervals:
                            # relevant quest active but not tracked; add to
                            # tracking with fresh intervals
                            self._track_quest(quest_i)
                        elif quest_i.name in interval_check_quests:
                            # quest is expected to be completed, but it isn't;
                            # re-track it with fresh intervals
                            self._track_quest(quest_i)
                    if quest['api_state'] == 3:
                        Log.log_msg(f"Turning in quest {quest_i.name}.")
                        self._turn_in_quest_idx(idx)
                        self._untrack_quest(quest_i)
                        sts.stats.quest.quests_turned_in += 1
                        quest_turned_in = True
                        break
                    if quest_i not in relevant_quests and context is not None:
                        Log.log_msg(f"Deactivating quest {quest_i.name}.")
                        self._click_quest_idx(idx)
                        self._untrack_quest(quest_i)
                        sts.stats.quest.quests_deactivated += 1
                        break
                page_processed = True
            if self.cur_page < self.tot_page:
                kca_u.kca.click_existing(
                    'lower_right', 'global|page_next.png', pad=PAGE_NAV)
                api.api.update_from_api({KCSAPIEnum.QUEST_LIST})
            else:
                no_action_taken = True
        return quest_turned_in

    def _toggle_quests(self, context):
        Log.log_debug(
            f"Checking for quests to activate with {context} context.")
        # quests should only be activated at this point
        relevant_quests = self._filter_quest_by_context(context)
        quest_types = sorted(
            list(self._get_types_from_quests(relevant_quests)),
            key=lambda quest_type: self.QUEST_TYPE_WEIGHTS[quest_type])

        for quest_type in quest_types:
            Log.log_debug(f"Navigating to {quest_type} quests tab.")
            kca_u.kca.click_existing(
                'left', f'quest|filter_tab_{quest_type}.png')
            api.api.update_from_api({KCSAPIEnum.QUEST_LIST})
            kca_u.kca.wait(
                'left', f'quest|filter_tab_{quest_type}_active.png',
                NEAR_EXACT)

            page_processed = False
            while not page_processed:
                for idx, quest in enumerate(self.visible_quests):
                    if quest == -1:
                        page_processed = True
                        break

                    if quest['api_no'] not in self.quest_library:
                        continue

                    quest_i = self.quest_library[quest['api_no']]
                    if quest['api_state'] == 1 and quest_i in relevant_quests:
                        Log.log_msg(f"Activating quest {quest_i.name}.")
                        self._track_quest(quest_i)
                        self._click_quest_idx(idx)
                        sts.stats.quest.quests_activated += 1
                        continue
                    if (
                            quest['api_state'] == 2
                            and quest_i not in relevant_quests):
                        Log.log_msg(f"Deactivating quest {quest_i.name}.")
                        self._click_quest_idx(idx)
                        self._untrack_quest(quest_i)
                        sts.stats.quest.quests_deactivated += 1
                        continue
                page_processed = True

            if self.cur_page < self.tot_page:
                kca_u.kca.click_existing(
                    'lower_right', 'global|page_next.png', pad=PAGE_NAV)
                api.api.update_from_api({KCSAPIEnum.QUEST_LIST})

    def _filter_quest_by_context(self, context):
        relevant_quests = []
        if context == 'combat':
            quest_groups = ['B', 'E']
        elif context == 'pvp':
            quest_groups = ['C', 'E']
        else:
            quest_groups = ['E']

        if cfg.config.expedition.enabled:
            quest_groups.append('D')

        for quest_name in cfg.config.quest.quests:
            if quest_name[0] not in quest_groups:
                continue
            q = self.quest_library[quest_name]

            if q.enemy_context:
                if not (
                        set(com.combat.map_data.enemy_context)
                        & set(q.enemy_context)):
                    continue
            if q.map_context:
                if cfg.config.combat.sortie_map not in q.map_context:
                    continue
            if q.expedition_context:
                if not (
                        set(cfg.config.expedition.all_expeditions)
                        & set(q.expedition_context)):
                    continue
            relevant_quests.append(q)

        return relevant_quests

    def _get_types_from_quests(self, quests):
        quest_types = set()
        for quest in quests:
            quest_types.add(quest.quest_type)
        return quest_types

    def _turn_in_quest_idx(self, idx):
        Log.log_debug(f"Turning in quest at position {idx}.")
        self._click_quest_idx(idx)
        kca_u.kca.wait('kc', 'quest|accept_reward_button.png', 30)
        while kca_u.kca.click_existing('kc', 'quest|accept_reward_button.png'):
            kca_u.kca.sleep(3)
        api.api.update_from_api({KCSAPIEnum.QUEST_LIST})

    def _click_quest_idx(self, idx):
        Log.log_debug(f"Clicking quest at position {idx}.")
        quest_list_region = Region(
            kca_u.kca.game_x + 230, kca_u.kca.game_y + 173 + (idx * 102),
            830, 30)
        quest_list_region.click()
        api.api.update_from_api(
            {KCSAPIEnum.QUEST_LIST, KCSAPIEnum.QUEST_TURN_IN}, need_all=False)
        kca_u.kca.sleep(1)

    def _untrack_quest(self, quest):
        Log.log_debug(f"No longer tracking quest {quest.name}.")
        self.next_check_intervals.pop(quest.name, None)

    def _track_quest(self, quest):
        Log.log_debug(f"Tracking quest {quest.name}.")
        self.next_check_intervals[quest.name] = self._generate_intervals(quest)

    def _generate_intervals(self, quest):
        next_combat = (
            quest.intervals[0] + sts.stats.combat.combat_sorties
            if quest.intervals[0] > 0
            else math.inf)
        next_pvp = (
            quest.intervals[1] + sts.stats.pvp.pvp_done
            if quest.intervals[1] > 0
            else math.inf)
        next_expedition = (
            quest.intervals[2] + sts.stats.expedition.expeditions_received
            if quest.intervals[2] > 0
            else math.inf)
        return (next_combat, next_pvp, next_expedition)

    def _get_quests_to_check_by_interval(self):
        quest_names = set()
        for quest_name in self.next_check_intervals:
            interval = self.next_check_intervals[quest_name]
            if (
                    sts.stats.combat.combat_sorties >= interval[0]
                    or sts.stats.pvp.pvp_done >= interval[1]
                    or sts.stats.expedition.expeditions_received >= interval[2]
            ):
                quest_names.add(quest_name)
        return quest_names

    @property
    def soonest_check_intervals(self):
        soonest_intervals = [math.inf, math.inf, math.inf]
        for quest_name in self.next_check_intervals:
            interval = self.next_check_intervals[quest_name]
            for idx in range(0, 3):
                if interval[idx] < soonest_intervals[idx]:
                    soonest_intervals[idx] = interval[idx]
        return soonest_intervals

    def _reset_next_quest_reset_time(self):
        jst_time = KCTime.convert_to_jst(datetime.now())
        if jst_time.hour == 5:
            temp_time = jst_time.replace(
                minute=randint(1, 5)) + timedelta(days=1)
        else:
            temp_time = jst_time.replace(hour=5, minute=randint(1, 5))
            if jst_time > temp_time:
                temp_time += timedelta(days=1)
        self.quest_reset_time = KCTime.convert_from_jst(temp_time)


quest = QuestCore()
