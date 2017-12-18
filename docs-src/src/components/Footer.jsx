import React from 'react'
import { withStyles } from 'material-ui/styles'
import PropTypes from 'prop-types'
import Divider from 'material-ui/Divider'

const styles = () => ({
  root: {
    marginTop: 20,
    width: '100%',
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
  return (
    <div className={classes.root}>
      <Divider />
      <div className={classes.flex}>
        version&nbsp;<strong>{process.version}</strong>&nbsp;
        | &copy; 2017
      </div>
    </div>
  )
}

Footer.propTypes = {
  classes: PropTypes.object.isRequired,
}

export default withStyles(styles)(Footer)
