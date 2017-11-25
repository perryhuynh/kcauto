import 'babel-polyfill'
import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { createStore, applyMiddleware, compose } from 'redux'
import thunk from 'redux-thunk'
import { createLogger } from 'redux-logger'

import Grid from 'material-ui/Grid'

import { getUIMode } from 'actions/ui/mode'
import { setUILanguage } from 'actions/ui/language'
import Reducers from 'reducers/'
import Menu from 'components/Menu'
import Body from 'components/Body'

let store = Reducers

const reduxMiddleware = process.env.NODE_ENV === 'production' ?
  applyMiddleware(thunk) :
  applyMiddleware(thunk, createLogger())

store = compose(reduxMiddleware)(createStore)(store)

store.dispatch(getUIMode())
store.dispatch(setUILanguage('english'))

render(
  <Provider store={store}>
    <Grid container>
      <Menu />
      <Body />
    </Grid>
  </Provider>,
  document.getElementById('app')
)
