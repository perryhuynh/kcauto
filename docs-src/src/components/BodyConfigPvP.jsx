import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Typography from 'material-ui/Typography'
import Switch from 'material-ui/Switch'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


class BodyConfigPvP extends PureComponent {
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
      pvpEnabled,
    } = this.state
    return (
      <Typography variant='display1'>
        <Localize field='bodyConfig.pvpHeader' />
        <Switch
          className={classes.switch}
          checked={pvpEnabled}
          onChange={
            (event, checked) => this.setState({ pvpEnabled: checked }, () => this.props.callback(this.state))} />
      </Typography>
    )
  }
}

BodyConfigPvP.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigPvP)
