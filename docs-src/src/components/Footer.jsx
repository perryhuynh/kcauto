import React from 'react'
import { withStyles } from 'material-ui/styles'
import PropTypes from 'prop-types'
import Divider from 'material-ui/Divider'
import blueGrey from 'material-ui/colors/blueGrey'
import { WalletGiftcard } from 'mdi-material-ui'
import * as urls from 'urls'

const styles = () => ({
  root: {
    marginTop: 20,
    width: '100%',
  },
  divider: {
    display: 'inline-block',
    padding: '0 5 0 5',
  },
  link: {
    color: blueGrey[500],
    fontSize: 14,
    textDecoration: 'none',
  },
  icon: {
    width: 22,
    height: 22,
    paddingRight: 3,
  },
  flex: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: 100,
    fontFamily: 'Roboto, sans-serif',
    fontSize: 14,
  },
})

const Footer = (props) => {
  const { classes } = props
  const displayDivider = () => <span className={classes.divider}>|</span>
  const displayVersion = () => <span>version <strong>{process.version}</strong></span>
  const displaySupportIcon = () => (
    <a href={urls.PATREON_LINK} className={classes.link}><WalletGiftcard className={classes.icon} /></a>
  )
  const displaySupportLink = () => (
    <a href={urls.PATREON_LINK} className={classes.link}>support the dev</a>
  )
  const displayCopy = () => <span>&copy; 2017-2018</span>

  return (
    <div className={classes.root}>
      <Divider />
      <div className={classes.flex}>
        {displayVersion()}
        {displayDivider()}
        {displaySupportIcon()}
        {displaySupportLink()}
        {displayDivider()}
        {displayCopy()}
      </div>
    </div>
  )
}

Footer.propTypes = {
  classes: PropTypes.object.isRequired,
}

export default withStyles(styles)(Footer)
