import React from 'react'
import { withStyles } from 'material-ui/styles'
import PropTypes from 'prop-types'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import Typography from 'material-ui/Typography'
import IconButton from 'material-ui/IconButton'
import { Ferry, GithubCircle, Discord } from 'mdi-material-ui'

import * as urls from 'urls'

const styles = () => ({
  root: {
    width: '100%',
  },
  flex: {
    flex: 1,
  },
  largeIcon: {
    width: 30,
    height: 30,
  },
})

const Menu = (props) => {
  const { classes } = props
  return (
    <div className={classes.root}>
      <AppBar position='static'>
        <Toolbar>
          <Typography type='title' color='inherit' className={classes.flex}>
            <Ferry /> kcauto-kai
          </Typography>
          <a href={urls.DISCORD_LINK}>
            <IconButton color='contrast'><Discord className={classes.largeIcon} /></IconButton>
          </a>
          <a href={urls.GITHUB_LINK}>
            <IconButton color='contrast'><GithubCircle className={classes.largeIcon} /></IconButton>
          </a>
        </Toolbar>
      </AppBar>
    </div>
  )
}

Menu.propTypes = {
  classes: PropTypes.object.isRequired,
}

export default withStyles(styles)(Menu)
