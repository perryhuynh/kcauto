import { combineReducers } from 'redux'
import ui from 'reducers/ui'
import config from 'reducers/config'

const Reducers = combineReducers({
  ui,
  config,
})

export default Reducers
