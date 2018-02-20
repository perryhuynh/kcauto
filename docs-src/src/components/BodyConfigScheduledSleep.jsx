import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Grid from 'material-ui/Grid'
import Typography from 'material-ui/Typography'
import Switch from 'material-ui/Switch'
import { InputLabel } from 'material-ui/Input'
import { FormControl } from 'material-ui/Form'
import TextField from 'material-ui/TextField'
import TimeInput from 'material-ui-time-picker'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


class BodyConfigScheduledSleep extends PureComponent {
  state = this.props.config

  componentDidUpdate = (nextProp, nextState) => {
    if (this.state !== nextState) {
      this.props.callback(this.state)
    }
  }

  render = () => {
    const {
      classes,
    } = this.props
    const {
      scheduledSleepEnabled,
      scheduledSleepStartTime,
      scheduledSleepSleepLength,
    } = this.state
    return (
      <Fragment>
        <Typography variant='display1'>
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
      </Fragment>
    )
  }
}

BodyConfigScheduledSleep.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigScheduledSleep)
