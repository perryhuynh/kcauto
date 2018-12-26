import * as types from 'types/'

export const setJsonConfigSuccess = config => (
  {
    type: types.SET_JSON_CONFIG,
    config,
  }
)

export const setJsonConfig = config => (
  dispatch => (
    dispatch(setJsonConfigSuccess(config))
  )
)

export const setPythonConfigSuccess = config => (
  {
    type: types.SET_PYTHON_CONFIG,
    config,
  }
)

export const setPythonConfig = config => (
  (dispatch) => {
    const configTemp = Object.keys(config).reduce((configTemp, key) => {
      const temp = configTemp
      switch (config[key]) {
        case true:
          temp[key] = 'True'
          break
        case false:
          temp[key] = 'False'
          break
        case null:
          temp[key] = ''
          break
        default:
          temp[key] = config[key]
      }
      return temp
    }, {})
    const scheduledSleepScriptSleepStartTime = config.scheduledSleepScriptSleepStartTime
      ? `${String(config.scheduledSleepScriptSleepStartTime.getHours()).padStart(2, '0')}`
        + `${String(config.scheduledSleepScriptSleepStartTime.getMinutes()).padStart(2, '0')}`
      : '0000'
    const scheduledSleepExpeditionSleepStartTime = config.scheduledSleepExpeditionSleepStartTime
      ? `${String(config.scheduledSleepExpeditionSleepStartTime.getHours()).padStart(2, '0')}`
        + `${String(config.scheduledSleepExpeditionSleepStartTime.getMinutes()).padStart(2, '0')}`
      : '0000'
    const scheduledSleepCombatSleepStartTime = config.scheduledSleepCombatSleepStartTime
      ? `${String(config.scheduledSleepCombatSleepStartTime.getHours()).padStart(2, '0')}`
        + `${String(config.scheduledSleepCombatSleepStartTime.getMinutes()).padStart(2, '0')}`
      : '0000'
    let scheduledStopScriptStopTime
    try {
      scheduledStopScriptStopTime = config.scheduledStopScriptStopTime
        ? `${String(config.scheduledStopScriptStopTime.getHours()).padStart(2, '0')}`
          + `${String(config.scheduledStopScriptStopTime.getMinutes()).padStart(2, '0')}`
        : '0000'
    } catch (e) {
      scheduledStopScriptStopTime = ''
    }
    let scheduledStopExpeditionStopTime
    try {
      scheduledStopExpeditionStopTime = config.scheduledStopExpeditionStopTime
        ? `${String(config.scheduledStopExpeditionStopTime.getHours()).padStart(2, '0')}`
          + `${String(config.scheduledStopExpeditionStopTime.getMinutes()).padStart(2, '0')}`
        : '0000'
    } catch (e) {
      scheduledStopExpeditionStopTime = ''
    }
    let scheduledStopCombatStopTime
    try {
      scheduledStopCombatStopTime = config.scheduledStopCombatStopTime
        ? `${String(config.scheduledStopCombatStopTime.getHours()).padStart(2, '0')}`
          + `${String(config.scheduledStopCombatStopTime.getMinutes()).padStart(2, '0')}`
        : '0000'
    } catch (e) {
      scheduledStopCombatStopTime = ''
    }
    const combatRepairTimeLimit = config.combatRepairTimeLimit
      ? `${String(config.combatRepairTimeLimit.getHours()).padStart(2, '0')}`
        + `${String(config.combatRepairTimeLimit.getMinutes()).padStart(2, '0')}`
      : '0000'
    const combatLBASGroup1Nodes = configTemp.combatLBASGroup1Node1 && configTemp.combatLBASGroup1Node2
      ? `${configTemp.combatLBASGroup1Node1.value},${configTemp.combatLBASGroup1Node2.value}`
      : ''
    const combatLBASGroup2Nodes = configTemp.combatLBASGroup2Node1 && configTemp.combatLBASGroup2Node2
      ? `${configTemp.combatLBASGroup2Node1.value},${configTemp.combatLBASGroup2Node2.value}`
      : ''
    const combatLBASGroup3Nodes = configTemp.combatLBASGroup3Node1 && configTemp.combatLBASGroup3Node2
      ? `${configTemp.combatLBASGroup3Node1.value},${configTemp.combatLBASGroup3Node2.value}`
      : ''
    const combatOptions = []
    if (config.combatOptionCheckFatigue) {
      combatOptions.push('CheckFatigue')
    }
    if (config.combatOptionReserveDocks) {
      combatOptions.push('ReserveDocks')
    }
    if (config.combatOptionPortCheck) {
      combatOptions.push('PortCheck')
    }
    if (config.combatOptionClearStop) {
      combatOptions.push('ClearStop')
    }
    if (config.combatOptionLastNodePush) {
      combatOptions.push('LastNodePush')
    }
    if (!configTemp.shipSwitcherSlot1Criteria.length || !configTemp.shipSwitcherSlot1Ships.length) {
      configTemp.shipSwitcherSlot1Criteria = []
      configTemp.shipSwitcherSlot1Ships = []
    }
    if (!configTemp.shipSwitcherSlot2Criteria.length || !configTemp.shipSwitcherSlot2Ships.length) {
      configTemp.shipSwitcherSlot2Criteria = []
      configTemp.shipSwitcherSlot2Ships = []
    }
    if (!configTemp.shipSwitcherSlot3Criteria.length || !configTemp.shipSwitcherSlot3Ships.length) {
      configTemp.shipSwitcherSlot3Criteria = []
      configTemp.shipSwitcherSlot3Ships = []
    }
    if (!configTemp.shipSwitcherSlot4Criteria.length || !configTemp.shipSwitcherSlot4Ships.length) {
      configTemp.shipSwitcherSlot4Criteria = []
      configTemp.shipSwitcherSlot4Ships = []
    }
    if (!configTemp.shipSwitcherSlot5Criteria.length || !configTemp.shipSwitcherSlot5Ships.length) {
      configTemp.shipSwitcherSlot5Criteria = []
      configTemp.shipSwitcherSlot5Ships = []
    }
    if (!configTemp.shipSwitcherSlot6Criteria.length || !configTemp.shipSwitcherSlot6Ships.length) {
      configTemp.shipSwitcherSlot6Criteria = []
      configTemp.shipSwitcherSlot6Ships = []
    }
    const questGroups = []
    if (config.questsQuestGroupsDaily) {
      questGroups.push('daily')
    }
    if (config.questsQuestGroupsWeekly) {
      questGroups.push('weekly')
    }
    if (config.questsQuestGroupsMonthly) {
      questGroups.push('monthly')
    }
    if (config.questsQuestGroupsOthers) {
      questGroups.push('others')
    }

    const pythonConfig = [
      '[General]',
      `Program: ${configTemp.generalProgram}`,
      `JSTOffset: ${configTemp.generalJSTOffset}`,
      `Pause: ${configTemp.generalPause.value}`,
      '',
      '[ScheduledSleep]',
      `ScriptSleepEnabled: ${configTemp.scheduledSleepScriptSleepEnabled}`,
      `ScriptSleepStartTime: ${scheduledSleepScriptSleepStartTime}`,
      `ScriptSleepLength: ${configTemp.scheduledSleepScriptSleepLength}`,
      `ExpeditionSleepEnabled: ${configTemp.scheduledSleepExpeditionSleepEnabled}`,
      `ExpeditionSleepStartTime: ${scheduledSleepExpeditionSleepStartTime}`,
      `ExpeditionSleepLength: ${configTemp.scheduledSleepExpeditionSleepLength}`,
      `CombatSleepEnabled: ${configTemp.scheduledSleepCombatSleepEnabled}`,
      `CombatSleepStartTime: ${scheduledSleepCombatSleepStartTime}`,
      `CombatSleepLength: ${configTemp.scheduledSleepCombatSleepLength}`,
      '',
      '[ScheduledStop]',
      `ScriptStopEnabled: ${configTemp.scheduledStopScriptStopEnabled}`,
      `ScriptStopCount: ${configTemp.scheduledStopScriptStopCount}`,
      `ScriptStopTime: ${scheduledStopScriptStopTime}`,
      `ExpeditionStopEnabled: ${configTemp.scheduledStopExpeditionStopEnabled}`,
      `ExpeditionStopMode: ${configTemp.scheduledStopExpeditionStopMode.value}`,
      `ExpeditionStopCount: ${configTemp.scheduledStopExpeditionStopCount}`,
      `ExpeditionStopTime: ${scheduledStopExpeditionStopTime}`,
      `CombatStopEnabled: ${configTemp.scheduledStopCombatStopEnabled}`,
      `CombatStopMode: ${configTemp.scheduledStopCombatStopMode.value}`,
      `CombatStopCount: ${configTemp.scheduledStopCombatStopCount}`,
      `CombatStopTime: ${scheduledStopCombatStopTime}`,
      '',
      '',
      '[Expeditions]',
      `Enabled: ${configTemp.expeditionsEnabled}`,
      `Fleet2: ${configTemp.expeditionsFleet2.map(opt => opt.value).join(',')}`,
      `Fleet3: ${configTemp.expeditionsFleet3.map(opt => opt.value).join(',')}`,
      `Fleet4: ${configTemp.expeditionsFleet4.map(opt => opt.value).join(',')}`,
      '',
      '[PvP]',
      `Enabled: ${configTemp.pvpEnabled}`,
      `Fleet: ${configTemp.pvpFleet.value || ''}`,
      '',
      '[Combat]',
      `Enabled: ${configTemp.combatEnabled}`,
      `Engine: ${configTemp.combatEngine.value}`,
      `Fleets: ${configTemp.combatFleets.map(opt => opt.value).join(',')}`,
      `Map: ${configTemp.combatMap.value}`,
      `FleetMode: ${configTemp.combatFleetMode.value}`,
      `RetreatNodes: ${configTemp.combatRetreatNodes.map(opt => opt.value).join(',')}`,
      `NodeSelects: ${configTemp.combatNodeSelects.map(opt => opt.value).join(',')}`,
      `Formations: ${configTemp.combatFormations.map(opt => opt.value).join(',')}`,
      `NightBattles: ${configTemp.combatNightBattles.map(opt => opt.value).join(',')}`,
      `RetreatLimit: ${configTemp.combatRetreatLimit.value}`,
      `RepairLimit: ${configTemp.combatRepairLimit.value}`,
      `RepairTimeLimit: ${combatRepairTimeLimit}`,
      `LBASGroups: ${configTemp.combatLBASGroups.map(opt => opt.value).join(',')}`,
      `LBASGroup1Nodes: ${combatLBASGroup1Nodes}`,
      `LBASGroup2Nodes: ${combatLBASGroup2Nodes}`,
      `LBASGroup3Nodes: ${combatLBASGroup3Nodes}`,
      `MiscOptions: ${combatOptions.join(',')}`,
      '',
      '[EventReset]',
      `Enabled: ${configTemp.eventResetEnabled}`,
      `Frequency: ${configTemp.eventResetFrequency.value}`,
      `FarmDifficulty: ${configTemp.eventResetFarmDifficulty.value}`,
      `ResetDifficulty: ${configTemp.eventResetResetDifficulty.value}`,
      '',
      '[ShipSwitcher]',
      `Enabled: ${configTemp.shipSwitcherEnabled}`,
      `Slot1Criteria: ${configTemp.shipSwitcherSlot1Criteria.map(opt => opt.value).join(',')}`,
      `Slot1Ships: ${configTemp.shipSwitcherSlot1Ships.map(opt => opt.value).join(',')}`,
      `Slot2Criteria: ${configTemp.shipSwitcherSlot2Criteria.map(opt => opt.value).join(',')}`,
      `Slot2Ships: ${configTemp.shipSwitcherSlot2Ships.map(opt => opt.value).join(',')}`,
      `Slot3Criteria: ${configTemp.shipSwitcherSlot3Criteria.map(opt => opt.value).join(',')}`,
      `Slot3Ships: ${configTemp.shipSwitcherSlot3Ships.map(opt => opt.value).join(',')}`,
      `Slot4Criteria: ${configTemp.shipSwitcherSlot4Criteria.map(opt => opt.value).join(',')}`,
      `Slot4Ships: ${configTemp.shipSwitcherSlot4Ships.map(opt => opt.value).join(',')}`,
      `Slot5Criteria: ${configTemp.shipSwitcherSlot5Criteria.map(opt => opt.value).join(',')}`,
      `Slot5Ships: ${configTemp.shipSwitcherSlot5Ships.map(opt => opt.value).join(',')}`,
      `Slot6Criteria: ${configTemp.shipSwitcherSlot6Criteria.map(opt => opt.value).join(',')}`,
      `Slot6Ships: ${configTemp.shipSwitcherSlot6Ships.map(opt => opt.value).join(',')}`,
      '',
      '[Quests]',
      `Enabled: ${configTemp.questsEnabled}`,
      `QuestGroups: ${questGroups.join(',')}`,
    ]
    return dispatch(setPythonConfigSuccess(pythonConfig))
  }
)
