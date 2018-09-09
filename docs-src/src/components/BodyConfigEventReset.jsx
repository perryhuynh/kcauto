import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Select from 'react-select'
import Grid from 'material-ui/Grid'
import Typography from 'material-ui/Typography'
import Switch from 'material-ui/Switch'
import { InputLabel } from 'material-ui/Input'
import { FormControl } from 'material-ui/Form'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'


const FREQUENCIES = ['1', '2', '3', '4', '5'].map(value => ({ value, label: value }))
const DIFFICULTIES = [
  { value: 'casual', label: <Localize field='bodyConfig.eventResetDifficultyCasual' /> },
  { value: 'easy', label: <Localize field='bodyConfig.eventResetDifficultyEasy' /> },
  { value: 'medium', label: <Localize field='bodyConfig.eventResetDifficultyMedium' /> },
  { value: 'hard', label: <Localize field='bodyConfig.eventResetDifficultyHard' /> }]

class BodyConfigEventReset extends PureComponent {
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
      eventResetEnabled,
      eventResetFrequency,
      eventResetFarmDifficulty,
      eventResetResetDifficulty,
      combatEnabled,
      combatMap,
    } = this.state
    return (
      <Fragment>
        <Typography variant='display1'>
          <Localize field='bodyConfig.eventResetHeader' />
          <Switch
            className={classes.switch}
            checked={eventResetEnabled}
            disabled={!combatEnabled || !(combatEnabled && combatMap[0] === 'E')}
            onChange={
              (event, checked) => this.setState(
                { eventResetEnabled: checked },
                () => this.props.callback(this.state)
              )} />
        </Typography>

        <Grid container spacing={0}>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl disabled={!eventResetEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='eventResetFrequency' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.eventResetFrequency' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                simpleValue={true}
                name='eventResetFrequency'
                value={eventResetFrequency}
                options={FREQUENCIES}
                clearable={false}
                onChange={
                  value => this.setState({ eventResetFrequency: value }, () => this.props.callback(this.state))}
                disabled={!eventResetEnabled}
                fullWidth />
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl disabled={!eventResetEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='eventResetFarmDifficulty' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.eventResetFarmDifficulty' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                simpleValue={true}
                name='eventResetFarmDifficulty'
                value={eventResetFarmDifficulty}
                options={DIFFICULTIES}
                clearable={false}
                onChange={
                  value => this.setState({ eventResetFarmDifficulty: value }, () => this.props.callback(this.state))}
                disabled={!eventResetEnabled}
                fullWidth />
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl disabled={!eventResetEnabled} margin='normal' fullWidth>
              <InputLabel htmlFor='eventResetResetDifficulty' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.eventResetResetDifficulty' />
              </InputLabel>
              <Select
                className={classes.reactSelect}
                simpleValue={true}
                name='eventResetResetDifficulty'
                value={eventResetResetDifficulty}
                options={DIFFICULTIES}
                clearable={false}
                onChange={
                  value => this.setState({ eventResetResetDifficulty: value }, () => this.props.callback(this.state))}
                disabled={!eventResetEnabled}
                fullWidth />
            </FormControl>
          </Grid>
        </Grid>
      </Fragment>
    )
  }
}

BodyConfigEventReset.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigEventReset)
