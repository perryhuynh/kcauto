import { combineReducers } from 'redux'
import { jsonConfig, pythonConfig } from 'reducers/config/config'

export default combineReducers({
  jsonConfig,
  pythonConfig,
})
