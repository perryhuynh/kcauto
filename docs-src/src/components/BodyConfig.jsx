import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import saveAs from 'save-as'

import Dropzone from 'react-dropzone'

import Grid from 'material-ui/Grid'
import Paper from 'material-ui/Paper'
import Typography from 'material-ui/Typography'
import Divider from 'material-ui/Divider'
import Button from 'material-ui/Button'
import { Upload, ContentSave } from 'mdi-material-ui'

import Localize from 'containers/LocalizeContainer'
import {
  BodyConfigGeneralContainer,
  BodyConfigScheduledSleepContainer,
  BodyConfigScheduledStopContainer,
  BodyConfigExpeditionsContainer,
  BodyConfigPvPContainer,
  BodyConfigCombatContainer,
  BodyConfigShipSwitcherContainer,
  BodyConfigQuestsContainer,
} from 'containers/BodyConfigSectionContainer'
import { styles } from 'components/BodyConfigStyles'


const createStateObjFromPythonConfig = (pyConfig) => {
  const pyConfigLines = pyConfig.split('\n')
  const pyConfigObj = {}
  let currentSection = ''
  pyConfigLines.forEach((line) => {
    if (line.indexOf('#') === 0) {
      // comment line
    } else if (line === '[General]') {
      currentSection = 'general'
    } else if (line === '[ScheduledSleep]') {
      currentSection = 'scheduledSleep'
    } else if (line === '[ScheduledStop]') {
      currentSection = 'scheduledStop'
    } else if (line === '[Expeditions]') {
      currentSection = 'expeditions'
    } else if (line === '[PvP]') {
      currentSection = 'pvp'
    } else if (line === '[Combat]') {
      currentSection = 'combat'
    } else if (line === '[ShipSwitcher]') {
      currentSection = 'shipSwitcher'
    } else if (line === '[Quests]') {
      currentSection = 'quests'
    } else {
      const splitLine = line.split(/:(.*)/, 2)
      // valid config line
      let value = splitLine[1] ? splitLine[1].trim() : null
      if (splitLine[0].indexOf('LBASGroup') > -1 && splitLine[0].indexOf('Nodes') > -1) {
        value = value ? value.split(',').map(node => node.trim()) : [null, null]
      } else if (splitLine[0] === 'MiscOptions') {
        value = value ? value.split(',').map(option => option.trim()) : []
      }
      pyConfigObj[`${currentSection}${splitLine[0].trim()}`] = value
    }
  })

  const jsonConfig = {
    dropzoneActive: false,
    generalProgram: pyConfigObj.generalProgram,
    generalJSTOffset: parseInt(pyConfigObj.generalJSTOffset, 10) || 0,
    generalPause: pyConfigObj.generalPause === 'True',
    scheduledSleepScriptSleepEnabled: pyConfigObj.scheduledSleepScriptSleepEnabled === 'True',
    scheduledSleepScriptSleepStartTime: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.scheduledSleepScriptSleepStartTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledSleepScriptSleepStartTime.substr(2, 2), 10), 0, 0
      )),
    scheduledSleepScriptSleepLength: pyConfigObj.scheduledSleepScriptSleepLength || '',
    scheduledSleepExpeditionSleepEnabled: pyConfigObj.scheduledSleepCombatSleepEnabled === 'True',
    scheduledSleepExpeditionSleepStartTime: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.scheduledSleepCombatSleepStartTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledSleepCombatSleepStartTime.substr(2, 2), 10), 0, 0
      )),
    scheduledSleepExpeditionSleepLength: pyConfigObj.scheduledSleepCombatSleepLength || '',
    scheduledSleepCombatSleepEnabled: pyConfigObj.scheduledSleepExpeditionSleepEnabled === 'True',
    scheduledSleepCombatSleepStartTime: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.scheduledSleepExpeditionSleepStartTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledSleepExpeditionSleepStartTime.substr(2, 2), 10), 0, 0
      )),
    scheduledSleepCombatSleepLength: pyConfigObj.scheduledSleepExpeditionSleepLength || '',
    scheduledStopScriptStopEnabled: pyConfigObj.scheduledStopScriptStopEnabled === 'True',
    scheduledStopScriptStopCount: parseInt(pyConfigObj.scheduledStopScriptStopCount, 10) || '',
    scheduledStopScriptStopTime: pyConfigObj.scheduledStopScriptStopTime ?
      new Date(new Date().setHours(
        parseInt(pyConfigObj.scheduledStopScriptStopTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledStopScriptStopTime.substr(2, 2), 10), 0, 0
      )) :
      null,
    scheduledStopExpeditionStopEnabled: pyConfigObj.scheduledStopExpeditionStopEnabled === 'True',
    scheduledStopExpeditionStopMode: pyConfigObj.scheduledStopExpeditionStopMode,
    scheduledStopExpeditionStopCount: parseInt(pyConfigObj.scheduledStopExpeditionStopCount, 10) || '',
    scheduledStopExpeditionStopTime: pyConfigObj.scheduledStopExpeditionStopTime ?
      new Date(new Date().setHours(
        parseInt(pyConfigObj.scheduledStopExpeditionStopTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledStopExpeditionStopTime.substr(2, 2), 10), 0, 0
      )) :
      null,
    scheduledStopCombatStopEnabled: pyConfigObj.scheduledStopCombatStopEnabled === 'True',
    scheduledStopCombatStopMode: pyConfigObj.scheduledStopCombatStopMode,
    scheduledStopCombatStopCount: parseInt(pyConfigObj.scheduledStopCombatStopCount, 10) || '',
    scheduledStopCombatStopTime: pyConfigObj.scheduledStopCombatStopTime ?
      new Date(new Date().setHours(
        parseInt(pyConfigObj.scheduledStopCombatStopTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledStopCombatStopTime.substr(2, 2), 10), 0, 0
      )) :
      null,
    expeditionsEnabled: pyConfigObj.expeditionsEnabled === 'True',
    expeditionsFleet2: pyConfigObj.expeditionsFleet2 || null,
    expeditionsFleet3: pyConfigObj.expeditionsFleet3 || null,
    expeditionsFleet4: pyConfigObj.expeditionsFleet4 || null,
    pvpEnabled: pyConfigObj.pvpEnabled === 'True',
    combatEnabled: pyConfigObj.combatEnabled === 'True',
    combatEngine: pyConfigObj.combatEngine || 'legacy',
    combatMap: pyConfigObj.combatMap || '1-1',
    combatFleetMode: pyConfigObj.combatFleetMode || '',
    combatDisableExpeditionsFleet2: false,
    combatDisableExpeditionsFleet3: false,
    combatDisableExpeditionsFleet4: false,
    combatCombatNodes: pyConfigObj.combatCombatNodes || null,
    combatNodeSelect1: null,
    combatNodeSelect2: null,
    combatNodeSelects: pyConfigObj.combatNodeSelects || null,
    combatFormationsNode: null,
    combatFormationsFormation: null,
    combatFormations: pyConfigObj.combatFormations || null,
    combatNightBattlesNode: null,
    combatNightBattlesMode: null,
    combatNightBattles: pyConfigObj.combatNightBattles || null,
    combatRetreatLimit: pyConfigObj.combatRetreatLimit || 'heavy',
    combatRepairLimit: pyConfigObj.combatRepairLimit || 'moderate',
    combatRepairTimeLimit: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.combatRepairTimeLimit.substr(0, 2), 10),
        parseInt(pyConfigObj.combatRepairTimeLimit.substr(2, 2), 10), 0, 0
      )),
    combatLBASGroups: pyConfigObj.combatLBASGroups || null,
    combatLBASGroup1Node1: pyConfigObj.combatLBASGroup1Nodes[0] || null,
    combatLBASGroup1Node2: pyConfigObj.combatLBASGroup1Nodes[1] || null,
    combatLBASGroup2Node1: pyConfigObj.combatLBASGroup2Nodes[0] || null,
    combatLBASGroup2Node2: pyConfigObj.combatLBASGroup2Nodes[1] || null,
    combatLBASGroup3Node1: pyConfigObj.combatLBASGroup3Nodes[0] || null,
    combatLBASGroup3Node2: pyConfigObj.combatLBASGroup3Nodes[1] || null,
    combatForceRetreatNodes: pyConfigObj.combatForceRetreatNodes || null,
    combatOptionCheckFatigue: pyConfigObj.combatMiscOptions.includes('CheckFatigue') || false,
    combatOptionReserveDocks: pyConfigObj.combatMiscOptions.includes('ReserveDocks') || false,
    combatOptionPortCheck: pyConfigObj.combatMiscOptions.includes('PortCheck') || false,
    combatOptionClearStop: pyConfigObj.combatMiscOptions.includes('ClearStop') || false,
    shipSwitcherEnabled: pyConfigObj.shipSwitcherEnabled === 'True',
    shipSwitcherSlot1Criteria: pyConfigObj.shipSwitcherSlot1Criteria || null,
    shipSwitcherSlot1Ships: pyConfigObj.shipSwitcherSlot1Ships || null,
    shipSwitcherSlot2Criteria: pyConfigObj.shipSwitcherSlot2Criteria || null,
    shipSwitcherSlot2Ships: pyConfigObj.shipSwitcherSlot2Ships || null,
    shipSwitcherSlot3Criteria: pyConfigObj.shipSwitcherSlot3Criteria || null,
    shipSwitcherSlot3Ships: pyConfigObj.shipSwitcherSlot3Ships || null,
    shipSwitcherSlot4Criteria: pyConfigObj.shipSwitcherSlot4Criteria || null,
    shipSwitcherSlot4Ships: pyConfigObj.shipSwitcherSlot4Ships || null,
    shipSwitcherSlot5Criteria: pyConfigObj.shipSwitcherSlot5Criteria || null,
    shipSwitcherSlot5Ships: pyConfigObj.shipSwitcherSlot5Ships || null,
    shipSwitcherSlot6Criteria: pyConfigObj.shipSwitcherSlot6Criteria || null,
    shipSwitcherSlot6Ships: pyConfigObj.shipSwitcherSlot6Ships || null,
    questsEnabled: pyConfigObj.questsEnabled === 'True',
  }

  return jsonConfig
}

class BodyConfig extends PureComponent {
  // grab default states from the store; defaults are in reducers/config/config.jsx
  state = this.props.config.jsonConfig

  componentDidMount = () => {
    // this.props.setJsonConfig(this.state)
    this.props.setPythonConfig(this.state)
  }

  onConfigLoadEnter = () => {
    this.setState({ dropzoneActive: true })
  }

  onConfigLoadLeave = () => {
    this.setState({ dropzoneActive: false })
  }

  onConfigLoad = (acceptedFiles, rejectedFiles) => {
    // only accept the first file
    if (acceptedFiles.length === 1) {
      const rawConfigFileHandle = acceptedFiles[0]
      const reader = new FileReader()
      reader.onload = () => {
        const newState = createStateObjFromPythonConfig(reader.result)
        this.updateStoreConfig(newState)
      }
      reader.readAsText(rawConfigFileHandle)
    }
    this.setState({ dropzoneActive: false })
  }

  onSaveClick = () => {
    // generates config.ini file for local save
    const configOutput = this.props.config.pythonConfig.reduce((config, line) => {
      let configTemp = config
      configTemp += `${line}\n`
      return configTemp
    }, `# config automatically generated from kcauto-kai frontend (v${process.version})\n\n`)
    const configBlob = new Blob([configOutput], { type: 'text/plain;charset=utf-8' })
    saveAs(configBlob, 'config.ini', true)
  }

  updateStoreConfig = (config) => {
    // method that updates the BodyConfig state
    this.props.setJsonConfig(config)
    this.props.setPythonConfig(config)
  }

  render = () => {
    const {
      classes,
      config,
    } = this.props
    const {
      dropzoneActive,
    } = this.state
    let configLoad

    return (
      <Dropzone
        ref={(node) => { configLoad = node }}
        style={{ position: 'relative' }}
        accept='.ini'
        onDrop={this.onConfigLoad}
        onDragEnter={this.onConfigLoadEnter}
        onDragLeave={this.onConfigLoadLeave}
        disableClick
      >
        { dropzoneActive ? <div className={classes.dropzoneOverlay}>drop your config file here</div> : null }
        <Grid container spacing={0}>
          <Grid item xs={12} md={8}>
            <Paper className={classes.paper} elevation={0}>
              <BodyConfigGeneralContainer callback={this.updateStoreConfig} />

              <Divider />

              <BodyConfigScheduledSleepContainer callback={this.updateStoreConfig} />

              <Divider />

              <BodyConfigScheduledStopContainer callback={this.updateStoreConfig} />

              <Divider />

              <BodyConfigExpeditionsContainer callback={this.updateStoreConfig} />

              <Divider />

              <BodyConfigPvPContainer callback={this.updateStoreConfig} />

              <Divider />

              <BodyConfigCombatContainer callback={this.updateStoreConfig} />

              <Divider />

              <BodyConfigShipSwitcherContainer callback={this.updateStoreConfig} />

              <Divider />

              <BodyConfigQuestsContainer callback={this.updateStoreConfig} />
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper className={classes.paper} elevation={0}>
              <Typography variant='display1' className={classes.flexReset}>
                <Localize field='bodyConfig.configHeader' />
                <Button
                  size='small'
                  color='primary'
                  className={classes.saveButton}
                  onClick={() => configLoad.open()}
                >
                  <Localize field='bodyConfig.configLoad' />
                  <Upload />
                </Button>
                <Button
                  size='small'
                  color='primary'
                  className={classes.saveButton}
                  onClick={() => this.onSaveClick()}
                >
                  <Localize field='bodyConfig.configSave' />
                  <ContentSave />
                </Button>
              </Typography>
              <Paper elevation={2}>
                <pre className={classes.pre}>
                  {config.pythonConfig.map(line => `${line}\n`)}
                </pre>
              </Paper>
            </Paper>
          </Grid>
        </Grid>
      </Dropzone>
    )
  }
}

BodyConfig.propTypes = {
  classes: PropTypes.object.isRequired,
  config: PropTypes.object.isRequired,
  setJsonConfig: PropTypes.func.isRequired,
  setPythonConfig: PropTypes.func.isRequired,
}

export default withStyles(styles)(BodyConfig)
