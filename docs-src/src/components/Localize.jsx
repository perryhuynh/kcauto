import PropTypes from 'prop-types'

import localizations from 'localizations'


const getLocalizedField = (field, lang) => (
  field.split('.').reduce((a, b) => (a && a[b]) || null, localizations[lang])
)

const Localize = ({ ui, field }) => {
  const lang = ui.language
  const langFallback = 'en'
  return getLocalizedField(field, lang) || getLocalizedField(field, langFallback)
}

Localize.propTypes = {
  ui: PropTypes.object.isRequired,
  field: PropTypes.string.isRequired,
}

export default Localize
