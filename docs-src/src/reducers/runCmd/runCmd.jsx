import * as types from 'types/'

export const sikuliPath = (state = '', action) => {
  switch (action.type) {
    case types.SET_SIKULI_PATH:
      return action.sikuliPath
    default:
      return state
  }
}

export const kcautoKaiPath = (state = '', action) => {
  switch (action.type) {
    case types.SET_KCAUTO_KAI_PATH:
      return action.kcautoKaiPath
    default:
      return state
  }
}
