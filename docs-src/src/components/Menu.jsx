import React, { PureComponent } from 'react'
import { withStyles } from 'material-ui/styles'
import PropTypes from 'prop-types'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import MuiMenu, { MenuItem } from 'material-ui/Menu'
import Typography from 'material-ui/Typography'
import IconButton from 'material-ui/IconButton'
import { Ferry, Earth, GithubCircle, Discord } from 'mdi-material-ui'

import * as urls from 'urls'
import { availableLocalizations } from 'localizations'

const styles = () => ({
  root: {
    width: '100%',
  },
  flex: {
    flex: 1,
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
    this.props.setUILanguage(language)
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
    const dropdownOpen = Boolean(languageDropdownAnchor)
    return (
      <div className={classes.root}>
        <AppBar position='static'>
          <Toolbar>
            <Typography variant='title' color='inherit' className={classes.flex}>
              <Ferry /> kcauto-kai
            </Typography>

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
              <IconButton color='inherit' title='kcauto-kai Discord'>
                <Discord className={classes.largeIcon} />
              </IconButton>
            </a>

            <a href={urls.GITHUB_LINK} className={classes.menuLink}>
              <IconButton color='inherit' title='kcauto-kai Github'>
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
