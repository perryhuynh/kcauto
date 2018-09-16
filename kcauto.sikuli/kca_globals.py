class Globals(object):
    # game window dimensions
    GAME_WIDTH = 1200
    GAME_HEIGHT = 720

    # for the sikuli scan and observe rates (times per second)
    SIKULI_SCANRATE = 30
    # time to wait before executing another kcauto loop
    LOOP_SLEEP_LENGTH = 15
    # how often to check the quests outside of other checkpoints
    QUEST_LOOP_CHECK_RATE = 5
    # the number of seconds to add to all waits
    SLEEP_MODIFIER = 0

    # similarity thresholds for various asset types
    DEFAULT_SIMILARITY = 0.8
    DAMAGE_SIMILARITY = 0.85
    FATIGUE_SIMILARITY = 0.85
    SHIP_LIST_SIMILARITY = 0.96
    FLEET_ICON_SIMILARITY = 0.8
    SHIP_LIST_FLEET_ICON_SIMILARITY = 0.75

    # types of recoveries enabled for the recovery module. Valid options are
    # 'catbomb' and 'chrome'. Enabled recoveries mean that the script will
    # attempt to restart the game when encountering a relevant crash; otherwise
    # the script will halt.
    ENABLED_RECOVERIES = ('chrome')

    # how many minutes to wait between sorties to allow for natural fatigue
    # recovery
    COMBAT_BUFFER_MINUTES = 0
    # how many combat sorties to conduct when sparkling
    SPARKLING_RUN_COUNT = 3

    # how many ships are in a shiplist page; static unless the game UI changes
    SHIPS_PER_PAGE = 10

    # area expansion presets; format is in [left, right, up, down] relative to
    # the center of the match
    EXPAND = {
        'repair_list': [-500, 20, -12, 12],
        'arrow_navigation': [-10, 10, -8, 8],
        'shiplist_sort': [-4, 36, -10, 10],
        'scroll_next': [-10, 10, -20, -6]
    }
