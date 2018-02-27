import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Select from 'react-select'
import Grid from 'material-ui/Grid'
import Typography from 'material-ui/Typography'
import TextField from 'material-ui/TextField'
import { InputLabel } from 'material-ui/Input'
import { FormControl } from 'material-ui/Form'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


const PAUSE_OPTIONS = [
  { value: true, label: <Localize field='bodyConfig.generalPauseTrue' /> },
  { value: false, label: <Localize field='bodyConfig.generalPauseFalse' /> },
]

class BodyConfigGeneral extends PureComponent {
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
      generalProgram,
      generalJSTOffset,
      generalPause,
    } = this.state
    return (
      <Fragment>
        <Typography variant='display1'><Localize field='bodyConfig.generalHeader' /></Typography>

        <Grid container spacing={0}>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <TextField
              id='generalProgram'
              label={<Localize field='bodyConfig.generalProgram' />}
              value={generalProgram}
              onChange={
                event => this.setState({ generalProgram: event.target.value }, () => this.props.callback(this.state))}
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
              onChange={
                event => this.setState({ generalJSTOffset: event.target.value }, () => this.props.callback(this.state))}
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
                simpleValue={true}
                name='generalPause'
                value={generalPause}
                options={PAUSE_OPTIONS}
                clearable={false}
                onChange={
                  value => this.setState({ generalPause: value }, () => this.props.callback(this.state))}
                fullWidth />
            </FormControl>
          </Grid>
        </Grid>
      </Fragment>
    )
  }
}

BodyConfigGeneral.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigGeneral)
