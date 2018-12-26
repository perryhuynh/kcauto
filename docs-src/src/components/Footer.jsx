import React from 'react'
import { withStyles } from '@material-ui/core/styles'
import PropTypes from 'prop-types'
import Divider from '@material-ui/core/Divider'
import blueGrey from '@material-ui/core/colors/blueGrey'
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
    fontWeight: 'bold',
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
  const changelogUrl = `${urls.CHANGELOG_LINK}#${process.version.replace(/\./g, '')}`
  const renderDivider = () => <span className={classes.divider}>|</span>
  const renderVersion = () => <span>version <a href={changelogUrl} className={classes.link}>{process.version}</a></span>
  const renderCopy = () => <span>&copy; 2017-2018</span>

  return (
    <div className={classes.root}>
      <Divider />
      <div className={classes.flex}>
        {renderVersion()}
        {renderDivider()}
        {renderCopy()}
      </div>
    </div>
  )
}

Footer.propTypes = {
  classes: PropTypes.object.isRequired,
}

export default withStyles(styles)(Footer)
