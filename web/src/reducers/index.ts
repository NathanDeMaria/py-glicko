import { combineReducers } from 'redux';

import {
  ILeaguesPayload,
  ITeamHistoryPayload,
  ITeamsPayload,
  IWeeklyUpdateAction,
  IWeekSelectorPayload,
} from 'src/actions/actionCreators';
import {
  SUCCESS_GET_LEAGUES,
  SUCCESS_GET_SEASONS,
  SUCCESS_GET_TEAM_HISTORY,
  SUCCESS_GET_TEAMS,
  SUCCESS_GET_WEEKLY_UPDATE,
} from 'src/actions/actionTypes';
import {
  ISeasons,
  ITeamHistories,
  ITeams,
  IWeeklyResult,
} from 'src/interfaces';


function weeklyUpdate(state: IWeeklyResult = {}, action: IWeeklyUpdateAction): IWeeklyResult {
  switch (action.type) {
    case SUCCESS_GET_WEEKLY_UPDATE:
      const {
        league,
        season,
        round,
        results,
      } = action.payload;
      const updated = {
        ...state,
        [league]: {
          [season]: {
            [round]: results,
          },
        },
      };
      return updated;
    default:
      return state;
  };
};

function weekSelector(state: ISeasons = {}, action: IWeekSelectorPayload): ISeasons {
  switch(action.type) {
    case SUCCESS_GET_SEASONS:
      const {payload: {
        seasons: seasonList,
        league,
      }} = action;
      return {
        [league]: seasonList,
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
        ...state,
        [league]: {
          [team]: history,
        },
      }
    default:
      return state;
  };
};

function leagueSelector(state: string[] = [], action: ILeaguesPayload): string[] {
  switch(action.type) {
    case SUCCESS_GET_LEAGUES:
      const { leagues } = action.payload;
      return leagues;
    default:
      return state;
  };
}

function teamsPicker(state: ITeams = {}, action: ITeamsPayload): ITeams {
  switch(action.type) {
    case SUCCESS_GET_TEAMS:
      const { league, teams } = action.payload;
      return {
        ...state,
        [league]: teams,
      };
    default:
      return state;
  }
}

const reducer = combineReducers({
  leagueSelector,
  teamHistory,
  teamsPicker,
  weekSelector,
  weeklyUpdate,
});

export default reducer;
