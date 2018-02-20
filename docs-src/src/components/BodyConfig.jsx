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
import Switch from 'material-ui/Switch'
import { Upload, ContentSave } from 'mdi-material-ui'

import Localize from 'containers/LocalizeContainer'
import BodyConfigGeneral from 'components/BodyConfigGeneral'
import BodyConfigScheduledSleep from 'components/BodyConfigScheduledSleep'
import BodyConfigExpeditions from 'components/BodyConfigExpeditions'
import BodyConfigPvP from 'components/BodyConfigPvP'
import BodyConfigCombat from 'components/BodyConfigCombat'
import BodyConfigQuests from 'components/BodyConfigQuests'
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
    } else if (line === '[Expeditions]') {
      currentSection = 'expeditions'
    } else if (line === '[PvP]') {
      currentSection = 'pvp'
    } else if (line === '[Combat]') {
      currentSection = 'combat'
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
    generalJSTOffset: pyConfigObj.generalJSTOffset || '0',
    scheduledSleepEnabled: pyConfigObj.scheduledSleepEnabled === 'True',
    scheduledSleepStartTime: new Date(new Date()
      .setHours(
        parseInt(pyConfigObj.scheduledSleepStartTime.substr(0, 2), 10),
        parseInt(pyConfigObj.scheduledSleepStartTime.substr(2, 2), 10), 0, 0
      )),
    scheduledSleepSleepLength: pyConfigObj.scheduledSleepSleepLength || null,
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
    combatOptionCheckFatigue: pyConfigObj.combatMiscOptions.includes('CheckFatigue') || false,
    combatOptionReserveDocks: pyConfigObj.combatMiscOptions.includes('ReserveDocks') || false,
    combatOptionPortCheck: pyConfigObj.combatMiscOptions.includes('PortCheck') || false,
    combatOptionMedalStop: pyConfigObj.combatMiscOptions.includes('MedalStop') || false,
    shipSwitcherEnabled: pyConfigObj.shipSwitcherEnabled === 'True',
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

  componentDidUpdate = (nextProp, nextState) => {
    if (this.state !== nextState && this.state.dropzoneActive === nextState.dropzoneActive) {
      // try not to fire the setConfig'ers if it's just the dropzone state changing
      this.props.setJsonConfig(this.state)
      this.props.setPythonConfig(this.state)
    }
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
        this.setState(newState)
      }
      reader.readAsText(rawConfigFileHandle)
    }
    this.setState({ dropzoneActive: false })
  }

  onSaveClick = () => {
    const configOutput = this.props.config.pythonConfig.reduce((config, line) => {
      let configTemp = config
      configTemp += `${line}\n`
      return configTemp
    }, '# config automatically generated from kcauto-kai frontend\n\n')
    const configBlob = new Blob([configOutput], { type: 'text/plain;charset=utf-8' })
    saveAs(configBlob, 'config.ini', true)
  }

  handleCombatToggle = (event, checked) => {
    // when the combat option is toggled back on, make sure to clear any expeditions based on the combat fleet mode
    if (checked) {
      if (this.state.combatFleetMode === 'striking') {
        this.setState({ expeditionsFleet3: [] })
      } else if (['ctf', 'stf', 'transport'].indexOf(this.state.combatFleetMode) > -1) {
        this.setState({ expeditionsFleet2: [] })
      }
    }
    this.setState({ combatEnabled: checked })
  }

  handleFleetModeChange = (value) => {
    // when changing the fleet mode, make sure to disable and clear any conflicting expeditions as needed
    if (value === 'striking') {
      this.setState({ expeditionsFleet2Enabled: true, expeditionsFleet3Enabled: false, expeditionsFleet3: [] })
    } else if (['ctf', 'stf', 'transport'].indexOf(value) > -1) {
      this.setState({ expeditionsFleet2Enabled: false, expeditionsFleet2: [], expeditionsFleet3Enabled: true })
    } else {
      this.setState({ expeditionsFleet2Enabled: true, expeditionsFleet3Enabled: true })
    }
    this.setState({ combatFleetMode: value })
  }

  handleCombatNodeSelectAdd = (node, targetNode) => {
    // automatically add a node select option based on the two previous helper fields; also checks against previously
    // entered values so that existing node selects for a node are overwritten
    const tempCombatNodeSelects = this.state.combatNodeSelects ? this.state.combatNodeSelects : ''
    const tempCombatNodeSelectsObj = this.optionsNodeSplitter(tempCombatNodeSelects, '>')
    tempCombatNodeSelectsObj[node] = targetNode
    const combatNodeSelects = Object.keys(tempCombatNodeSelectsObj).sort().map(key =>
      `${key}>${tempCombatNodeSelectsObj[key]}`).join(',')
    this.setState({ combatNodeSelect1: null, combatNodeSelect2: null, combatNodeSelects })
  }

  handleCombatFormationAdd = (node, formation) => {
    // automatically add a custom formation selection based on the two previous helper fields; also checks against
    // previously entered values so that existing formations for a node are overwritten
    const tempCombatFormations = this.state.combatFormations ? this.state.combatFormations : ''
    const tempCombatFormationsObj = this.optionsNodeSplitter(tempCombatFormations, ':')

    // if no node is specified, find next node number to apply formation to
    const targetNode = node || this.findMaxNumericNode(tempCombatFormationsObj) + 1
    tempCombatFormationsObj[targetNode] = formation
    const combatFormations = Object.keys(tempCombatFormationsObj).sort().map(key =>
      `${key}:${tempCombatFormationsObj[key]}`).join(',')
    this.setState({ combatFormationsNode: null, combatFormationsFormation: null, combatFormations })
  }

  handleCombatNightBattleAdd = (node, nightBattle) => {
    // automatically add a custom night battle selection based on the two previous helper fields; also checks against
    // previously entered values so that existing night battle selections for a node are overwritten
    const tempCombatNightBattles = this.state.combatNightBattles ? this.state.combatNightBattles : ''
    const tempCombatNightBattlesObj = this.optionsNodeSplitter(tempCombatNightBattles, ':')
    // if no node is specified, find next node number to apply night battle mode to
    const targetNode = node || this.findMaxNumericNode(tempCombatNightBattlesObj) + 1
    tempCombatNightBattlesObj[targetNode] = nightBattle
    const combatNightBattles = Object.keys(tempCombatNightBattlesObj).sort().map(key =>
      `${key}:${tempCombatNightBattlesObj[key]}`).join(',')
    this.setState({ combatNightBattlesNode: null, combatNightBattlesMode: null, combatNightBattles })
  }

  handleLBASGroupSelect = (value) => {
    // clear the LBAS node selects as needed based on the LBAS group selections
    if (!value.includes('1')) {
      this.setState({ combatLBASGroup1Node1: null, combatLBASGroup1Node2: null })
    }
    if (!value.includes('2')) {
      this.setState({ combatLBASGroup2Node1: null, combatLBASGroup2Node2: null })
    }
    if (!value.includes('3')) {
      this.setState({ combatLBASGroup3Node1: null, combatLBASGroup3Node2: null })
    }
    this.setState({ combatLBASGroups: value })
  }

  optionsNodeSplitter = (rawOption, divider) => {
    // helper method to convert a list of comma-separated values divided in two via a divider into an object with the
    // value left of the divider as the key, and the value right of the divider as the value
    const optionsObj = rawOption.split(',').reduce((obj, option) => {
      const tempObj = obj
      const optionInfo = option.split(divider)
      if (optionInfo.length === 2) {
        const node = optionInfo[0]
        const optionChoice = optionInfo[1]
        tempObj[node] = optionChoice
      }
      return tempObj
    }, {})
    return optionsObj
  }

  findMaxNumericNode = (object) => {
    // finds and returns the max numeric node specified in a node options object
    const nodes = Object.keys(object)
    if (nodes.length === 0) {
      return 0
    }
    return Math.max(...nodes.filter(node => parseFloat(node)).map(node => parseFloat(node)))
  }

  configCallback = (config) => {
    this.setState(config)
  }

  filterConfig = prefix => (
    Object.keys(this.state).filter(key => key.startsWith(prefix)).reduce((obj, key) => {
      const temp = obj
      temp[key] = this.state[key]
      return temp
    }, {})
  )

  render = () => {
    const {
      classes,
      config,
    } = this.props
    const {
      dropzoneActive,
      shipSwitcherEnabled,
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
              <BodyConfigGeneral callback={this.configCallback} config={this.filterConfig('general')} />

              <Divider />

              <BodyConfigScheduledSleep callback={this.configCallback} config={this.filterConfig('scheduledSleep')} />

              <Divider />

              <BodyConfigExpeditions
                callback={this.configCallback}
                config={this.filterConfig('expeditions')}
                extraConfig={this.filterConfig('combat')} />

              <Divider />

              <BodyConfigPvP callback={this.configCallback} config={this.filterConfig('pvp')} />

              <Divider />

              <BodyConfigCombat callback={this.configCallback} config={this.filterConfig('combat')} />

              <Divider />

              <Typography variant='display1'>
                <Localize field='bodyConfig.shipSwitcherHeader' />
                <Switch
                  className={classes.switch}
                  checked={shipSwitcherEnabled}
                  onChange={(event, checked) => this.setState({ shipSwitcherEnabled: checked })} />
              </Typography>

              <Divider />

              <BodyConfigQuests callback={this.configCallback} config={this.filterConfig('quests')} />
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
