import * as types from 'types/'

export const mode = (state = 'file', action) => {
  switch (action.type) {
    case types.SET_UI_MODE:
      return action.mode
    default:
      return state
  }
}
