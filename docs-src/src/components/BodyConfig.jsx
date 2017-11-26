import React from 'react'
import PropTypes from 'prop-types'
import Select, { Creatable } from 'react-select'
import { withStyles } from 'material-ui/styles'
import saveAs from 'save-as'

import TimeInput from 'material-ui-time-picker'

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
import { ChevronRight, ContentSave } from 'mdi-material-ui'

const EXPEDITIONS = Array.from({ length: 40 }, (value, key) => ({ value: String(key + 1), label: String(key + 1) }))
EXPEDITIONS.push({ value: '9998', label: 'Node Support' })
EXPEDITIONS.push({ value: '9999', label: 'Boss Support' })
const MAPS = ['1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '2-1', '2-2', '2-3', '2-4', '2-5', '3-1', '3-2', '3-3', '3-4',
  '3-5', '4-1', '4-2', '4-3', '4-4', '4-5', '5-1', '5-2', '5-3', '5-4', '5-5', '6-1', '6-2', '6-3', '6-4', '6-5',
  'E-1', 'E-2', 'E-3', 'E-4', 'E-5', 'E-6', 'E-7', 'E-8']
  .map(value => ({ value, label: value }))
const COMBINED_FLEET_MODES = [
  { value: '', label: 'Standard' }, { value: 'ctf', label: 'CTF' }, { value: 'stf', label: 'STF' },
  { value: 'transport', label: 'Transport' }, { value: 'striking', label: 'Striking' }]
const COMBAT_NODE_COUNTS = ['1', '2', '3', '4', '5'].map(value => ({ value, label: value }))
const NODES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(value => ({ value, label: value }))
const DAMAGE_STATES = ['heavy', 'moderate', 'minor'].map(value => ({ value, label: value }))
const LBAS_GROUPS = ['1', '2', '3'].map(value => ({ value, label: value }))

const styles = () => ({
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
    minWidth: 130,
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

class BodyConfig extends React.Component {
  state = {
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
    combatMap: '1-1',
    combatFleetMode: '',
    combatCombatNodes: null,
    combatNodeSelect1: null,
    combatNodeSelect2: null,
    combatNodeSelects: null,
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

  componentDidMount = () => {
    // this.props.setJsonConfig(this.state)
    this.props.setPythonConfig(this.state)
  }

  componentDidUpdate = (nextProp, nextState) => {
    if (this.state !== nextState) {
      // this.props.setJsonConfig(this.state)
      this.props.setPythonConfig(this.state)
    }
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

  handleFleetModeChange = (value) => {
    if (value === 'striking') {
      this.setState({ expeditionsFleet3Enabled: false, expeditionsFleet3: [] })
    } else if (value === 'ctf' || value === 'stf' || value === 'transport') {
      this.setState({ expeditionsFleet2Enabled: false, expeditionsFleet2: [] })
    } else {
      this.setState({ expeditionsFleet2Enabled: true, expeditionsFleet3Enabled: true })
    }
    this.setState({ combatFleetMode: value })
  }

  handleCombatNodeSelectAdd = (select1, select2) => {
    const combatNodeSelects = this.state.combatNodeSelects ?
      `${this.state.combatNodeSelects},${select1}>${select2}` :
      `${select1}>${select2}`
    this.setState({ combatNodeSelect1: null, combatNodeSelect2: null, combatNodeSelects })
  }

  handleLBASGroupSelect = (value) => {
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

  render = () => {
    const {
      classes,
      config,
    } = this.props
    const {
      generalProgram,
      generalJSTOffset,
      scheduledSleepEnabled,
      scheduledSleepStart,
      scheduledSleepLength,
      expeditionsEnabled,
      expeditionsFleet2Enabled,
      expeditionsFleet3Enabled,
      expeditionsFleet4Enabled,
      expeditionsFleet2,
      expeditionsFleet3,
      expeditionsFleet4,
      pvpEnabled,
      combatEnabled,
      combatMap,
      combatFleetMode,
      combatCombatNodes,
      combatNodeSelect1,
      combatNodeSelect2,
      combatNodeSelects,
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
    const combatLBASGroupsArray = combatLBASGroups ? combatLBASGroups.split(',') : []
    const combatLBASGroup1NodesDisabled = !combatEnabled || combatLBASGroupsArray.indexOf('1') < 0
    const combatLBASGroup2NodesDisabled = !combatEnabled || combatLBASGroupsArray.indexOf('2') < 0
    const combatLBASGroup3NodesDisabled = !combatEnabled || combatLBASGroupsArray.indexOf('3') < 0

    return (
      <Grid container spacing={0}>
        <Grid item xs={12} md={8}>
          <Paper className={classes.paper} elevation={0}>
            <Typography type='display1'>General</Typography>

            <Grid container spacing={0}>
              <Grid item xs={12} sm={8} className={classes.formGrid}>
                <TextField
                  id='generalProgram'
                  label='Program'
                  value={generalProgram}
                  onChange={event => this.setState({ generalProgram: event.target.value })}
                  helperText='Program that Kantai Collection is running in (ex: Chrome)'
                  className={classes.formControl}
                  fullWidth
                  margin='normal' />
              </Grid>
              <Grid item xs={12} sm={4} className={classes.formGrid}>
                <TextField
                  id='generalJSTOffset'
                  label='JST Offset'
                  value={generalJSTOffset}
                  onChange={event => this.setState({ generalJSTOffset: event.target.value })}
                  helperText='Hours offset from JST'
                  className={classes.formControl}
                  fullWidth
                  type='number'
                  margin='normal' />
              </Grid>
            </Grid>

            <Divider />

            <Typography type='display1'>
              Scheduled Sleep
              <Switch
                className={classes.switch}
                checked={scheduledSleepEnabled}
                onChange={(event, checked) => this.setState({ scheduledSleepEnabled: checked })} />
            </Typography>

            <Grid container spacing={0}>
              <Grid item xs={12} sm={6} className={classes.formGrid}>
                <FormControl disabled={!scheduledSleepEnabled} className={classes.formControl} fullWidth>
                  <InputLabel htmlFor='scheduledSleepStart'>Start Time</InputLabel>
                  <TimeInput
                    id='scheduledSleepStart'
                    mode='24h'
                    value={scheduledSleepStart}
                    onChange={time => this.setState({ scheduledSleepStart: time })}
                    fullWidth />
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6} className={classes.formGrid}>
                <TextField
                  id='scheduledSleepLength'
                  label='Length'
                  value={scheduledSleepLength}
                  onChange={event => this.setState({ scheduledSleepLength: event.target.value })}
                  helperText='How long to sleep for'
                  type='number'
                  margin='normal'
                  className={classes.formControl}
                  disabled={!scheduledSleepEnabled}
                  fullWidth />
              </Grid>
            </Grid>

            <Divider />

            <Typography type='display1'>
              Expeditions
              <Switch
                className={classes.switch}
                checked={expeditionsEnabled}
                onChange={(event, checked) => this.setState({ expeditionsEnabled: checked })} />
            </Typography>

            <Grid container spacing={0}>
              <Grid item xs={12} sm={4} className={classes.formGrid}>
                <FormControl disabled={!expeditionsEnabled || !expeditionsFleet2Enabled} margin='normal' fullWidth>
                  <InputLabel htmlFor='expeditionsFleet2' shrink={true} className={classes.reactSelectLabel}>
                    Fleet 2
                  </InputLabel>
                  <Select
                    multi
                    className={classes.reactSelect}
                    simpleValue={true}
                    name='expeditionsFleet2'
                    value={expeditionsFleet2}
                    options={EXPEDITIONS}
                    onChange={value => this.setState({ expeditionsFleet2: value })}
                    disabled={!expeditionsEnabled || !expeditionsFleet2Enabled}
                    fullWidth />
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={4} className={classes.formGrid}>
                <FormControl disabled={!expeditionsEnabled || !expeditionsFleet3Enabled} margin='normal' fullWidth>
                  <InputLabel htmlFor='expeditionsFleet3' shrink={true} className={classes.reactSelectLabel}>
                    Fleet 2
                  </InputLabel>
                  <Select
                    multi
                    className={classes.reactSelect}
                    simpleValue={true}
                    name='expeditionsFleet3'
                    value={expeditionsFleet3}
                    options={EXPEDITIONS}
                    onChange={value => this.setState({ expeditionsFleet3: value })}
                    disabled={!expeditionsEnabled || !expeditionsFleet3Enabled}
                    fullWidth />
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={4} className={classes.formGrid}>
                <FormControl disabled={!expeditionsEnabled || !expeditionsFleet4Enabled} margin='normal' fullWidth>
                  <InputLabel htmlFor='expeditionsFleet4' shrink={true} className={classes.reactSelectLabel}>
                    Fleet 2
                  </InputLabel>
                  <Select
                    multi
                    className={classes.reactSelect}
                    simpleValue={true}
                    name='expeditionsFleet4'
                    value={expeditionsFleet4}
                    options={EXPEDITIONS}
                    onChange={value => this.setState({ expeditionsFleet4: value })}
                    disabled={!expeditionsEnabled || !expeditionsFleet4Enabled}
                    fullWidth />
                </FormControl>
              </Grid>
            </Grid>

            <Divider />

            <Typography type='display1'>
              PvP
              <Switch
                className={classes.switch}
                checked={pvpEnabled}
                onChange={(event, checked) => this.setState({ pvpEnabled: checked })} />
            </Typography>

            <Divider />

            <Typography type='display1'>
              Combat
              <Switch
                className={classes.switch}
                checked={combatEnabled}
                onChange={(event, checked) => this.setState({ combatEnabled: checked })} />
            </Typography>

            <Grid container spacing={0}>
              <Grid item xs={12} sm={4} className={classes.formGrid}>
                <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                  <InputLabel htmlFor='combatMap' shrink={true} className={classes.reactSelectLabel}>
                    Map
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
                    Fleet Mode
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
                    Combat Node Count
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
                    If at this Node...
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
                    ...select this Node
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
                  disabled={!combatEnabled || (!combatNodeSelect1 || !combatNodeSelect2)}
                  onClick={() => this.handleCombatNodeSelectAdd(combatNodeSelect1, combatNodeSelect2)}
                >
                  Add
                  <ChevronRight />
                </Button>
              </Grid>
              <Grid item xs={12} sm={7} className={classes.formGrid}>
                <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                  <InputLabel htmlFor='combatNodeSelects' shrink={true} className={classes.reactSelectLabel}>
                    All Node Selects
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

              <Grid item xs={12} sm={4} className={classes.formGrid}>
                <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
                  <InputLabel htmlFor='combatRetreatLimit' shrink={true} className={classes.reactSelectLabel}>
                    Retreat Limit
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
                    Repair Limit
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
                  <InputLabel htmlFor='combatRepairTimeLimit'>Repair Time Limit</InputLabel>
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
                    LBAS Groups
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
                    Group 1 Nodes
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
                    Group 2 Nodes
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
                      onChange={value => this.setState({ combatLBASGroup2Node1: value })}
                      disabled={combatLBASGroup2NodesDisabled} />
                  </div>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={3} className={classes.formGrid}>
                <FormControl disabled={combatLBASGroup3NodesDisabled} margin='normal' fullWidth>
                  <InputLabel htmlFor='combatLBASGroup3Nodes' shrink={true} className={classes.reactSelectLabel}>
                    Group 3 Nodes
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
                  label='Check Fatigue'
                  disabled={!combatEnabled} />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={combatOptionReserveDocks}
                      onChange={(event, checked) => this.setState({ combatOptionReserveDocks: checked })}
                      disabled={true}
                      value='combatOptionReserveDocks' />
                  }
                  label='Reserve Docks'
                  disabled={true} />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={combatOptionPortCheck}
                      onChange={(event, checked) => this.setState({ combatOptionPortCheck: checked })}
                      disabled={!combatEnabled}
                      value='combatOptionPortCheck' />
                  }
                  label='Port Check'
                  disabled={!combatEnabled} />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={combatOptionMedalStop}
                      onChange={(event, checked) => this.setState({ combatOptionMedalStop: checked })}
                      disabled={true}
                      value='combatOptionMedalStop' />
                  }
                  label='Medal Stop'
                  disabled={true} />
              </Grid>

            </Grid>

            <Divider />

            <Typography type='display1'>
              Quests
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
              Config
              <Button
                dense
                color='primary'
                className={classes.saveButton}
                onClick={() => this.onSaveClick()}
              >
                Save
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
    )
  }
}

BodyConfig.propTypes = {
  classes: PropTypes.object.isRequired,
  ui: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  setJsonConfig: PropTypes.func.isRequired,
  setPythonConfig: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfig)
