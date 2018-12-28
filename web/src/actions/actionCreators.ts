import { ThunkDispatch } from 'redux-thunk';

import { Api } from 'src/api';
import {
  IAppState,
  ITeamRating,
  ITeamRoundResult,
} from 'src/interfaces';
import {
  SUCCESS_GET_LEAGUES,
  SUCCESS_GET_SEASONS,
  SUCCESS_GET_TEAM_HISTORY,
  SUCCESS_GET_WEEKLY_UPDATE,
} from './actionTypes';

export interface IWeeklyUpdateAction {
  payload: {
    results: ITeamRoundResult[],
    round: number,
    season: number,
  },
  type: string,
};

export const getWeeklyUpdate = (league: string, season: number, round: number) => {
  // TODO: do better than the any type param here
  return (dispatch: any) => {
    (new Api()).getWeeklyUpdate(league, season, round)
      .then(results => dispatch({
        payload: {
          results,
          round,
          season,
        },
        type: SUCCESS_GET_WEEKLY_UPDATE,
      }));
  };
};

export interface IWeekSelectorPayload {
  payload: {
    league: string,
    seasons: {
      [key: number]: number[],
    },
  }
  type: string,
};

export const getSeasons = (league: string) => {
  return (dispatch: ThunkDispatch<IAppState, void, IWeekSelectorPayload>) => {
    (new Api()).getSeasons(league)
      .then(seasons => dispatch({
        payload: {
          league,
          seasons,
        },
        type: SUCCESS_GET_SEASONS,
      }));
  }
};

export interface ITeamHistoryPayload {
  payload: {
    history: ITeamRating[],
    league: string,
    team: string,
  }
  type: string,
};

export const getTeamHistory = (league: string, team: string) => {
  return (dispatch: ThunkDispatch<IAppState, void, ITeamHistoryPayload>) => {
    (new Api()).getTeamHistory(league, team)
      .then(history => dispatch({
        payload: {
          history,
          league,
          team,
        },
        type: SUCCESS_GET_TEAM_HISTORY,
      }));
  };
};

export interface ILeaguesPayload {
  payload: {
    leagues: string[],
  },
  type: string,
};

export const getLeagues = () => {
  return (dispatch: ThunkDispatch<IAppState, void, ILeaguesPayload>) => {
    (new Api()).getLeagues()
      .then(leagues => dispatch({
        payload: {
          leagues,
        },
        type: SUCCESS_GET_LEAGUES,
      }));
  }
}
