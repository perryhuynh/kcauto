import argparse
from constants import DEFAULT
from version import __version__


class ArgsCore(object):
    parser = None
    parsed_args = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=(
                f"kcauto v{__version__} - "
                "automating your Kantai Collection needs"))
        self.parser.add_argument(
            '--cli', action='store_true',
            help="run kcauto without a GUI as a command-line script")
        self.parser.add_argument(
            '-c', '--cfg', type=str, action='store', default='config',
            help=(
                "name of config file to load (without .json) in the config "
                "directory; defaults to 'config' for the config.json file in "
                "the config directory"))
        self.parser.add_argument(
            '--cfg-path', type=str, action='store',
            help=(
                "full filepath of config file to load (with .json). Used for "
                "loading config files not in the config directory"))
        self.parser.add_argument(
            '--debug-output', action='store_true',
            help="enable granular kcauto debug log output")
        self.parser.add_argument(
            '--no-click-track', action='store_true',
            help="disable internal tracking of click locations")
        self.parser.add_argument(
            '--debug', action='store_true',
            help=(
                "debug mode that runs a 'find_all' on the screen. Use with "
                "--debug-asset and --debug-similarity"))
        self.parser.add_argument(
            '--debug-asset', type=str, action='store',
            help="asset to search for in debug mode")
        self.parser.add_argument(
            '--debug-similarity', type=float, action='store', default=DEFAULT,
            help=(
                "similarity to search asset with in debug mode; defaults to "
                f"{DEFAULT}"))

    def parse_args(self):
        self.parsed_args = self.parser.parse_args()
        return self.parsed_args


args = ArgsCore()
