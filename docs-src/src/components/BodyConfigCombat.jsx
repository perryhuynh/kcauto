import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'

import Select from 'react-select'
import CreatableSelect from 'react-select/lib/Creatable'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import Switch from '@material-ui/core/Switch'
import Button from '@material-ui/core/Button'
import InputLabel from '@material-ui/core/InputLabel'
import FormControl from '@material-ui/core/FormControl'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import Checkbox from '@material-ui/core/Checkbox'
import { TimePicker } from 'material-ui-pickers'
import { ChevronRight } from 'mdi-material-ui'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'

import {
  FLEET_PRESETS, COMBAT_ENGINES, MAPS, COMBINED_FLEET_MODES, COMBAT_NODE_COUNTS, NODES, FORMATIONS, NIGHT_BATTLES,
  DAMAGE_STATES, LBAS_GROUPS,
} from 'types/formOptions'

class BodyConfigCombat extends PureComponent {
  state = {
    combatNodeSelect1: null,
    combatNodeSelect2: null,
    combatFormationsNode: null,
    combatFormationsFormation: null,
    combatNightBattlesNode: null,
    combatNightBattlesMode: null,
  }

  handleCombatToggle = (event, checked) => {
    // when toggling the combat module, make sure to clear any conflicting expeditions as needed and disable the
    // ship switcher as needed
    const {
      config,
      combatFleetMode,
      updateObject,
    } = this.props

    if (checked) {
      if (combatFleetMode === 'striking') {
        updateObject(config, { combatEnabled: checked, expeditionsFleet3: [] })
      } else if (['ctf', 'stf', 'transport'].includes(combatFleetMode)) {
        updateObject(config, { combatEnabled: checked, expeditionsFleet2: [] })
      } else {
        updateObject(config, { combatEnabled: checked })
      }
    } else {
      updateObject(config, { combatEnabled: checked, shipSwitcherEnabled: false })
    }
  }

  handleMapChange = (value) => {
    // when changing the map, if the map is not an event map, disable the event reset module
    const {
      config,
      updateObject,
    } = this.props

    if (value[0] !== 'E') {
      updateObject(config, { combatMap: value, eventResetEnabled: false })
    } else {
      updateObject(config, { combatMap: value })
    }
  }

  handleFleetModeChange = (value) => {
    // when changing the fleet mode, make sure to disable and clear any conflicting expeditions as needed
    const {
      config,
      updateObject,
    } = this.props

    if (value.value === 'striking') {
      updateObject(config, {
        combatFleets: [],
        combatFleetMode: value,
        combatDisableExpeditionsFleet2: false,
        expeditionsFleet3: [],
        combatDisableExpeditionsFleet3: true,
        combatDisablePvP: false,
        pvpFleet: null,
        combatDisablePvPFleet: false,
      })
    } else if (['ctf', 'stf', 'transport'].includes(value.value)) {
      updateObject(config, {
        combatFleets: [],
        combatFleetMode: value,
        expeditionsFleet2: [],
        combatDisableExpeditionsFleet2: true,
        combatDisableExpeditionsFleet3: false,
        combatDisablePvP: true,
        pvpEnabled: false,
        pvpFleet: null,
        combatDisablePvPFleet: true,
      })
    } else {
      updateObject(config, {
        combatFleetMode: value,
        combatDisableExpeditionsFleet2: false,
        combatDisableExpeditionsFleet3: false,
        combatDisablePvP: false,
        combatDisablePvPFleet: false,
      })
    }
  }

  handleCombatRetreatNodesChange = (value) => {
    // only allow the most recently selected numeric combat node count value; the actual script only allows uses the
    // smallest integer value in this field, but this exists as a sanitation step for the user
    const {
      config,
      updateObject,
    } = this.props
    const newCombatRetreatNodes = []

    let lastCombatNodeCount = null
    // determine last-specified number
    value.forEach((opt) => {
      lastCombatNodeCount = !Number.isNaN(parseInt(opt.value, 10)) ? parseInt(opt.value, 10) : lastCombatNodeCount
    })
    // filter out every integer value other than the last specified one
    value.forEach((opt) => {
      if (Number.isNaN(parseInt(opt.value, 10)) || parseInt(opt.value, 10) === lastCombatNodeCount) {
        newCombatRetreatNodes.push(opt)
      }
    })

    updateObject(config, { combatRetreatNodes: newCombatRetreatNodes })
  }

  handleCombatNodeSelectAdd = (node, targetNode) => {
    // automatically add a node select option based on the two previous helper fields; also checks against previously
    // entered values so that existing node selects for a node are overwritten
    const {
      config,
      combatNodeSelects,
      updateObject,
    } = this.props

    const newVal = `${node.value}>${targetNode.value}`
    const newOpt = { label: newVal, value: newVal }

    this.setState({ combatNodeSelect1: null, combatNodeSelect2: null })
    const newCombatNodeSelects = combatNodeSelects.filter(
      opt => opt.value.split('>')[0] !== newVal.split('>')[0]
    )
    newCombatNodeSelects.push(newOpt)
    updateObject(config, { combatNodeSelects: newCombatNodeSelects })
  }

  handleCombatFormationAdd = (node, formation) => {
    // automatically add a custom formation selection based on the two previous helper fields; also checks against
    // previously entered values so that existing formations for a node are overwritten
    const {
      config,
      combatFormations,
      updateObject,
    } = this.props

    const newVal = `${node.value}:${formation.value}`
    const newOpt = { label: newVal, value: newVal }

    this.setState({ combatFormationsNode: null, combatFormationsFormation: null })
    const newCombatFormations = combatFormations.filter(
      opt => opt.value.split(':')[0] !== newVal.split(':')[0]
    )
    newCombatFormations.push(newOpt)
    updateObject(config, { combatFormations: newCombatFormations })
  }

  handleCombatNightBattleAdd = (node, nightBattle) => {
    // automatically add a custom night battle selection based on the two previous helper fields; also checks against
    // previously entered values so that existing night battle selections for a node are overwritten
    const {
      config,
      combatNightBattles,
      updateObject,
    } = this.props

    const newVal = `${node.value}:${nightBattle.value}`
    const newOpt = { label: newVal, value: newVal }

    this.setState({ combatNightBattlesNode: null, combatNightBattlesMode: null })
    const newCombatNightBattles = combatNightBattles.filter(
      opt => opt.value.split(':')[0] !== newVal.split(':')[0]
    )
    newCombatNightBattles.push(newOpt)
    updateObject(config, { combatNightBattles: newCombatNightBattles })
  }

  handleLBASGroupSelect = (value) => {
    // clear the LBAS node selects as needed based on the LBAS group selections
    const {
      config,
      updateObject,
    } = this.props

    const newLBASNodes = {}
    LBAS_GROUPS.forEach((opt) => {
      if (value.filter(val => val.value === opt.value).length === 0) {
        newLBASNodes[`combatLBASGroup${opt.label}Node1`] = null
        newLBASNodes[`combatLBASGroup${opt.label}Node2`] = null
      }
    })
    updateObject(config, { combatLBASGroups: value, ...newLBASNodes })
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
      combatEnabled,
      combatEngine,
      combatFleets,
      combatMap,
      combatFleetMode,
      combatRetreatNodes,
      combatNodeSelects,
      combatFormations,
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
      combatOptionLastNodePush,
      updateSwitch,
      updateSelect,
      updateTime,
    } = this.props
    const {
      combatNodeSelect1,
      combatNodeSelect2,
      combatFormationsNode,
      combatFormationsFormation,
      combatNightBattlesNode,
      combatNightBattlesMode,
    } = this.state

    const combatLBASGroup1NodesDisabled = !combatEnabled
      || combatLBASGroups.filter(opt => opt.value === '1').length === 0
    const combatLBASGroup2NodesDisabled = !combatEnabled
      || combatLBASGroups.filter(opt => opt.value === '2').length === 0
    const combatLBASGroup3NodesDisabled = !combatEnabled
      || combatLBASGroups.filter(opt => opt.value === '3').length === 0

    return (
      <>
        <Typography variant='h5'>
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
                name='combatEngine'
                value={combatEngine}
                options={COMBAT_ENGINES}
                onChange={value => updateSelect(config, value, 'combatEngine')}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>
        </Grid>

        <Grid container spacing={0}>
          <Grid item xs={12} sm={12} className={classes.formGrid}>
            <FormControl
              disabled={!combatEnabled
                || combatFleetMode !== COMBINED_FLEET_MODES.filter(opt => opt.value === '')[0]}
              margin='normal'
              fullWidth
            >
              <InputLabel htmlFor='combatFleets' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatFleets' />
              </InputLabel>
              <Select
                isMulti
                className={classes.reactSelect}
                name='combatFleets'
                value={combatFleets}
                options={FLEET_PRESETS}
                onChange={value => updateSelect(config, value, 'combatFleets')}
                isDisabled={!combatEnabled
                  || combatFleetMode !== COMBINED_FLEET_MODES.filter(opt => opt.value === '')[0]} />
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
                name='combatMap'
                value={combatMap}
                options={MAPS}
                onChange={this.handleMapChange}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatFleetMode' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatFleetMode' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                name='combatFleetMode'
                value={combatFleetMode}
                options={COMBINED_FLEET_MODES}
                onChange={this.handleFleetModeChange}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatRetreatNodes' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatRetreatNodes' />
              </InputLabel>
              <Select
                isMulti
                isClearable
                className={classes.reactSelect}
                name='combatRetreatNodes'
                value={combatRetreatNodes}
                options={COMBAT_NODE_COUNTS.concat(NODES)}
                onChange={this.handleCombatRetreatNodesChange}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>

          <Grid item xs={4} sm={2} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatNodeSelect1' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatNodeSelect1' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                name='combatNodeSelect1'
                value={combatNodeSelect1}
                options={NODES}
                onChange={value => this.setState({ combatNodeSelect1: value })}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>
          <Grid item xs={4} sm={2} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatNodeSelect2' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatNodeSelect2' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                name='combatNodeSelect2'
                value={combatNodeSelect2}
                options={NODES}
                onChange={value => this.setState({ combatNodeSelect2: value })}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>
          <Grid item xs={4} sm={1} className={classes.formGridButton}>
            <Button
              size='small'
              color='primary'
              disabled={!combatEnabled
                || (!combatNodeSelect1 || !combatNodeSelect2 || combatNodeSelect1 === combatNodeSelect2)}
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
              <CreatableSelect
                isMulti
                isClearable
                components={{ DropdownIndicator: null }}
                className={classes.reactSelect}
                name='combatNodeSelects'
                menuIsOpen={false}
                value={combatNodeSelects}
                onChange={value => updateSelect(config, value, 'combatNodeSelects')}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>

          <Grid item xs={4} sm={2} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatFormationsNode' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatCustomFormation1' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                name='combatFormationsNode'
                value={combatFormationsNode}
                options={combatEngine === 'legacy' ? COMBAT_NODE_COUNTS : COMBAT_NODE_COUNTS.concat(NODES)}
                onChange={value => this.setState({ combatFormationsNode: value })}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>
          <Grid item xs={4} sm={3} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatFormationsFormation' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatCustomFormation2' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                name='combatFormationsFormation'
                value={combatFormationsFormation}
                options={FORMATIONS}
                onChange={value => this.setState({ combatFormationsFormation: value })}
                isDisabled={!combatEnabled} />
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
              <CreatableSelect
                isMulti
                isClearable
                components={{ DropdownIndicator: null }}
                className={classes.reactSelect}
                name='combatFormations'
                menuIsOpen={false}
                value={combatFormations}
                onChange={value => updateSelect(config, value, 'combatFormations')}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>

          <Grid item xs={4} sm={2} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatNightBattlesNode' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatCustomNightBattle1' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                name='combatNightBattlesNode'
                value={combatNightBattlesNode}
                options={combatEngine === 'legacy' ? COMBAT_NODE_COUNTS : COMBAT_NODE_COUNTS.concat(NODES)}
                onChange={value => this.setState({ combatNightBattlesNode: value })}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>
          <Grid item xs={4} sm={3} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatNightBattlesMode' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatCustomNightBattle2' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                name='combatNightBattlesMode'
                value={combatNightBattlesMode}
                options={NIGHT_BATTLES}
                onChange={value => this.setState({ combatNightBattlesMode: value })}
                isDisabled={!combatEnabled} />
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
              <CreatableSelect
                isMulti
                isClearable
                components={{ DropdownIndicator: null }}
                className={classes.reactSelect}
                name='combatNightBattles'
                menuIsOpen={false}
                value={combatNightBattles}
                onChange={value => updateSelect(config, value, 'combatNightBattles')}
                isDisabled={!combatEnabled} />
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatRetreatLimit' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatRetreatLimit' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                name='combatRetreatLimit'
                value={combatRetreatLimit}
                options={DAMAGE_STATES}
                onChange={value => updateSelect(config, value, 'combatRetreatLimit')}
                isDisabled={!combatEnabled}
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
                name='combatRepairLimit'
                value={combatRepairLimit}
                options={DAMAGE_STATES}
                onChange={value => updateSelect(config, value, 'combatRepairLimit')}
                isDisabled={!combatEnabled}
                clearable={false}
                fullWidth />
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} fullWidth>
              <TimePicker
                autoOk
                id='combatRepairTimeLimit'
                label={<Localize field='bodyConfig.combatRepairTimeLimit' />}
                value={combatRepairTimeLimit}
                ampm={false}
                onChange={time => updateTime(config, time, 'combatRepairTimeLimit')}
                disabled={!combatEnabled} />
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={3} className={classes.formGrid}>
            <FormControl disabled={!combatEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='combatLBASGroups' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.combatLBASGroups' />
              </InputLabel>
              <Select
                isMulti
                isClearable
                className={classes.reactSelect}
                name='combatLBASGroups'
                value={combatLBASGroups}
                options={LBAS_GROUPS}
                onChange={this.handleLBASGroupSelect}
                isDisabled={!combatEnabled} />
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
                  name='combatLBASGroup1Node1'
                  value={combatLBASGroup1Node1}
                  options={NODES}
                  onChange={value => updateSelect(config, value, 'combatLBASGroup1Node1')}
                  isDisabled={combatLBASGroup1NodesDisabled} />
                <Select
                  className={classes.reactSelectHalfWidth}
                  name='combatLBASGroup1Node2'
                  value={combatLBASGroup1Node2}
                  options={NODES}
                  onChange={value => updateSelect(config, value, 'combatLBASGroup1Node2')}
                  isDisabled={combatLBASGroup1NodesDisabled} />
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
                  name='combatLBASGroup2Node1'
                  value={combatLBASGroup2Node1}
                  options={NODES}
                  onChange={value => updateSelect(config, value, 'combatLBASGroup2Node1')}
                  isDisabled={combatLBASGroup2NodesDisabled} />
                <Select
                  className={classes.reactSelectHalfWidth}
                  name='combatLBASGroup2Node2'
                  value={combatLBASGroup2Node2}
                  options={NODES}
                  onChange={value => updateSelect(config, value, 'combatLBASGroup2Node2')}
                  isDisabled={combatLBASGroup2NodesDisabled} />
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
                  name='combatLBASGroup3Node1'
                  value={combatLBASGroup3Node1}
                  options={NODES}
                  onChange={value => updateSelect(config, value, 'combatLBASGroup3Node1')}
                  isDisabled={combatLBASGroup3NodesDisabled} />
                <Select
                  className={classes.reactSelectHalfWidth}
                  name='combatLBASGroup3Node2'
                  value={combatLBASGroup3Node2}
                  options={NODES}
                  onChange={value => updateSelect(config, value, 'combatLBASGroup3Node2')}
                  isDisabled={combatLBASGroup3NodesDisabled} />
              </div>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={12} className={classes.formGrid}>
            <FormControlLabel
              control={(
                <Checkbox
                  checked={combatOptionCheckFatigue}
                  onChange={(event, checked) => updateSwitch(config, event, checked, 'combatOptionCheckFatigue')}
                  disabled={!combatEnabled}
                  name='combatOptionCheckFatigue' />
              )}
              label={<Localize field='bodyConfig.combatCheckFatigue' />}
              disabled={!combatEnabled} />
            <FormControlLabel
              control={(
                <Checkbox
                  checked={combatOptionReserveDocks}
                  onChange={(event, checked) => updateSwitch(config, event, checked, 'combatOptionReserveDocks')}
                  disabled={!combatEnabled}
                  name='combatOptionReserveDocks' />
              )}
              label={<Localize field='bodyConfig.combatReserveDocks' />}
              disabled={!combatEnabled} />
            <FormControlLabel
              control={(
                <Checkbox
                  checked={combatOptionPortCheck}
                  onChange={(event, checked) => updateSwitch(config, event, checked, 'combatOptionPortCheck')}
                  disabled={!combatEnabled}
                  name='combatOptionPortCheck' />
              )}
              label={<Localize field='bodyConfig.combatPortCheck' />}
              disabled={!combatEnabled} />
            <FormControlLabel
              control={(
                <Checkbox
                  checked={combatOptionClearStop}
                  onChange={(event, checked) => updateSwitch(config, event, checked, 'combatOptionClearStop')}
                  disabled={!combatEnabled}
                  name='combatOptionClearStop' />
              )}
              label={<Localize field='bodyConfig.combatClearStop' />}
              disabled={!combatEnabled} />
            <FormControlLabel
              control={(
                <Checkbox
                  checked={combatOptionLastNodePush}
                  onChange={(event, checked) => updateSwitch(config, event, checked, 'combatOptionLastNodePush')}
                  disabled={!combatEnabled}
                  name='combatOptionLastNodePush' />
              )}
              label={<Localize field='bodyConfig.combatLastNodePush' />}
              disabled={!combatEnabled} />
          </Grid>
        </Grid>
      </>
    )
  }
}

BodyConfigCombat.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  combatEnabled: PropTypes.bool.isRequired,
  combatEngine: PropTypes.object.isRequired,
  combatFleets: PropTypes.array,
  combatMap: PropTypes.object.isRequired,
  combatFleetMode: PropTypes.object,
  combatRetreatNodes: PropTypes.array,
  combatNodeSelects: PropTypes.array,
  combatFormations: PropTypes.array,
  combatNightBattles: PropTypes.array,
  combatRetreatLimit: PropTypes.object.isRequired,
  combatRepairLimit: PropTypes.object.isRequired,
  combatRepairTimeLimit: PropTypes.object.isRequired,
  combatLBASGroups: PropTypes.array,
  combatLBASGroup1Node1: PropTypes.object,
  combatLBASGroup1Node2: PropTypes.object,
  combatLBASGroup2Node1: PropTypes.object,
  combatLBASGroup2Node2: PropTypes.object,
  combatLBASGroup3Node1: PropTypes.object,
  combatLBASGroup3Node2: PropTypes.object,
  combatOptionCheckFatigue: PropTypes.bool,
  combatOptionReserveDocks: PropTypes.bool,
  combatOptionPortCheck: PropTypes.bool,
  combatOptionClearStop: PropTypes.bool,
  combatOptionLastNodePush: PropTypes.bool,
  updateSwitch: PropTypes.func.isRequired,
  updateSelect: PropTypes.func.isRequired,
  updateTime: PropTypes.func.isRequired,
  updateObject: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigCombat)
