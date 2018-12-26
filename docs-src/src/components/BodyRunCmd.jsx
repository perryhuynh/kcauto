import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'

import Grid from '@material-ui/core/Grid'
import Paper from '@material-ui/core/Paper'
import Typography from '@material-ui/core/Typography'
import TextField from '@material-ui/core/TextField'

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
  handleChangeSikuliPath = (event) => {
    const { setSikuliPath } = this.props
    setSikuliPath(event.target.value)
  }

  handleChangeKCAutoKaiPath = (event) => {
    const { setKCAutoPath } = this.props
    setKCAutoPath(event.target.value)
  }

  render = () => {
    const {
      classes,
      sikuliPath,
      kcautoPath,
    } = this.props
    const sikuliPathSlash = sikuliPath && sikuliPath.indexOf('/') > -1 ? '/' : '\\'
    const kcautoPathSlash = kcautoPath && kcautoPath.indexOf('/') > -1 ? '/' : '\\'

    return (
      <Grid container justify='center' spacing={0}>
        <Grid item xs={6}>
          <Paper className={classes.paper} elevation={0}>
            <Typography variant='body2' className={classes.paragraph}>
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
                  id='kcautoPath'
                  label={<Localize field='bodyRunCmd.kcautoPath' />}
                  placeholder='C:\kcauto'
                  value={kcautoPath}
                  onChange={this.handleChangeKCAutoKaiPath}
                  helperText={<Localize field='bodyRunCmd.kcautoPathDesc' />}
                  className={classes.formControl}
                  fullWidth
                  margin='normal' />
              </Grid>
            </Grid>

            <Typography variant='h6' className={classes.title}>
              <Localize field='bodyRunCmd.commandHeader' />
            </Typography>
            {sikuliPath && kcautoPath ? (
              <Paper elevation={2}>
                <pre className={classes.pre}>
                  java -jar {sikuliPath || '<placeholder>'}{sikuliPathSlash}sikulix.jar -r&nbsp;
                  {kcautoPath || '<placeholder>'}{kcautoPathSlash}kcauto.sikuli
                </pre>
              </Paper>)
              : (
                <Typography variant='body2' className={classes.paragraph}>
                  <Localize field='bodyRunCmd.noCommandNotice' />
                </Typography>)
            }
          </Paper>
        </Grid>
      </Grid>
    )
  }
}

BodyRunCmd.propTypes = {
  classes: PropTypes.object.isRequired,
  sikuliPath: PropTypes.string,
  kcautoPath: PropTypes.string,
  setSikuliPath: PropTypes.func.isRequired,
  setKCAutoPath: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyRunCmd)
