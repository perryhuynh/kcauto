from sikuli import App, Pattern
from time import strftime
from util import Util


class Debug(object):
    """Debug module that contains kcauto-kai's debug mode methods
    """

    @staticmethod
    def find(window, target, similarity=0.8):
        """Method for finding all matches of an image in the specified window
        with at least the specified similarity once.

        Args:
            window (str): name of window to search in
            target (str): name of image to find in the window
            similarity (float, optional): minimum similarity threshold for the
                match
        """
        target_window = App(window)
        target_region = target_window.focus().focusedWindow()
        print("")
        print("")
        print(
            "+  Sikuli match object for '{}' in window '{}'".format(
                target, window))
        print("+    with minimum similarity of {}:".format(similarity))

        debug_matches = Util.findAll_wrapper(
            target_region, Pattern(target).similar(similarity))

        for img_match in debug_matches:
            print(img_match)
            target_region.mouseMove(img_match)
        if isinstance(debug_matches, list) and len(debug_matches) == 0:
            print("No matches!")
        print("")
        print("")

    @staticmethod
    def continuously_find(window, target, similarity=0.8):
        """Method for finding all mathes of an image in the specified window
        with at least the specified similarity continuously. The user must
        manually exit out the script to halt the matching.

        Args:
            window (str): name of window to search in
            target (str): name of image to find in the window
            similarity (float, optional): minimum similarity threshold for the
                match
        """
        target_window = App(window)
        target_region = target_window.focus().focusedWindow()
        while True:
            print("+ {}:".format(strftime("%H:%M:%S")))
            print(
                "+  Sikuli match object for '{}' in window '{}'".format(
                    target, window))
            print("+    with minimum similarity of {}:".format(similarity))

            debug_matches = Util.findAll_wrapper(
                target_region, Pattern(target).similar(similarity))

            for img_match in debug_matches:
                print(img_match)
                target_region.mouseMove(img_match)
            if isinstance(debug_matches, list) and len(debug_matches) == 0:
                print("No matches!")
            print("")
