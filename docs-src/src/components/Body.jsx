import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import AppBar from 'material-ui/AppBar'
import Tabs, { Tab } from 'material-ui/Tabs'
import { Play, Settings, InformationOutline } from 'mdi-material-ui'

import BodyConfigContainer from 'containers/BodyConfigContainer'
import BodyRunCmdContainer from 'containers/BodyRunCmdContainer'
import BodyAbout from 'components/BodyAbout'

const styles = () => ({
  root: {
    flexGrow: 1,
  },
})

class Body extends PureComponent {
  state = {
    value: 0,
  }

  render = () => {
    const { classes } = this.props

    return (
      <div className={classes.root}>
        <AppBar position='static' color='default'>
          <Tabs
            value={this.state.value}
            onChange={(event, value) => this.setState({ value })}
            indicatorColor='primary'
            textColor='primary'
            centered
          >
            <Tab icon={<Settings />} label='Config' />
            <Tab icon={<Play />} label='Run Cmd' />
            <Tab icon={<InformationOutline />} label='About' />
          </Tabs>
        </AppBar>
        { this.state.value === 0 ?
          <BodyConfigContainer /> :
          null}
        { this.state.value === 1 ?
          <BodyRunCmdContainer /> :
          null}
        { this.state.value === 2 ?
          <BodyAbout /> :
          null}
      </div>
    )
  }
}

Body.propTypes = {
  classes: PropTypes.object.isRequired,
}

export default withStyles(styles)(Body)
