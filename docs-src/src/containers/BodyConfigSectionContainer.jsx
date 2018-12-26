import { connect } from 'react-redux'

import BodyConfigGeneral from 'components/BodyConfigGeneral'
import BodyConfigScheduledSleep from 'components/BodyConfigScheduledSleep'
import BodyConfigScheduledStop from 'components/BodyConfigScheduledStop'
import BodyConfigExpeditions from 'components/BodyConfigExpeditions'
import BodyConfigPvP from 'components/BodyConfigPvP'
import BodyConfigCombat from 'components/BodyConfigCombat'
import BodyConfigEventReset from 'components/BodyConfigEventReset'
import BodyConfigShipSwitcher from 'components/BodyConfigShipSwitcher'
import BodyConfigQuests from 'components/BodyConfigQuests'

const mapGeneralStateToProps = state => (
  {
    config: state.config.jsonConfig,
    generalProgram: state.config.jsonConfig.generalProgram,
    generalJSTOffset: state.config.jsonConfig.generalJSTOffset,
    generalPause: state.config.jsonConfig.generalPause,
  }
)

const mapScheduledSleepStateToProps = state => (
  {
    config: state.config.jsonConfig,
    scheduledSleepScriptSleepEnabled: state.config.jsonConfig.scheduledSleepScriptSleepEnabled,
    scheduledSleepScriptSleepStartTime: state.config.jsonConfig.scheduledSleepScriptSleepStartTime,
    scheduledSleepScriptSleepLength: state.config.jsonConfig.scheduledSleepScriptSleepLength,
    scheduledSleepExpeditionSleepEnabled: state.config.jsonConfig.scheduledSleepExpeditionSleepEnabled,
    scheduledSleepExpeditionSleepStartTime: state.config.jsonConfig.scheduledSleepExpeditionSleepStartTime,
    scheduledSleepExpeditionSleepLength: state.config.jsonConfig.scheduledSleepExpeditionSleepLength,
    scheduledSleepCombatSleepEnabled: state.config.jsonConfig.scheduledSleepCombatSleepEnabled,
    scheduledSleepCombatSleepStartTime: state.config.jsonConfig.scheduledSleepCombatSleepStartTime,
    scheduledSleepCombatSleepLength: state.config.jsonConfig.scheduledSleepCombatSleepLength,
  }
)

const mapScheduledStopStateToProps = state => (
  {
    config: state.config.jsonConfig,
    scheduledStopScriptStopEnabled: state.config.jsonConfig.scheduledStopScriptStopEnabled,
    scheduledStopScriptStopCount: state.config.jsonConfig.scheduledStopScriptStopCount,
    scheduledStopScriptStopTime: state.config.jsonConfig.scheduledStopScriptStopTime,
    scheduledStopExpeditionStopEnabled: state.config.jsonConfig.scheduledStopExpeditionStopEnabled,
    scheduledStopExpeditionStopMode: state.config.jsonConfig.scheduledStopExpeditionStopMode,
    scheduledStopExpeditionStopCount: state.config.jsonConfig.scheduledStopExpeditionStopCount,
    scheduledStopExpeditionStopTime: state.config.jsonConfig.scheduledStopExpeditionStopTime,
    scheduledStopCombatStopEnabled: state.config.jsonConfig.scheduledStopCombatStopEnabled,
    scheduledStopCombatStopMode: state.config.jsonConfig.scheduledStopCombatStopMode,
    scheduledStopCombatStopCount: state.config.jsonConfig.scheduledStopCombatStopCount,
    scheduledStopCombatStopTime: state.config.jsonConfig.scheduledStopCombatStopTime,
  }
)

const mapExpeditionStateToProps = state => (
  {
    config: state.config.jsonConfig,
    expeditionsEnabled: state.config.jsonConfig.expeditionsEnabled,
    expeditionsFleet2: state.config.jsonConfig.expeditionsFleet2,
    expeditionsFleet3: state.config.jsonConfig.expeditionsFleet3,
    expeditionsFleet4: state.config.jsonConfig.expeditionsFleet4,
    combatEnabled: state.config.jsonConfig.combatEnabled,
    combatDisableExpeditionsFleet2: state.config.jsonConfig.combatDisableExpeditionsFleet2,
    combatDisableExpeditionsFleet3: state.config.jsonConfig.combatDisableExpeditionsFleet3,
    combatDisableExpeditionsFleet4: state.config.jsonConfig.combatDisableExpeditionsFleet4,
  }
)

const mapPvPStateToProps = state => (
  {
    config: state.config.jsonConfig,
    pvpEnabled: state.config.jsonConfig.pvpEnabled,
    pvpFleet: state.config.jsonConfig.pvpFleet,
    combatEnabled: state.config.jsonConfig.combatEnabled,
    combatDisablePvP: state.config.jsonConfig.combatDisablePvP,
    combatDisablePvPFleet: state.config.jsonConfig.combatDisablePvPFleet,
  }
)

const mapCombatStateToProps = state => (
  {
    config: state.config.jsonConfig,
    combatEnabled: state.config.jsonConfig.combatEnabled,
    combatEngine: state.config.jsonConfig.combatEngine,
    combatFleets: state.config.jsonConfig.combatFleets,
    combatMap: state.config.jsonConfig.combatMap,
    combatFleetMode: state.config.jsonConfig.combatFleetMode,
    combatRetreatNodes: state.config.jsonConfig.combatRetreatNodes,
    combatNodeSelects: state.config.jsonConfig.combatNodeSelects,
    combatFormations: state.config.jsonConfig.combatFormations,
    combatNightBattles: state.config.jsonConfig.combatNightBattles,
    combatRetreatLimit: state.config.jsonConfig.combatRetreatLimit,
    combatRepairLimit: state.config.jsonConfig.combatRepairLimit,
    combatRepairTimeLimit: state.config.jsonConfig.combatRepairTimeLimit,
    combatLBASGroups: state.config.jsonConfig.combatLBASGroups,
    combatLBASGroup1Node1: state.config.jsonConfig.combatLBASGroup1Node1,
    combatLBASGroup1Node2: state.config.jsonConfig.combatLBASGroup1Node2,
    combatLBASGroup2Node1: state.config.jsonConfig.combatLBASGroup2Node1,
    combatLBASGroup2Node2: state.config.jsonConfig.combatLBASGroup2Node2,
    combatLBASGroup3Node1: state.config.jsonConfig.combatLBASGroup3Node1,
    combatLBASGroup3Node2: state.config.jsonConfig.combatLBASGroup3Node2,
    combatOptionCheckFatigue: state.config.jsonConfig.combatOptionCheckFatigue,
    combatOptionReserveDocks: state.config.jsonConfig.combatOptionReserveDocks,
    combatOptionPortCheck: state.config.jsonConfig.combatOptionPortCheck,
    combatOptionClearStop: state.config.jsonConfig.combatOptionClearStop,
    combatOptionLastNodePush: state.config.jsonConfig.combatOptionLastNodePush,
  }
)

const mapEventResetStateToProps = state => (
  {
    config: state.config.jsonConfig,
    eventResetEnabled: state.config.jsonConfig.eventResetEnabled,
    eventResetFrequency: state.config.jsonConfig.eventResetFrequency,
    eventResetFarmDifficulty: state.config.jsonConfig.eventResetFarmDifficulty,
    eventResetResetDifficulty: state.config.jsonConfig.eventResetResetDifficulty,
    combatEnabled: state.config.jsonConfig.combatEnabled,
    combatMap: state.config.jsonConfig.combatMap,
  }
)

const mapShipSwitcherStateToProps = state => (
  {
    config: state.config.jsonConfig,
    shipSwitcherEnabled: state.config.jsonConfig.shipSwitcherEnabled,
    shipSwitcherSlot1Criteria: state.config.jsonConfig.shipSwitcherSlot1Criteria,
    shipSwitcherSlot1Ships: state.config.jsonConfig.shipSwitcherSlot1Ships,
    shipSwitcherSlot2Criteria: state.config.jsonConfig.shipSwitcherSlot2Criteria,
    shipSwitcherSlot2Ships: state.config.jsonConfig.shipSwitcherSlot2Ships,
    shipSwitcherSlot3Criteria: state.config.jsonConfig.shipSwitcherSlot3Criteria,
    shipSwitcherSlot3Ships: state.config.jsonConfig.shipSwitcherSlot3Ships,
    shipSwitcherSlot4Criteria: state.config.jsonConfig.shipSwitcherSlot4Criteria,
    shipSwitcherSlot4Ships: state.config.jsonConfig.shipSwitcherSlot4Ships,
    shipSwitcherSlot5Criteria: state.config.jsonConfig.shipSwitcherSlot5Criteria,
    shipSwitcherSlot5Ships: state.config.jsonConfig.shipSwitcherSlot5Ships,
    shipSwitcherSlot6Criteria: state.config.jsonConfig.shipSwitcherSlot6Criteria,
    shipSwitcherSlot6Ships: state.config.jsonConfig.shipSwitcherSlot6Ships,
    combatEnabled: state.config.jsonConfig.combatEnabled,
  }
)

const mapQuestStateToProps = state => (
  {
    config: state.config.jsonConfig,
    questsEnabled: state.config.jsonConfig.questsEnabled,
    questsQuestGroupsDaily: state.config.jsonConfig.questsQuestGroupsDaily,
    questsQuestGroupsWeekly: state.config.jsonConfig.questsQuestGroupsWeekly,
    questsQuestGroupsMonthly: state.config.jsonConfig.questsQuestGroupsMonthly,
    questsQuestGroupsOthers: state.config.jsonConfig.questsQuestGroupsOthers,
  }
)

export const BodyConfigGeneralContainer = connect(mapGeneralStateToProps)(BodyConfigGeneral)
export const BodyConfigScheduledSleepContainer = connect(mapScheduledSleepStateToProps)(BodyConfigScheduledSleep)
export const BodyConfigScheduledStopContainer = connect(mapScheduledStopStateToProps)(BodyConfigScheduledStop)
export const BodyConfigExpeditionsContainer = connect(mapExpeditionStateToProps)(BodyConfigExpeditions)
export const BodyConfigPvPContainer = connect(mapPvPStateToProps)(BodyConfigPvP)
export const BodyConfigCombatContainer = connect(mapCombatStateToProps)(BodyConfigCombat)
export const BodyConfigEventResetContainer = connect(mapEventResetStateToProps)(BodyConfigEventReset)
export const BodyConfigShipSwitcherContainer = connect(mapShipSwitcherStateToProps)(BodyConfigShipSwitcher)
export const BodyConfigQuestsContainer = connect(mapQuestStateToProps)(BodyConfigQuests)
