import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import { setSikuliPath, setKCAutoPath } from 'actions/runCmd'
import BodyRunCmd from 'components/BodyRunCmd'


const mapStateToProps = state => (
  {
    sikuliPath: state.runCmd.sikuliPath,
    kcautoPath: state.runCmd.kcautoPath,
  }
)

const mapDispatchToProps = dispatch => (
  bindActionCreators({
    setSikuliPath,
    setKCAutoPath,
  }, dispatch)
)

export default connect(mapStateToProps, mapDispatchToProps)(BodyRunCmd)
