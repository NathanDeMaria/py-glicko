import { combineReducers } from 'redux';

import {
  ITeamHistoryPayload,
  IWeeklyUpdateAction,
  IWeekSelectorPayload,
} from 'src/actions/actionCreators';
import {
  SUCCESS_GET_SEASONS,
  SUCCESS_GET_TEAM_HISTORY,
  SUCCESS_GET_WEEKLY_UPDATE,
} from 'src/actions/actionTypes';
import {
  ISeasons,
  ITeamHistories,
  IWeeklyResult,
} from 'src/interfaces';


function weeklyUpdate(state: IWeeklyResult = {}, action: IWeeklyUpdateAction): IWeeklyResult {
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

function weekSelector(state: ISeasons = {}, action: IWeekSelectorPayload): ISeasons {
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

function teamHistory(state: ITeamHistories = {}, action: ITeamHistoryPayload): ITeamHistories {
  switch(action.type) {
    case SUCCESS_GET_TEAM_HISTORY:
      const {
        history,
        league,
        team,
      } = action.payload;
      return {
        [league]: {
          [team]: history,
        },
        ...state,
      }
    default:
      return state;
  };
};

const reducer = combineReducers({
  teamHistory,
  weekSelector,
  weeklyUpdate,
});

export default reducer;
