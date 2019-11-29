import json
import os
from abc import ABC

from util.logger import Log


class JsonData(ABC):
    """kcauto json helper module.
    """
    @classmethod
    def create_path(cls, path):
        """Helper method for generating OS-friendly path from kcauto-style
        path.

        Args:
            path (str): kcauto-style path.

        Returns:
            str: OS-friendly path
        """
        return os.path.join(*path.split('|'))

    @classmethod
    def dump_json(cls, data, path, pretty=False):
        """Method for serializing an object into a json file.

        Args:
            data (object): object to serialize.
            path (str): kcauto-style path.
            pretty (bool, optional): flag for pretty-printing the dumped file.
                Defaults to False.
        """
        json_path = cls.create_path(path)
        Log.log_debug(f"Writing data to '{json_path}'.")
        with open(json_path, 'w', encoding='utf-8') as json_file:
            if not pretty:
                json.dump(data, json_file, ensure_ascii=False)
            else:
                json.dump(data, json_file, ensure_ascii=False, indent=2)

    @classmethod
    def load_json(cls, path):
        """Method for deserializing a json file.

        Args:
            path (str): kcauto-style path to json file.

        Returns:
            object: deserialized object.
        """
        json_path = cls.create_path(path)
        Log.log_debug(f"Loading data from '{json_path}'.")
        with open(json_path, encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    @classmethod
    def print_json(cls, data):
        """Method for serializing an object into a json string.

        Args:
            data (object): object to serialize.

        Returns:
            str: serialized json string.
        """
        pretty_json = json.dumps(data, ensure_ascii=False, indent=2)
        return pretty_json

    @classmethod
    def load_json_str(cls, json_str):
        """Method for deserializing a json string.

        Args:
            json_str (str): json string representation.

        Returns:
            object: deserialized object.
        """
        return json.loads(json_str)
