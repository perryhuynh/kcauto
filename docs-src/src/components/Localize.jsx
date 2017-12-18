import PropTypes from 'prop-types'

import localizations from 'localizations'


const getLocalizedField = (field, lang) => (
  // function to return the value stored for the field in the specified language from the localizations object
  field.split('.').reduce((a, b) => (a && a[b]) || null, localizations[lang])
)

const Localize = ({ ui, field }) => {
  // object that returns the string or JSX for the specified field for the specified language; falls back to the english
  // version of the string if it is not specified in the specified language
  const lang = ui.language
  const langFallback = 'en'
  return getLocalizedField(field, lang) || getLocalizedField(field, langFallback)
}

Localize.propTypes = {
  ui: PropTypes.object.isRequired,
  field: PropTypes.string.isRequired,
}

export default Localize
