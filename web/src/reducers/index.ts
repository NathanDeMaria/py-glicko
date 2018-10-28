import { combineReducers } from 'redux';

import { SUCCESS_GET_WEEKLY_UPDATE } from 'src/actions/actionTypes';

interface IState {
  [key: number]: {
    [key: number]: any,
  }
}

// TODO: share this with other relevant places
interface IAction {
  type: string,
  payload: any,
}

function weeklyUpdate(state: IState = {}, action: IAction) {
  switch (action.type) {
    case SUCCESS_GET_WEEKLY_UPDATE:
      const {
        season,
        round,
        results,
      } = action.payload;
      return {
        weeklyResults: {
          [season]: {
            [round]: results,
          },
        },
        ...state,
      };
    default:
      return state;
  };
};

const reducer = combineReducers({
  weeklyUpdate,
});

export default reducer;
