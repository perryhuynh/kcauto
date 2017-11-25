import * as types from 'types/'

export const setUILanguageSuccess = language => (
  {
    type: types.SET_UI_LANGUAGE,
    language,
  }
)

export const setUILanguage = language => (
  dispatch => (
    dispatch(setUILanguageSuccess(language))
  )
)
