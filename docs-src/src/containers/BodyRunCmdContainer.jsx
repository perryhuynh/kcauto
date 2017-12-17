import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import { setSikuliPath, setKCAutoKaiPath } from 'actions/runCmd'
import BodyRunCmd from 'components/BodyRunCmd'


const mapStateToProps = state => (
  {
    ui: state.ui,
    runCmd: state.runCmd,
  }
)

const mapDispatchToProps = dispatch => (
  bindActionCreators({
    setSikuliPath,
    setKCAutoKaiPath,
  }, dispatch)
)

export default connect(mapStateToProps, mapDispatchToProps)(BodyRunCmd)
