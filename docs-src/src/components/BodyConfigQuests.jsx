import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Grid from 'material-ui/Grid'
import Typography from 'material-ui/Typography'
import Switch from 'material-ui/Switch'
import { FormControlLabel } from 'material-ui/Form'
import Checkbox from 'material-ui/Checkbox'

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
      questsQuestGroupsDaily,
      questsQuestGroupsWeekly,
      questsQuestGroupsMonthly,
    } = this.state
    return (
      <Fragment>
        <Typography variant='display1'>
          <Localize field='bodyConfig.questsHeader' />
          <Switch
            className={classes.switch}
            checked={questsEnabled}
            onChange={
              (event, checked) => {
                const newState = { questsEnabled: checked }
                if (checked && !questsQuestGroupsDaily && !questsQuestGroupsWeekly && !questsQuestGroupsMonthly) {
                  newState.questsQuestGroupsDaily = true
                  newState.questsQuestGroupsWeekly = true
                  newState.questsQuestGroupsMonthly = true
                }
                this.setState(newState, () => this.props.callback(this.state))
              }
            } />
        </Typography>

        <Grid item xs={12} sm={12} className={classes.formGrid}>
          <FormControlLabel
            control={
              <Checkbox
                checked={questsQuestGroupsDaily}
                onChange={
                  (event, checked) => this.setState(
                    { questsQuestGroupsDaily: checked },
                    () => this.props.callback(this.state)
                  )}
                disabled={!questsEnabled}
                value='questsQuestGroupsDaily' />
            }
            label={<Localize field='bodyConfig.questsQuestGroupsDaily' />}
            disabled={!questsEnabled} />
          <FormControlLabel
            control={
              <Checkbox
                checked={questsQuestGroupsWeekly}
                onChange={
                  (event, checked) => this.setState(
                    { questsQuestGroupsWeekly: checked },
                    () => this.props.callback(this.state)
                  )}
                disabled={!questsEnabled}
                value='questsQuestGroupsWeekly' />
            }
            label={<Localize field='bodyConfig.questsQuestGroupsWeekly' />}
            disabled={!questsEnabled} />
          <FormControlLabel
            control={
              <Checkbox
                checked={questsQuestGroupsMonthly}
                onChange={
                  (event, checked) => this.setState(
                    { questsQuestGroupsMonthly: checked },
                    () => this.props.callback(this.state)
                  )}
                disabled={!questsEnabled}
                value='questsQuestGroupsMonthly' />
            }
            label={<Localize field='bodyConfig.questsQuestGroupsMonthly' />}
            disabled={!questsEnabled} />
        </Grid>
      </Fragment>
    )
  }
}

BodyConfigQuests.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigQuests)
