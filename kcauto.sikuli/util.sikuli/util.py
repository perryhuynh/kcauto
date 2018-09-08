from sikuli import Screen, App, Region, Location, Pattern, Match, Button
import org.sikuli.script.FindFailed as FindFailed
# alternate Region class to check instasnce type against
# https://answers.launchpad.net/sikuli/+question/269004
import org.sikuli.script.Region as JRegion
import org.sikuli.script.Match as JMatch
import org.sikuli.script.Pattern as JPattern
from time import strftime
from random import uniform, gauss
from math import ceil
from time import sleep
from datetime import timedelta
from re import match, sub
from kca_globals import Globals


class Util(object):
    """Util module for serving up various functionality used program-wide. The
    methods here are accessible from other modules as static and class methods;
    Util should not be instantiated directly.

    Attributes:
        CLR_* (str): shell coloring prefixes and suffixes
    """

    CLR_MSG = '\033[94m'
    CLR_SUCCESS = '\033[92m'
    CLR_WARNING = '\033[93m'
    CLR_ERROR = '\033[91m'
    CLR_END = '\033[0m'

    @staticmethod
    def kc_sleep(base=None, flex=None):
        """Method for putting the program to sleep for a random amount of time.
        If base is not provided, defaults to somewhere along with 0.3 and 0.7
        seconds. If base is provided, the sleep length will be between base
        and 2*base. If base and flex are provided, the sleep length will be
        between base and base+flex. The global SLEEP_MODIFIER is than added to
        this for the ifnal sleep length.

        Args:
            base (int, optional): minimum amount of time to go to sleep for
            flex (int, optional): the delta for the max amount of time to go
                to sleep for
        """
        if base is None:
            sleep(uniform(0.3, 0.7) + Globals.SLEEP_MODIFIER)
        else:
            flex = base if flex is None else flex
            sleep(uniform(base, base + flex) + Globals.SLEEP_MODIFIER)

    @staticmethod
    def convert_to_jst(time, config={}):
        """Method that converts a datetime object to JST by offsetting the
        number of hours by the value provided in jst_offset.

        Args:
            time (datetime): datetime instance pre-conversion to JST
            config (Config, optional): Config instance of kcauto

        Returns:
            datetime: datetime instance converted to JST
        """
        return time + timedelta(hours=getattr(config, 'jst_offset', 0))

    @staticmethod
    def convert_from_jst(time, config={}):
        """Method that converts a datetime object to local time by offsetting
        the number of hours by the value provided in jst_offset.

        Args:
            time (datetime): datetime instance in JST
            config (Config, optional): Config instance of kcauto

        Returns:
            datetime: datetime instance converted to local time
        """
        return time - timedelta(hours=getattr(config, 'jst_offset', 0))

    @staticmethod
    def read_ocr_number_text(kc_region, text_ref=None, rdir=None, width=None):
        """Method for reading in text in reference to an asset or Match
        instance, and then cleaning up the OCR results, tuned for numbers.

        Args:
            kc_region (Region): sikuli Region instance containing the last
                known location of the Kantai Collection game screen
            text_ref (str, Match): image name of reference or Match of
                reference the OCR read should happen in relation to
            rdir (str): specifies in what direction relative to text_ref the
                OCR read should occur: 'r' for 'right of text_ref' and 'l' for
                'left of text_ref'
            width (int): width (in pixels) of the region the OCR read should
                occur in

        Returns:
            str: OCR read results, tuned for numbers
        """
        if text_ref is None and rdir is None and width is None:
            text = kc_region.text().encode('utf-8')
        if isinstance(text_ref, str) and rdir and width:
            if rdir == 'r':
                text = kc_region.find(text_ref).right(width).text().encode(
                    'utf-8')
            elif rdir == 'l':
                text = kc_region.find(text_ref).left(width).text().encode(
                    'utf-8')
        elif (
                isinstance(text_ref, Match) or isinstance(text_ref, JMatch)
                and rdir and width):
            if rdir == 'r':
                text = text_ref.right(width).text().encode('utf-8')
            elif rdir == 'l':
                text = text_ref.left(width).text().encode('utf-8')
        # replace characters to numbers
        text = (
            text.replace('O', '0').replace('o', '0').replace('D', '0')
            .replace('Q', '0').replace('@', '0').replace('l', '1')
            .replace('I', '1').replace('[', '1').replace(']', '1')
            .replace('|', '1').replace('!', '1').replace('Z', '2')
            .replace('S', '5').replace('s', '5').replace('$', '5')
            .replace('B', '8').replace(':', '8').replace(' ', '')
            .replace('-', '')
        )
        return text

    @classmethod
    def read_timer(cls, kc_region, timer_ref, dir, width, attempt_limit=0):
        """Method for reading various timers in the format of ##:##:## via OCR.

        Args:
            kc_region (Region): sikuli Region instance containing the last
                known location of the Kantai Collection game screen
            timer_ref (str, Match): image name of reference or Match of
                reference the OCR read should happen in relation to
            dir (str): specifies in what direction relative to text_ref the
                OCR read should occur: 'r' for 'right of text_ref' and 'l' for
                'left of text_ref'
            width (int): width (in pixels) of the region the OCR read should
                occur in
            attempt_limit (int, optional): how many attempts should be made to
                read the timer

        Returns:
            dict: dict of hours, minutes, and seconds of a successful timer
                read
        """
        ocr_matching = True
        timer_dict = {'hours': 95, 'minutes': 0, 'seconds': 0}
        attempt = 0
        while ocr_matching:
            attempt += 1
            timer = cls.read_ocr_number_text(kc_region, timer_ref, dir, width)
            if len(timer) == 8:
                # valid length for timer ('##:##:##')
                timer = list(timer)
                timer[2] = ':'
                timer[5] = ':'
                timer = ''.join(timer)
                timer_format_match = match(r'^\d{2}:\d{2}:\d{2}$', timer)
                if timer_format_match:
                    # valid timer reading; return timer reading
                    ocr_matching = False
                    cls.log_msg("Got valid timer (%s)!" % timer)
                    timer_dict = {
                        'hours': int(timer[0:2]),
                        'minutes': int(timer[3:5]),
                        'seconds': int(timer[6:8])
                    }
                    return timer_dict
            # the timer reading is invalid; if the attempt_limit is set and
            # met, return 95:00:00
            if attempt_limit != 0 and attempt == attempt_limit:
                cls.log_warning(
                    "Got invalid timer and met attempt threshold. Returning "
                    "95:00:00!")
                return timer_dict
            # otherwise, try again
            cls.log_warning(
                "Got invalid timer ({})... trying again!".format(timer))
            sleep(0.2)

    @classmethod
    def read_number(cls, kc_region, number_ref, dir, width, attempt_limit=0):
        """Method for reading various numbers via OCR.

        Args:
            kc_region (Region): sikuli Region instance containing the last
                known location of the Kantai Collection game screen
            timer_ref (str, Match): image name of reference or Match of
                reference the OCR read should happen in relation to
            dir (str): specifies in what direction relative to text_ref the
                OCR read should occur: 'r' for 'right of text_ref' and 'l' for
                'left of text_ref'
            width (int): width (in pixels) of the region the OCR read should
                occur in
            attempt_limit (int, optional): how many attempts should be made to
                read the number

        Returns:
            int: the number recognized via OCR
        """
        ocr_matching = True
        attempt = 0
        while ocr_matching:
            attempt += 1
            number = cls.read_ocr_number_text(
                kc_region, number_ref, dir, width)
            m = match(r'^\d+$', number)
            if m:
                # OCR match is a number; return it
                ocr_matching = False
                return int(number)
            # the number reading is invalid; if the attempt limit is set and
            # met, return 0
            if attempt_limit != 0 and attempt == attempt_limit:
                return 0
            # otherwise, try again
            cls.log_warning(
                "Got invalid number ({})... trying again!".format(number))
            sleep(0.2)

    @classmethod
    def get_shiplist_counts(cls, regions):
        """Method that gets the ship-list related counts based on the number of
        ships in the port.
        """
        ship_count = cls._get_ship_count(regions)
        ship_page_count = int(
            ceil(ship_count / float(Globals.SHIPS_PER_PAGE)))
        ship_last_page_count = (
            ship_count % Globals.SHIPS_PER_PAGE
            if ship_count % Globals.SHIPS_PER_PAGE is not 0
            else Globals.SHIPS_PER_PAGE)
        return (ship_count, ship_page_count, ship_last_page_count)

    @staticmethod
    def _get_ship_count(regions):
        """Method that returns the number of ships in the port via the counter
        at the top of the screen when at home. Directly calls the
        read_ocr_number_text method then strips all non-number characters
        because Tesseract OCR has issues detecting short number of characters
        that are also white font on black backgrounds. Trick this by capturing
        more of the region than is needed (includes a bit of the bucket icon)
        then stripping out the superfluous/mis-recognized characters.

        Returns:
            int: number of ships in port
        """
        initial_read = Util.read_ocr_number_text(regions['ship_counter'])
        number_read = sub(r"\D", "", initial_read)
        if len(number_read) > 3:
            # the read number is too long; truncate anything past the 3rd digit
            number_read = number_read[:3]
        number_read = int(number_read)
        if number_read > 370:
            # to account for edge cases where a digit is appended at the end
            number_read = number_read / 10
        return number_read

    @staticmethod
    def findAll_wrapper(region, pattern):
        """Method for wrapping sikuli Region's findAll method to return an
        empty list instead of None on no matches.
        Relevant bug ticket: https://bugs.launchpad.net/sikuli/+bug/1677134

        Args:
            region (Region): Region to conduct the findAll in
            pattern (str, Pattern): filename of asset or Pattern to match for
                with the findAll

        Returns:
            list: list of all Matches of pattern in the region
        """
        try:
            matches = region.findAll(pattern)
            return matches if matches is not None else []
        except FindFailed:
            return []

    @staticmethod
    def multithreader(threads):
        """Method for starting and threading multithreadable Threads in
        threads.

        Args:
            threads (list): list of Threads to multithread
        """
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    @staticmethod
    def focus_app(config):
        """Method to focus the specified game window.

        Args:
            config (Config): kcauto Config instance

        Returns:
            Region: region returned by sikuli's focusedWindow method
        """
        kc = App.focus(config.program).focusedWindow()
        kc.setAutoWaitTimeout(1)
        return kc

    @classmethod
    def focus_kc(cls, config):
        """Method for focusing on the window Kantai Collection is running in
        and defining all the pre-defined regions based off of it.

        Args:
            config (Config): kcauto Config instance

        Returns:
            Region: Region instance containing the  location of the Kantai
                Collection game screen
            list: list of pre-defined Regions
        """
        kc = cls.focus_app(config)
        # match one of the many reference points to find the exact location of
        # the game within the game container window
        ref_region = None
        find_attempt = 0
        while not ref_region:
            try:
                ref_region = kc.find(Pattern('kc_ref_point_1.png').exact())
            except FindFailed:
                pass
            try:
                ref_region = kc.find(Pattern('kc_ref_point_2.png').exact())
            except FindFailed:
                pass
            try:
                ref_region = kc.find(Pattern('kc_ref_point_3.png').exact())
            except FindFailed:
                pass
            find_attempt += 1
            sleep(1)
            if find_attempt > 3:
                Util.log_error("Could not find a reference point.")
                raise FindFailed
        x = ref_region.x - 144
        y = ref_region.y

        regions = {}
        # pre-defined regions are defined as (X_start, Y_start, width, height)
        # generic regions
        width = Globals.GAME_WIDTH
        height = Globals.GAME_HEIGHT
        half_width = width / 2
        half_height = height / 2
        regions['game'] = Region(x, y, width, height)
        regions['left'] = Region(x, y, half_width, height)
        regions['right'] = Region(x + half_width, y, half_width, height)
        regions['upper'] = Region(x, y, width, half_height)
        regions['lower'] = Region(x, y + half_height, width, half_height)
        regions['upper_left'] = Region(x, y, half_width, half_height)
        regions['upper_right'] = Region(
            x + half_width, y, half_width, half_height)
        regions['lower_left'] = Region(
            x, y + half_height, half_width, half_height)
        regions['lower_right'] = Region(
            x + half_width, y + half_height, half_width, half_height)
        regions['lower_right_corner'] = Region(x + 1100, y + 620, 100, 100)
        # function-specific regions
        regions['expedition_flag'] = Region(x + 750, y + 20, 70, 50)
        regions['top_menu'] = Region(x + 185, y + 50, 800, 50)
        regions['home_menu'] = Region(x + 45, y + 130, 500, 490)
        regions['side_menu'] = Region(x, y + 190, 145, 400)
        regions['top_submenu'] = Region(x + 145, y + 145, 1055, 70)
        regions['quest_status'] = Region(x + 1065, y + 165, 95, 500)
        regions['check_supply'] = Region(x + 695, y + 195, 40, 440)
        regions['ship_counter'] = Region(x + 735, y + 15, 55, 20)
        # combat-related regions
        regions['formation_line_ahead'] = Region(x + 596, y + 256, 150, 44)
        regions['formation_double_line'] = Region(x + 791, y + 256, 150, 44)
        regions['formation_diamond'] = Region(x + 989, y + 256, 150, 44)
        regions['formation_echelon'] = Region(x + 596, y + 495, 252, 44)
        regions['formation_line_abreast'] = Region(x + 791, y + 495, 253, 44)
        regions['formation_vanguard'] = Region(x + 989, y + 495, 150, 44)
        regions['formation_combinedfleet_1'] = Region(
            x + 420, y + 150, 160, 50)  # NU
        regions['formation_combinedfleet_2'] = Region(
            x + 580, y + 150, 160, 50)  # NU
        regions['formation_combinedfleet_3'] = Region(
            x + 420, y + 280, 160, 50)  # NU
        regions['formation_combinedfleet_4'] = Region(
            x + 580, y + 280, 160, 50)  # NU

        return (kc, regions)

    @classmethod
    def rejigger_mouse(cls, regions, preset):
        """Method to move the mouse to a random X,Y coordinate in the specified
        preset region.

        Args:
            regions (dict): dict of pre-defined kcauto regions
            preset (str): name of preset-area to move the mouse to
        """
        # preset areas are designated as (X_start, X_end, Y_start, Y_end)
        presets = {
            'game': (0, Globals.GAME_WIDTH, 0, Globals.GAME_HEIGHT),
            'center': (225, 975, 180, 540),
            'top': (400, 1200, 12, 42),
            'quest_menu': (790, 895, 50, 95),
            'shipgirl': (700, 1100, 130, 550),
            'lbas': (350, 450, 5, 50),  # NU
            'lbas_mode_switch_button': (763, 788, 137, 179),  # NU
            '7th_next': (386, 413, 400, 427)  # NU
        }

        if isinstance(preset, str):
            x1, x2, y1, y2 = presets[preset]
            # max bounds
            temp_screen = Screen().getBounds()
            max_x = temp_screen.width
            max_y = temp_screen.height

            rand_x = regions['game'].x + cls.randint_gauss(x1, x2)
            rand_y = regions['game'].y + cls.randint_gauss(y1, y2)

            rand_x = max_x - 1 if rand_x > max_x else rand_x
            rand_y = max_y - 1 if rand_y > max_y else rand_y
        elif (isinstance(preset, Region) or isinstance(preset, JRegion)
                or isinstance(preset, Match) or isinstance(preset, JMatch)):
            rand_x = cls.randint_gauss(preset.x, preset.x + preset.w)
            rand_y = cls.randint_gauss(preset.y, preset.y + preset.h)

        regions['game'].mouseMove(Location(rand_x, rand_y))

    @classmethod
    def click_preset_region(cls, regions, preset):
        """Method to move the mouse to one of the preset regions defined in
        rejigger_mouse() and simulate clicking the mouse in the location.

        Args:
            regions (dict): dict of pre-defined kcauto regions
            preset (str): name of preset-area to move the mouse to
        """
        cls.rejigger_mouse(regions, preset)
        cls.click_mouse(regions['game'])

    @classmethod
    def click_coords(cls, region, x, y):
        """Method to move the mouse to the specified x,y coordinates and
        simulate clicking the mouse on the location.

        Args:
            region (Region): sikuli Region instance containing the last known
                location of the Kantai Collection game screen
            x (int): x-coords in pixels, relative to upper-left corner of game
            y (int): y-coords in pixels, relative to upper-left corner of game
        """
        # offset x,y coords relative to upper-left corner of game to upper-left
        # corner of screen
        offset_x = region.x + x
        offset_y = region.y + y
        # move the mouse to offset location
        region.mouseMove(Location(offset_x, offset_y))
        cls.click_mouse(region)

    @classmethod
    def click_mouse(cls, region):
        """Method to simulate clicking the mouse at its present location.

        Args:
            region (Region): sikuli Region instance containing the last known
                location of the Kantai Collection game screen
        """
        region.mouseDown(Button.LEFT)
        cls.kc_sleep()
        region.mouseUp(Button.LEFT)

    @classmethod
    def check_and_click(cls, region, target, expand=[]):
        """Method to check for an image match then click it.

        Args:
            region (Region): Region to conduct the match in
            target (str, Pattern): the filename of the asset or Pattern to
                search for
            expand (list, optional): area expansion for the click

        Returns:
            bool: True if the asset was found and clicked, False otherwise
        """
        if region.exists(target):
            region.click(cls.generate_pattern(region, target, expand, True))
            cls.kc_sleep()
            return True
        return False

    @classmethod
    def wait_and_click(cls, region, target, time=10, expand=[]):
        """Method to wait for the appearance of an image match then click it.

        Args:
            region (Region): Region to conduct the match in
            target (str, Pattern): the filename of the asset or Pattern to
                search for
            time (int, optional): max amount of time to wait for the asset to
                appear
            expand (list, optional): area expansion for the click
        """
        region.wait(target, time)
        if Globals.SLEEP_MODIFIER:
            cls.kc_sleep()
        region.click(cls.generate_pattern(region, target, expand, True))
        cls.kc_sleep()

    @classmethod
    def wait_and_click_and_wait(
            cls, click_region, click_target, wait_region, wait_target, time=10,
            expand=[]):
        """Method to wait for the appearance of an image match, click it,
        then wait for another subsequent image match.

        Args:
            click_region (Region): Region to conduct the initial match in
            click_target (str, Pattern): the filename of the asset or Pattern
                to search for the initial click
            wait_region (Region): Region to conduct the second match in
            wait_target (str, Pattern): the filename of the asset or Pattern
                to search for in the second wait check
            time (int, optional): max amount of time to wait for assets to
                appear
            expand (list, optional): area expansion for the click
        """
        click_region.wait(click_target, time)
        if Globals.SLEEP_MODIFIER:
            cls.kc_sleep()
        click_region.click(
            cls.generate_pattern(click_region, click_target, expand, True))
        try:
            wait_region.wait(wait_target, time)
        except FindFailed:
            # the initial click might have failed due to lag within the client;
            # rejigger the mouse and retry the click if this happens
            click_region.mouseMove(Location(1, 1))
            cls.wait_and_click_and_wait(
                click_region, click_target, wait_region, wait_target, time,
                expand)

        cls.kc_sleep()

    @classmethod
    def generate_pattern(cls, region, target, expand=[], prematched=False):
        """Method to generate a pattern with a custom targetOffset (click
        point) based on the randint_gauss() method.

        Args:
            region (Region): Region to conduct the search in
            target (str, Pattern): the filename of the asset or Pattern to
                search for
            expand (list, optional): area expansion for the targetOffset
            prematched (bool, optional): specifies whether or not the target
                was matched in the region immediately prior to the
                generate_pattern() call. This allows for the use of
                getLastMatch() to generate the match, instead of re-searching.

        Returns:
            Pattern: new Pattern object with the custom targetOffset
        """
        if len(expand) == 0:
            if not prematched:
                region.find(target)
            matched_region = region.getLastMatch()

            if matched_region:
                x_width = matched_region.w / 2
                y_height = matched_region.h / 2
                expand = [-x_width, x_width, -y_height, y_height]

        if isinstance(target, str):
            created_pattern = Pattern(target).targetOffset(
                int(round(cls.randint_gauss(expand[0], expand[1]))),
                int(round(cls.randint_gauss(expand[2], expand[3]))))
        elif isinstance(target, Pattern) or isinstance(target, JPattern):
            created_pattern = target.targetOffset(
                int(round(cls.randint_gauss(expand[0], expand[1]))),
                int(round(cls.randint_gauss(expand[2], expand[3]))))

        return created_pattern

    @staticmethod
    def randint_gauss(min_val, max_val):
        """Method to generate a random value based on the min_val and max_val
        with a gaussian (normal) distribution.

        Args:
            min_val (int): minimum value of the random number
            max_val (int): maximum value of the random number

        Returns:
            int: the generated random number
        """
        summed_val = float(min_val) + float(max_val)
        diff = float(abs(min_val) - abs(max_val))

        mu = summed_val / 2
        sigma = diff / 6

        return int(max(min_val, min(gauss(mu, sigma), max_val)))

    @staticmethod
    def log_format(msg):
        """Method to add a timestamp to a log message

        Args:
            msg (str): log msg

        Returns:
            str: log msg with timestamp appended
        """
        return "[{}] {}".format(strftime("%Y-%m-%d %H:%M:%S"), msg)

    @classmethod
    def log_msg(cls, msg):
        """Method to print a log message to the console, with the 'msg' colors

        Args:
            msg (str): log msg
        """
        print("{}{}{}").format(
            cls.CLR_MSG, cls.log_format(msg), cls.CLR_END)

    @classmethod
    def log_success(cls, msg):
        """Method to print a log message to the console, with the 'success'
        colors

        Args:
            msg (str): log msg
        """
        print("{}{}{}").format(
            cls.CLR_SUCCESS, cls.log_format(msg), cls.CLR_END)

    @classmethod
    def log_warning(cls, msg):
        """Method to print a log message to the console, with the 'warning'
        colors

        Args:
            msg (str): log msg
        """
        print("{}{}{}").format(
            cls.CLR_WARNING, cls.log_format(msg), cls.CLR_END)

    @classmethod
    def log_error(cls, msg):
        """Method to print a log message to the console, with the 'error'
        colors

        Args:
            msg (str): log msg
        """
        print("{}{}{}").format(
            cls.CLR_ERROR, cls.log_format(msg), cls.CLR_END)
