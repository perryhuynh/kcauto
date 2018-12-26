import React, { Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'

import Select from 'react-select'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import Switch from '@material-ui/core/Switch'
import InputLabel from '@material-ui/core/InputLabel'
import FormControl from '@material-ui/core/FormControl'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import TextField from '@material-ui/core/TextField'
import { TimePicker } from 'material-ui-pickers'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'

import { STOP_MODE_OPTIONS } from 'types/formOptions'

const BodyConfigScheduledStop = (props) => {
  const {
    classes,
    config,
    updateSwitch,
    updateText,
    updateSelect,
    updateTime,
  } = props

  return (
    <>
      <Typography variant='h5'><Localize field='bodyConfig.scheduledStopHeader' /></Typography>

      <Grid container spacing={0}>
        {['Script', 'Expedition', 'Combat'].map(module => (
          <Fragment key={module}>
            <Grid item xs={12} sm={3} className={classes.formGrid}>
              <FormControlLabel
                control={(
                  <Switch
                    className={classes.switch}
                    checked={props[`scheduledStop${module}StopEnabled`]}
                    onChange={(event, checked) => updateSwitch(
                      config, event, checked, `scheduledStop${module}StopEnabled`
                    )} />
                )}
                label={<Localize field={`bodyConfig.scheduledStop${module}StopEnabled`} />} />
            </Grid>
            <Grid item xs={12} sm={3} className={classes.formGrid}>
              { module !== 'Script'
                ? (
                  <FormControl
                    disabled={!props[`scheduledStop${module}StopEnabled`]}
                    margin='normal'
                    fullWidth
                  >
                    <InputLabel
                      htmlFor={`scheduledStop${module}StopMode`}
                      shrink={true}
                      className={classes.reactSelectLabel}
                    >
                      <Localize field={`bodyConfig.scheduledStop${module}StopMode`} />
                    </InputLabel>
                    <Select
                      className={classes.reactSelect}
                      name={`scheduledStop${module}StopMode`}
                      value={props[`scheduledStop${module}StopMode`]}
                      options={STOP_MODE_OPTIONS}
                      clearable={false}
                      onChange={value => updateSelect(config, value, `scheduledStop${module}StopMode`)}
                      isDisabled={!props[`scheduledStop${module}StopEnabled`]}
                      fullWidth />
                  </FormControl>)
                : null }
            </Grid>
            <Grid item xs={12} sm={3} className={classes.formGrid}>
              <FormControl>
                <TextField
                  id={`scheduledStop${module}StopCount`}
                  label={<Localize field={`bodyConfig.scheduledStop${module}StopCount`} />}
                  value={props[`scheduledStop${module}StopCount`]}
                  onChange={event => updateText(config, event, `scheduledStop${module}StopCount`)}
                  type='number'
                  margin='normal'
                  className={classes.formControl}
                  disabled={!props[`scheduledStop${module}StopEnabled`]}
                  fullWidth />
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={3} className={classes.formGrid}>
              <FormControl
                disabled={!props[`scheduledStop${module}StopEnabled`]}
                fullWidth
              >
                <TimePicker
                  autoOk
                  clearable
                  id={`scheduledStop${module}StopTime`}
                  label={<Localize field={`bodyConfig.scheduledStop${module}StopTime`} />}
                  ampm={false}
                  value={props[`scheduledStop${module}StopTime`]}
                  onChange={time => updateTime(config, time, `scheduledStop${module}StopTime`)}
                  disabled={!props[`scheduledStop${module}StopEnabled`]} />
              </FormControl>
            </Grid>
          </Fragment>
        ))}
      </Grid>
    </>
  )
}

BodyConfigScheduledStop.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  scheduledStopScriptStopEnabled: PropTypes.bool.isRequired,
  scheduledStopScriptStopCount: PropTypes.string,
  scheduledStopScriptStopTime: PropTypes.object,
  scheduledStopExpeditionStopEnabled: PropTypes.bool.isRequired,
  scheduledStopExpeditionStopMode: PropTypes.object.isRequired,
  scheduledStopExpeditionStopCount: PropTypes.string,
  scheduledStopExpeditionStopTime: PropTypes.object,
  scheduledStopCombatStopEnabled: PropTypes.bool.isRequired,
  scheduledStopCombatStopMode: PropTypes.object.isRequired,
  scheduledStopCombatStopCount: PropTypes.string,
  scheduledStopCombatStopTime: PropTypes.object,
  updateSwitch: PropTypes.func.isRequired,
  updateText: PropTypes.func.isRequired,
  updateSelect: PropTypes.func.isRequired,
  updateTime: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigScheduledStop)
