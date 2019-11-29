from abc import ABC
from time import strftime

import args.args_core as arg


class Log(ABC):
    CLR_MSG = '\033[94m'
    CLR_SUCCESS = '\033[92m'
    CLR_WARNING = '\033[93m'
    CLR_ERROR = '\033[91m'
    CLR_END = '\033[0m'

    @staticmethod
    def _log_format(msg):
        """Method to add a timestamp to a log message.

        Args:
            msg (str): log message.

        Returns:
            str: log message with timestamp appended.
        """
        return f"[{strftime('%Y-%m-%d %H:%M:%S')}] {msg}"

    @classmethod
    def log_msg(cls, msg):
        """Method to print a log message to the console, with the 'msg' colors.

        Args:
            msg (str): log message.
        """
        print(
            f"{cls.CLR_MSG}{cls._log_format(msg)}{cls.CLR_END}",
            flush=True)

    @classmethod
    def log_success(cls, msg):
        """Method to print a log message to the console, with the 'success'
        colors.

        Args:
            msg (str): log message.
        """
        print(
            f"{cls.CLR_SUCCESS}{cls._log_format(msg)}{cls.CLR_END}",
            flush=True)

    @classmethod
    def log_warn(cls, msg):
        """Method to print a log message to the console, with the 'warning'
        colors.

        Args:
            msg (str): log message.
        """
        print(
            f"{cls.CLR_WARNING}{cls._log_format(msg)}{cls.CLR_END}",
            flush=True)

    @classmethod
    def log_error(cls, msg):
        """Method to print a log message to the console, with the 'error'
        colors.

        Args:
            msg (str): log message.
        """
        print(
            f"{cls.CLR_ERROR}{cls._log_format(msg)}{cls.CLR_END}",
            flush=True)

    @classmethod
    def log_debug(cls, msg):
        """Method to print a debug log message to the console. Only prints if
        the debug flag is set to True.

        Args:
            msg (str): log message.
        """
        if arg.args.parsed_args.debug_output:
            print(cls._log_format(msg), flush=True)
