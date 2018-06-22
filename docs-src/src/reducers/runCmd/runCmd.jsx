import * as types from 'types/'

export const sikuliPath = (state = '', action) => {
  switch (action.type) {
    case types.SET_SIKULI_PATH:
      return action.sikuliPath
    default:
      return state
  }
}

export const kcautoPath = (state = '', action) => {
  switch (action.type) {
    case types.SET_KCAUTO_PATH:
      return action.kcautoPath
    default:
      return state
  }
}
