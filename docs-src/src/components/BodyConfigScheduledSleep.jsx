import React, { Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'

import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import Switch from '@material-ui/core/Switch'
import FormControl from '@material-ui/core/FormControl'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import TextField from '@material-ui/core/TextField'
import { TimePicker } from 'material-ui-pickers'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


const BodyConfigScheduledSleep = (props) => {
  const {
    classes,
    config,
    updateSwitch,
    updateText,
    updateTime,
  } = props

  return (
    <>
      <Typography variant='h5'><Localize field='bodyConfig.scheduledSleepHeader' /></Typography>

      <Grid container spacing={0}>
        {['Script', 'Expedition', 'Combat'].map(module => (
          <Fragment key={module}>
            <Grid item xs={12} sm={4} className={classes.formGrid}>
              <FormControlLabel
                control={(
                  <Switch
                    className={classes.switch}
                    checked={props[`scheduledSleep${module}SleepEnabled`]}
                    onChange={(event, checked) => updateSwitch(
                      config, event, checked, `scheduledSleep${module}SleepEnabled`
                    )} />
                )}
                label={<Localize field={`bodyConfig.scheduledSleep${module}SleepEnabled`} />} />
            </Grid>
            <Grid item xs={12} sm={4} className={classes.formGrid}>
              <FormControl
                disabled={!props[`scheduledSleep${module}SleepEnabled`]}
                className={classes.formControl}
                fullWidth
              >
                <TimePicker
                  autoOk
                  clearable
                  id={`scheduledSleep${module}SleepStartTime`}
                  label={<Localize field={`bodyConfig.scheduledSleep${module}SleepStartTime`} />}
                  ampm={false}
                  value={props[`scheduledSleep${module}SleepStartTime`]}
                  onChange={time => updateTime(config, time, `scheduledSleep${module}SleepStartTime`)}
                  disabled={!props[`scheduledSleep${module}SleepEnabled`]} />
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4} className={classes.formGrid}>
              <TextField
                id={`scheduledSleep${module}SleepLength`}
                label={<Localize field={`bodyConfig.scheduledSleep${module}SleepLength`} />}
                value={props[`scheduledSleep${module}SleepLength`]}
                onChange={event => updateText(config, event, `scheduledSleep${module}SleepLength`)}
                type='number'
                margin='normal'
                className={classes.formControl}
                disabled={!props[`scheduledSleep${module}SleepEnabled`]}
                fullWidth />
            </Grid>
          </Fragment>
        ))}
      </Grid>
    </>
  )
}

BodyConfigScheduledSleep.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  scheduledSleepScriptSleepEnabled: PropTypes.bool.isRequired,
  scheduledSleepScriptSleepStartTime: PropTypes.object,
  scheduledSleepScriptSleepLength: PropTypes.string,
  scheduledSleepExpeditionSleepEnabled: PropTypes.bool.isRequired,
  scheduledSleepExpeditionSleepStartTime: PropTypes.object,
  scheduledSleepExpeditionSleepLength: PropTypes.string,
  scheduledSleepCombatSleepEnabled: PropTypes.bool.isRequired,
  scheduledSleepCombatSleepStartTime: PropTypes.object,
  scheduledSleepCombatSleepLength: PropTypes.string,
  updateSwitch: PropTypes.func.isRequired,
  updateText: PropTypes.func.isRequired,
  updateTime: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigScheduledSleep)
