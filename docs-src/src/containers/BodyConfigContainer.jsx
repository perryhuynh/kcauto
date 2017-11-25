import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import { setJsonConfig, setPythonConfig } from 'actions/config'
import BodyConfig from 'components/BodyConfig'


const mapStateToProps = state => (
  {
    ui: state.ui,
    config: state.config,
  }
)

const mapDispatchToProps = dispatch => (
  bindActionCreators({
    setJsonConfig,
    setPythonConfig,
  }, dispatch)
)

export default connect(mapStateToProps, mapDispatchToProps)(BodyConfig)
