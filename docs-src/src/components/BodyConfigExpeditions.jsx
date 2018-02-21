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


const EXPEDITIONS = Array.from({ length: 40 }, (value, key) => ({ value: String(key + 1), label: String(key + 1) }))
EXPEDITIONS.push({ value: '9998', label: 'Node Support' })
EXPEDITIONS.push({ value: '9999', label: 'Boss Support' })

class BodyConfigExpeditions extends PureComponent {
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
      expeditionsEnabled,
      expeditionsFleet2,
      expeditionsFleet3,
      expeditionsFleet4,
      combatEnabled,
      combatDisableExpeditionsFleet2,
      combatDisableExpeditionsFleet3,
      combatDisableExpeditionsFleet4,
    } = this.state
    return (
      <Fragment>
        <Typography variant='display1'>
          <Localize field='bodyConfig.expeditionsHeader' />
          <Switch
            className={classes.switch}
            checked={expeditionsEnabled}
            onChange={
              (event, checked) => this.setState(
                { expeditionsEnabled: checked },
                () => this.props.callback(this.state)
              )} />
        </Typography>

        <Grid container spacing={0}>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl
              disabled={
                !expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet2)}
              margin='normal'
              fullWidth
            >
              <InputLabel htmlFor='expeditionsFleet2' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.expeditionsFleet2' />
              </InputLabel>
              <Select
                multi
                className={classes.reactSelect}
                simpleValue={true}
                name='expeditionsFleet2'
                value={expeditionsFleet2}
                options={EXPEDITIONS}
                onChange={value => this.setState({ expeditionsFleet2: value }, () => this.props.callback(this.state))}
                disabled={
                  !expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet2)}
                fullWidth />
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl
              disabled={
                !expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet3)}
              margin='normal'
              fullWidth
            >
              <InputLabel htmlFor='expeditionsFleet3' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.expeditionsFleet3' />
              </InputLabel>
              <Select
                multi
                className={classes.reactSelect}
                simpleValue={true}
                name='expeditionsFleet3'
                value={expeditionsFleet3}
                options={EXPEDITIONS}
                onChange={value => this.setState({ expeditionsFleet3: value }, () => this.props.callback(this.state))}
                disabled={
                  !expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet3)}
                fullWidth />
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={4} className={classes.formGrid}>
            <FormControl
              disabled={
                !expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet4)}
              margin='normal'
              fullWidth
            >
              <InputLabel htmlFor='expeditionsFleet4' shrink={true} className={classes.reactSelectLabel}>
                <Localize field='bodyConfig.expeditionsFleet4' />
              </InputLabel>
              <Select
                multi
                className={classes.reactSelect}
                simpleValue={true}
                name='expeditionsFleet4'
                value={expeditionsFleet4}
                options={EXPEDITIONS}
                onChange={value => this.setState({ expeditionsFleet4: value }, () => this.props.callback(this.state))}
                disabled={
                  !expeditionsEnabled || (combatEnabled && combatDisableExpeditionsFleet4)}
                fullWidth />
            </FormControl>
          </Grid>
        </Grid>
      </Fragment>
    )
  }
}

BodyConfigExpeditions.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigExpeditions)
