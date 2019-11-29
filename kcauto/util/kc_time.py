from abc import ABC
from datetime import datetime, timedelta

import config.config_core as cfg


class KCTime(ABC):
    """kcauto datetime helper module.
    """
    @staticmethod
    def convert_epoch(epoch):
        """Method that converts epoch timestamp to a datetime object. Primarily
        used to convert timestamps from the kancolle api calls. The api call
        timestamps are in milliseconds, so they must first be converted to
        seconds before converting to datetime.

        Args:
            epoch (int): epoch timestamp in milliseconds to convert.

        Raises:
            ValueError: the converted timestamp contains the wrong number of
                digits.

        Returns:
            datetime: datetime representation of epoch timestamp.
        """
        len_epoch = len(str(epoch))
        if len_epoch == 13:
            epoch = epoch / 1000
        elif epoch == 0:
            return None
        else:
            raise ValueError(f"Invalid timestamp '{epoch}'")
        return datetime.fromtimestamp(epoch)

    @staticmethod
    def datetime_to_str(input_datetime):
        """Method that converts datetime instance to a human-readable string.

        Args:
            input_datetime (datetime): datetime to convert.

        Returns:
            str: human-readable representation of datetime.
        """
        return input_datetime.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def timedelta_to_str(cls, input_timedelta):
        """Method that converts timedelta objects to a human-readable string.

        Args:
            input_timedelta (timedelta): timedelta to convert.

        Returns:
            str: human-readable representation of timedelta.
        """
        dhms = cls._seconds_to_dhms_dict(input_timedelta.seconds)
        return (
            f"{dhms['days']}d {dhms['hours']}h "
            f"{dhms['minutes']}m {dhms['seconds']}s")

    @classmethod
    def seconds_to_timedelta(cls, seconds):
        """Method that converts seconds to an appropriate timedelta object.

        Args:
            seconds (int): number of seconds

        Returns:
            timedelta: timedelta of seconds
        """
        return timedelta(**cls._seconds_to_dhms_dict(seconds))

    @staticmethod
    def convert_to_jst(time):
        """Method that converts a datetime object to JST by offsetting the
        number of hours by the value provided in jst_offset.

        Args:
            time (datetime): datetime instance pre-conversion to JST.
            config (Config, optional): Config instance of kcauto.

        Returns:
            datetime: datetime instance converted to JST.
        """
        return time + timedelta(hours=cfg.config.general.jst_offset)

    @staticmethod
    def convert_from_jst(time):
        """Method that converts a datetime object to local time by offsetting
        the number of hours by the value provided in jst_offset.

        Args:
            time (datetime): datetime instance in JST.
            config (Config, optional): Config instance of kcauto.

        Returns:
            datetime: datetime instance converted to local time.
        """
        return time - timedelta(hours=cfg.config.general.jst_offset)

    @staticmethod
    def _seconds_to_dhms_dict(seconds):
        """Method that converts seconds to a dict of days, hours, minutes,
        and seconds.

        Args:
            seconds (int): number of seconds

        Returns:
            dict: dict of days, hours, minutes, and seconds
        """
        dhms = {}
        dhms['days'], rem = divmod(seconds, 24 * 60 * 60)
        dhms['hours'], rem = divmod(rem, 60 * 60)
        dhms['minutes'], dhms['seconds'] = divmod(rem, 60)
        return dhms
