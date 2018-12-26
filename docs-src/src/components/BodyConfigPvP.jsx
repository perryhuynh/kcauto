import React, { PureComponent } from 'react'
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

import { FLEET_PRESETS } from 'types/formOptions'


class BodyConfigPvP extends PureComponent {
  componentDidUpdate = (prevProps) => {
    const {
      config,
      combatEnabled,
      combatDisablePvP,
      combatDisablePvPFleet,
      updateObject,
    } = this.props
    if (combatEnabled && !prevProps.combatEnabled) {
      // disable PvP and/or clear PvP Fleets accordingly depending on Combat Fleet Mode - this is in case the user
      // defines a PvP-disabling fleet mode, disabled the Combat module, enables PvP and reassigns PvP fleets, then
      // re-enables the Combat module
      const updatedPvPConfig = {}
      if (combatDisablePvP) updatedPvPConfig.pvpEnabled = false
      if (combatDisablePvPFleet) updatedPvPConfig.pvpFleet = null
      if (updatedPvPConfig) updateObject(config, updatedPvPConfig)
    }
  }

  render = () => {
    const {
      classes,
      config,
      pvpEnabled,
      pvpFleet,
      combatEnabled,
      combatDisablePvP,
      combatDisablePvPFleet,
      updateSwitch,
      updateSelect,
    } = this.props
    return (
      <>
        <Typography variant='h5'>
          <Localize field='bodyConfig.pvpHeader' />
          <Switch
            className={classes.switch}
            checked={pvpEnabled}
            onChange={(event, checked) => updateSwitch(config, event, checked, 'pvpEnabled')}
            disabled={combatEnabled && combatDisablePvP} />
        </Typography>

        <Grid container spacing={0}>
          <Grid item xs={12} sm={12} className={classes.formGrid}>
            <FormControl
              disabled={!pvpEnabled || (combatEnabled && combatDisablePvPFleet)}
              margin='normal'
              fullWidth
            >
              <InputLabel htmlFor='pvpFleet' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.pvpFleet' />
              </InputLabel>
              <Select
                isClearable
                className={classes.reactSelect}
                name='pvpFleet'
                value={pvpFleet}
                options={FLEET_PRESETS}
                onChange={value => updateSelect(config, value, 'pvpFleet')}
                isDisabled={!pvpEnabled || (combatEnabled && combatDisablePvPFleet)} />
              <span className={classes.helperText}><Localize field='bodyConfig.pvpFleetDesc' /></span>
            </FormControl>
          </Grid>
        </Grid>
      </>
    )
  }
}

BodyConfigPvP.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  pvpEnabled: PropTypes.bool.isRequired,
  pvpFleet: PropTypes.object,
  combatEnabled: PropTypes.bool.isRequired,
  combatDisablePvP: PropTypes.bool,
  combatDisablePvPFleet: PropTypes.bool,
  updateSwitch: PropTypes.func.isRequired,
  updateSelect: PropTypes.func.isRequired,
  updateObject: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigPvP)
