import { en } from 'localizations/en'
import { kr } from 'localizations/kr'

const localizations = {
  en,
  kr,
}

export const availableLocalizations = Object.keys(localizations).sort()

export default localizations
