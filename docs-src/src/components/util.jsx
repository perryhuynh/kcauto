import {
  PAUSE_OPTIONS, STOP_MODE_OPTIONS, EXPEDITIONS, FLEET_PRESETS, COMBAT_ENGINES, MAPS, COMBINED_FLEET_MODES, NODES,
  DAMAGE_STATES, LBAS_GROUPS, FREQUENCIES, DIFFICULTIES, SWITCH_CRITERIA,
} from 'types/formOptions'

export const createStateObjFromPythonConfig = (pyConfig) => {
  const pyConfigLines = pyConfig.split('\n')
  const pyConfigObj = {}
  let currentSection = ''
  pyConfigLines.forEach((line) => {
    if (line.indexOf('#') === 0) {
      // comment line
    } else if (line === '[General]') {
      currentSection = 'general'
    } else if (line === '[ScheduledSleep]') {
      currentSection = 'scheduledSleep'
    } else if (line === '[ScheduledStop]') {
      currentSection = 'scheduledStop'
    } else if (line === '[Expeditions]') {
      currentSection = 'expeditions'
    } else if (line === '[PvP]') {
      currentSection = 'pvp'
    } else if (line === '[Combat]') {
      currentSection = 'combat'
    } else if (line === '[EventReset]') {
      currentSection = 'eventReset'
    } else if (line === '[ShipSwitcher]') {
      currentSection = 'shipSwitcher'
    } else if (line === '[Quests]') {
      currentSection = 'quests'
    } else {
      const splitLine = line.split(/:(.*)/, 2)
      // valid config line
      let value = splitLine[1] ? splitLine[1].trim() : null
      if (splitLine[0].indexOf('LBASGroup') > -1 && splitLine[0].indexOf('Nodes') > -1) {
        value = value ? value.split(',').map(node => node.trim()) : [null, null]
      } else if (splitLine[0] === 'MiscOptions') {
        value = value ? value.split(',').map(option => option.trim()) : []
      }
      pyConfigObj[`${currentSection}${splitLine[0].trim()}`] = value
    }
  })

  const jsonConfig = {
    dropzoneActive: false,
    generalProgram: pyConfigObj.generalProgram,
    generalJSTOffset: pyConfigObj.generalJSTOffset || '0',
    generalPause: PAUSE_OPTIONS.filter(opt => opt.value === (pyConfigObj.generalPause === 'True'))[0],
    scheduledSleepScriptSleepEnabled: pyConfigObj.scheduledSleepScriptSleepEnabled === 'True',
    scheduledSleepScriptSleepStartTime: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.scheduledSleepScriptSleepStartTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledSleepScriptSleepStartTime.substr(2, 2), 10), 0, 0
      )),
    scheduledSleepScriptSleepLength: pyConfigObj.scheduledSleepScriptSleepLength || '',
    scheduledSleepExpeditionSleepEnabled: pyConfigObj.scheduledSleepExpeditionSleepEnabled === 'True',
    scheduledSleepExpeditionSleepStartTime: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.scheduledSleepExpeditionSleepStartTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledSleepExpeditionSleepStartTime.substr(2, 2), 10), 0, 0
      )),
    scheduledSleepExpeditionSleepLength: pyConfigObj.scheduledSleepExpeditionSleepLength || '',
    scheduledSleepCombatSleepEnabled: pyConfigObj.scheduledSleepCombatSleepEnabled === 'True',
    scheduledSleepCombatSleepStartTime: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.scheduledSleepCombatSleepStartTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledSleepCombatSleepStartTime.substr(2, 2), 10), 0, 0
      )),
    scheduledSleepCombatSleepLength: pyConfigObj.scheduledSleepCombatSleepLength || '',
    scheduledStopScriptStopEnabled: pyConfigObj.scheduledStopScriptStopEnabled === 'True',
    scheduledStopScriptStopCount: pyConfigObj.scheduledStopScriptStopCount || '',
    scheduledStopScriptStopTime: pyConfigObj.scheduledStopScriptStopTime
      ? new Date(new Date().setHours(
        parseInt(pyConfigObj.scheduledStopScriptStopTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledStopScriptStopTime.substr(2, 2), 10), 0, 0
      ))
      : null,
    scheduledStopExpeditionStopEnabled: pyConfigObj.scheduledStopExpeditionStopEnabled === 'True',
    scheduledStopExpeditionStopMode: STOP_MODE_OPTIONS.filter(
      opt => opt.value === pyConfigObj.scheduledStopExpeditionStopMode
    )[0],
    scheduledStopExpeditionStopCount: pyConfigObj.scheduledStopExpeditionStopCount || '',
    scheduledStopExpeditionStopTime: pyConfigObj.scheduledStopExpeditionStopTime
      ? new Date(new Date().setHours(
        parseInt(pyConfigObj.scheduledStopExpeditionStopTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledStopExpeditionStopTime.substr(2, 2), 10), 0, 0
      ))
      : null,
    scheduledStopCombatStopEnabled: pyConfigObj.scheduledStopCombatStopEnabled === 'True',
    scheduledStopCombatStopMode: STOP_MODE_OPTIONS.filter(
      opt => opt.value === pyConfigObj.scheduledStopCombatStopMode
    )[0],
    scheduledStopCombatStopCount: pyConfigObj.scheduledStopCombatStopCount || '',
    scheduledStopCombatStopTime: pyConfigObj.scheduledStopCombatStopTime
      ? new Date(new Date().setHours(
        parseInt(pyConfigObj.scheduledStopCombatStopTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledStopCombatStopTime.substr(2, 2), 10), 0, 0
      ))
      : null,
    expeditionsEnabled: pyConfigObj.expeditionsEnabled === 'True',
    expeditionsFleet2: pyConfigObj.expeditionsFleet2
      ? pyConfigObj.expeditionsFleet2.split(',').map(val => EXPEDITIONS.filter(opt => opt.value === val)[0])
      : [],
    expeditionsFleet3: pyConfigObj.expeditionsFleet3
      ? pyConfigObj.expeditionsFleet3.split(',').map(val => EXPEDITIONS.filter(opt => opt.value === val)[0])
      : [],
    expeditionsFleet4: pyConfigObj.expeditionsFleet4
      ? pyConfigObj.expeditionsFleet4.split(',').map(val => EXPEDITIONS.filter(opt => opt.value === val)[0])
      : [],
    pvpEnabled: pyConfigObj.pvpEnabled === 'True',
    pvpFleet: FLEET_PRESETS.filter(opt => opt.value === pyConfigObj.pvpFleet)[0] || null,
    combatEnabled: pyConfigObj.combatEnabled === 'True',
    combatEngine: COMBAT_ENGINES.filter(opt => opt.value === pyConfigObj.combatEngine)[0],
    combatFleets: pyConfigObj.combatFleets
      ? pyConfigObj.combatFleets.split(',').map(val => FLEET_PRESETS.filter(opt => opt.value === val)[0])
      : [],
    combatMap: MAPS.filter(opt => opt.value === pyConfigObj.combatMap)[0],
    combatFleetMode: COMBINED_FLEET_MODES.filter(opt => opt.value === pyConfigObj.combatFleetMode)[0]
      || COMBINED_FLEET_MODES[0],
    combatDisableExpeditionsFleet2: ['ctf', 'stf', 'transport'].includes(pyConfigObj.combatFleetMode),
    combatDisableExpeditionsFleet3: ['striking'].includes(pyConfigObj.combatFleetMode),
    combatDisableExpeditionsFleet4: false,
    combatDisablePvP: ['ctf', 'stf', 'transport'].includes(pyConfigObj.combatFleetMode),
    combatDisablePvPFleet: pyConfigObj.combatFleetMode !== '',
    combatRetreatNodes: pyConfigObj.combatRetreatNodes
      ? pyConfigObj.combatRetreatNodes.split(',').map(val => ({ label: val, value: val }))
      : [],
    combatNodeSelect1: null,
    combatNodeSelect2: null,
    combatNodeSelects: pyConfigObj.combatNodeSelects
      ? pyConfigObj.combatNodeSelects.split(',').map(val => ({ label: val, value: val }))
      : [],
    combatFormationsNode: null,
    combatFormationsFormation: null,
    combatFormations: pyConfigObj.combatFormations
      ? pyConfigObj.combatFormations.split(',').map(val => ({ label: val, value: val }))
      : [],
    combatNightBattlesNode: null,
    combatNightBattlesMode: null,
    combatNightBattles: pyConfigObj.combatNightBattles
      ? pyConfigObj.combatNightBattles.split(',').map(val => ({ label: val, value: val }))
      : [],
    combatRetreatLimit: DAMAGE_STATES.filter(opt => opt.value === pyConfigObj.combatRetreatLimit)[0]
      || DAMAGE_STATES[0],
    combatRepairLimit: DAMAGE_STATES.filter(opt => opt.value === pyConfigObj.combatRepairLimit)[0]
      || DAMAGE_STATES[1],
    combatRepairTimeLimit: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.combatRepairTimeLimit.substr(0, 2), 10),
        parseInt(pyConfigObj.combatRepairTimeLimit.substr(2, 2), 10), 0, 0
      )),
    combatLBASGroups: pyConfigObj.combatLBASGroups
      ? pyConfigObj.combatLBASGroups.split(',').map(val => LBAS_GROUPS.filter(opt => opt.value === val)[0])
      : [],
    combatLBASGroup1Node1: NODES.filter(opt => opt.value === pyConfigObj.combatLBASGroup1Nodes[0])[0] || null,
    combatLBASGroup1Node2: NODES.filter(opt => opt.value === pyConfigObj.combatLBASGroup1Nodes[1])[0] || null,
    combatLBASGroup2Node1: NODES.filter(opt => opt.value === pyConfigObj.combatLBASGroup2Nodes[0])[0] || null,
    combatLBASGroup2Node2: NODES.filter(opt => opt.value === pyConfigObj.combatLBASGroup2Nodes[1])[0] || null,
    combatLBASGroup3Node1: NODES.filter(opt => opt.value === pyConfigObj.combatLBASGroup3Nodes[0])[0] || null,
    combatLBASGroup3Node2: NODES.filter(opt => opt.value === pyConfigObj.combatLBASGroup3Nodes[1])[0] || null,
    combatOptionCheckFatigue: pyConfigObj.combatMiscOptions.includes('CheckFatigue') || false,
    combatOptionReserveDocks: pyConfigObj.combatMiscOptions.includes('ReserveDocks') || false,
    combatOptionPortCheck: pyConfigObj.combatMiscOptions.includes('PortCheck') || false,
    combatOptionClearStop: pyConfigObj.combatMiscOptions.includes('ClearStop') || false,
    combatOptionLastNodePush: pyConfigObj.combatMiscOptions.includes('LastNodePush') || false,
    eventResetEnabled: pyConfigObj.eventResetEnabled === 'True',
    eventResetFrequency: FREQUENCIES.filter(opt => opt.value === pyConfigObj.eventResetFrequency)[0] || FREQUENCIES[2],
    eventResetFarmDifficulty: DIFFICULTIES.filter(opt => opt.value === pyConfigObj.eventResetFarmDifficulty)[0]
      || DIFFICULTIES[1],
    eventResetResetDifficulty: DIFFICULTIES.filter(opt => opt.value === pyConfigObj.eventResetResetDifficulty)[0]
      || DIFFICULTIES[2],
    shipSwitcherEnabled: pyConfigObj.shipSwitcherEnabled === 'True',
    shipSwitcherSlot1Criteria: pyConfigObj.shipSwitcherSlot1Criteria
      ? pyConfigObj.shipSwitcherSlot1Criteria.split(',').map(val => SWITCH_CRITERIA.filter(opt => opt.value === val)[0])
      : [],
    shipSwitcherSlot1Ships: pyConfigObj.shipSwitcherSlot1Ships
      ? pyConfigObj.shipSwitcherSlot1Ships.split(',').map(val => ({ label: val, value: val }))
      : [],
    shipSwitcherSlot2Criteria: pyConfigObj.shipSwitcherSlot2Criteria
      ? pyConfigObj.shipSwitcherSlot2Criteria.split(',').map(val => SWITCH_CRITERIA.filter(opt => opt.value === val)[0])
      : [],
    shipSwitcherSlot2Ships: pyConfigObj.shipSwitcherSlot2Ships
      ? pyConfigObj.shipSwitcherSlot1Ships.split(',').map(val => ({ label: val, value: val }))
      : [],
    shipSwitcherSlot3Criteria: pyConfigObj.shipSwitcherSlot3Criteria
      ? pyConfigObj.shipSwitcherSlot3Criteria.split(',').map(val => SWITCH_CRITERIA.filter(opt => opt.value === val)[0])
      : [],
    shipSwitcherSlot3Ships: pyConfigObj.shipSwitcherSlot3Ships
      ? pyConfigObj.shipSwitcherSlot3Ships.split(',').map(val => ({ label: val, value: val }))
      : [],
    shipSwitcherSlot4Criteria: pyConfigObj.shipSwitcherSlot4Criteria
      ? pyConfigObj.shipSwitcherSlot4Criteria.split(',').map(val => SWITCH_CRITERIA.filter(opt => opt.value === val)[0])
      : [],
    shipSwitcherSlot4Ships: pyConfigObj.shipSwitcherSlot4Ships
      ? pyConfigObj.shipSwitcherSlot4Ships.split(',').map(val => ({ label: val, value: val }))
      : [],
    shipSwitcherSlot5Criteria: pyConfigObj.shipSwitcherSlot5Criteria
      ? pyConfigObj.shipSwitcherSlot5Criteria.split(',').map(val => SWITCH_CRITERIA.filter(opt => opt.value === val)[0])
      : [],
    shipSwitcherSlot5Ships: pyConfigObj.shipSwitcherSlot5Ships
      ? pyConfigObj.shipSwitcherSlot5Ships.split(',').map(val => ({ label: val, value: val }))
      : [],
    shipSwitcherSlot6Criteria: pyConfigObj.shipSwitcherSlot6Criteria
      ? pyConfigObj.shipSwitcherSlot6Criteria.split(',').map(val => SWITCH_CRITERIA.filter(opt => opt.value === val)[0])
      : [],
    shipSwitcherSlot6Ships: pyConfigObj.shipSwitcherSlot6Ships
      ? pyConfigObj.shipSwitcherSlot6Ships.split(',').map(val => ({ label: val, value: val }))
      : [],
    questsEnabled: pyConfigObj.questsEnabled === 'True',
    questsQuestGroupsDaily: pyConfigObj.questsQuestGroups.includes('daily') || false,
    questsQuestGroupsWeekly: pyConfigObj.questsQuestGroups.includes('weekly') || false,
    questsQuestGroupsMonthly: pyConfigObj.questsQuestGroups.includes('monthly') || false,
    questsQuestGroupsOthers: pyConfigObj.questsQuestGroups.includes('others') || false,
  }

  return jsonConfig
}
