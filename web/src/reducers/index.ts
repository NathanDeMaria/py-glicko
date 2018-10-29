import { combineReducers } from 'redux';

import { IWeeklyUpdateAction } from 'src/actions/actionCreators';
import { SUCCESS_GET_WEEKLY_UPDATE } from 'src/actions/actionTypes';
import { IWeeklyResultState } from 'src/interfaces';


function weeklyUpdate(state: IWeeklyResultState = {}, action: IWeeklyUpdateAction): IWeeklyResultState {
  switch (action.type) {
    case SUCCESS_GET_WEEKLY_UPDATE:
      const {
        season,
        round,
        results,
      } = action.payload;
      return {
        [season]: {
          [round]: results,
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
