#### 4.0.0

* Kantai Collection Phase 2 Block 1 compatibility - 1st pass
  * Expedition
  * PvP
  * Quests
  * Navigation
  * Basic combat up to map 1-3
* The following are currently not compatible with the game. Please **do not** use the following features:
  * Combat beyond map 1-3
  * LBAS
  * Ship Switcher
  * CheckFatigue
  * ClearStop

#### 3.1.1

* Critical bugfix to Combat module
* Critical bugfix to FleetSwitcher module

#### 3.1.0

* Improvements to Live Combat Engine's node detection logic
* Improvements and bugfixes to FleetSwitcher module
  * Fleet Switcher stats are now tracked and reported
  * Fleet Switcher only switches when previously set fleet preset is different from the new fleet preset

#### 3.0.0

* Add support for expedition fleet resupply fairy
  * Resupply fairy availability is automatically determined
* Add support for extra expeditions (A1-A3, B1-B2)
* Better labeling of expeditions in webUI
* Bugfix to FleetSwitcher
* ***Note**: 2.0.0 configs are compatible with 3.0.0, but 3.0.0 configs may not be backwards-compatible with 2.0.0*

#### 2.0.0

* Rename kcauto-kai to kcauto. Please update your repos and/or bookmarks!
* It may be overkill, but adopt [Semantic Versioning](https://semver.org/)

#### 1.0.0

* Implement FleetSwitcher functionality
  * Can specify 1 fleet preset for PvP, and multiple fleet presets for Combat
* Improvements to Quest module
  * Add ability to filter out daily, weekly, and/or monthly quests
  * Quest module is now context aware: only turns on PvP quests if doing PvP, Combat quests if doing combat
* Support for setting custom retreat node via config
* Bugfixes to ShipSwitcher module

#### 0.5.1

* Fix PortCheck on non-Event maps
* Better checking of fatigue on ringed ships
* Stability fix to live combat engine
* Bugfix to sparkle mode in ShipSwitcher

#### 0.5.0

* Implements ScheduledStop functionality
* Support fleet-specific ship repairs past the first page of the repair screen's ship list
* Optimizations and bugfixes to node detection in live combat engine
* Bugfix to ShipSwitcher being stuck on the last page
* Bugfix to Expedition module crash when attempting to sortie a fleet with ships under repair

#### 0.4.6-bugfix

* Bugfix to repair module crashing if no timers are stored (thanks to @perryhuynh)

#### 0.4.6

* Improvements to setting of next combat timer based on repair timers in various situations
* Implement daily quest reset
* Force resupply after ship switching
* Longer transient waits in Ship Switcher module

#### 0.4.5

* Archive 2018 Winter Event assets
* Add 6-5 support (thanks to @perryhuynh)
* Add additional fallback formations to combat module
* Better handling of expedition retrieval
* Bugfix with formation selections with legacy combat engine
* Additional checks in config reader regarding LBAS setups
* Hopeful bugfix where sometimes LBAS resupply action fails
* Bugfix to webUI where importing previous configs did not work
* Additional stats reported at end of cycle

#### 0.4.4

* Add ability to set buffer time between sorties in `kca_globals` to allow for natural fatigue recovery
* Improvements to Catbomb Recovery and Recovery module in general
* Bugfix in LBAS module to support newer versions of Sikuli
* Bugfix in Combat module to ensure proper handling of damaged escort fleet flagship
* Hopeful bugfix to address proper handling of receiving two or more expeditions in close proximity of each other

#### 0.4.3

* Bugfix to ShipSwitcher

#### 0.4.2

* Fixes and improvements to ShipSwitcher
  * When sparkling while specifying ships by class, ShipSwitcher will no longer revisit pages that did had valid ships but no available ships
  * When sparkling while specifying ships by class, ShipSwitcher will end the combat module if there are no ships in the port available to be sparkled
  * When specifying ships by position, ShipSwitcher will no longer switch in ships already in other fleets (thanks to @angryturbot)
  * Better detection of Musashi Kai Ni sparkle state
* Revised and fixed Basic and Catbomb Recoveries
* Defaults Striking Fleet formations to Vanguard
* Bugfix to rare navigation bug after an expedition is received, not resupplied, then the script goes into recovery
* Bugfix to E-5 map JSON (thanks to @sakura-quest)

#### 0.4.1

* Add 2018 Winter Event assets (thanks to @perryhuynh and @twisting2017)
* Bugfix to LBAS assets

#### 0.4.0

* Pause capability
  * If set to True, kcauto-kai will pause operations until you set it to False again, allowing you to interact with the game with no time pressure without having to stop and restart kcauto-kai
* Expanded Scheduled Sleep options
  * You can now set separate scheduled sleeps for the Expedition and Combat modules
  * Note that the kcauto-kai scheduled sleep overrides both Expedition and Combat module-level sleeps
* Better handling of ending on resource nodes - should alleviate instances of infinite looping while clicking on the screen after ending on a resource node
* Bugfix to Combat where the program would crash when attempting to sortie a Striking Fleet
* Added `ISSUE_TEMPLATE.md` and preliminary `CONTRIBUTING.md`
* Minor tweaks to webUI

#### 0.3.3

* Bugfix to ShipSwitcher where specifying multiple ships via level would only apply the level rules of the last specified ship

#### 0.3.2

* Changes and bugfixes to ShipSwitcher
  * More console messages
  * When sparkling, ShipSwitcher will no longer re-visit previously checked ships
  * When sparkling, ShipSwitcher will disable the Combat module if there are no more potential ships to switch to, avoiding infinite sorties with the last ship
* Changes and bugfixes to Combat module
  * More console messages
  * Better handling of post-combat screens
  * Combat stats will report when the module was disabled
* Bugfix to Repair module
  * Repair module should not get stuck trying to repair damaged ships in fleet when all docks are full

#### 0.3.1

* Bugfixes to ShipSwitcher (thanks to @Perry for heavy testing)
* Updates to webUI

#### 0.3.0

* Implements the ShipSwitcher module (thanks to @Perry for heavy testing)
  * Allows for switching of ships based on class, ship, or position on a per-slot basis and based on damage, fatigue, or sparkled status
  * Due to the complexity of the config, it is strongly recommended that the [webUI](https://mrmin123.github.io/kcauto-kai/) be used to generate the relevant config
  * May be buggy
* Implements `ClearStop` combat option
  * Like the `MedalStop` option of kancolle-auto, but also works for Event maps
  * May be buggy
* New damage-state assets for more accurate damage state detection of ringed ships
* Added Patreon link to UI, in case you want to support the dev!
* Major refactor of webUI
* Various performance and memory optimizations
* Various tweaks and bugfixes

#### 0.2.10

* Bugfix in combat and fleet modules

#### 0.2.9

* Add support for LBAS in non-Event maps
* Fix bug in `MapData` leading to incorrect node detection in the live combat engine

#### 0.2.8

* Update live combat engine to support 'retreat' node types via the JSON file (currently applied to 1-3E, 2-4C, 3-1A, and 4-1H)
* Revise expedition retrieval logic to reduce chance of infinite logic loop
* Add expeditions 33 and 34 to list of expeditions that get reset after a combat sortie
* Bugfix in Combat module where the script would hang if a sortie ended on a resource node
* Fix typo on webUI

#### 0.2.7

* Revise sleeps for expeditions and click points for PvP
* Add Run Cmd tab to webUI: refer to this tab if you need help building the command needed to start kcauto-kai from the command line/terminal
* Localization support to webUI
  * Currently English and partial Korean support only; please refer to `docs-src/localizations/_template.jsx` if you would like to provide additional localization options for the webUI
* webUI automatically calculates JST offset on initial load
* Add footer to webUI that displays the version of kcauto-kai the webUI is compatible with
* Various code cleanup on webUI

#### 0.2.6

* Bugfix where combat sorties could not be started if LBAS was enabled but all groups were set on air defense
* Revised formation check areas in preparation for vanguard formation being removed from game

#### 0.2.5

* Critical bugfix on combined fleet 2nd flagship damage checking - please update if you use kcauto-kai to sortie to combined fleet maps

#### 0.2.4

* Minor bugfixes

#### 0.2.3

* Better cross-talk between Repair and Combat modules - Repair module will set the Combat module's next sortie time more accurately
* Improvements to console output
* Bugfixes in webUI and Combat module

#### 0.2.2

* Bugfix on webUI where the scheduledSleep options were not being exported properly

#### 0.2.1

* webUI config options does not reset when changing tabs to About and back
* webUI now supports loading of existing kcauto-kai configs; use the 'Load' button and select your file, or drag and drop the file into the browser
* Minor bugfix in Config module

#### 0.2.0

* Implements the Combat Engine option
  * 'legacy' uses per-combat-node specification of formations and night battles
  * 'live' uses live tracking of the fleet icon to automatically determine formations and night battles
* Implements the Formations and NightBattles options
  * Formations are comma-separated and must be specified in the form of <Node>:<Formation>
  * NightBattles are comma-separated and must be specified in the form of <Node>:<True|False>
  * The <Node>s for the two options must be specified as the nth-combat node number in 'legacy' mode. In 'live' mode, the <Node>s can be specified as either the nth-combat node number or the alpha-numeric node name. The nth-combat node number takes priority over the alpha-numeric node name
* Updates the webUI to support the above additions to the config
* Hardens `wait_and_click_and_wait()` so the script is less likely to crash when the Kantai Collection servers are slow
* Improves `recovery()` so that it attempts to recovery in more locations
* Various bugfixes

#### 0.1.3

* Implements checks for damage state of flagship of escort fleet in combined fleets; if it is the only heavily damaged ship in the combined fleet it will not retreat since it is immune to sinking
* Updates E-4 map data
* Minor bugfixes

#### 0.1.2 (webUI only)

* Better handling of LBAS Group Node assignment on webUI

#### 0.1.1

* Updates E-4 map data
* Tweaks to resupply logic to avoid crashes when clicking the resupply all button does not resolve the first time
* Tweaks to loop between combat nodes to properly resolve with 1-ship fleets
* Bugfix on web UI where 'minor' damage was denoted as 'light'

#### 0.1.0

* Initial beta release
