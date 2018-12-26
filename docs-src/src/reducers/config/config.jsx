import { SET_JSON_CONFIG, SET_PYTHON_CONFIG } from 'types/index'
import {
  PAUSE_OPTIONS, STOP_MODE_OPTIONS, EXPEDITIONS, COMBAT_ENGINES, MAPS, COMBINED_FLEET_MODES, DAMAGE_STATES, FREQUENCIES,
  DIFFICULTIES,
} from 'types/formOptions'

const jsonConfigDefaults = {
  dropzoneActive: false,
  generalProgram: 'Chrome',
  generalJSTOffset: (-((new Date().getTimezoneOffset() / 60) + 9)).toString(10),
  generalPause: PAUSE_OPTIONS.filter(val => val.value === false)[0],
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
  scheduledStopExpeditionStopMode: STOP_MODE_OPTIONS.filter(opt => opt.value === 'module')[0],
  scheduledStopExpeditionStopCount: '',
  scheduledStopExpeditionStopTime: null,
  scheduledStopCombatStopEnabled: false,
  scheduledStopCombatStopMode: STOP_MODE_OPTIONS.filter(opt => opt.value === 'module')[0],
  scheduledStopCombatStopCount: '',
  scheduledStopCombatStopTime: null,
  expeditionsEnabled: true,
  expeditionsFleet2Enabled: true,
  expeditionsFleet3Enabled: true,
  expeditionsFleet4Enabled: true,
  expeditionsFleet2: EXPEDITIONS.filter(opt => opt.value === '2'),
  expeditionsFleet3: EXPEDITIONS.filter(opt => opt.value === '5'),
  expeditionsFleet4: EXPEDITIONS.filter(opt => opt.value === '38'),
  pvpEnabled: true,
  pvpFleet: null,
  combatEnabled: false,
  combatEngine: COMBAT_ENGINES.filter(opt => opt.value === 'live')[0],
  combatFleets: [],
  combatMap: MAPS.filter(opt => opt.value === '1-1')[0],
  combatFleetMode: COMBINED_FLEET_MODES.filter(opt => opt.value === '')[0],
  combatRetreatNodes: [],
  combatNodeSelect1: null,
  combatNodeSelect2: null,
  combatNodeSelects: [],
  combatFormationsNode: null,
  combatFormationsFormation: null,
  combatFormations: [],
  combatNightBattlesNode: null,
  combatNightBattlesMode: null,
  combatNightBattles: [],
  combatRetreatLimit: DAMAGE_STATES.filter(opt => opt.value === 'heavy')[0],
  combatRepairLimit: DAMAGE_STATES.filter(opt => opt.value === 'moderate')[0],
  combatRepairTimeLimit: new Date(new Date().setHours(0, 30, 0, 0)),
  combatLBASGroups: [],
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
  combatOptionLastNodePush: false,
  eventResetEnabled: false,
  eventResetFrequency: FREQUENCIES.filter(opt => opt.value === '3')[0],
  eventResetFarmDifficulty: DIFFICULTIES.filter(opt => opt.value === 'easy')[0],
  eventResetResetDifficulty: DIFFICULTIES.filter(opt => opt.value === 'medium')[0],
  shipSwitcherEnabled: false,
  shipSwitcherSlot1Criteria: [],
  shipSwitcherSlot1Ships: [],
  shipSwitcherSlot2Criteria: [],
  shipSwitcherSlot2Ships: [],
  shipSwitcherSlot3Criteria: [],
  shipSwitcherSlot3Ships: [],
  shipSwitcherSlot4Criteria: [],
  shipSwitcherSlot4Ships: [],
  shipSwitcherSlot5Criteria: [],
  shipSwitcherSlot5Ships: [],
  shipSwitcherSlot6Criteria: [],
  shipSwitcherSlot6Ships: [],
  questsEnabled: true,
  questsQuestGroupsDaily: true,
  questsQuestGroupsWeekly: true,
  questsQuestGroupsMonthly: true,
  questsQuestGroupsOthers: true,
}

export const jsonConfig = (state = jsonConfigDefaults, action) => {
  switch (action.type) {
    case SET_JSON_CONFIG:
      return action.config
    default:
      return state
  }
}

export const pythonConfig = (state = [], action) => {
  switch (action.type) {
    case SET_PYTHON_CONFIG:
      return action.config
    default:
      return state
  }
}
