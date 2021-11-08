# kcauto

**kcauto** is a robust Kantai Collection automation tool. kcauto and it's predecessor [kancolle-auto](https://github.com/mrmin123/kancolle-auto) are proof-of-concepts in using vision-based automation to play Kantai Collection. They are exercises in automating large, convoluted, and complex game-playing logic. kcauto is written in Python 3.7.

kcauto is not designed to be the fastest automation tool, but is instead meant to be robust, highly customizable, and relatively safe to use. Please read the Disclaimer below before use!

---

You can also reach out to the dev (Perry) and other kcauto users on [Discord](https://discord.gg/KEHSmUs)!

<a href="https://discord.gg/KEHSmUs"><img src="https://discordapp.com/assets/e4923594e694a21542a489471ecffa50.svg" width="130" /></a>

---

> ### Disclaimer

> kcauto is meant for educational purposes only. Botting is against the rules and prolonged usage of kcauto may result in your account being banned. The developer of kcauto takes no responsibility for repercussions related to the usage of kcauto. You have been warned!

> Although unlikely, users may lose ships and equipment when using kcauto to conduct combat sorties. While kcauto has been painstakingly designed to reduce the chances of this happening, the developer of kcauto does not take responsibility for any loss of ships and/or resources.

### Features

* Expedition &mdash; automate expeditions
  * Multiple expeditions per fleet
  * Event and non-event boss and node support expeditions
* PvP Module &mdash; automate PvP
  * Automatic diamond or line abreast formations against submarine-heavy opponents
* Combat Module &mdash; automate combat sorties
* LBAS Module &mdash; automatic LBAS management
  * Automatic resupply, fatigue management, and node assignment
* Ship Switcher Module &mdash; automatic switching of ships based on specified criteria between combat sorties
* Fleet Switcher Module &mdash; automatic switching of fleet presets for PvP and combat sorties
* Quests Module &mdash; automatic quest management
* Repair & Resupply Modules &mdash; automatic resupply and repair of fleet ships
  * Passive Repair &mdash; automatic repair of non-active ships when docks are available
* Stats &mdash; keeps stats on various actions performed
* Click Tracking &mdash; optional tracking of clicks done by kcauto
* Scheduled and manual sleeping and pausing of individual modules or entire script
* Automatic catbomb and script recovery
* Random variations in navigation, timers, and click positions to combat bot detection
* Hot-reload config files
* Open-source codebase

## Installation

* Install Python 3.7.3
  * Warning for Windows users: *DO NOT* install Python 3.7 the Windows 10 Microsoft Store; this version of Python is not fully functional
  * Note for Windows users: you may need to log out and back in for environment paths to properly propagate
* (Unix only) Install additional pacakges `python3-tk scrot`
* Install pip if not already installed
* (Optional, but recommended) Install `pipenv` using `pip install pipenv`
* Install dependencies:
  * `pip`-mode: `pip install -r requirements.txt`
  * `pipenv`-mode: `pipenv shell`, then `pipenv install --ignore-pipfile`
* Alternative dependencies installation for Windows Users:
    * Run Setup.bat for setup. 

## Kancolle setup

* Run Chrome or Chromium equivalent with the `--remote-debugging-port` option:
  * ex: `chrome --remote-debugging-port=9222`
  * Note: This remote-debugging-enabled instance of Chrome must be the *first* instance of Chrome run. If you have other Chrome windows open, close all of them before re-starting it with remote-debugging enabled.
* Load Kancolle
  * First run: leave it in the 'Start' screen, where you press the button to enter homeport. You will not have to start kcauto from this screen in subsequent runs, although it is recommended you do this after each game maintenance to allow kcauto to load the latest game data.
  * Ensure that the game is scaled to 100% size/1x scaling &mdash; the entire game should be 1200 pixels wide and 720 pixels tall if you take a screenshot of it


## Running kcauto

The following assumes the `python` alias points to Python 3.7. If your alias for Python 3.7 is different (e.g. `python3`, `py -3`), modify the commands as needed. Run these commands on the command line/shell.

* (Windows only) First run `set PYTHONIOENCODING=utf-8`
* Run kcauto in GUI mode: `python kcauto`
* Or, run kcauto in CLI mode: `python kcauto --cli`
  * Run kcauto in CLI mode with a custom config file `custom.json` in the `configs` folder: `python kcauto -cli -cfg custom` (note that you do not add `.json` here)
  * Run kcauto in CLI mode with a custom config file in a custom path: `python kcauto -cli -cfg-path <full-path-to-cfg>`
* Alternative Windows Users Run:
  * Close all existing instances of Chrome.
  * Run Start.bat which starts chrome with port --remote-debugging-port=9222 opened and launches python kcauto GUI by default.
