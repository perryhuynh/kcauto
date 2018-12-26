import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'

import Select from 'react-select'
import CreatableSelect from 'react-select/lib/Creatable'
import Grid from '@material-ui/core/Grid'
import Paper from '@material-ui/core/Paper'
import Typography from '@material-ui/core/Typography'
import Switch from '@material-ui/core/Switch'
import TextField from '@material-ui/core/TextField'
import Button from '@material-ui/core/Button'
import Divider from '@material-ui/core/Divider'
import InputLabel from '@material-ui/core/InputLabel'
import FormControl from '@material-ui/core/FormControl'
import { PlusBox } from 'mdi-material-ui'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'
import {
  BASE_SPECIFICATION, SORT_BY, OFFSET_START, ASSETS, LEVEL_EQUALITY, LOCKED, RINGED,
} from 'types/formOptions'


class BodyConfigShipSwitcherModal extends PureComponent {
  state = {
    configLine: null,
    specificationType: '',
    sortOrder: '',
    offsetStart: '',
    offset: 1,
    shipClass: '',
    levelEnabled: false,
    levelEquality: LEVEL_EQUALITY.filter(opt => opt.value === '<')[0],
    level: '',
    locked: LOCKED.filter(opt => opt.value === '_')[0],
    ringed: RINGED.filter(opt => opt.value === '_')[0],
  }

  componentDidUpdate = (nextProp, nextState) => {
    if (this.state !== nextState) {
      this.setConfigLine()
    }
  }

  setSpecificationType = (value) => {
    // reset fields for other specification when switching specification
    this.setState({ specificationType: value })
    if (value.value === 'P') {
      this.setState({
        configLine: null,
        shipClass: '',
        levelEnabled: false,
        levelEquality: LEVEL_EQUALITY.filter(opt => opt.value === '<')[0],
        level: '',
        locked: LOCKED.filter(opt => opt.value === '_')[0],
        ringed: RINGED.filter(opt => opt.value === '_')[0],
      })
    } else if (value.value === 'A') {
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
    if (specificationType.value === 'P') {
      if (!sortOrder || !offsetStart || !offset) {
        this.setState({ configLine })
        return configLine
      }
      configLine = `${specificationType.value}:${sortOrder.value}:${offsetStart.value}:${offset}`
    } else if (specificationType.value === 'A') {
      if (levelEnabled) {
        if (!levelEquality || !level) {
          this.setState({ configLine })
          return configLine
        }
        levelLine = `${levelEquality.value}${level}`
      } else {
        levelLine = '_'
      }
      if (!shipClass) {
        this.setState({ configLine })
        return configLine
      }
      configLine = `${specificationType.value}:${shipClass.value}:${levelLine}:${locked.value}:${ringed.value}`
    }
    this.setState({ configLine })
    return configLine
  }

  addAction = () => {
    // fires callback method from parent form, which also closes the modal
    const {
      slot,
      callback,
    } = this.props
    const { configLine } = this.state
    callback(slot, configLine)
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
    const SPECIFICATION = BASE_SPECIFICATION.filter(
      spec => spec.value.startsWith(prevValues.length > 0 ? prevValues[0].value[0] : '')
    )
    return (
      <>
        <Typography variant='h6'>Specifications for Slot {slot}</Typography>

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
                  name='specificationType'
                  value={specificationType}
                  options={SPECIFICATION}
                  onChange={this.setSpecificationType}
                  fullWidth />
              </FormControl>
            </Grid>
            {specificationType.value === 'P'
              ? <>
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
              </>
              : null
            }

            {specificationType.value === 'A'
              ? <>
                <Grid item xs={12} sm={12} className={classes.formGrid}>
                  <FormControl
                    margin='normal'
                    fullWidth
                  >
                    <InputLabel htmlFor='shipClass' shrink={true} className={classes.reactSelectLabel}>
                      <Localize field='bodyConfig.shipSwitcherModalAssets' />
                    </InputLabel>
                    <CreatableSelect
                      className={classes.reactSelect}
                      name='shipClass'
                      value={shipClass}
                      options={ASSETS}
                      onChange={value => this.setState({ shipClass: value })}
                      isClearable
                      fullWidth />
                    <span className={classes.helperText}>
                      <Localize field='bodyConfig.shipSwitcherModalAssetsDesc' />
                    </span>
                  </FormControl>
                </Grid>

                <Grid item xs={4} sm={4} className={classes.formGrid}>
                  <Typography variant='body2'>
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
                    name='levelEquality'
                    value={levelEquality}
                    options={LEVEL_EQUALITY}
                    onChange={value => this.setState({ levelEquality: value })}
                    isDisabled={!levelEnabled}
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
                    clearable={false}
                    name='ringed'
                    value={ringed}
                    options={RINGED}
                    onChange={value => this.setState({ ringed: value })}
                    fullWidth />
                </Grid>
              </>
              : null
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
      </>
    )
  }
}

BodyConfigShipSwitcherModal.propTypes = {
  classes: PropTypes.object.isRequired,
  slot: PropTypes.number.isRequired,
  prevValues: PropTypes.array.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigShipSwitcherModal)
