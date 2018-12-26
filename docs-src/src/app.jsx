import 'babel-polyfill'
import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { createStore, applyMiddleware, compose } from 'redux'
import thunk from 'redux-thunk'
import { createLogger } from 'redux-logger'

import Grid from '@material-ui/core/Grid'
import MuiThemeProvider from '@material-ui/core/styles/MuiThemeProvider'
import { createMuiTheme } from '@material-ui/core/styles'
import blueGrey from '@material-ui/core/colors/blueGrey'

import { MuiPickersUtilsProvider } from 'material-ui-pickers'
import DateFnsUtils from '@date-io/date-fns'

import { getUIMode } from 'actions/ui/mode'
import { setUILanguage } from 'actions/ui/language'
import Reducers from 'reducers/'
import MenuContainer from 'containers/MenuContainer'
import Body from 'components/Body'
import Footer from 'components/Footer'


const theme = createMuiTheme({
  typography: {
    useNextVariants: true,
  },
  palette: {
    primary: blueGrey,
    secondary: blueGrey,
    contrastText: blueGrey[50],
    contrastThreshold: 3,
  },
})

let store = Reducers

const reduxMiddleware = process.env.NODE_ENV === 'production'
  ? applyMiddleware(thunk)
  : applyMiddleware(thunk, createLogger())

store = compose(reduxMiddleware)(createStore)(store)

store.dispatch(getUIMode())
store.dispatch(setUILanguage('en'))

render(
  <Provider store={store}>
    <MuiThemeProvider theme={theme}>
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
        <Grid container>
          <MenuContainer />
          <Body />
          <Footer />
        </Grid>
      </MuiPickersUtilsProvider>
    </MuiThemeProvider>
  </Provider>,
  document.getElementById('app')
)
