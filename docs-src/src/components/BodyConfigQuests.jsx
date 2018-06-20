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

  handleQuestGroupCheck = (event, checked) => {
    // handle the quest group checkboxes and disable the entire module when all options are unchecked
    const tempState = { [event.target.value]: checked }
    const questGroups = ['questsQuestGroupsDaily', 'questsQuestGroupsWeekly', 'questsQuestGroupsMonthly']
    let enableQuests = false
    // ascertained if all groups are now disabled
    questGroups.forEach((group) => {
      if (group === event.target.value) {
        if (checked === true) {
          enableQuests = true
        }
      } else {
        enableQuests = enableQuests || this.state[group]
      }
    })
    // if all groups are disabled, also disable the quests section
    if (!enableQuests) {
      tempState.questsEnabled = false
    }
    this.setState(tempState, () => this.props.callback(this.state))
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
    const allGroupsDisabled = !questsQuestGroupsDaily && !questsQuestGroupsWeekly && !questsQuestGroupsMonthly
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
                if (checked && allGroupsDisabled) {
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
                onChange={this.handleQuestGroupCheck}
                disabled={!questsEnabled}
                value='questsQuestGroupsDaily' />
            }
            label={<Localize field='bodyConfig.questsQuestGroupsDaily' />}
            disabled={!questsEnabled} />
          <FormControlLabel
            control={
              <Checkbox
                checked={questsQuestGroupsWeekly}
                onChange={this.handleQuestGroupCheck}
                disabled={!questsEnabled}
                value='questsQuestGroupsWeekly' />
            }
            label={<Localize field='bodyConfig.questsQuestGroupsWeekly' />}
            disabled={!questsEnabled} />
          <FormControlLabel
            control={
              <Checkbox
                checked={questsQuestGroupsMonthly}
                onChange={this.handleQuestGroupCheck}
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
