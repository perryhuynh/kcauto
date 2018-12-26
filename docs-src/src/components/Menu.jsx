import React, { PureComponent } from 'react'
import { withStyles } from '@material-ui/core/styles'
import PropTypes from 'prop-types'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import MuiMenu from '@material-ui/core/Menu'
import MenuItem from '@material-ui/core/MenuItem'
import Typography from '@material-ui/core/Typography'
import IconButton from '@material-ui/core/IconButton'
import {
  Ferry, WalletGiftcard, Earth, GithubCircle, Discord,
} from 'mdi-material-ui'

import * as urls from 'urls'
import { availableLocalizations } from 'localizations'

const styles = () => ({
  root: {
    width: '100%',
  },
  flex: {
    flex: 1,
  },
  icon: {
    width: 20,
    height: 20,
    paddingRight: 3,
  },
  support: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    paddingRight: 20,
    fontFamily: 'Roboto, sans-serif',
    fontSize: 12,
  },
  link: {
    color: '#fff',
    fontWeight: 'bold',
    textDecoration: 'none',
  },
  langaugeButton: {
    width: 'auto',
    marginRight: 10,
    fontFamily: 'Roboto, sans-serif',
    fontSize: 14,
  },
  selected: {
    fontWeight: 'bold',
  },
  largeIcon: {
    width: 30,
    height: 30,
  },
  menuLink: {
    color: '#fff',
  },
})

class Menu extends PureComponent {
  state = {
    languageDropdownAnchor: null,
  }

  handleChangeLanguage = (language) => {
    const { setUILanguage } = this.props
    setUILanguage(language)
    this.setState({ languageDropdownAnchor: null })
  }

  render = () => {
    const {
      classes,
      ui,
    } = this.props
    const {
      languageDropdownAnchor,
    } = this.state

    const renderSupportIcon = () => <WalletGiftcard className={classes.icon} />
    const renderPatreonLink = () => <a href={urls.PATREON_LINK} className={classes.link}>Patreon</a>
    const renderSupportText = () => <span>support the dev on {renderPatreonLink()}</span>
    const dropdownOpen = Boolean(languageDropdownAnchor)
    return (
      <div className={classes.root}>
        <AppBar position='static'>
          <Toolbar>
            <Typography variant='h6' color='inherit' className={classes.flex}>
              <Ferry /> kcauto
            </Typography>

            <div className={classes.support}>
              {renderSupportIcon()}
              {renderSupportText()}
            </div>
            <IconButton
              color='inherit'
              className={classes.langaugeButton}
              onClick={event => this.setState({ languageDropdownAnchor: event.currentTarget })}
              title='change webUI language'
            >
              <Earth className={classes.largeIcon} /> {availableLocalizations[ui.language]}
            </IconButton>
            <MuiMenu
              id='languageDropdown'
              anchorEl={languageDropdownAnchor}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'center',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'center',
              }}
              open={dropdownOpen}
            >
              {Object.keys(availableLocalizations).map(localization => (
                <MenuItem
                  key={localization}
                  onClick={() => this.handleChangeLanguage(localization)}
                  className={localization === ui.language ? classes.selected : null}
                >
                  {availableLocalizations[localization]}
                </MenuItem>
              ))}
            </MuiMenu>

            <a href={urls.DISCORD_LINK} className={classes.menuLink}>
              <IconButton color='inherit' title='kcauto Discord'>
                <Discord className={classes.largeIcon} />
              </IconButton>
            </a>

            <a href={urls.GITHUB_LINK} className={classes.menuLink}>
              <IconButton color='inherit' title='kcauto Github'>
                <GithubCircle className={classes.largeIcon} />
              </IconButton>
            </a>
          </Toolbar>
        </AppBar>
      </div>
    )
  }
}

Menu.propTypes = {
  classes: PropTypes.object.isRequired,
  ui: PropTypes.object.isRequired,
  setUILanguage: PropTypes.func.isRequired,
}

export default withStyles(styles)(Menu)
