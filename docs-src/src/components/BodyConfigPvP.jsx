import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Select from 'react-select'
import Grid from 'material-ui/Grid'
import Typography from 'material-ui/Typography'
import Switch from 'material-ui/Switch'
import { InputLabel } from 'material-ui/Input'
import { FormControl } from 'material-ui/Form'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


const FLEET_PRESETS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'].map(value => (
  { value, label: value }))

class BodyConfigPvP extends PureComponent {
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
    const {
      pvpEnabled,
      pvpFleet,
    } = this.state
    return (
      <Fragment>
        <Typography variant='display1'>
          <Localize field='bodyConfig.pvpHeader' />
          <Switch
            className={classes.switch}
            checked={pvpEnabled}
            onChange={
              (event, checked) => this.setState({ pvpEnabled: checked }, () => this.props.callback(this.state))} />
        </Typography>

        <Grid container spacing={0}>
          <Grid item xs={12} sm={12} className={classes.formGrid}>
            <FormControl
              disabled={!pvpEnabled}
              margin='normal'
              fullWidth
            >
              <InputLabel htmlFor='pvpFleet' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.pvpFleet' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                simpleValue={true}
                name='pvpFleet'
                value={pvpFleet}
                options={FLEET_PRESETS}
                onChange={value => this.setState({ pvpFleet: value }, () => this.props.callback(this.state))}
                disabled={
                  !pvpEnabled}
                fullWidth />
              <span className={classes.helperText}><Localize field='bodyConfig.pvpFleetDesc' /></span>
            </FormControl>
          </Grid>
        </Grid>
      </Fragment>
    )
  }
}

BodyConfigPvP.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigPvP)
