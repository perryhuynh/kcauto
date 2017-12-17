import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Grid from 'material-ui/Grid'
import Paper from 'material-ui/Paper'
import Typography from 'material-ui/Typography'

import * as urls from 'urls'


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
          <strong>kcauto-kai</strong> is a robust Kantai Collection automation tool. The successor
          to <a href='https://github.com/mrmin123/kancolle-auto'>kancolle-auto</a>, both it and kcauto-kai are
          proof-of-concepts in using Sikuli for vision-based scripting to automate the playing of Kantai Collection
          and are exercises in automating large, convoluted, and complex game logic. It is not designed to be the
          fastest automation tool, but instead designed to be robust and highly
          customizable. <strong>Please read the Disclaimer section before use!</strong>
        </Typography>

        <Typography type='body1' className={classes.paragraph}>
          Visit the <a href={urls.GITHUB_LINK}>kcauto-kai GitHub repository</a> for the latest releases and to
          report any bugs. Join the <a href={urls.DISCORD_LINK}>kcauto-kai Discord</a> for up to date information
          and help.
        </Typography>

        <Typography type='title'>
          Disclaimer
        </Typography>

        <Typography type='body2' className={classes.paragraph}>
          kcauto-kai is meant for educational purposes only! Actual and prolonged usage of kcauto-kai may result
          in your account being banned. Remember that botting is against rules! The author of kcauto-kai makes no
          guarantee that the end user will not be caught and penalized for using kcauto-kai, and will not take any
          responsibility for any repercussions that befall the end user. Spamming expeditions and sorties nonstop
          raises your chances of being flagged and banned.
        </Typography>

        <Typography type='body2' className={classes.paragraph}>
          In addition, although unlikely, you may lose ships if you allow kcauto-kai to conduct combat sorties.
          While kcauto-kai has been painstakingly designed to reduce the chances of this happening, the author of
          kcauto-kai takes no responsibility regarding the preservation of your ships.
        </Typography>
      </Paper>
    </Grid>
  </Grid>
)

BodyAbout.propTypes = {
  classes: PropTypes.object.isRequired,
  ui: PropTypes.object.isRequired,
}

export default withStyles(styles)(BodyAbout)
