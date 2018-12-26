import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'
import saveAs from 'save-as'

import Dropzone from 'react-dropzone'

import Grid from '@material-ui/core/Grid'
import Paper from '@material-ui/core/Paper'
import Typography from '@material-ui/core/Typography'
import Divider from '@material-ui/core/Divider'
import Button from '@material-ui/core/Button'
import { Upload, ContentSave } from 'mdi-material-ui'

import Localize from 'containers/LocalizeContainer'
import {
  BodyConfigGeneralContainer,
  BodyConfigScheduledSleepContainer,
  BodyConfigScheduledStopContainer,
  BodyConfigExpeditionsContainer,
  BodyConfigPvPContainer,
  BodyConfigCombatContainer,
  BodyConfigEventResetContainer,
  BodyConfigShipSwitcherContainer,
  BodyConfigQuestsContainer,
} from 'containers/BodyConfigSectionContainer'
import { styles } from 'components/BodyConfigStyles'
import { createStateObjFromPythonConfig } from 'components/util'


class BodyConfig extends PureComponent {
  // grab default states from the store; defaults are in reducers/config/config.jsx
  // state = this.props.config.jsonConfig
  state = {
    dropzoneActive: false,
  }

  componentDidMount = () => {
    // this.props.setJsonConfig(this.state)
    const { config, setPythonConfig } = this.props
    setPythonConfig(config.jsonConfig)
  }

  onConfigLoadEnter = () => {
    this.setState({ dropzoneActive: true })
  }

  onConfigLoadLeave = () => {
    this.setState({ dropzoneActive: false })
  }

  onConfigLoad = (acceptedFiles) => {
    // only accept the first file
    if (acceptedFiles.length === 1) {
      const rawConfigFileHandle = acceptedFiles[0]
      const reader = new FileReader()
      reader.onload = () => {
        const newConfig = createStateObjFromPythonConfig(reader.result)
        this.updateStoreConfig(newConfig)
      }
      reader.readAsText(rawConfigFileHandle)
    }
    this.setState({ dropzoneActive: false })
  }

  onSaveClick = () => {
    // generates config.ini file for local save
    const { config } = this.props
    const configOutput = config.pythonConfig.reduce((config, line) => {
      let configTemp = config
      configTemp += `${line}\n`
      return configTemp
    }, `# config automatically generated from kcauto frontend (v${process.version})\n\n`)
    const configBlob = new Blob([configOutput], { type: 'text/plain;charset=utf-8' })
    saveAs(configBlob, 'config.ini', true)
  }

  updateStoreConfig = (config) => {
    // method that updates the BodyConfig state
    const {
      setJsonConfig,
      setPythonConfig,
    } = this.props
    setJsonConfig(config)
    setPythonConfig(config)
  }

  updateSwitch = (config, event, checked, field) => {
    const updatedConfig = config
    updatedConfig[field] = checked
    this.updateStoreConfig(updatedConfig)
  }

  updateText = (config, event, field) => {
    const updatedConfig = config
    updatedConfig[field] = event.target.value
    this.updateStoreConfig(updatedConfig)
  }

  updateSelect = (config, value, field) => {
    const updatedConfig = config
    updatedConfig[field] = value
    this.updateStoreConfig(updatedConfig)
  }

  updateTime = (config, time, field) => {
    const updatedConfig = config
    updatedConfig[field] = time
    this.updateStoreConfig(updatedConfig)
  }

  updateObject = (config, obj) => {
    const updatedConfig = { ...config, ...obj }
    this.updateStoreConfig(updatedConfig)
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
              <BodyConfigGeneralContainer
                updateText={this.updateText}
                updateSelect={this.updateSelect} />

              <Divider />

              <BodyConfigScheduledSleepContainer
                updateSwitch={this.updateSwitch}
                updateText={this.updateText}
                updateTime={this.updateTime} />

              <Divider />

              <BodyConfigScheduledStopContainer
                updateSwitch={this.updateSwitch}
                updateText={this.updateText}
                updateSelect={this.updateSelect}
                updateTime={this.updateTime} />

              <Divider />

              <BodyConfigExpeditionsContainer
                updateSwitch={this.updateSwitch}
                updateSelect={this.updateSelect} />

              <Divider />

              <BodyConfigPvPContainer
                updateSwitch={this.updateSwitch}
                updateSelect={this.updateSelect}
                updateObject={this.updateObject} />

              <Divider />

              <BodyConfigCombatContainer
                updateSwitch={this.updateSwitch}
                updateSelect={this.updateSelect}
                updateTime={this.updateTime}
                updateObject={this.updateObject} />

              <Divider />

              <BodyConfigEventResetContainer
                updateSwitch={this.updateSwitch}
                updateSelect={this.updateSelect} />

              <Divider />

              <BodyConfigShipSwitcherContainer
                updateSwitch={this.updateSwitch}
                updateSelect={this.updateSelect}
                updateObject={this.updateObject} />

              <Divider />

              <BodyConfigQuestsContainer
                updateSwitch={this.updateSwitch}
                updateObject={this.updateObject} />
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper className={classes.paper} elevation={0}>
              <Typography variant='h5' className={classes.flexReset}>
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
