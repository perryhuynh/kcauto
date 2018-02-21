import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Typography from 'material-ui/Typography'
import Switch from 'material-ui/Switch'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


class BodyConfigQuests extends PureComponent {
  state = this.props.config

  componentWillReceiveProps = (nextProps) => {
    if (this.props.config !== nextProps.config) {
      this.setState(nextProps.config)
    }
  }

  render = () => {
    const {
      classes,
    } = this.props
    const {
      questsEnabled,
    } = this.state
    return (
      <Typography variant='display1'>
        <Localize field='bodyConfig.questsHeader' />
        <Switch
          className={classes.switch}
          checked={questsEnabled}
          onChange={
            (event, checked) => this.setState({ questsEnabled: checked }, () => this.props.callback(this.state))} />
      </Typography>
    )
  }
}

BodyConfigQuests.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigQuests)
