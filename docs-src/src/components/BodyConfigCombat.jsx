import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Select, { Creatable } from 'react-select'
import Grid from 'material-ui/Grid'
import Typography from 'material-ui/Typography'
import Switch from 'material-ui/Switch'
import Button from 'material-ui/Button'
import { InputLabel } from 'material-ui/Input'
import { FormControl, FormControlLabel } from 'material-ui/Form'
import Checkbox from 'material-ui/Checkbox'
import TimeInput from 'material-ui-time-picker'
import { ChevronRight } from 'mdi-material-ui'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


const FLEET_PRESETS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'].map(value => (
  { value, label: value }))
const COMBAT_ENGINES = [
  { value: 'live', label: <Localize field='bodyConfig.combatEngineLive' /> },
  { value: 'legacy', label: <Localize field='bodyConfig.combatEngineLegacy' /> }]
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
const COMBAT_NODE_COUNTS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'].map(value => (
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

class BodyConfigCombat extends PureComponent {
  state = this.props.config

  componentWillReceiveProps = (nextProps) => {
    if (this.props.config !== nextProps.config) {
      this.setState(nextProps.config)
    }
  }

  handleCombatToggle = (event, checked) => {
    // when toggling the combat module, make sure to clear any conflicting expeditions as needed and disable the
    // ship switcher as needed; these states are not actually used in here, but used to inform the other sections of
    // available fields
    if (checked) {
      if (this.state.combatFleetMode === 'striking') {
        this.setState({ combatEnabled: checked, expeditionsFleet3: [] }, () => this.props.callback(this.state))
      } else if (['ctf', 'stf', 'transport'].includes(this.state.combatFleetMode)) {
        this.setState({ combatEnabled: checked, expeditionsFleet2: [] }, () => this.props.callback(this.state))
      } else {
        this.setState({ combatEnabled: checked }, () => this.props.callback(this.state))
      }
    } else {
      this.setState({ combatEnabled: checked, shipSwitcherEnabled: false }, () => this.props.callback(this.state))
    }
  }

  handleFleetModeChange = (value) => {
    // when changing the fleet mode, make sure to disable and clear any conflicting expeditions as needed; these states
    // are not actually used in here, but used to inform the expedition section of available fields
    if (value === 'striking') {
      this.setState(
        {
          combatFleets: [],
          combatFleetMode: value,
          combatDisableExpeditionsFleet2: false,
          expeditionsFleet3: [],
          combatDisableExpeditionsFleet3: true,
          pvpFleet: null,
          combatDisablePvPFleet: true,
        },
        () => this.props.callback(this.state)
      )
    } else if (['ctf', 'stf', 'transport'].indexOf(value) > -1) {
      this.setState(
        {
          combatFleets: [],
          combatFleetMode: value,
          expeditionsFleet2: [],
          combatDisableExpeditionsFleet2: true,
          combatDisableExpeditionsFleet3: false,
          pvpFleet: null,
          combatDisablePvPFleet: true,
        },
        () => this.props.callback(this.state)
      )
    } else {
      this.setState(
        {
          combatFleetMode: value,
          combatDisableExpeditionsFleet2: false,
          combatDisableExpeditionsFleet3: false,
          combatDisablePvPFleet: false,
        },
        () => this.props.callback(this.state)
      )
    }
  }

  handleCombatRetreatNodesChange = (value) => {
    // only allow the most recently selected numeric combat node count value; the actual script only allows uses the
    // smallest integer value in this field, but this exists as a sanitation step for the user
    const validCombatRetreatNodes = []
    let lastCombatNodeCount = null
    // determine last-specified number
    value.split(',').forEach((val) => {
      lastCombatNodeCount = !Number.isNaN(parseInt(val, 10)) ? parseInt(val, 10) : lastCombatNodeCount
    })
    // filter out every integer value other than the last specified one
    value.split(',').forEach((val) => {
      if (Number.isNaN(parseInt(val, 10)) || parseInt(val, 10) === lastCombatNodeCount) {
        validCombatRetreatNodes.push(val)
      }
    })
    this.setState({
      combatRetreatNodes: validCombatRetreatNodes.length > 0 ? validCombatRetreatNodes.join(',') : null,
    }, () => this.props.callback(this.state))
  }

  handleCombatNodeSelectAdd = (node, targetNode) => {
    // automatically add a node select option based on the two previous helper fields; also checks against previously
    // entered values so that existing node selects for a node are overwritten
    const tempCombatNodeSelects = this.state.combatNodeSelects ? this.state.combatNodeSelects : ''
    const tempCombatNodeSelectsObj = this.optionsNodeSplitter(tempCombatNodeSelects, '>')
    tempCombatNodeSelectsObj[node] = targetNode
    const combatNodeSelects = Object.keys(tempCombatNodeSelectsObj).sort().map(key =>
      `${key}>${tempCombatNodeSelectsObj[key]}`).join(',')
    this.setState(
      { combatNodeSelect1: null, combatNodeSelect2: null, combatNodeSelects },
      () => this.props.callback(this.state)
    )
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
    this.setState(
      { combatFormationsNode: null, combatFormationsFormation: null, combatFormations },
      () => this.props.callback(this.state)
    )
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
    this.setState(
      { combatNightBattlesNode: null, combatNightBattlesMode: null, combatNightBattles },
      () => this.props.callback(this.state)
    )
  }

  handleLBASGroupSelect = (value) => {
    // clear the LBAS node selects as needed based on the LBAS group selections
    if (!value.includes('1')) {
      this.setState({ combatLBASGroup1Node1: null, combatLBASGroup1Node2: null }, () => this.props.callback(this.state))
    }
    if (!value.includes('2')) {
      this.setState({ combatLBASGroup2Node1: null, combatLBASGroup2Node2: null }, () => this.props.callback(this.state))
    }
    if (!value.includes('3')) {
      this.setState({ combatLBASGroup3Node1: null, combatLBASGroup3Node2: null }, () => this.props.callback(this.state))
    }
    this.setState({ combatLBASGroups: value })
  }

  handleMiscOptionCheck = (event, checked) => {
    // handling of misc option checkboxes
    this.setState({ [event.target.value]: checked }, () => this.props.callback(this.state))
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
    } = this.props
    const {
      combatEnabled,
      combatFleets,
      combatEngine,
      combatMap,
      combatFleetMode,
      combatRetreatNodes,
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
      combatOptionClearStop,
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

    return (
      <Fragment>
        <Typography variant='display1'>
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
                onChange={value => this.setState({ combatEngine: value }, () => this.props.callback(this.state))}
                disabled={!combatEnabled}
                clearable={false}
                fullWidth />
            </FormControl>
          </Grid>
        </Grid>

        <Grid container spacing={0}>
          <Grid item xs={12} sm={12} className={classes.formGrid}>
            <FormControl
              disabled={!combatEnabled || combatFleetMode !== ''}
              margin='normal'
              fullWidth
            >
              <InputLabel htmlFor='combatFleets' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatFleets' />
              </InputLabel>
              <Select
                multi
                className={classes.reactSelect}
                simpleValue={true}
                name='combatFleets'
                value={combatFleets}
                options={FLEET_PRESETS}
                onChange={value => this.setState({ combatFleets: value }, () => this.props.callback(this.state))}
                disabled={!combatEnabled || combatFleetMode !== ''}
                fullWidth />
              <span className={classes.helperText}><Localize field='bodyConfig.combatFleetsDesc' /></span>
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
                onChange={value => this.setState({ combatMap: value }, () => this.props.callback(this.state))}
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
                clearable={false}
                fullWidth />
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatRetreatNodes' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatRetreatNodes' />
              </InputLabel>
              <Select
                multi
                className={classes.reactSelect}
                simpleValue={true}
                name='combatRetreatNodes'
                value={combatRetreatNodes}
                options={COMBAT_NODE_COUNTS.concat(NODES)}
                onChange={this.handleCombatRetreatNodesChange}
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
              size='small'
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
                onChange={value => this.setState({ combatNodeSelects: value }, () => this.props.callback(this.state))}
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
                onChange={
                  value => this.setState({ combatFormationsFormation: value })}
                disabled={!combatEnabled}
                fullWidth />
            </FormControl>
          </Grid>
          <Grid item xs={4} sm={1} className={classes.formGridButton}>
            <Button
              size='small'
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
                onChange={value => this.setState({ combatFormations: value }, () => this.props.callback(this.state))}
                disabled={!combatEnabled}
                fullWidth />
            </FormControl>
          </Grid>

          <Grid item xs={4} sm={2} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatNightBattlesNode' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatCustomNightBattle1' />
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
                <Localize field='bodyConfig.combatCustomNightBattle2' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                simpleValue={true}
                name='combatNightBattlesMode'
                value={combatNightBattlesMode}
                options={NIGHT_BATTLES}
                onChange={
                  value => this.setState({ combatNightBattlesMode: value })}
                disabled={!combatEnabled}
                fullWidth />
            </FormControl>
          </Grid>
          <Grid item xs={4} sm={1} className={classes.formGridButton}>
            <Button
              size='small'
              color='primary'
              disabled={!combatEnabled || !combatNightBattlesMode}
              onClick={() => this.handleCombatNightBattleAdd(combatNightBattlesNode, combatNightBattlesMode)}
            >
              <Localize field='bodyConfig.combatCustomNightBattleAdd' />
              <ChevronRight />
            </Button>
          </Grid>
          <Grid item xs={12} sm={6} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatNightBattles' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatCustomNightBattles' />
              </InputLabel>
              <Creatable
                multi
                className={classes.reactSelect}
                simpleValue={true}
                name='combatNightBattles'
                value={combatNightBattles}
                options={combatNightBattleOptions}
                onChange={value => this.setState({ combatNightBattles: value }, () => this.props.callback(this.state))}
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
                onChange={value => this.setState({ combatRetreatLimit: value }, () => this.props.callback(this.state))}
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
                onChange={value => this.setState({ combatRepairLimit: value }, () => this.props.callback(this.state))}
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
                autoOk={true}
                value={combatRepairTimeLimit}
                onChange={time => this.setState({ combatRepairTimeLimit: time }, () => this.props.callback(this.state))}
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
                  onChange={
                    value => this.setState({ combatLBASGroup1Node1: value }, () => this.props.callback(this.state))}
                  disabled={combatLBASGroup1NodesDisabled} />
                <Select
                  className={classes.reactSelectHalfWidth}
                  simpleValue={true}
                  name='combatLBASGroup1Node2'
                  value={combatLBASGroup1Node2}
                  options={NODES}
                  onChange={
                    value => this.setState({ combatLBASGroup1Node2: value }, () => this.props.callback(this.state))}
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
                  onChange={
                    value => this.setState({ combatLBASGroup2Node1: value }, () => this.props.callback(this.state))}
                  disabled={combatLBASGroup2NodesDisabled} />
                <Select
                  className={classes.reactSelectHalfWidth}
                  simpleValue={true}
                  name='combatLBASGroup2Node2'
                  value={combatLBASGroup2Node2}
                  options={NODES}
                  onChange={
                    value => this.setState({ combatLBASGroup2Node2: value }, () => this.props.callback(this.state))}
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
                  onChange={
                    value => this.setState({ combatLBASGroup3Node1: value }, () => this.props.callback(this.state))}
                  disabled={combatLBASGroup3NodesDisabled} />
                <Select
                  className={classes.reactSelectHalfWidth}
                  simpleValue={true}
                  name='combatLBASGroup3Node2'
                  value={combatLBASGroup3Node2}
                  options={NODES}
                  onChange={
                    value => this.setState({ combatLBASGroup3Node2: value }, () => this.props.callback(this.state))}
                  disabled={combatLBASGroup3NodesDisabled} />
              </div>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={12} className={classes.formGrid}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={combatOptionCheckFatigue}
                  onChange={this.handleMiscOptionCheck}
                  disabled={!combatEnabled}
                  value='combatOptionCheckFatigue' />
              }
              label={<Localize field='bodyConfig.combatCheckFatigue' />}
              disabled={!combatEnabled} />
            <FormControlLabel
              control={
                <Checkbox
                  checked={combatOptionReserveDocks}
                  onChange={this.handleMiscOptionCheck}
                  disabled={!combatEnabled}
                  value='combatOptionReserveDocks' />
              }
              label={<Localize field='bodyConfig.combatReserveDocks' />}
              disabled={!combatEnabled} />
            <FormControlLabel
              control={
                <Checkbox
                  checked={combatOptionPortCheck}
                  onChange={this.handleMiscOptionCheck}
                  disabled={!combatEnabled}
                  value='combatOptionPortCheck' />
              }
              label={<Localize field='bodyConfig.combatPortCheck' />}
              disabled={!combatEnabled} />
            <FormControlLabel
              control={
                <Checkbox
                  checked={combatOptionClearStop}
                  onChange={this.handleMiscOptionCheck}
                  disabled={!combatEnabled}
                  value='combatOptionClearStop' />
              }
              label={<Localize field='bodyConfig.combatClearStop' />}
              disabled={!combatEnabled} />
          </Grid>
        </Grid>
      </Fragment>
    )
  }
}

BodyConfigCombat.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigCombat)
