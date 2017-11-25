import * as types from 'types/'

export const jsonConfig = (state = {}, action) => {
  switch (action.type) {
    case types.SET_JSON_CONFIG:
      return action.config
    default:
      return state
  }
}

export const pythonConfig = (state = [], action) => {
  switch (action.type) {
    case types.SET_PYTHON_CONFIG:
      return action.config
    default:
      return state
  }
}
