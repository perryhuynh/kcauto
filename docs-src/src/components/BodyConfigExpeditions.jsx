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

import { EXPEDITIONS } from 'types/formOptions'

const BodyConfigExpeditions = (props) => {
  const {
    classes,
    config,
    expeditionsEnabled,
    expeditionsFleet2,
    expeditionsFleet3,
    expeditionsFleet4,
    combatEnabled,
    combatDisableExpeditionsFleet2,
    combatDisableExpeditionsFleet3,
    combatDisableExpeditionsFleet4,
    updateSwitch,
    updateSelect,
  } = props

  return (
    <>
      <Typography variant='h5'>
        <Localize field='bodyConfig.expeditionsHeader' />
        <Switch
          className={classes.switch}
          checked={expeditionsEnabled}
          onChange={(event, checked) => updateSwitch(config, event, checked, 'expeditionsEnabled')} />
      </Typography>

      <Grid container spacing={0}>
        <Grid item xs={12} sm={4} className={classes.formGrid}>
          <FormControl
            disabled={!expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet2)}
            margin='normal'
            fullWidth
          >
            <InputLabel htmlFor='expeditionsFleet2' shrink={true} className={classes.reactSelectLabel}>
              <Localize field='bodyConfig.expeditionsFleet2' />
            </InputLabel>
            <Select
              className={classes.reactSelect}
              name='expeditionsFleet2'
              value={expeditionsFleet2}
              options={EXPEDITIONS}
              onChange={value => updateSelect(config, value, 'expeditionsFleet2')}
              isDisabled={!expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet2)}
              isClearable
              isMulti />
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={4} className={classes.formGrid}>
          <FormControl
            disabled={!expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet3)}
            margin='normal'
            fullWidth
          >
            <InputLabel htmlFor='expeditionsFleet3' shrink={true} className={classes.reactSelectLabel}>
              <Localize field='bodyConfig.expeditionsFleet3' />
            </InputLabel>
            <Select
              className={classes.reactSelect}
              name='expeditionsFleet3'
              value={expeditionsFleet3}
              options={EXPEDITIONS}
              onChange={value => updateSelect(config, value, 'expeditionsFleet3')}
              isDisabled={!expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet3)}
              isClearable
              isMulti />
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={4} className={classes.formGrid}>
          <FormControl
            disabled={!expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet4)}
            margin='normal'
            fullWidth
          >
            <InputLabel htmlFor='expeditionsFleet4' shrink={true} className={classes.reactSelectLabel}>
              <Localize field='bodyConfig.expeditionsFleet4' />
            </InputLabel>
            <Select
              className={classes.reactSelect}
              name='expeditionsFleet4'
              value={expeditionsFleet4}
              options={EXPEDITIONS}
              onChange={value => updateSelect(config, value, 'expeditionsFleet4')}
              isDisabled={!expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet4)}
              isClearable
              isMulti />
          </FormControl>
        </Grid>
      </Grid>
    </>
  )
}

BodyConfigExpeditions.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  expeditionsEnabled: PropTypes.bool.isRequired,
  expeditionsFleet2: PropTypes.array,
  expeditionsFleet3: PropTypes.array,
  expeditionsFleet4: PropTypes.array,
  combatEnabled: PropTypes.bool.isRequired,
  combatDisableExpeditionsFleet2: PropTypes.bool,
  combatDisableExpeditionsFleet3: PropTypes.bool,
  combatDisableExpeditionsFleet4: PropTypes.bool,
  updateSwitch: PropTypes.func.isRequired,
  updateSelect: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigExpeditions)
