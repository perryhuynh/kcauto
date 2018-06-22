import * as types from 'types/'

export const setSikuliPathSuccess = sikuliPath => (
  {
    type: types.SET_SIKULI_PATH,
    sikuliPath,
  }
)

export const setSikuliPath = sikuliPath => (
  dispatch => (
    dispatch(setSikuliPathSuccess(sikuliPath))
  )
)

export const setKCAutoPathSuccess = kcautoPath => (
  {
    type: types.SET_KCAUTO_KAI_PATH,
    kcautoPath,
  }
)

export const setKCAutoPath = kcautoPath => (
  dispatch => (
    dispatch(setKCAutoPathSuccess(kcautoPath))
  )
)
