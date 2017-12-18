import { combineReducers } from 'redux'
import ui from 'reducers/ui'
import config from 'reducers/config'
import runCmd from 'reducers/runCmd'

const Reducers = combineReducers({
  ui,
  config,
  runCmd,
})

export default Reducers
