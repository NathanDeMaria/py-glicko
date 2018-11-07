import { combineReducers } from 'redux';

import { IWeeklyUpdateAction, IWeekSelectorAction } from 'src/actions/actionCreators';
import {
  SUCCESS_GET_SEASONS,
  SUCCESS_GET_WEEKLY_UPDATE,
} from 'src/actions/actionTypes';
import { IWeeklyResultState, IWeekSelectorState } from 'src/interfaces';


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

function weekSelector(state: IWeekSelectorState = {}, action: IWeekSelectorAction): IWeekSelectorState {
  switch(action.type) {
    case SUCCESS_GET_SEASONS:
      const {payload: {seasons: seasonList}} = action;
      return {
        ...seasonList,
        ...state,
      }
    default:
      return state;
  };
};

const reducer = combineReducers({
  weekSelector,
  weeklyUpdate,
});

export default reducer;
