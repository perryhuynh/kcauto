import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import AppBar from 'material-ui/AppBar'
import Tabs, { Tab } from 'material-ui/Tabs'
import Grid from 'material-ui/Grid'
import { InformationOutline, Settings } from 'mdi-material-ui'

import BodyConfigContainer from 'containers/BodyConfigContainer'
import BodyAboutContainer from 'containers/BodyAboutContainer'

const styles = () => ({
  root: {
    flexGrow: 1,
  },
})

class Body extends React.Component {
  state = {
    value: 0,
  }

  handleChange = (event, value) => {
    this.setState({ value })
  }

  render = () => {
    const { classes } = this.props

    return (
      <div className={classes.root}>
        <AppBar position='static' color='default'>
          <Tabs
            value={this.state.value}
            onChange={this.handleChange}
            indicatorColor='primary'
            textColor='primary'
            centered
          >
            <Tab icon={<Settings />} label='Config' />
            <Tab icon={<InformationOutline />} label='About' />
          </Tabs>
        </AppBar>
        { this.state.value === 0 ?
          <BodyConfigContainer /> :
          null}
        { this.state.value === 1 ?
          <BodyAboutContainer /> :
          null}
      </div>
    )
  }
}

Body.propTypes = {
  classes: PropTypes.object.isRequired,
}

export default withStyles(styles)(Body)
