import config.config_core as cfg
import stats.stats_core as sts
import util.kca as kca_u
from util.logger import Log


class EventReset(object):
    enabled = False
    next_reset_sortie_count = 0

    def __init__(self):
        self.enabled = cfg.config.event_reset.enabled
        self._increment_next_reset_sortie_count()

    def _increment_next_reset_sortie_count(self):
        self.next_reset_sortie_count = (
            sts.stats.combat.combat_sorties
            + cfg.config.event_reset.frequency)

    @property
    def need_to_reset(self):
        return sts.stats.combat.combat_sorties > self.next_reset_sortie_count

    def reset_event_difficulty(self):
        map_name = cfg.config.combat.sortie_map.value
        Log.log_msg(f"Resetting {map_name} difficulty.")
        self._dismiss_chalkboards()
        self._switch_difficulty(cfg.config.event_reset.reset_difficulty)

        kca_u.kca.click_existing('lower_right', 'combat|c_world_1.png')
        kca_u.kca.click_existing(
            'kc', f'combat|_event_world_{map_name}.png')

        self._dismiss_chalkboards()
        self._switch_difficulty(cfg.config.event_reset.farm_difficulty)

        self._increment_next_reset_sortie_count()
        sts.stats.combat.event_resets += 1
        Log.log_msg(
            f"Next reset after sortie #{self.next_reset_sortie_count}.")

    def _dismiss_chalkboards(self):
        kca_u.kca.sleep(1)
        while (
                not kca_u.kca.exists(
                    'upper', 'combat|event_difficulty_select.png')
                and kca_u.kca.exists('lower', 'combat|event_chalkboard.png')):
            kca_u.kca.r['center'].click()
            kca_u.kca.wait('lower', 'combat|event_chalkboard.png')
            kca_u.kca.sleep(1)

    def _switch_difficulty(self, difficulty):
        kca_u.kca.wait_and_click('upper', 'combat|event_difficulty_select.png')
        kca_u.kca.wait_and_click(
            'kc', f'combat|event_difficulty_{difficulty.name.lower()}.png')
        kca_u.kca.sleep(1)
        if not kca_u.kca.exists(
                'lower_right', 'combat|event_difficulty_accept.png'):
            kca_u.kca.click_existing(
                'lower_right', 'combat|event_difficulty_cancel.png')
        else:
            kca_u.kca.click_existing(
                'lower_right', 'event_difficulty_accept.png')
        kca_u.kca.wait('lower_right', 'global|sortie_select.png')


reset = EventReset()
