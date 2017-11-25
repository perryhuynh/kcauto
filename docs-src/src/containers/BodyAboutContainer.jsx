import { connect } from 'react-redux'

import BodyAbout from 'components/BodyAbout'


const mapStateToProps = state => (
  {
    ui: state.ui,
  }
)

export default connect(mapStateToProps)(BodyAbout)
