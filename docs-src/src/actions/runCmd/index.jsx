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

export const setKCAutoKaiPathSuccess = kcautoKaiPath => (
  {
    type: types.SET_KCAUTO_KAI_PATH,
    kcautoKaiPath,
  }
)

export const setKCAutoKaiPath = kcautoKaiPath => (
  dispatch => (
    dispatch(setKCAutoKaiPathSuccess(kcautoKaiPath))
  )
)
