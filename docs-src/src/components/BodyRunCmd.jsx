import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Grid from 'material-ui/Grid'
import Paper from 'material-ui/Paper'
import Typography from 'material-ui/Typography'
import TextField from 'material-ui/TextField'


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

class BodyRunCmd extends React.Component {
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
            <Typography type='body1' className={classes.paragraph}>
              Fill out the two fields below to generate the command you need to run in your command prompt/cmd/terminal
              to run kcauto-kai.
            </Typography>

            <Grid container spacing={0}>
              <Grid item xs={12} className={classes.formGrid}>
                <TextField
                  id='sikuliPath'
                  label='Sikuli Path'
                  value={sikuliPath}
                  placeholder='C:\sikulix'
                  onChange={this.handleChangeSikuliPath}
                  helperText='Full path to the folder/directory where Sikuli is installed (where sikulix.jar exists)'
                  className={classes.formControl}
                  fullWidth
                  margin='normal' />
              </Grid>
              <Grid item xs={12} className={classes.formGrid}>
                <TextField
                  id='kcautoKaiPath'
                  label='kcauto-kai Path'
                  placeholder='C:\kcauto-kai'
                  value={kcautoKaiPath}
                  onChange={this.handleChangeKCAutoKaiPath}
                  helperText='Full path to the folder/directory where kcauto-kai is installed (where config.ini exists)'
                  className={classes.formControl}
                  fullWidth
                  margin='normal' />
              </Grid>
            </Grid>

            <Typography type='title' className={classes.title}>Command</Typography>
            {sikuliPath && kcautoKaiPath ?
              <Paper elevation={2}>
                <pre className={classes.pre}>
                  java -jar {sikuliPath || '<placeholder>'}{sikuliPathSlash}sikulix.jar -r&nbsp;
                  {kcautoKaiPath || '<placeholder>'}{kcautoKaiPathSlash}kcauto-kai.sikuli
                </pre>
              </Paper> :
              <Typography type='body1' className={classes.paragraph}>
                Fill out the above two fields to generate the command.
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
  ui: PropTypes.object.isRequired,
  setSikuliPath: PropTypes.func.isRequired,
  setKCAutoKaiPath: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyRunCmd)
