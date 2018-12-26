import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'

import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import Switch from '@material-ui/core/Switch'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import Checkbox from '@material-ui/core/Checkbox'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


class BodyConfigQuests extends PureComponent {
  componentDidUpdate = (prevProps) => {
    const {
      config,
      questsEnabled,
      questsQuestGroupsDaily,
      questsQuestGroupsWeekly,
      questsQuestGroupsMonthly,
      questsQuestGroupsOthers,
      updateObject,
    } = this.props
    if (questsEnabled && prevProps.questsEnabled) {
      // disable the Quests module if all Quest groups are disabled
      if (!questsQuestGroupsDaily && !questsQuestGroupsWeekly && !questsQuestGroupsMonthly
          && !questsQuestGroupsOthers) {
        updateObject(config, { questsEnabled: false })
      }
    }
  }

  render = () => {
    const {
      classes,
      config,
      questsEnabled,
      questsQuestGroupsDaily,
      questsQuestGroupsWeekly,
      questsQuestGroupsMonthly,
      questsQuestGroupsOthers,
      updateSwitch,
      updateObject,
    } = this.props

    const allGroupsDisabled = (
      !questsQuestGroupsDaily && !questsQuestGroupsWeekly && !questsQuestGroupsMonthly
      && !questsQuestGroupsOthers)
    return (
      <>
        <Typography variant='h5'>
          <Localize field='bodyConfig.questsHeader' />
          <Switch
            className={classes.switch}
            checked={questsEnabled}
            onChange={
              (event, checked) => updateObject(
                config,
                checked && allGroupsDisabled
                  ? {
                    questsEnabled: checked,
                    questsQuestGroupsDaily: true,
                    questsQuestGroupsWeekly: true,
                    questsQuestGroupsMonthly: true,
                    questsQuestGroupsOthers: true,
                  }
                  : { questsEnabled: checked }
              )
            } />
        </Typography>

        <Grid item xs={12} sm={12} className={classes.formGrid}>
          <FormControlLabel
            control={(
              <Checkbox
                checked={questsQuestGroupsDaily}
                onChange={(event, checked) => updateSwitch(config, event, checked, 'questsQuestGroupsDaily')}
                disabled={!questsEnabled}
                value='questsQuestGroupsDaily' />
            )}
            label={<Localize field='bodyConfig.questsQuestGroupsDaily' />}
            disabled={!questsEnabled} />
          <FormControlLabel
            control={(
              <Checkbox
                checked={questsQuestGroupsWeekly}
                onChange={(event, checked) => updateSwitch(config, event, checked, 'questsQuestGroupsWeekly')}
                disabled={!questsEnabled}
                value='questsQuestGroupsWeekly' />
            )}
            label={<Localize field='bodyConfig.questsQuestGroupsWeekly' />}
            disabled={!questsEnabled} />
          <FormControlLabel
            control={(
              <Checkbox
                checked={questsQuestGroupsMonthly}
                onChange={(event, checked) => updateSwitch(config, event, checked, 'questsQuestGroupsMonthly')}
                disabled={!questsEnabled}
                value='questsQuestGroupsMonthly' />
            )}
            label={<Localize field='bodyConfig.questsQuestGroupsMonthly' />}
            disabled={!questsEnabled} />
          <FormControlLabel
            control={(
              <Checkbox
                checked={questsQuestGroupsOthers}
                onChange={(event, checked) => updateSwitch(config, event, checked, 'questsQuestGroupsOthers')}
                disabled={!questsEnabled}
                value='questsQuestGroupsOthers' />
            )}
            label={<Localize field='bodyConfig.questsQuestGroupsOthers' />}
            disabled={!questsEnabled} />
        </Grid>
      </>
    )
  }
}

BodyConfigQuests.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  questsEnabled: PropTypes.bool.isRequired,
  questsQuestGroupsDaily: PropTypes.bool,
  questsQuestGroupsWeekly: PropTypes.bool,
  questsQuestGroupsMonthly: PropTypes.bool,
  questsQuestGroupsOthers: PropTypes.bool,
  updateSwitch: PropTypes.func.isRequired,
  updateObject: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigQuests)
