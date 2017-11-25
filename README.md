# kcauto-kai

**kcauto-kai** is a robust Kantai Collection automation tool. The successor to [kancolle-auto](https://github.com/mrmin123/kancolle-auto), both it and kcauto-kai are proof-of-concepts in using [Sikuli](http://sikulix.com/) for vision-based scripting to automate the playing of Kantai Collection and are exercises in automating large, convoluted, and complex game logic. It is not designed to be the fastest automation tool, but instead designed to be robust and highly customizable. Please read the Disclaimer section before use!

### Beta Notice

kcauto-kai is still in beta. This means that it is relatively unstable and full of undiscovered bugs and behavior. In addition, certain features from kancolle-auto have yet to have been ported over: Medal Stop, Reserve Docks, Submarine Switcher, Fleet Switcher, and a robust recovery system are still not in place. If you rely on these functionality please retain a working copy of kancolle-auto until they have been ported to kcauto-kai. If you'd like to report any bugs or unexpected behavior, please open an [issue ticket](https://github.com/mrmin123/kcauto-kai/issues) or reach out to me on the [kcauto-kai Discord](https://discord.gg/smAhRKw).

### Disclaimer

kcauto-kai is meant for educational purposes only! Actual and prolonged usage of kcauto-kai may result in your account being banned. Remember that botting is against rules! The author of kcauto-kai makes no guarantee that the end user will not be caught and penalized for using kcauto-kai, and will not take any responsibility for any repercussions that befall the end user. Spamming expeditions and sorties nonstop raises your chances of being flagged and banned.

In addition, although unlikely, you may lose ships if you allow kcauto-kai to conduct combat sorties. While kcauto-kai has been painstakingly designed to reduce the chances of this happening, the author of kcauto-kai takes no responsibility regarding the preservation of your ships.

### Quick Start

1. Install [Java JRE 8](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html)
2. Install the latest [SikuliX Nightly](http://nightly.sikuli.de/) with option 1 (Pack 1) selected
3. Download kcauto-kai either by downloading the repo or cloning it
4. Set up kcauto-kai's config file using the [web interface](https://mrmin123.github.io/kcauto-kai) or by opening your local copy of `docs/index.html` in a browser
5. Run Kantai Collection in your favorite browser or viewer
6. Run kcauto-kai using command `java -jar <path_to_sikuli>/sikulix.jar -r <path_to_kcauto-kai>/kcauto-kai.sikuli` (replacing `<path_to_sikuli>` and `<path_to_kcauto-kai>` with the correct directories for your installs)
