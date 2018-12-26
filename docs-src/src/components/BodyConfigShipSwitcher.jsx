/* eslint react/no-unused-prop-types: 0 */
import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'

import Select from 'react-select'
import CreatableSelect from 'react-select/lib/Creatable'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import Modal from '@material-ui/core/Modal'
import Switch from '@material-ui/core/Switch'
import Button from '@material-ui/core/Button'
import InputLabel from '@material-ui/core/InputLabel'
import FormControl from '@material-ui/core/FormControl'
import { PlusBox } from 'mdi-material-ui'

import Localize from 'containers/LocalizeContainer'
import { styles } from 'components/BodyConfigStyles'
import BodyConfigShipSwitcherModal from 'components/BodyConfigShipSwitcherModal'
import { SWITCH_CRITERIA } from 'types/formOptions'

const getModalStyle = () => {
  const top = 50
  const left = 50

  return {
    top: `${top}%`,
    left: `${left}%`,
    transform: `translate(-${top}%, -${left}%)`,
  }
}

class BodyConfigShipSwitcher extends PureComponent {
  state = {
    modalOpen: false,
    modalSlot: null,
  }

  openModal = (modalSlot) => {
    this.setState({ modalSlot, modalOpen: true })
  }

  closeModal = () => {
    this.setState({ modalOpen: false })
  }

  modalCallback = (slot, line) => {
    // take value from modal form and update the ship value in the parent form accordingly
    const {
      config,
      updateObject,
    } = this.props
    const varName = `shipSwitcherSlot${slot}Ships`
    const newOpt = { label: line, value: line }
    const updatedOpts = config[varName] || []
    updatedOpts.push(newOpt)
    this.setState({ modalOpen: false })
    updateObject(config, { [varName]: updatedOpts })
  }

  render = () => {
    const {
      classes,
      config,
      shipSwitcherEnabled,
      combatEnabled,
      updateSwitch,
      updateSelect,
    } = this.props
    const {
      modalOpen,
      modalSlot,
    } = this.state
    return (
      <>
        <Typography variant='h5'>
          <Localize field='bodyConfig.shipSwitcherHeader' />
          <Switch
            className={classes.switch}
            checked={shipSwitcherEnabled}
            disabled={!combatEnabled}
            onChange={(event, checked) => updateSwitch(config, event, checked, 'shipSwitcherEnabled')} />
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
                      isMulti
                      className={classes.reactSelect}
                      name={criteria}
                      value={config[criteria]}
                      options={SWITCH_CRITERIA}
                      onChange={value => updateSelect(config, value, criteria)}
                      isDisabled={!shipSwitcherEnabled}
                      placeholder={<Localize field='bodyConfig.shipSwitcherCriteria' />}
                      fullWidth />
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={7} className={classes.formGrid}>
                  <FormControl disabled={!shipSwitcherEnabled} margin='normal' fullWidth>
                    <CreatableSelect
                      isMulti
                      isClearable
                      components={{ DropdownIndicator: null }}
                      className={classes.reactSelect}
                      name={ships}
                      menuIsOpen={false}
                      value={config[ships]}
                      onChange={value => updateSelect(config, value, ships)}
                      isDisabled={!shipSwitcherEnabled} />
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
              prevValues={config[`shipSwitcherSlot${modalSlot}Ships`] || []}
              callback={this.modalCallback} />
          </div>
        </Modal>
      </>
    )
  }
}

BodyConfigShipSwitcher.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  shipSwitcherEnabled: PropTypes.bool.isRequired,
  shipSwitcherSlot1Criteria: PropTypes.array,
  shipSwitcherSlot1Ships: PropTypes.array,
  shipSwitcherSlot2Criteria: PropTypes.array,
  shipSwitcherSlot2Ships: PropTypes.array,
  shipSwitcherSlot3Criteria: PropTypes.array,
  shipSwitcherSlot3Ships: PropTypes.array,
  shipSwitcherSlot4Criteria: PropTypes.array,
  shipSwitcherSlot4Ships: PropTypes.array,
  shipSwitcherSlot5Criteria: PropTypes.array,
  shipSwitcherSlot5Ships: PropTypes.array,
  shipSwitcherSlot6Criteria: PropTypes.array,
  shipSwitcherSlot6Ships: PropTypes.array,
  combatEnabled: PropTypes.bool.isRequired,
  updateSwitch: PropTypes.func.isRequired,
  updateSelect: PropTypes.func.isRequired,
  updateObject: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfigShipSwitcher)
