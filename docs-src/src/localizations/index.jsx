import { en } from 'localizations/en'
import { kr } from 'localizations/kr'

const localizations = {
  en,
  kr,
}

export const availableLocalizations = Object.keys(localizations).reduce((localizationsObj, localization) => {
  // function to return an object of the specified localizations with the country code as the key and the localization
  // file's label as its value
  const tempLocalizationsObj = localizationsObj
  tempLocalizationsObj[localization] = localizations[localization].label
  return tempLocalizationsObj
}, {})

export default localizations
