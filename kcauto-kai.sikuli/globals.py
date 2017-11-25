class Globals(object):
    # for the sikuli scan and observe rates (times per second)
    SIKULI_SCANRATE = 20
    # time to wait before executing another kcauto-kai loop
    LOOP_SLEEP_LENGTH = 15
    # how often to check the quests outside of other checkpoints
    QUEST_LOOP_CHECK_RATE = 5
    # the number of seconds to add to all waits
    SLEEP_MODIFIER = 0

    # similarity thresholds for various asset types
    DEFAULT_SIMILARITY = 0.8
    DAMAGE_SIMILARITY = 0.7
    FATIGUE_SIMILARITY = 0.8
    FLEET_ICON_SIMILARITY = 0.6

    # area expansion presets
    EXPAND = {
        'repair_list': [-325, 35, -10, 6],
        'arrow_navigation': [-10, 10, -5, 5]
    }
