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

const TABS = ['config', 'runcmd', 'about']

class Body extends PureComponent {
  state = {
    tab: window.location.hash ? window.location.hash.substr(1) : 'config',
  }

  render = () => {
    const { classes } = this.props
    const { tab } = this.state

    return (
      <div className={classes.root}>
        <AppBar position='static' color='default'>
          <Tabs
            value={TABS.indexOf(tab)}
            onChange={(event, value) => this.setState({ tab: TABS[value] })}
            indicatorColor='primary'
            textColor='primary'
            centered
          >
            <Tab icon={<Settings />} label='Config' />
            <Tab icon={<Play />} label='Run Cmd' />
            <Tab icon={<InformationOutline />} label='About' />
          </Tabs>
        </AppBar>
        { tab === 'config' ?
          <BodyConfigContainer /> :
          null}
        { tab === 'runcmd' ?
          <BodyRunCmdContainer /> :
          null}
        { tab === 'about' ?
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
