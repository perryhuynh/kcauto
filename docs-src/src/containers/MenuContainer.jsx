import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import { setUILanguage } from 'actions/ui/language'
import Menu from 'components/Menu'


const mapStateToProps = state => (
  {
    ui: state.ui,
  }
)

const mapDispatchToProps = dispatch => (
  bindActionCreators({
    setUILanguage,
  }, dispatch)
)

export default connect(mapStateToProps, mapDispatchToProps)(Menu)
