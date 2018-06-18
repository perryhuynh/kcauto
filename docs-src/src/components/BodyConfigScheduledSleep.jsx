import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Grid from 'material-ui/Grid'
import Typography from 'material-ui/Typography'
import Switch from 'material-ui/Switch'
import { InputLabel } from 'material-ui/Input'
import { FormControl, FormControlLabel } from 'material-ui/Form'
import TextField from 'material-ui/TextField'
import TimeInput from 'material-ui-time-picker'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


class BodyConfigScheduledSleep extends PureComponent {
  state = this.props.config

  componentWillReceiveProps = (nextProps) => {
    if (this.props.config !== nextProps.config) {
      this.setState(nextProps.config)
    }
  }

  render = () => {
    const {
      classes,
    } = this.props
    return (
      <Fragment>
        <Typography variant='display1'><Localize field='bodyConfig.scheduledSleepHeader' /></Typography>

        <Grid container spacing={0}>
          {['Script', 'Expedition', 'Combat'].map(module => (
            <Fragment key={module}>
              <Grid item xs={12} sm={4} className={classes.formGrid}>
                <FormControlLabel
                  control={
                    <Switch
                      className={classes.switch}
                      checked={this.state[`scheduledSleep${module}SleepEnabled`]}
                      onChange={
                        (event, checked) => this.setState(
                          { [`scheduledSleep${module}SleepEnabled`]: checked },
                          () => this.props.callback(this.state)
                        )} />
                  }
                  label={<Localize field={`bodyConfig.scheduledSleep${module}SleepEnabled`} />} />
              </Grid>
              <Grid item xs={12} sm={4} className={classes.formGrid}>
                <FormControl
                  disabled={!this.state[`scheduledSleep${module}SleepEnabled`]}
                  className={classes.formControl}
                  fullWidth
                >
                  <InputLabel htmlFor={`scheduledSleep${module}SleepStartTime`}>
                    <Localize field={`bodyConfig.scheduledSleep${module}SleepStartTime`} />
                  </InputLabel>
                  <TimeInput
                    id={`scheduledSleep${module}SleepStartTime`}
                    mode='24h'
                    autoOk={true}
                    value={this.state[`scheduledSleep${module}SleepStartTime`]}
                    onChange={
                      time => this.setState(
                        { [`scheduledSleep${module}SleepStartTime`]: time },
                        () => this.props.callback(this.state)
                      )}
                    fullWidth />
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={4} className={classes.formGrid}>
                <TextField
                  id={`scheduledSleep${module}SleepLength`}
                  label={<Localize field={`bodyConfig.scheduledSleep${module}SleepLength`} />}
                  value={this.state[`scheduledSleep${module}SleepLength`]}
                  onChange={
                    event => this.setState(
                      { [`scheduledSleep${module}SleepLength`]: event.target.value },
                      () => this.props.callback(this.state)
                    )}
                  type='number'
                  margin='normal'
                  className={classes.formControl}
                  disabled={!this.state[`scheduledSleep${module}SleepEnabled`]}
                  fullWidth />
              </Grid>
            </Fragment>
          ))}
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
