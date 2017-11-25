import * as types from 'types/'

export const setUIMode = mode => (
  {
    type: types.SET_UI_MODE,
    mode,
  }
)

export const getUIMode = () => (
  (dispatch) => {
    switch (window.location.protocol) {
      case 'http:':
      case 'https:':
        dispatch(setUIMode('server'))
        break
      case 'file:':
        dispatch(setUIMode('local'))
        break
      default:
        dispatch(setUIMode('file'))
    }
  }
)
