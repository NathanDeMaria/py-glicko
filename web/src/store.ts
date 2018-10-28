import { applyMiddleware, compose, createStore } from 'redux';
import thunkMiddleware from 'redux-thunk';

import combinedReducer from 'src/reducers';

// @ts-ignore
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export default function configureStore() {
  return createStore(
    combinedReducer,
    {},
    composeEnhancers(applyMiddleware(thunkMiddleware))
  );
};
