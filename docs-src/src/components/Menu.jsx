import React, { Component } from 'react'
import { withStyles } from 'material-ui/styles'
import PropTypes from 'prop-types'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import MuiMenu, { MenuItem } from 'material-ui/Menu'
import Typography from 'material-ui/Typography'
import IconButton from 'material-ui/IconButton'
import { Ferry, Earth, GithubCircle, Discord } from 'mdi-material-ui'

import * as urls from 'urls'

const styles = () => ({
  root: {
    width: '100%',
  },
  flex: {
    flex: 1,
  },
  langaugeButton: {
    fontFamily: 'Roboto, sans-serif',
    fontSize: '14px',
  },
  largeIcon: {
    width: 30,
    height: 30,
  },
})

class Menu extends Component {
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
            <Typography type='title' color='inherit' className={classes.flex}>
              <Ferry /> kcauto-kai
            </Typography>

            <IconButton
              color='contrast'
              className={classes.langaugeButton}
              onClick={event => this.setState({ languageDropdownAnchor: event.currentTarget })}
            >
              <Earth className={classes.largeIcon} /> {ui.language.toUpperCase()}
            </IconButton>
            <MuiMenu
              id='languageDropdown'
              anchorEl={languageDropdownAnchor}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={dropdownOpen}
              onRequestClose={() => this.setState({ languageDropdownAnchor: null })}
            >
              <MenuItem onClick={() => this.handleChangeLanguage('en')}>EN</MenuItem>
              <MenuItem onClick={() => this.handleChangeLanguage('kr')}>KR</MenuItem>
            </MuiMenu>

            <a href={urls.DISCORD_LINK}>
              <IconButton color='contrast'><Discord className={classes.largeIcon} /></IconButton>
            </a>
            <a href={urls.GITHUB_LINK}>
              <IconButton color='contrast'><GithubCircle className={classes.largeIcon} /></IconButton>
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
