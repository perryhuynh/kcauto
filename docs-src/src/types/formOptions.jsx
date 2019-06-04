import React from 'react'
import Localize from 'containers/LocalizeContainer'

// general section
export const PAUSE_OPTIONS = [
  { value: true, label: <Localize field='bodyConfig.generalPauseTrue' /> },
  { value: false, label: <Localize field='bodyConfig.generalPauseFalse' /> },
]

// scheduled stop section
export const STOP_MODE_OPTIONS = [
  { value: 'module', label: <Localize field='bodyConfig.scheduledStopStopModeModule' /> },
  { value: 'script', label: <Localize field='bodyConfig.scheduledStopStopModeScript' /> },
]

// expedition section
export const EXPEDITIONS = Array.from({ length: 8 }, (value, key) => (
  { value: String(key + 1), label: String(key + 1) }))
EXPEDITIONS.push({ value: 'A1', label: 'A1' })
EXPEDITIONS.push({ value: 'A2', label: 'A2' })
EXPEDITIONS.push({ value: 'A3', label: 'A3' })
EXPEDITIONS.push(...Array.from({ length: 8 }, (value, key) => ({ value: String(key + 9), label: String(key + 9) })))
EXPEDITIONS.push({ value: 'B1', label: 'B1' })
EXPEDITIONS.push({ value: 'B2', label: 'B2' })
EXPEDITIONS.push(...Array.from({ length: 16 }, (value, key) => ({ value: String(key + 17), label: String(key + 17) })))
EXPEDITIONS.push({ value: '33', label: '33 - Node Support' })
EXPEDITIONS.push({ value: '34', label: '34 - Boss Support' })
EXPEDITIONS.push(...Array.from({ length: 6 }, (value, key) => ({ value: String(key + 35), label: String(key + 35) })))
EXPEDITIONS.push({ value: '9998', label: 'Event Node Support' })
EXPEDITIONS.push({ value: '9999', label: 'Event Boss Support' })

// pvp/combat sections
export const FLEET_PRESETS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'].map(value => (
  { value, label: value }))
export const COMBAT_ENGINES = [
  { value: 'live', label: <Localize field='bodyConfig.combatEngineLive' /> },
  { value: 'legacy', label: <Localize field='bodyConfig.combatEngineLegacy' /> }]
export const MAPS = ['1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '2-1', '2-2', '2-3', '2-4', '2-5', '3-1', '3-2', '3-3',
  '3-4', '3-5', '4-1', '4-2', '4-3', '4-4', '4-5', '5-1', '5-2', '5-3', '5-4', '5-5', '6-1', '6-2', '6-3', '6-4', '6-5',
  '7-1', '7-2', 'E-1', 'E-2', 'E-3', 'E-4', 'E-5', 'E-6', 'E-7', 'E-8'].map(value => ({ value, label: value }))
export const COMBINED_FLEET_MODES = [
  { value: '', label: <Localize field='bodyConfig.combatFleetModeStandard' /> },
  { value: 'ctf', label: <Localize field='bodyConfig.combatFleetModeCTF' /> },
  { value: 'stf', label: <Localize field='bodyConfig.combatFleetModeSTF' /> },
  { value: 'transport', label: <Localize field='bodyConfig.combatFleetModeTransport' /> },
  { value: 'striking', label: <Localize field='bodyConfig.combatFleetModeStriking' /> }]
export const COMBAT_NODE_COUNTS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'].map(value => (
  { value, label: value }))
export const NODES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(value => ({ value, label: value }))
NODES.push(...['O1', 'O2', 'O3', 'P1', 'P2', 'P3', 'Q1', 'Q2', 'Q3', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8',
  'Z9', 'ZZ', 'ZZ1', 'ZZ2', 'ZZ3'].map(value => ({ value, label: value })))
export const FORMATIONS = [
  { value: 'line_ahead', label: <Localize field='bodyConfig.combatFormationLineAhead' /> },
  { value: 'double_line', label: <Localize field='bodyConfig.combatFormationDoubleLine' /> },
  { value: 'diamond', label: <Localize field='bodyConfig.combatFormationDiamond' /> },
  { value: 'echelon', label: <Localize field='bodyConfig.combatFormationEchelon' /> },
  { value: 'line_abreast', label: <Localize field='bodyConfig.combatFormationLineAbreast' /> },
  { value: 'vanguard', label: <Localize field='bodyConfig.combatFormationVanguard' /> },
  { value: 'combinedfleet_1', label: <Localize field='bodyConfig.combatFormationCombinedFleet1' /> },
  { value: 'combinedfleet_2', label: <Localize field='bodyConfig.combatFormationCombinedFleet2' /> },
  { value: 'combinedfleet_3', label: <Localize field='bodyConfig.combatFormationCombinedFleet3' /> },
  { value: 'combinedfleet_4', label: <Localize field='bodyConfig.combatFormationCombinedFleet4' /> }]
export const NIGHT_BATTLES = [
  { value: 'True', label: <Localize field='bodyConfig.combatNightBattleTrue' /> },
  { value: 'False', label: <Localize field='bodyConfig.combatNightBattleFalse' /> }]
export const DAMAGE_STATES = [
  { value: 'heavy', label: <Localize field='bodyConfig.combatDamageStateHeavy' /> },
  { value: 'moderate', label: <Localize field='bodyConfig.combatDamageStateModerate' /> },
  { value: 'minor', label: <Localize field='bodyConfig.combatDamageStateMinor' /> }]
export const LBAS_GROUPS = ['1', '2', '3'].map(value => ({ value, label: value }))

// event reset section
export const FREQUENCIES = ['1', '2', '3', '4', '5'].map(value => ({ value, label: value }))
export const DIFFICULTIES = [
  { value: 'casual', label: <Localize field='bodyConfig.eventResetDifficultyCasual' /> },
  { value: 'easy', label: <Localize field='bodyConfig.eventResetDifficultyEasy' /> },
  { value: 'medium', label: <Localize field='bodyConfig.eventResetDifficultyMedium' /> },
  { value: 'hard', label: <Localize field='bodyConfig.eventResetDifficultyHard' /> }]

// ship switcher section
export const SWITCH_CRITERIA = [
  { value: 'damage', label: <Localize field='bodyConfig.shipSwitcherCriteriaDamage' /> },
  { value: 'fatigue', label: <Localize field='bodyConfig.shipSwitcherCriteriaFatigue' /> },
  { value: 'sparkle', label: <Localize field='bodyConfig.shipSwitcherCriteriaSparkle' /> }]
export const BASE_SPECIFICATION = [
  { value: 'P', label: <Localize field='bodyConfig.shipSwitcherModalSpecificationPosition' /> },
  { value: 'A', label: <Localize field='bodyConfig.shipSwitcherModalSpecificationAsset' /> }]
export const SORT_BY = [
  { value: 'N', label: <Localize field='bodyConfig.shipSwitcherModalSortByDateAcquired' /> },
  { value: 'C', label: <Localize field='bodyConfig.shipSwitcherModalSortByClass' /> },
  { value: 'L', label: <Localize field='bodyConfig.shipSwitcherModalSortByLevel' /> }]
export const OFFSET_START = [
  { value: 'S', label: <Localize field='bodyConfig.shipSwitcherModalOffsetStartStart' /> },
  { value: 'E', label: <Localize field='bodyConfig.shipSwitcherModalOffsetStartEnd' /> }]
export const ASSETS = ['SS_U-511', 'AO', 'AR', 'AS', 'AV', 'BB', 'BBV', 'CA', 'CAV', 'CL', 'CLT', 'CT', 'CV', 'CVB',
  'CVL', 'DD', 'DE', 'LHA', 'SS', 'SSV'].map(value => ({ value, label: value }))
export const LEVEL_EQUALITY = ['<', '>'].map(value => ({ value, label: value }))
export const LOCKED = [
  { value: '_', label: <Localize field='bodyConfig.shipSwitcherModalLockedIgnore' /> },
  { value: 'L', label: <Localize field='bodyConfig.shipSwitcherModalLockedYes' /> },
  { value: 'N', label: <Localize field='bodyConfig.shipSwitcherModalLockedNo' /> }]
export const RINGED = [
  { value: '_', label: <Localize field='bodyConfig.shipSwitcherModalRingedIgnore' /> },
  { value: 'R', label: <Localize field='bodyConfig.shipSwitcherModalRingedYes' /> },
  { value: 'N', label: <Localize field='bodyConfig.shipSwitcherModalRingedNo' /> }]
