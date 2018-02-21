import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Grid from 'material-ui/Grid'
import Typography from 'material-ui/Typography'
import TextField from 'material-ui/TextField'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


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
    } = this.state
    return (
      <Fragment>
        <Typography variant='display1'><Localize field='bodyConfig.generalHeader' /></Typography>

        <Grid container spacing={0}>
          <Grid item xs={12} sm={8} className={classes.formGrid}>
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
