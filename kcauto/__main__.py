import args.args_core as arg
from util.logger import Log
from version import __version__


if __name__ == '__main__':
    """Main entry point for kcauto script. Decides whether or not to launch in
    CLI, GUI, or debug mode.
    """

    args = arg.args.parse_args()

    if args.cli:
        from kcauto_wrapper import kcauto_main
        cfg = args.cfg_path if args.cfg_path else args.cfg
        Log.log_success(
            f"Initializing kcauto v{__version__} in command-line mode with "
            f"the '{cfg}' config file.")
        kcauto_main()
    elif args.debug:
        if not args.debug_asset:
            raise ValueError(
                "--debug-asset must be specified when using --debug.")
        from util.debug import debug
        debug.find_all(args.debug_asset, args.debug_similarity)
    else:
        from kcauto_gui import gui_main
        Log.log_success(f"Initializing kcauto v{__version__} GUI.")
        gui_main()
