#### v8.1.0
* Spring 2021 Event Support
* Support for "Strike Force" fleets

#### v8.0.0-rc1
* **kcauto re-write**
  * No longer dependent on Sikuli
  * Runs from Python directly
  * Built-in optional GUI
  * No longer browser-agnostic: requires that kcauto runs on Chrome with a dev port open
  * Multiple interaction mode: mouse-driven or Chrome-driver-driven (does not take over mouse)
  * Utilizes kancolle API payloads directly
  * Optional tracking of clicks
  * New scheduler rules based off of ship rescues
  * Long-awaited Passive Repair capability

#### 7.5.3
* Add fancy Github Sponsor button

#### 7.5.2

* Archive 2019 Summer Event assets (thanks to @perryhuynh)
* Fix bug where Transport fleet mode did not allow for combined fleet formations (thanks to @perryhuynh)

#### 7.5.1

* Update Fleet flag assets to support UI changes from August 2019 Kantai Collection update
* Update Expedition Module logic to better support UI changes from July 2019 Kantai Collection update

#### 7.5.0

* Update Expedition Module logic and assets to support UI changes in July 2019 Kantai Collection update
* Add support for expeditions A4 and 41 in both backend and webUI
* Archive 2019 Spring Event assets

#### 7.4.1

* Add support for event O, P, and Q nodes in webUI
* Add anonymous analytics reporting to webUI
* Update readme

#### 7.4.0

* Add support for 7-2 to kcauto core and webUI
* Update asset in Resupply Module for February 2019 Kantai Collection update
* Remove support for 2019 Setsubun PvP Quest
* Further adjust crash detection functionality

#### 7.3.1

* Dial back the aggressiveness of whitescreen crash detection

#### 7.3.0

* Archive 2019 Winter Event assets
* Add support for 2019 Setsubun PvP quest
* Add support for whitescreen crash recovery
* Refactor Recovery module

#### 7.2.1

* Add support for node ZZ to webUI
* Revise 2019 Winter Event node information
* Bugfix to FleetSwitcher not initializing properly
* Better recovery reports

#### 7.2.0

* Preliminary pass of 2019 Winter Event support (thanks to @perryhuynh)
* Bugfix to Scheduled Stop section of webUI

#### 7.1.1

* Bugfix to config readers (thanks to @perryhuynh)

#### 7.1.0

* Major housekeeping release
  * Refactor and overhaul config reader for cleaner code, hardened config checking, and ease of maintenance moving forward
  * Update, upgrade, refactor, and overhaul webUI for cleaner code, more complex logic, and ease of maintenance moving forward

#### 7.0.0

* Catbomb and Chrome crash recovery mid-combat and mid-PvP
* Improved and dynamic support for boss dialogue screens
* Add `TEXT_SIMILARITY` and `SHIP_LIST_SIMILARITY` variables to `kca_globals` to compensate for fonts being rendered differently on different machines
  * Use when having issues with finding PvP opponents and Expeditions
* Harden escort fleet flagship damage detection
* Add support for variable number of chalkboards pre-event sortie
* Archive 2018 Early Fall Event assets
* Add alt coords for 5-5 boss node
* Bugfix to ShipSwitcher page navigation
* Bugfix to quest logic for quests D9 and D11
* Bugfix and improvements to Recovery module (both Catbomb and Chrome crashes)

#### 6.8.5

* Update assets for better World 6 sortie compatibility
* Update Combat module code and assets to help mitigate mid-sortie crashes
* Bugfix to LBAS module so that kcauto does not crash when all active LBAS groups are in Defense mode

#### 6.8.4

* Bugfix to Combat where Combined Fleet 2nd fleet damage states would carry over to the next sortie

#### 6.8.3

* Bugfix to LBAS fatigue check sometimes not working

#### 6.8.2

* Bugfix to Event-map specific combat region definition

#### 6.8.1

* Push staged 6.8.0 files to master

#### 6.8.0

* Refactor parts of PvP, Combat, and LBAS to avoid blind clicking calls (thanks to @stackhanovets)
* Blind clicks are reported to console
* Additional check in Recovery

#### 6.7.0

* Update FCF assets for FCF compatibility (thanks to @perryhuynh)

#### 6.6.2

* Better fleet icon tracking in Live combat engine
* Hopefully better damage tracking

#### 6.6.1

* Bugfixes to ShipSwitcher not working in various ways
* Bugfix to ClearStop and Event maps so it will only stop after Event map clears only if ClearStop is specified
* Bugfix to page navigation in Repair module
* Bugfix to Next scrolling in Expedition module
* Bugfix/harden OCR matching on numbers and timers

#### 6.6.0

* Additional altCoords specified for boss nodes of event maps
* Additional bugfixes to LBAS
* Bugfix to Event Map sorties shutting down Combat module

#### 6.5.1

* Fix LBAS-related regions

#### 6.5.0

* Add support for 3rd LBAS squadron
* Add back support for sparkle check in ShipSwitcher
* Add additional node for E-2 (thanks to @stackhanovets)
* Update 6-5 panel asset
* Bugfix to infinite loop while being stuck in LBAS resupply/state change
* Other minor fixes and improvements

#### 6.4.0

* Add 2018 Early Fall Event assets
  * Support for E-4 and E-5 (thanks to @ksks222)
* Expanded ship counter region for hopefully more accurate readings (thanks to @waicool20)
* Bugfix to random click coord method calling
* Bugfix to support Line Ahead and Double Line formations when Diamond is not available

#### 6.3.0

* Add ability to specify recover modes via kca_globals
  * Choose whether or not to enable catbomb and/or Chrome recovery
  * Catbomb recovery is turned off by default to deter from recovering through macro detection catbombs
* Update Combined Fleet Formation assets (Combined Fleet sorties should now be compatible)
* Update Combined Fleet icons for hopefully better tracking via Live combat engine
* Update fatigue assets to improve identification on ringed ships
* Streamline navigations to home
* Bugfix to click areas of Next and Prev scroll buttons

#### 6.2.0

* Update Combined Fleet assets (Combined Fleet sorties still not actually compatible)
* Better fleet tracking in Live combat engine
* Add support for Others tab and some Quarterly quests
* Switch out normal distribution for uniform distribution in random coordinate generator

#### 6.1.0

* Add recovery for Chrome tab crashes
* Update Vanguard formation asset (thanks to @perryhuynh)

#### 6.0.0

* Add 2018 Early Fall Event assets
  * Note: Map data is currently incomplete
* Event LBAS support (thanks to @ksks222)
  * LBAS squad 3 still not supported
* Event (Map Progress) Reset feature
  * Resets Event map progress by switching between specified difficulties at specified combat sortie frequency to facilitate Event map farming
  * Update webUI to support Event Reset feature
* Smarter Quest module that only enables combat quests relevant to map being sortied (carrier/sub/transport quests)

#### 5.0.0

* Kantai Collection Phase 2 Block 1 compatibility - 4th (final) pass
  * ShipSwitcher
    * Update config format for ShipSwitcher; please refer to the updated webUI for changes
    * Individual SS and SSV assets are no longer provided
    * Traversing pages in the ship list is a bit funky at the moment
* Update page navigation code
* Update resupply asset
* Revise debug function
* Fix panel assets to account for boss bars
* Fix random gaussian coordinate generator

#### 4.2.0

* Kantai Collection Phase 2 Block 1 compatibility - 3rd pass
  * Combat sorties to all maps should be supported now (thanks to @stackhanovets and @perryhuynh)
  * Support for node select nodes
  * LBAS support for non-Event maps (and excluding Squad 3)
  * Bugfix to damaged flagship detection mid-sortie
  * Bugfix to navigation to equipment page
  * Fix link to Sikuli in readme
  * Some performance improvements to live engine mode
* Ship Switcher is **not** compatible as of this release

#### 4.1.1

* Bugfix to Expeditions not working properly across OS and browsers

#### 4.1.0

* Kantai Collection Phase 2 Block 1 compatibility - 2nd pass
  * For the time being, please use UI 2 (Updated Classic) or UI 4/5 (White)
  * Combat up to map 5-1, and map 7-1 (thanks to Kal, @perryhuynh, ksks222, @zerolength, @millionsbar, @twisting2017)
  * Live Combat Engine ship tracking and optimization
  * Flagship retreat
  * CheckFatigue, ClearStop
  * FleetSwitcher
  * Repair
  * Panel page navigation
  * Updates to Expedition and Expedition assets for better cross-OS/browser compatibility (thanks to @waicool20)
  * Bugfix to Quests not properly being toggled
* The following are currently not compatible with the game. Please **do not** use the following features:
  * Combat to maps not listed above
  * LBAS
  * Ship Switcher

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
