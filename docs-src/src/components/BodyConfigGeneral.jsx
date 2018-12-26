import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'

import Select from 'react-select'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import TextField from '@material-ui/core/TextField'
import InputLabel from '@material-ui/core/InputLabel'
import FormControl from '@material-ui/core/FormControl'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'

import { PAUSE_OPTIONS } from 'types/formOptions'

const BodyConfigGeneral = (props) => {
  const {
    classes,
    config,
    generalProgram,
    generalJSTOffset,
    generalPause,
    updateText,
    updateSelect,
  } = props

  return (
    <>
      <Typography variant='h5'><Localize field='bodyConfig.generalHeader' /></Typography>

      <Grid container spacing={0}>
        <Grid item xs={12} sm={4} className={classes.formGrid}>
          <TextField
            id='generalProgram'
            label={<Localize field='bodyConfig.generalProgram' />}
            value={generalProgram}
            onChange={event => updateText(config, event, 'generalProgram')}
            helperText={<Localize field='bodyConfig.generalProgramDesc' />}
            className={classes.formControl}
            fullWidth
            margin='normal' />
        </Grid>
        <Grid item xs={12} sm={4} className={classes.formGrid}>
          <TextField
            id='generalJSTOffset'
            label={<Localize field='bodyConfig.generalJSTOffset' />}
            value={generalJSTOffset}
            onChange={event => updateText(config, event, 'generalJSTOffset')}
            helperText={<Localize field='bodyConfig.generalJSTOffsetDesc' />}
            className={classes.formControl}
            fullWidth
            type='number'
            margin='normal' />
        </Grid>
        <Grid item xs={12} sm={4} className={classes.formGrid}>
          <FormControl margin='normal' fullWidth>
            <InputLabel htmlFor='generalPause' shrink={true} className={classes.reactSelectLabel}>
              <Localize field='bodyConfig.generalPause' />
            </InputLabel>
            <Select
              className={classes.reactSelect}
              name='generalPause'
              value={generalPause}
              options={PAUSE_OPTIONS}
              clearable={false}
              onChange={value => updateSelect(config, value, 'generalPause')}
              fullWidth />
          </FormControl>
        </Grid>
      </Grid>
    </>
  )
}

BodyConfigGeneral.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  generalProgram: PropTypes.string.isRequired,
  generalJSTOffset: PropTypes.string.isRequired,
  generalPause: PropTypes.object.isRequired,
  updateText: PropTypes.func.isRequired,
  updateSelect: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigGeneral)
