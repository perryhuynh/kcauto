import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Select, { Creatable } from 'react-select'
import { withStyles } from 'material-ui/styles'
import saveAs from 'save-as'

import TimeInput from 'material-ui-time-picker'
import Dropzone from 'react-dropzone'

import Grid from 'material-ui/Grid'
import Paper from 'material-ui/Paper'
import { InputLabel } from 'material-ui/Input'
import { FormControl, FormControlLabel } from 'material-ui/Form'
import Typography from 'material-ui/Typography'
import TextField from 'material-ui/TextField'
import Divider from 'material-ui/Divider'
import Button from 'material-ui/Button'
import Checkbox from 'material-ui/Checkbox'
import Switch from 'material-ui/Switch'
import { ChevronRight, Upload, ContentSave } from 'mdi-material-ui'

import Localize from 'containers/LocalizeContainer'

const EXPEDITIONS = Array.from({ length: 40 }, (value, key) => ({ value: String(key + 1), label: String(key + 1) }))
EXPEDITIONS.push({ value: '9998', label: 'Node Support' })
EXPEDITIONS.push({ value: '9999', label: 'Boss Support' })
const COMBAT_ENGINES = [
  { value: 'legacy', label: <Localize field='bodyConfig.combatEngineLegacy' /> },
  { value: 'live', label: <Localize field='bodyConfig.combatEngineLive' /> }]
const MAPS = ['1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '2-1', '2-2', '2-3', '2-4', '2-5', '3-1', '3-2', '3-3', '3-4',
  '3-5', '4-1', '4-2', '4-3', '4-4', '4-5', '5-1', '5-2', '5-3', '5-4', '5-5', '6-1', '6-2', '6-3', '6-4', '6-5',
  'E-1', 'E-2', 'E-3', 'E-4', 'E-5', 'E-6', 'E-7', 'E-8']
  .map(value => ({ value, label: value }))
const COMBINED_FLEET_MODES = [
  { value: '', label: <Localize field='bodyConfig.combatFleetModeStandard' /> },
  { value: 'ctf', label: <Localize field='bodyConfig.combatFleetModeCTF' /> },
  { value: 'stf', label: <Localize field='bodyConfig.combatFleetModeSTF' /> },
  { value: 'transport', label: <Localize field='bodyConfig.combatFleetModeTransport' /> },
  { value: 'striking', label: <Localize field='bodyConfig.combatFleetModeStriking' /> }]
const COMBAT_NODE_COUNTS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'].map(value => (
  { value, label: value }))
const NODES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(value => ({ value, label: value }))
NODES.push(...['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'ZZ1', 'ZZ2', 'ZZ3'].map(value => (
  { value, label: value })))
const FORMATIONS = [
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
const NIGHT_BATTLES = [
  { value: 'True', label: <Localize field='bodyConfig.combatNightBattleTrue' /> },
  { value: 'False', label: <Localize field='bodyConfig.combatNightBattleFalse' /> }]
const DAMAGE_STATES = [
  { value: 'heavy', label: <Localize field='bodyConfig.combatDamageStateHeavy' /> },
  { value: 'moderate', label: <Localize field='bodyConfig.combatDamageStateModerate' /> },
  { value: 'minor', label: <Localize field='bodyConfig.combatDamageStateMinor' /> }]
const LBAS_GROUPS = ['1', '2', '3'].map(value => ({ value, label: value }))

const styles = () => ({
  dropzoneOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    display: 'flex',
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    fontFamily: 'Roboto, sans-serif',
    fontSize: 24,
    fontWeight: 'bold',
    background: 'rgba(255,255,255,0.8)',
    zIndex: 9,
  },
  paper: {
    marginTop: 10,
    padding: 20,
  },
  pre: {
    padding: 20,
    fontFamily: '"Source Code Pro", monospace',
    fontSize: 12,
    overflowX: 'auto',
  },
  formGrid: {
    padding: 8,
    paddingTop: 0,
    paddingBottom: 0,
  },
  formGridButton: {
    padding: 0,
    paddingTop: 14,
    textAlign: 'center',
  },
  formControl: {
    marginTop: 0,
  },
  switch: {
    zIndex: 0,
  },
  reactSelectLabel: {
    transform: 'translate(0, -15px) scale(0.75)',
    minWidth: '150%',
  },
  reactSelect: {
    fontFamily: 'Roboto, sans-serif',
  },
  reactSelectHalfWidth: {
    width: '50%',
    fontFamily: 'Roboto, sans-serif',
  },
  flexReset: {
    display: 'flex',
  },
  saveButton: {
    marginLeft: 10,
  },
})

const createStateObjFromPythonConfig = (pyConfig) => {
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
    } else if (line === '[Expeditions]') {
      currentSection = 'expeditions'
    } else if (line === '[PvP]') {
      currentSection = 'pvp'
    } else if (line === '[Combat]') {
      currentSection = 'combat'
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
    scheduledSleepEnabled: pyConfigObj.scheduledSleepEnabled === 'True',
    scheduledSleepStartTime: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.scheduledSleepStartTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledSleepStartTime.substr(2, 2), 10), 0, 0
      )),
    scheduledSleepSleepLength: pyConfigObj.scheduledSleepSleepLength || null,
    expeditionsEnabled: pyConfigObj.expeditionsEnabled === 'True',
    expeditionsFleet2Enabled: true,
    expeditionsFleet3Enabled: true,
    expeditionsFleet4Enabled: true,
    expeditionsFleet2: pyConfigObj.expeditionsFleet2 || null,
    expeditionsFleet3: pyConfigObj.expeditionsFleet3 || null,
    expeditionsFleet4: pyConfigObj.expeditionsFleet4 || null,
    pvpEnabled: pyConfigObj.pvpEnabled === 'True',
    combatEnabled: pyConfigObj.combatEnabled === 'True',
    combatEngine: pyConfigObj.combatEngine || 'legacy',
    combatMap: pyConfigObj.combatMap || '1-1',
    combatFleetMode: pyConfigObj.combatFleetMode || '',
    combatCombatNodes: pyConfigObj.combatCombatNodes || null,
    combatNodeSelect1: null,
    combatNodeSelect2: null,
    combatNodeSelects: pyConfigObj.combatNodeSelects || null,
    combatFormationsNode: null,
    combatFormationsFormation: null,
    combatFormations: pyConfigObj.combatFormations || null,
    combatNightBattlesNode: null,
    combatNightBattlesMode: null,
    combatNightBattles: pyConfigObj.combatNightBattles || null,
    combatRetreatLimit: pyConfigObj.combatRetreatLimit || 'heavy',
    combatRepairLimit: pyConfigObj.combatRepairLimit || 'moderate',
    combatRepairTimeLimit: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.combatRepairTimeLimit.substr(0, 2), 10),
        parseInt(pyConfigObj.combatRepairTimeLimit.substr(2, 2), 10), 0, 0
      )),
    combatLBASGroups: pyConfigObj.combatLBASGroups || null,
    combatLBASGroup1Node1: pyConfigObj.combatLBASGroup1Nodes[0] || null,
    combatLBASGroup1Node2: pyConfigObj.combatLBASGroup1Nodes[1] || null,
    combatLBASGroup2Node1: pyConfigObj.combatLBASGroup2Nodes[0] || null,
    combatLBASGroup2Node2: pyConfigObj.combatLBASGroup2Nodes[1] || null,
    combatLBASGroup3Node1: pyConfigObj.combatLBASGroup3Nodes[0] || null,
    combatLBASGroup3Node2: pyConfigObj.combatLBASGroup3Nodes[1] || null,
    combatOptionCheckFatigue: pyConfigObj.combatMiscOptions.includes('CheckFatigue') || false,
    combatOptionReserveDocks: pyConfigObj.combatMiscOptions.includes('ReserveDocks') || false,
    combatOptionPortCheck: pyConfigObj.combatMiscOptions.includes('PortCheck') || false,
    combatOptionMedalStop: pyConfigObj.combatMiscOptions.includes('MedalStop') || false,
    questsEnabled: pyConfigObj.questsEnabled === 'True',
  }

  return jsonConfig
}

class BodyConfig extends Component {
  // grab default states from the store; defaults are in reducers/config/config.jsx
  state = this.props.config.jsonConfig

  componentDidMount = () => {
    // this.props.setJsonConfig(this.state)
    this.props.setPythonConfig(this.state)
  }

  componentDidUpdate = (nextProp, nextState) => {
    if (this.state !== nextState && this.state.dropzoneActive === nextState.dropzoneActive) {
      // try not to fire the setConfig'ers if it's just the dropzone state changing
      this.props.setJsonConfig(this.state)
      this.props.setPythonConfig(this.state)
    }
  }

  onConfigLoadEnter = () => {
    this.setState({ dropzoneActive: true })
  }

  onConfigLoadLeave = () => {
    this.setState({ dropzoneActive: false })
  }

  onConfigLoad = (acceptedFiles, rejectedFiles) => {
    // only accept the first file
    if (acceptedFiles.length === 1) {
      const rawConfigFileHandle = acceptedFiles[0]
      const reader = new FileReader()
      reader.onload = () => {
        const newState = createStateObjFromPythonConfig(reader.result)
        this.setState(newState)
      }
      reader.readAsText(rawConfigFileHandle)
    }
    this.setState({ dropzoneActive: false })
  }

  onSaveClick = () => {
    const configOutput = this.props.config.pythonConfig.reduce((config, line) => {
      let configTemp = config
      configTemp += `${line}\n`
      return configTemp
    }, '# config automatically generated from kcauto-kai frontend\n\n')
    const configBlob = new Blob([configOutput], { type: 'text/plain;charset=utf-8' })
    saveAs(configBlob, 'config.ini', true)
  }

  handleCombatToggle = (event, checked) => {
    // when the combat option is toggled back on, make sure to clear any expeditions based on the combat fleet mode
    if (checked) {
      if (this.state.combatFleetMode === 'striking') {
        this.setState({ expeditionsFleet3: [] })
      } else if (['ctf', 'stf', 'transport'].indexOf(this.state.combatFleetMode) > -1) {
        this.setState({ expeditionsFleet2: [] })
      }
    }
    this.setState({ combatEnabled: checked })
  }

  handleFleetModeChange = (value) => {
    // when changing the fleet mode, make sure to disable and clear any conflicting expeditions as needed
    if (value === 'striking') {
      this.setState({ expeditionsFleet2Enabled: true, expeditionsFleet3Enabled: false, expeditionsFleet3: [] })
    } else if (['ctf', 'stf', 'transport'].indexOf(value) > -1) {
      this.setState({ expeditionsFleet2Enabled: false, expeditionsFleet2: [], expeditionsFleet3Enabled: true })
    } else {
      this.setState({ expeditionsFleet2Enabled: true, expeditionsFleet3Enabled: true })
    }
    this.setState({ combatFleetMode: value })
  }

  handleCombatNodeSelectAdd = (node, targetNode) => {
    // automatically add a node select option based on the two previous helper fields; also checks against previously
    // entered values so that existing node selects for a node are overwritten
    const tempCombatNodeSelects = this.state.combatNodeSelects ? this.state.combatNodeSelects : ''
    const tempCombatNodeSelectsObj = this.optionsNodeSplitter(tempCombatNodeSelects, '>')
    tempCombatNodeSelectsObj[node] = targetNode
    const combatNodeSelects = Object.keys(tempCombatNodeSelectsObj).sort().map(key =>
      `${key}>${tempCombatNodeSelectsObj[key]}`).join(',')
    this.setState({ combatNodeSelect1: null, combatNodeSelect2: null, combatNodeSelects })
  }

  handleCombatFormationAdd = (node, formation) => {
    // automatically add a custom formation selection based on the two previous helper fields; also checks against
    // previously entered values so that existing formations for a node are overwritten
    const tempCombatFormations = this.state.combatFormations ? this.state.combatFormations : ''
    const tempCombatFormationsObj = this.optionsNodeSplitter(tempCombatFormations, ':')

    // if no node is specified, find next node number to apply formation to
    const targetNode = node || this.findMaxNumericNode(tempCombatFormationsObj) + 1
    tempCombatFormationsObj[targetNode] = formation
    const combatFormations = Object.keys(tempCombatFormationsObj).sort().map(key =>
      `${key}:${tempCombatFormationsObj[key]}`).join(',')
    this.setState({ combatFormationsNode: null, combatFormationsFormation: null, combatFormations })
  }

  handleCombatNightBattleAdd = (node, nightBattle) => {
    // automatically add a custom night battle selection based on the two previous helper fields; also checks against
    // previously entered values so that existing night battle selections for a node are overwritten
    const tempCombatNightBattles = this.state.combatNightBattles ? this.state.combatNightBattles : ''
    const tempCombatNightBattlesObj = this.optionsNodeSplitter(tempCombatNightBattles, ':')
    // if no node is specified, find next node number to apply night battle mode to
    const targetNode = node || this.findMaxNumericNode(tempCombatNightBattlesObj) + 1
    tempCombatNightBattlesObj[targetNode] = nightBattle
    const combatNightBattles = Object.keys(tempCombatNightBattlesObj).sort().map(key =>
      `${key}:${tempCombatNightBattlesObj[key]}`).join(',')
    this.setState({ combatNightBattlesNode: null, combatNightBattlesMode: null, combatNightBattles })
  }

  handleLBASGroupSelect = (value) => {
    // clear the LBAS node selects as needed based on the LBAS group selections
    if (!value.includes('1')) {
      this.setState({ combatLBASGroup1Node1: null, combatLBASGroup1Node2: null })
    }
    if (!value.includes('2')) {
      this.setState({ combatLBASGroup2Node1: null, combatLBASGroup2Node2: null })
    }
    if (!value.includes('3')) {
      this.setState({ combatLBASGroup3Node1: null, combatLBASGroup3Node2: null })
    }
    this.setState({ combatLBASGroups: value })
  }

  optionsNodeSplitter = (rawOption, divider) => {
    // helper method to convert a list of comma-separated values divided in two via a divider into an object with the
    // value left of the divider as the key, and the value right of the divider as the value
    const optionsObj = rawOption.split(',').reduce((obj, option) => {
      const tempObj = obj
      const optionInfo = option.split(divider)
      if (optionInfo.length === 2) {
        const node = optionInfo[0]
        const optionChoice = optionInfo[1]
        tempObj[node] = optionChoice
      }
      return tempObj
    }, {})
    return optionsObj
  }

  findMaxNumericNode = (object) => {
    // finds and returns the max numeric node specified in a node options object
    const nodes = Object.keys(object)
    if (nodes.length === 0) {
      return 0
    }
    return Math.max(...nodes.filter(node => parseFloat(node)).map(node => parseFloat(node)))
  }

  render = () => {
    const {
      classes,
      config,
    } = this.props
    const {
      dropzoneActive,
      generalProgram,
      generalJSTOffset,
      scheduledSleepEnabled,
      scheduledSleepStartTime,
      scheduledSleepSleepLength,
      expeditionsEnabled,
      expeditionsFleet2Enabled,
      expeditionsFleet3Enabled,
      expeditionsFleet4Enabled,
      expeditionsFleet2,
      expeditionsFleet3,
      expeditionsFleet4,
      pvpEnabled,
      combatEnabled,
      combatEngine,
      combatMap,
      combatFleetMode,
      combatCombatNodes,
      combatNodeSelect1,
      combatNodeSelect2,
      combatNodeSelects,
      combatFormationsNode,
      combatFormationsFormation,
      combatFormations,
      combatNightBattlesNode,
      combatNightBattlesMode,
      combatNightBattles,
      combatRetreatLimit,
      combatRepairLimit,
      combatRepairTimeLimit,
      combatLBASGroups,
      combatLBASGroup1Node1,
      combatLBASGroup1Node2,
      combatLBASGroup2Node1,
      combatLBASGroup2Node2,
      combatLBASGroup3Node1,
      combatLBASGroup3Node2,
      combatOptionCheckFatigue,
      combatOptionReserveDocks,
      combatOptionPortCheck,
      combatOptionMedalStop,
      questsEnabled,
    } = this.state

    const combatNodeSelectOptions = combatNodeSelects ?
      combatNodeSelects.split(',').map(value => ({ value, label: value })) :
      []
    const combatFormationOptions = combatFormations ?
      combatFormations.split(',').map(value => ({ value, label: value })) :
      []
    const combatNightBattleOptions = combatNightBattles ?
      combatNightBattles.split(',').map(value => ({ value, label: value })) :
      []
    const combatLBASGroupsArray = combatLBASGroups ? combatLBASGroups.split(',') : []
    const combatLBASGroup1NodesDisabled = !combatEnabled || combatLBASGroupsArray.indexOf('1') < 0
    const combatLBASGroup2NodesDisabled = !combatEnabled || combatLBASGroupsArray.indexOf('2') < 0
    const combatLBASGroup3NodesDisabled = !combatEnabled || combatLBASGroupsArray.indexOf('3') < 0
    let configLoad

    return (
      <Dropzone
        ref={(node) => { configLoad = node }}
        style={{ position: 'relative' }}
        accept='.ini'
        onDrop={this.onConfigLoad}
        onDragEnter={this.onConfigLoadEnter}
        onDragLeave={this.onConfigLoadLeave}
        disableClick
      >
        { dropzoneActive ? <div className={classes.dropzoneOverlay}>drop your config file here</div> : null }
        <Grid container spacing={0}>
          <Grid item xs={12} md={8}>
            <Paper className={classes.paper} elevation={0}>
              <Typography type='display1'><Localize field='bodyConfig.generalHeader' /></Typography>

              <Grid container spacing={0}>
                <Grid item xs={12} sm={8} className={classes.formGrid}>
                  <TextField
                    id='generalProgram'
                    label={<Localize field='bodyConfig.generalProgram' />}
                    value={generalProgram}
                    onChange={event => this.setState({ generalProgram: event.target.value })}
                    helperText={<Localize field='bodyConfig.generalProgramDesc' />}
                    className={classes.formControl}
                    fullWidth
                    margin='normal' />
                </Grid>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <TextField
                    id='generalJSTOffset'
                    label={<Localize field='bodyConfig.generalJSTOffset' />}
                    value={generalJSTOffset}
                    onChange={event => this.setState({ generalJSTOffset: event.target.value })}
                    helperText={<Localize field='bodyConfig.generalJSTOffsetDesc' />}
                    className={classes.formControl}
                    fullWidth
                    type='number'
                    margin='normal' />
                </Grid>
              </Grid>

              <Divider />

              <Typography type='display1'>
                <Localize field='bodyConfig.scheduledSleepHeader' />
                <Switch
                  className={classes.switch}
                  checked={scheduledSleepEnabled}
                  onChange={(event, checked) => this.setState({ scheduledSleepEnabled: checked })} />
              </Typography>

              <Grid container spacing={0}>
                <Grid item xs={12} sm={6} className={classes.formGrid}>
                  <FormControl disabled={!scheduledSleepEnabled} className={classes.formControl} fullWidth>
                    <InputLabel htmlFor='scheduledSleepStartTime'>
                      <Localize field='bodyConfig.scheduledSleepStartTime' />
                    </InputLabel>
                    <TimeInput
                      id='scheduledSleepStartTime'
                      mode='24h'
                      value={scheduledSleepStartTime}
                      onChange={time => this.setState({ scheduledSleepStartTime: time })}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={6} className={classes.formGrid}>
                  <TextField
                    id='scheduledSleepSleepLength'
                    label={<Localize field='bodyConfig.scheduledSleepLength' />}
                    value={scheduledSleepSleepLength}
                    onChange={event => this.setState({ scheduledSleepSleepLength: event.target.value })}
                    helperText={<Localize field='bodyConfig.scheduledSleepLengthDesc' />}
                    type='number'
                    margin='normal'
                    className={classes.formControl}
                    disabled={!scheduledSleepEnabled}
                    fullWidth />
                </Grid>
              </Grid>

              <Divider />

              <Typography type='display1'>
                <Localize field='bodyConfig.expeditionsHeader' />
                <Switch
                  className={classes.switch}
                  checked={expeditionsEnabled}
                  onChange={(event, checked) => this.setState({ expeditionsEnabled: checked })} />
              </Typography>

              <Grid container spacing={0}>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl
                    disabled={!expeditionsEnabled || (combatEnabled && !expeditionsFleet2Enabled)}
                    margin='normal'
                    fullWidth
                  >
                    <InputLabel htmlFor='expeditionsFleet2' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.expeditionsFleet2' />
                    </InputLabel>
                    <Select
                      multi
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='expeditionsFleet2'
                      value={expeditionsFleet2}
                      options={EXPEDITIONS}
                      onChange={value => this.setState({ expeditionsFleet2: value })}
                      disabled={!expeditionsEnabled || (combatEnabled && !expeditionsFleet2Enabled)}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl
                    disabled={!expeditionsEnabled || (combatEnabled && !expeditionsFleet3Enabled)}
                    margin='normal'
                    fullWidth
                  >
                    <InputLabel htmlFor='expeditionsFleet3' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.expeditionsFleet3' />
                    </InputLabel>
                    <Select
                      multi
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='expeditionsFleet3'
                      value={expeditionsFleet3}
                      options={EXPEDITIONS}
                      onChange={value => this.setState({ expeditionsFleet3: value })}
                      disabled={!expeditionsEnabled || (combatEnabled && !expeditionsFleet3Enabled)}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl
                    disabled={!expeditionsEnabled || (combatEnabled && !expeditionsFleet4Enabled)}
                    margin='normal'
                    fullWidth
                  >
                    <InputLabel htmlFor='expeditionsFleet4' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.expeditionsFleet4' />
                    </InputLabel>
                    <Select
                      multi
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='expeditionsFleet4'
                      value={expeditionsFleet4}
                      options={EXPEDITIONS}
                      onChange={value => this.setState({ expeditionsFleet4: value })}
                      disabled={!expeditionsEnabled || (combatEnabled && !expeditionsFleet4Enabled)}
                      fullWidth />
                  </FormControl>
                </Grid>
              </Grid>

              <Divider />

              <Typography type='display1'>
                <Localize field='bodyConfig.pvpHeader' />
                <Switch
                  className={classes.switch}
                  checked={pvpEnabled}
                  onChange={(event, checked) => this.setState({ pvpEnabled: checked })} />
              </Typography>

              <Divider />

              <Typography type='display1'>
                <Localize field='bodyConfig.combatHeader' />
                <Switch
                  className={classes.switch}
                  checked={combatEnabled}
                  onChange={this.handleCombatToggle} />
              </Typography>

              <Grid container spacing={0}>
                <Grid item xs={12} sm={12} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatEngine' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatEngine' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatEngine'
                      value={combatEngine}
                      options={COMBAT_ENGINES}
                      onChange={value => this.setState({ combatEngine: value })}
                      disabled={!combatEnabled}
                      clearable={false}
                      fullWidth />
                  </FormControl>
                </Grid>
              </Grid>

              <Grid container spacing={0}>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatMap' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatMap' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatMap'
                      value={combatMap}
                      options={MAPS}
                      onChange={value => this.setState({ combatMap: value })}
                      disabled={!combatEnabled}
                      clearable={false}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatFleetMode' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatFleetMode' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatFleetMode'
                      value={combatFleetMode}
                      options={COMBINED_FLEET_MODES}
                      onChange={this.handleFleetModeChange}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatCombatNodes' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatCombatNodeCount' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatCombatNodes'
                      value={combatCombatNodes}
                      options={COMBAT_NODE_COUNTS}
                      onChange={value => this.setState({ combatCombatNodes: value })}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>

                <Grid item xs={4} sm={2} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatNodeSelect1' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatNodeSelect1' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatNodeSelect1'
                      value={combatNodeSelect1}
                      options={NODES}
                      onChange={value => this.setState({ combatNodeSelect1: value })}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={4} sm={2} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatNodeSelect2' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatNodeSelect2' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatNodeSelect2'
                      value={combatNodeSelect2}
                      options={NODES}
                      onChange={value => this.setState({ combatNodeSelect2: value })}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={4} sm={1} className={classes.formGridButton}>
                  <Button
                    dense
                    color='primary'
                    disabled={!combatEnabled ||
                      (!combatNodeSelect1 || !combatNodeSelect2 || combatNodeSelect1 === combatNodeSelect2)}
                    onClick={() => this.handleCombatNodeSelectAdd(combatNodeSelect1, combatNodeSelect2)}
                  >
                    <Localize field='bodyConfig.combatNodeSelectAdd' />
                    <ChevronRight />
                  </Button>
                </Grid>
                <Grid item xs={12} sm={7} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatNodeSelects' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatNodeSelects' />
                    </InputLabel>
                    <Creatable
                      multi
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatNodeSelects'
                      value={combatNodeSelects}
                      options={combatNodeSelectOptions}
                      onChange={value => this.setState({ combatNodeSelects: value })}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>

                <Grid item xs={4} sm={2} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatFormationsNode' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatCustomFormation1' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatFormationsNode'
                      value={combatFormationsNode}
                      options={combatEngine === 'legacy' ? COMBAT_NODE_COUNTS : COMBAT_NODE_COUNTS.concat(NODES)}
                      onChange={value => this.setState({ combatFormationsNode: value })}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={4} sm={3} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatFormationsFormation' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatCustomFormation2' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatFormationsFormation'
                      value={combatFormationsFormation}
                      options={FORMATIONS}
                      onChange={value => this.setState({ combatFormationsFormation: value })}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={4} sm={1} className={classes.formGridButton}>
                  <Button
                    dense
                    color='primary'
                    disabled={!combatEnabled || !combatFormationsFormation}
                    onClick={() => this.handleCombatFormationAdd(combatFormationsNode, combatFormationsFormation)}
                  >
                    <Localize field='bodyConfig.combatCustomFormationAdd' />
                    <ChevronRight />
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatFormations' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatCustomFormations' />
                    </InputLabel>
                    <Creatable
                      multi
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatFormations'
                      value={combatFormations}
                      options={combatFormationOptions}
                      onChange={value => this.setState({ combatFormations: value })}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>

                <Grid item xs={4} sm={2} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatNightBattlesNode' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatNightBattle1' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatNightBattlesNode'
                      value={combatNightBattlesNode}
                      options={combatEngine === 'legacy' ? COMBAT_NODE_COUNTS : COMBAT_NODE_COUNTS.concat(NODES)}
                      onChange={value => this.setState({ combatNightBattlesNode: value })}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={4} sm={3} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatNightBattlesMode' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatNightBattle2' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatNightBattlesMode'
                      value={combatNightBattlesMode}
                      options={NIGHT_BATTLES}
                      onChange={value => this.setState({ combatNightBattlesMode: value })}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={4} sm={1} className={classes.formGridButton}>
                  <Button
                    dense
                    color='primary'
                    disabled={!combatEnabled || !combatNightBattlesMode}
                    onClick={() => this.handleCombatNightBattleAdd(combatNightBattlesNode, combatNightBattlesMode)}
                  >
                    <Localize field='bodyConfig.combatNightBattleAdd' />
                    <ChevronRight />
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatNightBattles' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatNightBattles' />
                    </InputLabel>
                    <Creatable
                      multi
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatNightBattles'
                      value={combatNightBattles}
                      options={combatNightBattleOptions}
                      onChange={value => this.setState({ combatNightBattles: value })}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>

                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatRetreatLimit' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatRetreatLimit' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatRetreatLimit'
                      value={combatRetreatLimit}
                      options={DAMAGE_STATES}
                      onChange={value => this.setState({ combatRetreatLimit: value })}
                      disabled={!combatEnabled}
                      clearable={false}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatRepairLimit' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatRepairLimit' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatRepairLimit'
                      value={combatRepairLimit}
                      options={DAMAGE_STATES}
                      onChange={value => this.setState({ combatRepairLimit: value })}
                      disabled={!combatEnabled}
                      clearable={false}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} fullWidth>
                    <InputLabel htmlFor='combatRepairTimeLimit'>
                      <Localize field='bodyConfig.combatRepairTimeLimit' />
                    </InputLabel>
                    <TimeInput
                      id='combatRepairTimeLimit'
                      mode='24h'
                      value={combatRepairTimeLimit}
                      onChange={time => this.setState({ combatRepairTimeLimit: time })}
                      fullWidth />
                  </FormControl>
                </Grid>

                <Grid item xs={12} sm={3} className={classes.formGrid}>
                  <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatLBASGroups' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatLBASGroups' />
                    </InputLabel>
                    <Select
                      multi
                      className={classes.reactSelect}
                      simpleValue={true}
                      name='combatLBASGroups'
                      value={combatLBASGroups}
                      options={LBAS_GROUPS}
                      onChange={this.handleLBASGroupSelect}
                      disabled={!combatEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={3} className={classes.formGrid}>
                  <FormControl disabled={combatLBASGroup1NodesDisabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatLBASGroup1Nodes' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatLBASGroup1' />
                    </InputLabel>
                    <div className={classes.flexReset}>
                      <Select
                        className={classes.reactSelectHalfWidth}
                        simpleValue={true}
                        name='combatLBASGroup1Node1'
                        value={combatLBASGroup1Node1}
                        options={NODES}
                        onChange={value => this.setState({ combatLBASGroup1Node1: value })}
                        disabled={combatLBASGroup1NodesDisabled} />
                      <Select
                        className={classes.reactSelectHalfWidth}
                        simpleValue={true}
                        name='combatLBASGroup1Node2'
                        value={combatLBASGroup1Node2}
                        options={NODES}
                        onChange={value => this.setState({ combatLBASGroup1Node2: value })}
                        disabled={combatLBASGroup1NodesDisabled} />
                    </div>
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={3} className={classes.formGrid}>
                  <FormControl disabled={combatLBASGroup2NodesDisabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatLBASGroup2Nodes' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatLBASGroup2' />
                    </InputLabel>
                    <div className={classes.flexReset}>
                      <Select
                        className={classes.reactSelectHalfWidth}
                        simpleValue={true}
                        name='combatLBASGroup2Node1'
                        value={combatLBASGroup2Node1}
                        options={NODES}
                        onChange={value => this.setState({ combatLBASGroup2Node1: value })}
                        disabled={combatLBASGroup2NodesDisabled} />
                      <Select
                        className={classes.reactSelectHalfWidth}
                        simpleValue={true}
                        name='combatLBASGroup2Node2'
                        value={combatLBASGroup2Node2}
                        options={NODES}
                        onChange={value => this.setState({ combatLBASGroup2Node2: value })}
                        disabled={combatLBASGroup2NodesDisabled} />
                    </div>
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={3} className={classes.formGrid}>
                  <FormControl disabled={combatLBASGroup3NodesDisabled} margin='normal' fullWidth>
                    <InputLabel htmlFor='combatLBASGroup3Nodes' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.combatLBASGroup3' />
                    </InputLabel>
                    <div className={classes.flexReset}>
                      <Select
                        className={classes.reactSelectHalfWidth}
                        simpleValue={true}
                        name='combatLBASGroup3Node1'
                        value={combatLBASGroup3Node1}
                        options={NODES}
                        onChange={value => this.setState({ combatLBASGroup3Node1: value })}
                        disabled={combatLBASGroup3NodesDisabled} />
                      <Select
                        className={classes.reactSelectHalfWidth}
                        simpleValue={true}
                        name='combatLBASGroup3Node2'
                        value={combatLBASGroup3Node2}
                        options={NODES}
                        onChange={value => this.setState({ combatLBASGroup3Node2: value })}
                        disabled={combatLBASGroup3NodesDisabled} />
                    </div>
                  </FormControl>
                </Grid>

                <Grid item xs={12} sm={12} className={classes.formGrid}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={combatOptionCheckFatigue}
                        onChange={(event, checked) => this.setState({ combatOptionCheckFatigue: checked })}
                        disabled={!combatEnabled}
                        value='combatOptionCheckFatigue' />
                    }
                    label={<Localize field='bodyConfig.combatCheckFatigue' />}
                    disabled={!combatEnabled} />
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={combatOptionReserveDocks}
                        onChange={(event, checked) => this.setState({ combatOptionReserveDocks: checked })}
                        disabled={true}
                        value='combatOptionReserveDocks' />
                    }
                    label={<Localize field='bodyConfig.combatReserveDocks' />}
                    disabled={true} />
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={combatOptionPortCheck}
                        onChange={(event, checked) => this.setState({ combatOptionPortCheck: checked })}
                        disabled={!combatEnabled}
                        value='combatOptionPortCheck' />
                    }
                    label={<Localize field='bodyConfig.combatPortCheck' />}
                    disabled={!combatEnabled} />
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={combatOptionMedalStop}
                        onChange={(event, checked) => this.setState({ combatOptionMedalStop: checked })}
                        disabled={true}
                        value='combatOptionMedalStop' />
                    }
                    label={<Localize field='bodyConfig.combatMedalStop' />}
                    disabled={true} />
                </Grid>
              </Grid>

              <Divider />

              <Typography type='display1'>
                <Localize field='bodyConfig.questsHeader' />
                <Switch
                  className={classes.switch}
                  checked={questsEnabled}
                  onChange={(event, checked) => this.setState({ questsEnabled: checked })} />
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper className={classes.paper} elevation={0}>
              <Typography type='display1' className={classes.flexReset}>
                <Localize field='bodyConfig.configHeader' />
                <Button
                  dense
                  color='primary'
                  className={classes.saveButton}
                  onClick={() => configLoad.open()}
                >
                  <Localize field='bodyConfig.configLoad' />
                  <Upload />
                </Button>
                <Button
                  dense
                  color='primary'
                  className={classes.saveButton}
                  onClick={() => this.onSaveClick()}
                >
                  <Localize field='bodyConfig.configSave' />
                  <ContentSave />
                </Button>
              </Typography>
              <Paper elevation={2}>
                <pre className={classes.pre}>
                  {config.pythonConfig.map(line => `${line}\n`)}
                </pre>
              </Paper>
            </Paper>
          </Grid>
        </Grid>
      </Dropzone>
    )
  }
}

BodyConfig.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  setJsonConfig: PropTypes.func.isRequired,
  setPythonConfig: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfig)
