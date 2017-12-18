import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Grid from 'material-ui/Grid'
import Paper from 'material-ui/Paper'
import Typography from 'material-ui/Typography'

import Localize from 'containers/LocalizeContainer'


const styles = () => ({
  paper: {
    marginTop: 10,
    padding: 20,
  },
  paragraph: {
    marginBottom: 15,
  },
})

const BodyAbout = ({ classes }) => (
  <Grid container justify='center' spacing={0}>
    <Grid item xs={6}>
      <Paper className={classes.paper} elevation={0}>
        <Typography type='body1' className={classes.paragraph}>
          <Localize field='bodyAbout.intro1' />
        </Typography>

        <Typography type='body1' className={classes.paragraph}>
          <Localize field='bodyAbout.intro2' />
        </Typography>

        <Typography type='title'>
          <Localize field='bodyAbout.disclaimerHeader' />
        </Typography>

        <Typography type='body2' className={classes.paragraph}>
          <Localize field='bodyAbout.disclaimer1' />
        </Typography>

        <Typography type='body2' className={classes.paragraph}>
          <Localize field='bodyAbout.disclaimer2' />
        </Typography>
      </Paper>
    </Grid>
  </Grid>
)

BodyAbout.propTypes = {
  classes: PropTypes.object.isRequired,
}

export default withStyles(styles)(BodyAbout)
