import { connect } from 'react-redux'

import BodyConfigGeneral from 'components/BodyConfigGeneral'
import BodyConfigScheduledSleep from 'components/BodyConfigScheduledSleep'
import BodyConfigScheduledStop from 'components/BodyConfigScheduledStop'
import BodyConfigExpeditions from 'components/BodyConfigExpeditions'
import BodyConfigPvP from 'components/BodyConfigPvP'
import BodyConfigCombat from 'components/BodyConfigCombat'
import BodyConfigShipSwitcher from 'components/BodyConfigShipSwitcher'
import BodyConfigQuests from 'components/BodyConfigQuests'


const mapStateToProps = state => (
  {
    config: state.config.jsonConfig,
  }
)

export const BodyConfigGeneralContainer = connect(mapStateToProps)(BodyConfigGeneral)
export const BodyConfigScheduledSleepContainer = connect(mapStateToProps)(BodyConfigScheduledSleep)
export const BodyConfigScheduledStopContainer = connect(mapStateToProps)(BodyConfigScheduledStop)
export const BodyConfigExpeditionsContainer = connect(mapStateToProps)(BodyConfigExpeditions)
export const BodyConfigPvPContainer = connect(mapStateToProps)(BodyConfigPvP)
export const BodyConfigCombatContainer = connect(mapStateToProps)(BodyConfigCombat)
export const BodyConfigShipSwitcherContainer = connect(mapStateToProps)(BodyConfigShipSwitcher)
export const BodyConfigQuestsContainer = connect(mapStateToProps)(BodyConfigQuests)
