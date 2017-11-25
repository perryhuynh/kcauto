import { combineReducers } from 'redux'
import { mode } from 'reducers/ui/mode'
import { language } from 'reducers/ui/language'

export default combineReducers({
  mode,
  language,
})
