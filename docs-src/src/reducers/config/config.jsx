import * as types from 'types/'

const jsonConfigDefaults = {
  dropzoneActive: false,
  generalProgram: 'Chrome',
  generalJSTOffset: -((new Date().getTimezoneOffset() / 60) + 9),
  generalPause: false,
  scheduledSleepScriptSleepEnabled: true,
  scheduledSleepScriptSleepStartTime: new Date(new Date().setHours(0, 0, 0, 0)),
  scheduledSleepScriptSleepLength: '4',
  scheduledSleepExpeditionSleepEnabled: false,
  scheduledSleepExpeditionSleepStartTime: new Date(new Date().setHours(0, 0, 0, 0)),
  scheduledSleepExpeditionSleepLength: '3',
  scheduledSleepCombatSleepEnabled: false,
  scheduledSleepCombatSleepStartTime: new Date(new Date().setHours(0, 0, 0, 0)),
  scheduledSleepCombatSleepLength: '5',
  scheduledStopScriptStopEnabled: false,
  scheduledStopScriptStopCount: '',
  scheduledStopScriptStopTime: null,
  scheduledStopExpeditionStopEnabled: false,
  scheduledStopExpeditionStopMode: 'module',
  scheduledStopExpeditionStopCount: '',
  scheduledStopExpeditionStopTime: null,
  scheduledStopCombatStopEnabled: false,
  scheduledStopCombatStopMode: 'module',
  scheduledStopCombatStopCount: '',
  scheduledStopCombatStopTime: null,
  expeditionsEnabled: true,
  expeditionsFleet2Enabled: true,
  expeditionsFleet3Enabled: true,
  expeditionsFleet4Enabled: true,
  expeditionsFleet2: '2',
  expeditionsFleet3: '5',
  expeditionsFleet4: '38',
  pvpEnabled: true,
  pvpFleet: null,
  combatEnabled: false,
  combatEngine: 'live',
  combatFleets: null,
  combatMap: '1-1',
  combatFleetMode: '',
  combatRetreatNodes: null,
  combatNodeSelect1: null,
  combatNodeSelect2: null,
  combatNodeSelects: null,
  combatFormationsNode: null,
  combatFormationsFormation: null,
  combatFormations: null,
  combatNightBattlesNode: null,
  combatNightBattlesMode: null,
  combatNightBattles: null,
  combatRetreatLimit: 'heavy',
  combatRepairLimit: 'moderate',
  combatRepairTimeLimit: new Date(new Date().setHours(0, 30, 0, 0)),
  combatLBASGroups: null,
  combatLBASGroup1Node1: null,
  combatLBASGroup1Node2: null,
  combatLBASGroup2Node1: null,
  combatLBASGroup2Node2: null,
  combatLBASGroup3Node1: null,
  combatLBASGroup3Node2: null,
  combatOptionCheckFatigue: false,
  combatOptionReserveDocks: false,
  combatOptionPortCheck: false,
  combatOptionClearStop: false,
  shipSwitcherEnabled: false,
  shipSwitcherSlot1Criteria: null,
  shipSwitcherSlot1Ships: null,
  shipSwitcherSlot2Criteria: null,
  shipSwitcherSlot2Ships: null,
  shipSwitcherSlot3Criteria: null,
  shipSwitcherSlot3Ships: null,
  shipSwitcherSlot4Criteria: null,
  shipSwitcherSlot4Ships: null,
  shipSwitcherSlot5Criteria: null,
  shipSwitcherSlot5Ships: null,
  shipSwitcherSlot6Criteria: null,
  shipSwitcherSlot6Ships: null,
  questsEnabled: true,
  questsQuestGroupsDaily: null,
  questsQuestGroupsWeekly: null,
  questsQuestGroupsMonthly: null,
  questsQuestGroupsQuarterly: null,
}

export const jsonConfig = (state = jsonConfigDefaults, action) => {
  switch (action.type) {
    case types.SET_JSON_CONFIG:
      return action.config
    default:
      return state
  }
}

export const pythonConfig = (state = [], action) => {
  switch (action.type) {
    case types.SET_PYTHON_CONFIG:
      return action.config
    default:
      return state
  }
}
