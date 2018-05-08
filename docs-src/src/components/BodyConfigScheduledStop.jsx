import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Select from 'react-select'
import Grid from 'material-ui/Grid'
import Typography from 'material-ui/Typography'
import Switch from 'material-ui/Switch'
import { InputLabel } from 'material-ui/Input'
import { FormControl, FormControlLabel } from 'material-ui/Form'
import TextField from 'material-ui/TextField'
import TimeInput from 'material-ui-time-picker'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


const STOP_MODE_OPTIONS = [
  { value: 'module', label: <Localize field='bodyConfig.scheduledStopStopModeModule' /> },
  { value: 'script', label: <Localize field='bodyConfig.scheduledStopStopModeScript' /> },
]

class BodyConfigScheduledStop extends PureComponent {
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
        <Typography variant='display1'><Localize field='bodyConfig.scheduledStopHeader' /></Typography>

        <Grid container spacing={0}>
          {['Script', 'Expedition', 'Combat'].map(module => (
            <Fragment key={module}>
              <Grid item xs={12} sm={3} className={classes.formGrid}>
                <FormControlLabel
                  control={
                    <Switch
                      className={classes.switch}
                      checked={this.state[`scheduledStop${module}StopEnabled`]}
                      onChange={
                        (event, checked) => this.setState(
                          { [`scheduledStop${module}StopEnabled`]: checked },
                          () => this.props.callback(this.state)
                        )} />
                  }
                  label={<Localize field={`bodyConfig.scheduledStop${module}StopEnabled`} />} />
              </Grid>
              <Grid item xs={12} sm={3} className={classes.formGrid}>
                { module !== 'Script' ?
                  <FormControl
                    disabled={!this.state[`scheduledStop${module}StopEnabled`]}
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
                      simpleValue={true}
                      name={`scheduledStop${module}StopMode`}
                      value={this.state[`scheduledStop${module}StopMode`]}
                      options={STOP_MODE_OPTIONS}
                      clearable={false}
                      onChange={
                        value => this.setState(
                          { [`scheduledStop${module}StopMode`]: value },
                          () => this.props.callback(this.state)
                        )}
                      disabled={!this.state[`scheduledStop${module}StopEnabled`]}
                      fullWidth />
                  </FormControl> :
                  null }
              </Grid>
              <Grid item xs={12} sm={3} className={classes.formGrid}>
                <TextField
                  id={`scheduledStop${module}StopCount`}
                  label={<Localize field={`bodyConfig.scheduledStop${module}StopCount`} />}
                  value={this.state[`scheduledStop${module}StopCount`]}
                  onChange={
                    event => this.setState(
                      { [`scheduledStop${module}StopCount`]: event.target.value },
                      () => this.props.callback(this.state)
                    )}
                  type='number'
                  margin='normal'
                  className={classes.formControl}
                  disabled={!this.state[`scheduledStop${module}StopEnabled`]}
                  fullWidth />
              </Grid>
              <Grid item xs={12} sm={3} className={classes.formGrid}>
                <FormControl
                  disabled={!this.state[`scheduledStop${module}StopEnabled`]}
                  fullWidth
                >
                  <InputLabel htmlFor={`scheduledStop${module}StopTime`}>
                    <Localize field={`bodyConfig.scheduledStop${module}StopTime`} />
                  </InputLabel>
                  <TimeInput
                    id={`scheduledStop${module}StopTime`}
                    mode='24h'
                    autoOk={true}
                    value={this.state[`scheduledStop${module}StopTime`]}
                    onChange={
                      time => this.setState(
                        { [`scheduledStop${module}StopTime`]: time },
                        () => this.props.callback(this.state)
                      )}
                    fullWidth />
                </FormControl>
              </Grid>
            </Fragment>
          ))}
        </Grid>
      </Fragment>
    )
  }
}

BodyConfigScheduledStop.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigScheduledStop)
