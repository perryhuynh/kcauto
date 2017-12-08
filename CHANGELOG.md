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
