import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'

import Select from 'react-select'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import Switch from '@material-ui/core/Switch'
import InputLabel from '@material-ui/core/InputLabel'
import FormControl from '@material-ui/core/FormControl'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'

import { FREQUENCIES, DIFFICULTIES } from 'types/formOptions'

const BodyConfigEventReset = (props) => {
  const {
    classes,
    config,
    eventResetEnabled,
    eventResetFrequency,
    eventResetFarmDifficulty,
    eventResetResetDifficulty,
    combatEnabled,
    combatMap,
    updateSwitch,
    updateSelect,
  } = props

  return (
    <>
      <Typography variant='h5'>
        <Localize field='bodyConfig.eventResetHeader' />
        <Switch
          className={classes.switch}
          checked={eventResetEnabled}
          disabled={!combatEnabled || !(combatEnabled && combatMap.value[0] === 'E')}
          onChange={(event, checked) => updateSwitch(
            config, event, checked, 'eventResetEnabled'
          )} />
      </Typography>

      <Grid container spacing={0}>
        <Grid item xs={12} sm={4} className={classes.formGrid}>
          <FormControl disabled={!eventResetEnabled} margin='normal' fullWidth>
            <InputLabel htmlFor='eventResetFrequency' shrink={true} className={classes.reactSelectLabel}>
              <Localize field='bodyConfig.eventResetFrequency' />
            </InputLabel>
            <Select
              className={classes.reactSelect}
              name='eventResetFrequency'
              value={eventResetFrequency}
              options={FREQUENCIES}
              clearable={false}
              onChange={value => updateSelect(config, value, 'eventResetFrequency')}
              isDisabled={!eventResetEnabled}
              fullWidth />
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={4} className={classes.formGrid}>
          <FormControl disabled={!eventResetEnabled} margin='normal' fullWidth>
            <InputLabel htmlFor='eventResetFarmDifficulty' shrink={true} className={classes.reactSelectLabel}>
              <Localize field='bodyConfig.eventResetFarmDifficulty' />
            </InputLabel>
            <Select
              className={classes.reactSelect}
              name='eventResetFarmDifficulty'
              value={eventResetFarmDifficulty}
              options={DIFFICULTIES}
              clearable={false}
              onChange={value => updateSelect(config, value, 'eventResetFarmDifficulty')}
              isDisabled={!eventResetEnabled}
              fullWidth />
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={4} className={classes.formGrid}>
          <FormControl disabled={!eventResetEnabled} margin='normal' fullWidth>
            <InputLabel htmlFor='eventResetResetDifficulty' shrink={true} className={classes.reactSelectLabel}>
              <Localize field='bodyConfig.eventResetResetDifficulty' />
            </InputLabel>
            <Select
              className={classes.reactSelect}
              name='eventResetResetDifficulty'
              value={eventResetResetDifficulty}
              options={DIFFICULTIES}
              clearable={false}
              onChange={value => updateSelect(config, value, 'eventResetResetDifficulty')}
              isDisabled={!eventResetEnabled}
              fullWidth />
          </FormControl>
        </Grid>
      </Grid>
    </>
  )
}

BodyConfigEventReset.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  eventResetEnabled: PropTypes.bool.isRequired,
  eventResetFrequency: PropTypes.object.isRequired,
  eventResetFarmDifficulty: PropTypes.object.isRequired,
  eventResetResetDifficulty: PropTypes.object.isRequired,
  combatEnabled: PropTypes.bool.isRequired,
  combatMap: PropTypes.object.isRequired,
  updateSwitch: PropTypes.func.isRequired,
  updateSelect: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigEventReset)
