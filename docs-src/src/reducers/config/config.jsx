import * as types from 'types/'

const jsonConfigDefaults = {
  dropzoneActive: false,
  generalProgram: 'Chrome',
  generalJSTOffset: '0',
  scheduledSleepEnabled: true,
  scheduledSleepStart: new Date(new Date().setHours(0, 0, 0, 0)),
  scheduledSleepLength: '4',
  expeditionsEnabled: false,
  expeditionsFleet2Enabled: true,
  expeditionsFleet3Enabled: true,
  expeditionsFleet4Enabled: true,
  expeditionsFleet2: '2',
  expeditionsFleet3: '5',
  expeditionsFleet4: '38',
  pvpEnabled: false,
  combatEnabled: false,
  combatEngine: 'legacy',
  combatMap: '1-1',
  combatFleetMode: '',
  combatCombatNodes: null,
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
  combatOptionMedalStop: false,
  questsEnabled: true,
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
