import { connect } from 'react-redux'

import Localize from 'components/Localize'


const mapStateToProps = state => (
  {
    ui: state.ui,
  }
)

export default connect(mapStateToProps)(Localize)
