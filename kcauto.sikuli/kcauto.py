# Workaround to get jython imports working
# https://bugs.launchpad.net/sikuli/+bug/1504901
# https://github.com/RaiMan/SikuliX-2014/issues/151
import sikuli
import org.sikuli.script.FindFailed as FindFailed
import org.sikuli.util.JythonHelper as JythonHelper
import os
import sys
from time import sleep

JythonHelper.get().addSysPath(sikuli.getBundlePath())
sys.path.append(os.getcwd())

# kcauto imports
from main import KCAuto  # noqa
from kca_globals import Globals  # noqa
from args import Args  # noqa
from config import Config  # noqa
from debug import Debug  # noqa
from recovery import Recovery  # noqa
from util import Util  # noqa

# Sikuli settings
sikuli.Settings.MinSimilarity = Globals.DEFAULT_SIMILARITY
sikuli.Settings.WaitScanRate = Globals.SIKULI_SCANRATE
sikuli.Settings.ObserveScanRate = Globals.SIKULI_SCANRATE
sikuli.Settings.OcrTextRead = True
sikuli.Settings.AutoWaitTimeout = 1
sikuli.Settings.RepeatWaitTime = 0

# check run-time args
args = None
if len(sys.argv) > 1:
    args = Args(sys.argv)

# check args, and if none provided, load default config
if args and args.mode == 'cfg':
    config = Config(args.cfg)
elif args and args.mode == 'debug':
    Debug.find(args.window, args.target, args.similarity)
    sys.exit(0)
elif args and args.mode == 'debugc':
    Debug.continuously_find(args.window, args.target, args.similarity)
    sys.exit(0)  # never actually reached
else:
    config = Config('config.ini')

kcauto = KCAuto(config)

while True:
    try:
        # update config on every main loop
        kcauto.refresh_config()

        if not (kcauto.conduct_scheduled_sleep()
                or kcauto.conduct_pause()):

            kcauto.run_receive_expedition_cycle()

            kcauto.run_quest_cycle()

            kcauto.run_expedition_cycle()

            kcauto.run_pvp_cycle()

            kcauto.run_combat_cycle()

            kcauto.run_repair_cycle()

            kcauto.run_ship_switch_cycle()

            kcauto.run_resupply_cycle()

            kcauto.run_quest_cycle()

            kcauto.conduct_module_sleeps()

            kcauto.conduct_scheduled_stops()

            kcauto.print_cycle_stats()

        sleep(Globals.LOOP_SLEEP_LENGTH)
    except FindFailed as e:
        Recovery.recover(kcauto, config, e)
