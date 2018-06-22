# kcauto

**kcauto** (previously called kcauto-kai) is a robust Kantai Collection automation tool. kcauto and it's predecessor, [kancolle-auto](https://github.com/mrmin123/kancolle-auto), are proof-of-concepts in using [Sikuli](http://sikulix.com/) for vision-based automation to play Kantai Collection. They are exercises in automating large, convoluted, and complex game-playing logic. The primary logic of kcauto is written in Jython 2.7, with a standalone browser interface for config generation written in React JavaScript.

kcauto is not designed to be the fastest automation tool, but is instead robust, highly customizable, and relatively safe to use. Please read the Disclaimer below before use!

---

Consider supporting the developer on [Patreon](https://www.patreon.com/mrmin123) or [MakerSupport](https://www.makersupport.com/mrmin123)!

<a href="https://www.patreon.com/mrmin123"><img src="https://c5.patreon.com/external/logo/become_a_patron_button.png" width="130" /></a>

---

> ### Disclaimer

> kcauto is meant for educational purposes only. Botting is against the rules and prolonged usage of kcauto may result in your account being banned. The developer of kcauto takes no responsibility for repercussions related to the usage of kcauto. You have been warned!

> Although unlikely, users may lose ships and equipment when using kcauto to conduct combat sorties. While kcauto has been painstakingly designed to reduce the chances of this happening, the developer of kcauto does not take responsibility for any loss of ships and/or resources.

---

### Features

* Expedition Module &mdash; automate expeditions
  * Multiple expeditions per fleet
  * Event and non-event boss and node support expeditions
* PvP Module &mdash; automate PvP
  * Automatic diamond or line abreast formations against submarine-heavy opponents
* Combat Module &mdash; automate combat sorties
  * Choice between [Live and Legacy combat engines](https://github.com/mrmin123/kcauto/wiki/Config:-Combat-section#engine)
* LBAS Module &mdash; automatic LBAS management
  * Automatic resupply, fatigue management, and node assignment
* Ship Switcher Module &mdash; automatic switching of ships based on specified criteria between combat sorties
* Fleet Switcher Module &mdash; automatic switching of fleet presets for PvP and combat sorties
* Quests Module &mdash; automatic quest management
* Repair & Resupply Modules &mdash; automatic resupply and repair of fleet ships
* Stats &mdash; keeps stats on various actions performed
* Scheduled and manual sleeping and pausing of individual modules or entire script
* Automatic catbomb and script recovery
* Browser/viewer-agnostic
* Random variations in navigation, timers, and click positions to combat bot detection
* Open-source codebase and no reporting or phoning home
* Hot-reload config files
* [Web interface](https://mrmin123.github.io/kcauto/) to generate and modify config files


### Installation and Usage

1. Install [Java JRE 8](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html)
2. Install the latest [SikuliX Nightly](https://raiman.github.io/SikuliX1/nightly.html) with option 1 (Pack 1) selected
3. Download kcauto either by downloading the repo or cloning it
4. Set up kcauto's config file using the [web interface](https://mrmin123.github.io/kcauto/) or by opening the local copy of `docs/index.html` in a browser
    * Please refer to the [Wiki](https://github.com/mrmin123/kcauto/wiki/Configuration#config-file) for a detailed explanation of each of the config fields
5. Run Kantai Collection in your favorite browser or viewer
    * Take note to turn off any browser/viewer features that obscure parts of the game screen (such as subtitles). These have the ability to hinder proper damage state detection by kcauto, which may lead to loss of ships.
6. Run kcauto using the command `java -jar <path_to_sikuli>/sikulix.jar -r <path_to_kcauto>/kcauto.sikuli` (replacing `<path_to_sikuli>` and `<path_to_kcauto>` with the correct directories for your installs); you can also use the [RunCmd tab](https://mrmin123.github.io/kcauto/#runcmd) of the web interface to help generate the command

Users not comfortable with the command line and looking for a GUI solution can use [KAGA](https://github.com/waicool20/KAGA) to both create the config and run kcauto. Please note that KAGA is not developed by the developer of kcauto, and there may be times when KAGA is not compatible with the latest version of kcauto.

### Updating

The preferred method of keeping kcauto up to date is via git. This requires you have a working [git](https://git-scm.com/) installation, have cloned the kcauto repository, and are running kcauto off of said clone.

If you do have git and cloned the kcauto repository, use one of the following command to update to the latest release (`master` version) of kcauto:

* `git pull origin master` or `git pull`

If you do not have git but would still like to keep up with `master`, please use [this guide](https://github.com/KC3Kai/KC3Kai/wiki/Setup-development-build) for setting up tortoisegit, but with the clone URL changed to `https://github.com/mrmin123/kcauto.git`

If you do not have git, tortoisegit, or a clone of the kcauto repository, head to the [Releases page](https://github.com/mrmin123/kcauto/releases) and download the latest tagged version. Overwrite your local kcauto installation with the contents of the new release, taking care to first back up or not overwrite your config file. Note that your config file may need updating to be compatible with new releases.

### Getting help and contacting the dev

Please submit bugs and feature requests on the [kcauto issue tracker](https://github.com/mrmin123/kcauto/issues). Please make sure you are on the latest release of kcauto and that the bug/feature has not been reported already before opening an issue on the tracker.

In addition, there are two kcauto-related Discord servers available:
* The [official kcauto server](https://discord.gg/KEHSmUs) &mdash; join for kcauto-specific news, updates, help, and discussion
* The [Kancolle Auto server](https://discord.gg/2tt5Der) &mdash; maintained by the developer of KAGA; join for KAGA updates, unofficial kcauto news and help, and general Kantai Collection discussion

If you need to get in touch with the developer of kcauto, please join the official kcauto server or DM **mrmin123#4639** on Discord. Please allow up to 24h for a response due to my busy schedule. Feature requests are best done via the Github issue tracker.

### Contributing

If you would like to contribute to the development of kcauto, whether in the form of new features, bugfixes, documentation, or translations, please read the [contribution guide](https://github.com/mrmin123/kcauto/blob/master/CONTRIBUTING.md) first.
