import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'

import Select from 'react-select'
import Grid from 'material-ui/Grid'
import Typography from 'material-ui/Typography'
import Modal from 'material-ui/Modal'
import Switch from 'material-ui/Switch'
import Button from 'material-ui/Button'
import { InputLabel } from 'material-ui/Input'
import { FormControl } from 'material-ui/Form'
import { PlusBox } from 'mdi-material-ui'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'
import BodyConfigShipSwitcherModal from 'components/BodyConfigShipSwitcherModal'


const getModalStyle = () => {
  const top = 50
  const left = 50

  return {
    top: `${top}%`,
    left: `${left}%`,
    transform: `translate(-${top}%, -${left}%)`,
  }
}

const SWITCH_CRITERIA = [
  { value: 'damage', label: <Localize field='bodyConfig.shipSwitcherCriteriaDamage' /> },
  { value: 'fatigue', label: <Localize field='bodyConfig.shipSwitcherCriteriaFatigue' /> },
  { value: 'sparkle', label: <Localize field='bodyConfig.shipSwitcherCriteriaSparkle' /> }]

class BodyConfigShipSwitcher extends PureComponent {
  state = this.props.config

  componentWillReceiveProps = (nextProps) => {
    if (this.props.config !== nextProps.config) {
      this.setState(nextProps.config)
    }
  }

  openModal = (modalSlot) => {
    this.setState({ modalSlot, modalOpen: true })
  }

  closeModal = () => {
    this.setState({ modalOpen: false })
  }

  modalCallback = (slot, line) => {
    // take value from modal form and update the ship value in the parent form accordingly
    const varName = `shipSwitcherSlot${slot}Ships`
    const prevVal = this.state[varName] ? this.state[varName] : ''
    const newVal = prevVal ? `${prevVal},${line}` : line
    this.setState({
      modalOpen: false,
      [varName]: newVal,
    }, () => this.props.callback(this.state))
  }

  render = () => {
    const {
      classes,
    } = this.props
    const {
      shipSwitcherEnabled,
      combatEnabled,
      modalOpen,
      modalSlot,
    } = this.state
    // create react-select-friendly form values for ship specifications
    const slotShipChoices = [...Array(6).keys()].reduce((obj, slot) => {
      const tempObj = obj
      const nSlot = slot + 1
      if (this.state[`shipSwitcherSlot${nSlot}Ships`]) {
        tempObj[nSlot] = this.state[`shipSwitcherSlot${nSlot}Ships`].split(',').map(value => ({ value, label: value }))
      }
      return tempObj
    }, {})
    return (
      <Fragment>
        <Typography variant='display1'>
          <Localize field='bodyConfig.shipSwitcherHeader' />
          <Switch
            className={classes.switch}
            checked={shipSwitcherEnabled}
            disabled={!combatEnabled}
            onChange={
              (event, checked) => this.setState(
                { shipSwitcherEnabled: checked },
                () => this.props.callback(this.state)
              )} />
        </Typography>

        { [...Array(6).keys()].map((key) => {
          const slot = key + 1
          const label = `shipSwitcherSlot${slot}`
          const criteria = `shipSwitcherSlot${slot}Criteria`
          const ships = `shipSwitcherSlot${slot}Ships`
          return (
            <Fragment key={key}>
              <Grid container spacing={0}>
                <Grid item xs={12} sm={4} className={classes.formGrid}>
                  <FormControl disabled={!shipSwitcherEnabled} margin='normal' fullWidth>
                    <InputLabel htmlFor={criteria} shrink={true} className={classes.reactSelectLabel}>
                      <Localize field={`bodyConfig.${label}`} />
                    </InputLabel>
                    <Select
                      multi
                      className={classes.reactSelect}
                      simpleValue={true}
                      name={criteria}
                      value={this.state[criteria]}
                      options={SWITCH_CRITERIA}
                      onChange={value => this.setState({ [criteria]: value }, () => this.props.callback(this.state))}
                      disabled={!shipSwitcherEnabled}
                      placeholder={<Localize field='bodyConfig.shipSwitcherCriteria' />}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={7} className={classes.formGrid}>
                  <FormControl disabled={!shipSwitcherEnabled} margin='normal' fullWidth>
                    <Select
                      multi
                      className={classes.reactSelect}
                      simpleValue={true}
                      options={slotShipChoices[slot]}
                      name={ships}
                      value={this.state[ships]}
                      onChange={value => this.setState({ [ships]: value }, () => this.props.callback(this.state))}
                      disabled={!shipSwitcherEnabled}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={4} sm={1} className={classes.formGridButton}>
                  <Button
                    size='small'
                    color='primary'
                    disabled={!shipSwitcherEnabled}
                    onClick={() => this.openModal(slot)}
                  >
                    <PlusBox />
                  </Button>
                </Grid>
              </Grid>
            </Fragment>
          )
        })}

        <Modal
          open={modalOpen || false}
          onClose={this.closeModal}
        >
          <div style={getModalStyle()} className={classes.modal}>
            <BodyConfigShipSwitcherModal
              slot={modalSlot}
              prevValues={this.state[`shipSwitcherSlot${modalSlot}Ships`] || ''}
              callback={this.modalCallback} />
          </div>
        </Modal>
      </Fragment>
    )
  }
}

BodyConfigShipSwitcher.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  callback: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigShipSwitcher)
