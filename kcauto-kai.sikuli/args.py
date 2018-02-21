from kca_globals import Globals
from util import Util


class Args(object):
    """Args module for processing the command line arguments passed into
    kcauto-kai.

    Attributes:
        cfg (str): name of non-default config file
        mode (str): specifies which special mode kcauto-kai should run in
        similarity (float, optional): minimum similarity threshold for image
            matching
        target (str): name of image to match for
        window (str): window name to image match in
    """

    mode = None
    cfg = None
    window = None
    target = None
    similarity = None

    def __init__(self, argv):
        """Initializes the Args object with the passed in arguments in argv

        Args:
            argv (list): sequential list of passed in arguments (argv[0] is
                the name of the script)
        """
        if argv[1] == 'cfg':
            self.set_cfg(argv)
        if argv[1] == 'debug' or argv[1] == 'debugc':
            self.set_debug(argv)

    def set_cfg(self, argv):
        """If kcauto-kai is in custom-cfg mode, this method sets the
        appropriate attributes

        Args:
            argv (list): sequential list of passed in arguments (see __init__)
        """
        if len(argv) == 3:
            self.mode = argv[1]
            self.cfg = argv[2]
        else:
            Util.log_error('Invalid parameters for cfg arguments')
            Util.log_msg('Usage: -- cfg <path_to_cfg_file>')

    def set_debug(self, argv):
        """If kcauto-kai is in debug mode, this method sets the appropriate
        attributes

        Args:
            argv (list): sequential list of passed in arguments (see __init__)
        """
        if len(argv) >= 4:
            self.mode = argv[1]
            self.window = argv[2]
            self.target = argv[3]
            # use default similarity if a custom similarity threshold was not
            # passed in
            self.similarity = Globals.DEFAULT_SIMILARITY

            if len(argv) == 5:
                try:
                    self.similarity = float(argv[4])
                except:
                    Util.log_error(
                        '4th argument is not a valid decimal value for '
                        'similarity')
        else:
            Util.log_error('Invalid parameters for debug arguments')
            Util.log_msg(
                'Usage: -- debug name_of_window '
                'path_to_file_to_match [optional:similarity (decimal between '
                '0 and 1)]')
