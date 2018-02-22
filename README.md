# kcauto-kai

**kcauto-kai** is a robust Kantai Collection automation tool. kcauto-kai and it's predecessor, [kancolle-auto](https://github.com/mrmin123/kancolle-auto), are proof-of-concepts in using [Sikuli](http://sikulix.com/) for vision-based automation to play Kantai Collection. They are an exercises in automating large, convoluted, and complex game-playing logic.

kcauto-kai is not designed to be the fastest automation tool, but is instead robust, highly customizable, and relatively safe to use. Please read the Disclaimer below before use!

---

Please submit bugs and feature requests on the [kcauto-kai issue tracker](https://github.com/mrmin123/kcauto-kai/issues). Also consider joining the [kcauto-kai Discord server](https://discord.gg/smAhRKw) for kcauto-kai news, updates, and discussion. For more general Kantai Collection discussion, please join the [sister Discord server](https://discord.gg/2tt5Der).

Also, consider supporting the developer on [Patreon](https://www.patreon.com/mrmin123) or [MakerSupport](https://www.makersupport.com/mrmin123)!

<a href="https://www.patreon.com/mrmin123"><img src="https://c5.patreon.com/external/logo/become_a_patron_button.png" width="130" /></a>

---

> ### Disclaimer

> kcauto-kai is meant for educational purposes only! Actual and prolonged usage of kcauto-kai may result in your account being banned. Remember that botting is against rules! The developer of kcauto-kai makes no guarantee that the end-user will not be caught and penalized for using kcauto-kai, and does not take any responsibility for any repercussions that befall the end-user. Non-stop expeditions and sorties increases the chances of being flagged and banned for botting.

> In addition, although unlikely, you may lose ships if you allow kcauto-kai to conduct combat sorties. While kcauto-kai has been painstakingly designed to reduce the chances of this happening, the developer of kcauto-kai does not take responsibility regarding loss of ships and/or resources.

---

### Features

* Expedition Module &mdash; automate expeditions
  * Multiple expeditions per fleet
  * Event and non-event boss and node support expeditions
* PvP Module &mdash; automate PvP
  * Automatic diamond or line abreast formations against submarine-heavy opponents
* Combat Module &mdash; automate combat sorties
  * Two available modes: Live and Legacy
    * Live: tracks fleet position and automatically makes formation, night battle, retreat, and node selects based on specified JSON files
    * Legacy: specify formation, night battle, retreat on a per-#-node basis
* LBAS Module &mdash; automatic LBAS management
  * Automatic resupply, fatigue management, and node assignment
* Ship Switcher Module &mdash; automatic switching of ships based on specified criteria between combat sorties
* Quests Module &mdash; automatic quest management
* Repair & Resupply Modules &mdash; automatic resupply and repair of fleet ships
* Scheduled sleep/pausing of script
* Stats Module &mdash; keeps stats on various actions performed
* Random variations in navigation, timers, and click positions to combat bot detection
* [Web interface](https://mrmin123.github.io/kcauto-kai/) to generate and modify config files


### Installation and Usage

1. Install [Java JRE 8](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html)
2. Install the latest [SikuliX Nightly](http://nightly.sikuli.de/) with option 1 (Pack 1) selected
3. Download kcauto-kai either by downloading the repo or cloning it
4. Set up kcauto-kai's config file using the [web interface](https://mrmin123.github.io/kcauto-kai/) or by opening the local copy of `docs/index.html` in a browser
5. Run Kantai Collection in your favorite browser or viewer
6. Run kcauto-kai using the command `java -jar <path_to_sikuli>/sikulix.jar -r <path_to_kcauto-kai>/kcauto-kai.sikuli` (replacing `<path_to_sikuli>` and `<path_to_kcauto-kai>` with the correct directories for your installs); you can also use the [RunCmd tab](https://mrmin123.github.io/kcauto-kai/#runcmd) of the web interface to help generate the command
