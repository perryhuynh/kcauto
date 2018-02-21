import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Grid from 'material-ui/Grid'
import Paper from 'material-ui/Paper'
import Typography from 'material-ui/Typography'
import TextField from 'material-ui/TextField'

import Localize from 'containers/LocalizeContainer'


const styles = () => ({
  paper: {
    marginTop: 10,
    padding: 20,
  },
  paragraph: {
    marginBottom: 10,
  },
  title: {
    marginTop: 20,
  },
  formGrid: {
    padding: 8,
    paddingTop: 0,
    paddingBottom: 0,
  },
  formControl: {
    marginTop: 0,
  },
  pre: {
    padding: 20,
    fontFamily: '"Source Code Pro", monospace',
    fontSize: 12,
    overflowX: 'auto',
  },
})

class BodyRunCmd extends PureComponent {
  state = {
    sikuliPath: this.props.runCmd.sikuliPath,
    kcautoKaiPath: this.props.runCmd.kcautoKaiPath,
  }

  handleChangeSikuliPath = (event) => {
    this.setState({ sikuliPath: event.target.value })
    this.props.setSikuliPath(event.target.value)
  }

  handleChangeKCAutoKaiPath = (event) => {
    this.setState({ kcautoKaiPath: event.target.value })
    this.props.setKCAutoKaiPath(event.target.value)
  }

  render = () => {
    const {
      classes,
    } = this.props
    const {
      sikuliPath,
      kcautoKaiPath,
    } = this.state
    const sikuliPathSlash = sikuliPath && sikuliPath.indexOf('/') > -1 ? '/' : '\\'
    const kcautoKaiPathSlash = kcautoKaiPath && kcautoKaiPath.indexOf('/') > -1 ? '/' : '\\'

    return (
      <Grid container justify='center' spacing={0}>
        <Grid item xs={6}>
          <Paper className={classes.paper} elevation={0}>
            <Typography variant='body1' className={classes.paragraph}>
              <Localize field='bodyRunCmd.intro' />
            </Typography>

            <Grid container spacing={0}>
              <Grid item xs={12} className={classes.formGrid}>
                <TextField
                  id='sikuliPath'
                  label={<Localize field='bodyRunCmd.sikuliPath' />}
                  value={sikuliPath}
                  placeholder='C:\sikulix'
                  onChange={this.handleChangeSikuliPath}
                  helperText={<Localize field='bodyRunCmd.sikuliPathDesc' />}
                  className={classes.formControl}
                  fullWidth
                  margin='normal' />
              </Grid>
              <Grid item xs={12} className={classes.formGrid}>
                <TextField
                  id='kcautoKaiPath'
                  label={<Localize field='bodyRunCmd.kcautoKaiPath' />}
                  placeholder='C:\kcauto-kai'
                  value={kcautoKaiPath}
                  onChange={this.handleChangeKCAutoKaiPath}
                  helperText={<Localize field='bodyRunCmd.kcautoKaiPathDesc' />}
                  className={classes.formControl}
                  fullWidth
                  margin='normal' />
              </Grid>
            </Grid>

            <Typography variant='title' className={classes.title}>
              <Localize field='bodyRunCmd.commandHeader' />
            </Typography>
            {sikuliPath && kcautoKaiPath ?
              <Paper elevation={2}>
                <pre className={classes.pre}>
                  java -jar {sikuliPath || '<placeholder>'}{sikuliPathSlash}sikulix.jar -r&nbsp;
                  {kcautoKaiPath || '<placeholder>'}{kcautoKaiPathSlash}kcauto-kai.sikuli
                </pre>
              </Paper> :
              <Typography variant='body1' className={classes.paragraph}>
                <Localize field='bodyRunCmd.noCommandNotice' />
              </Typography>
            }
          </Paper>
        </Grid>
      </Grid>
    )
  }
}

BodyRunCmd.propTypes = {
  classes: PropTypes.object.isRequired,
  runCmd: PropTypes.object.isRequired,
  setSikuliPath: PropTypes.func.isRequired,
  setKCAutoKaiPath: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyRunCmd)
