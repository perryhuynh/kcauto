import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Select, { Creatable } from 'react-select'
import Grid from 'material-ui/Grid'
import Paper from 'material-ui/Paper'
import Typography from 'material-ui/Typography'
import Switch from 'material-ui/Switch'
import TextField from 'material-ui/TextField'
import Button from 'material-ui/Button'
import Divider from 'material-ui/Divider'
import { InputLabel } from 'material-ui/Input'
import { FormControl } from 'material-ui/Form'
import { PlusBox } from 'mdi-material-ui'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


const BASE_SPECIFICATION = [
  { value: 'P', label: <Localize field='bodyConfig.shipSwitcherModalSpecificationPosition' /> },
  { value: 'A', label: <Localize field='bodyConfig.shipSwitcherModalSpecificationAsset' /> }]
const SORT_BY = [
  { value: 'N', label: <Localize field='bodyConfig.shipSwitcherModalSortByDateAcquired' /> },
  { value: 'C', label: <Localize field='bodyConfig.shipSwitcherModalSortByClass' /> },
  { value: 'L', label: <Localize field='bodyConfig.shipSwitcherModalSortByLevel' /> }]
const OFFSET_START = [
  { value: 'S', label: <Localize field='bodyConfig.shipSwitcherModalOffsetStartStart' /> },
  { value: 'E', label: <Localize field='bodyConfig.shipSwitcherModalOffsetStartEnd' /> }]
const CLASSES = ['AO', 'AR', 'AS', 'AV', 'BB', 'BBV', 'CA', 'CAV', 'CL', 'CLT', 'CT', 'CV', 'CVB', 'CVL', 'DD', 'DE',
  'LHA', 'SS', 'SSV']
  .map(value => ({ value, label: value }))
const SHIPS = ['SS_U-511']
  .map(value => ({ value, label: value }))
const LEVEL_EQUALITY = ['<', '>'].map(value => ({ value, label: value }))
const LOCKED = [
  { value: '_', label: <Localize field='bodyConfig.shipSwitcherModalLockedIgnore' /> },
  { value: 'L', label: <Localize field='bodyConfig.shipSwitcherModalLockedYes' /> },
  { value: 'N', label: <Localize field='bodyConfig.shipSwitcherModalLockedNo' /> }]
const RINGED = [
  { value: '_', label: <Localize field='bodyConfig.shipSwitcherModalRingedIgnore' /> },
  { value: 'R', label: <Localize field='bodyConfig.shipSwitcherModalRingedYes' /> },
  { value: 'N', label: <Localize field='bodyConfig.shipSwitcherModalRingedNo' /> }]

class BodyConfigShipSwitcherModal extends PureComponent {
  state = {
    configLine: null,
    specificationType: '',
    sortOrder: '',
    offsetStart: '',
    offset: 1,
    shipClass: '',
    levelEnabled: false,
    levelEquality: '',
    level: '',
    locked: '_',
    ringed: '_',
  }

  componentDidUpdate = (nextProp, nextState) => {
    if (this.state !== nextState) {
      this.setConfigLine()
    }
  }

  setSpecificationType = (value) => {
    // reset fields for other specification when switching specification
    this.setState({ specificationType: value })
    if (value === 'P') {
      this.setState({
        configLine: null, shipClass: '', levelEnabled: false, levelEquality: '', level: '', locked: '_', ringed: '_',
      })
    } else if (value === 'A') {
      this.setState({
        configLine: null, shipClass: '', sortOrder: false, offsetStart: '', offset: 1,
      })
    }
  }

  setConfigLine = () => {
    // generate the config-friendly ship specification line, if possible; otherwise return null
    const {
      specificationType,
      sortOrder,
      offsetStart,
      offset,
      shipClass,
      levelEnabled,
      levelEquality,
      level,
      locked,
      ringed,
    } = this.state
    let configLine = null
    let levelLine = null
    if (this.state.specificationType === 'P') {
      if (!sortOrder || !offsetStart || !offset) {
        this.setState({ configLine })
        return configLine
      }
      configLine = `${specificationType}:${sortOrder}:${offsetStart}:${offset}`
    } else if (this.state.specificationType === 'A') {
      if (levelEnabled) {
        if (!levelEquality || !level) {
          this.setState({ configLine })
          return configLine
        }
        levelLine = `${levelEquality}${level}`
      } else {
        levelLine = '_'
      }
      if (!shipClass) {
        this.setState({ configLine })
        return configLine
      }
      configLine = `${specificationType}:${shipClass}:${levelLine}:${locked}:${ringed}`
    }
    this.setState({ configLine })
    return configLine
  }

  addAction = () => {
    // fires callback method from parent form, which also closes the modal
    this.props.callback(this.props.slot, this.state.configLine)
  }

  render = () => {
    const {
      classes,
      slot,
      prevValues,
    } = this.props
    const {
      configLine,
      specificationType,
      sortOrder,
      offsetStart,
      offset,
      shipClass,
      levelEnabled,
      levelEquality,
      level,
      locked,
      ringed,
    } = this.state
    // only allow the same type of specification, if one exists already
    const SPECIFICATION = BASE_SPECIFICATION.filter(spec => spec.value.startsWith(prevValues ? prevValues[0] : ''))
    return (
      <Fragment>
        <Typography variant='title'>Specifications for Slot {slot}</Typography>

        <Divider />

        <Paper className={classes.paper} elevation={0}>
          <Grid container spacing={0}>
            <Grid item xs={12} sm={12} className={classes.formGrid}>
              <FormControl
                margin='normal'
                fullWidth
              >
                <InputLabel htmlFor='specificationType' shrink={true} className={classes.reactSelectLabel}>
                  <Localize field='bodyConfig.shipSwitcherModalSpecification' />
                </InputLabel>
                <Select
                  className={classes.reactSelect}
                  simpleValue={true}
                  clearable={false}
                  name='specificationType'
                  value={specificationType}
                  options={SPECIFICATION}
                  onChange={this.setSpecificationType}
                  fullWidth />
              </FormControl>
            </Grid>
            {specificationType === 'P' ?
              <Fragment>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl
                    margin='normal'
                    fullWidth
                  >
                    <InputLabel htmlFor='sortOrder' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.shipSwitcherModalSortBy' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      clearable={false}
                      name='sortOrder'
                      value={sortOrder}
                      options={SORT_BY}
                      onChange={value => this.setState({ sortOrder: value })}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl
                    margin='normal'
                    fullWidth
                  >
                    <InputLabel htmlFor='offsetStart' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.shipSwitcherModalOffsetStart' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      clearable={false}
                      name='offsetStart'
                      value={offsetStart}
                      options={OFFSET_START}
                      onChange={value => this.setState({ offsetStart: value })}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <TextField
                    id='offset'
                    label={<Localize field='bodyConfig.shipSwitcherModalOffsetCount' />}
                    value={offset}
                    type='number'
                    onChange={event => this.setState({ offset: event.target.value })}
                    className={classes.formControl}
                    fullWidth
                    margin='normal' />
                </Grid>
              </Fragment> :
              null
            }

            {specificationType === 'A' ?
              <Fragment>
                <Grid item xs={4} sm={4} className={classes.formGrid}>
                  <FormControl
                    margin='normal'
                    fullWidth
                  >
                    <InputLabel htmlFor='shipClass' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.shipSwitcherModalClasses' />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      simpleValue={true}
                      clearable={false}
                      name='shipClass'
                      value={shipClass}
                      options={CLASSES}
                      onChange={value => this.setState({ shipClass: value })}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid container xs={2} sm={2} justify='center' alignItems='center' className={classes.formGrid}>
                  <Typography variant='body1'>- or -</Typography>
                </Grid>
                <Grid item xs={6} sm={6} className={classes.formGrid}>
                  <FormControl
                    margin='normal'
                    fullWidth
                  >
                    <InputLabel htmlFor='shipClass' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.shipSwitcherModalShips' />
                    </InputLabel>
                    <Creatable
                      className={classes.reactSelect}
                      simpleValue={true}
                      clearable={false}
                      name='shipClass'
                      value={shipClass}
                      options={SHIPS}
                      onChange={value => this.setState({ shipClass: value })}
                      fullWidth />
                    <span className={classes.helperText}><Localize field='bodyConfig.shipSwitcherModalShipsDesc' /></span>
                  </FormControl>
                </Grid>

                <Grid item xs={4} sm={4} className={classes.formGrid}>
                  <Typography variant='body1'>
                    <Localize field='bodyConfig.shipSwitcherModalLevel' />
                    <Switch
                      className={classes.switch}
                      checked={levelEnabled}
                      onChange={(event, checked) => this.setState({ levelEnabled: checked })} />
                  </Typography>
                </Grid>
                <Grid item xs={2} sm={2} className={classes.formGrid}>
                  <Select
                    className={classes.reactSelect}
                    simpleValue={true}
                    clearable={false}
                    name='levelEquality'
                    value={levelEquality}
                    options={LEVEL_EQUALITY}
                    onChange={value => this.setState({ levelEquality: value })}
                    disabled={!levelEnabled}
                    fullWidth />
                </Grid>
                <Grid item xs={6} sm={6} className={classes.formGrid}>
                  <TextField
                    id='level'
                    value={level}
                    type='number'
                    onChange={event => this.setState({ level: event.target.value })}
                    className={classes.formControl}
                    fullWidth
                    disabled={!levelEnabled}
                    margin='normal' />
                </Grid>

                <Grid item xs={6} sm={6} className={classes.formGrid}>
                  <Select
                    className={classes.reactSelect}
                    simpleValue={true}
                    clearable={false}
                    name='locked'
                    value={locked}
                    options={LOCKED}
                    onChange={value => this.setState({ locked: value })}
                    fullWidth />
                </Grid>
                <Grid item xs={6} sm={6} className={classes.formGrid}>
                  <Select
                    className={classes.reactSelect}
                    simpleValue={true}
                    clearable={false}
                    name='ringed'
                    value={ringed}
                    options={RINGED}
                    onChange={value => this.setState({ ringed: value })}
                    fullWidth />
                </Grid>
              </Fragment> :
              null
            }
          </Grid>
        </Paper>

        <Divider />

        <Grid container spacing={0}>
          <Grid item xs={10} sm={10} className={classes.formGrid} />
          <Grid item xs={2} sm={2} className={classes.formGrid}>
            <Button
              color='primary'
              disabled={!configLine}
              onClick={this.addAction}
            >
              <PlusBox />
            </Button>
          </Grid>
        </Grid>
      </Fragment>
    )
  }
}

BodyConfigShipSwitcherModal.propTypes = {
  classes: PropTypes.object.isRequired,
  slot: PropTypes.number.isRequired,
  prevValues: PropTypes.string.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigShipSwitcherModal)
