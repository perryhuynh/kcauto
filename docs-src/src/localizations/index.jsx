import { en } from 'localizations/en'
import { kr } from 'localizations/kr'

const localizations = {
  en,
  kr,
}

export const availableLocalizations = Object.keys(localizations).reduce((localizationsObj, localization) => {
  const tempLocalizationsObj = localizationsObj
  tempLocalizationsObj[localization] = localizations[localization].label
  return tempLocalizationsObj
}, {})

export default localizations
