import { ThunkDispatch } from 'redux-thunk';

import { Api } from 'src/api';
import { IAppState, ITeamRating, ITeamRoundResult } from 'src/interfaces';
import {
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
    dispatch({
      payload: {
        history: [
          {mean: 1, variance: 1, season: 2018, round: 1},
          {mean: 1, variance: 1, season: 2018, round: 2},
          {mean: 1, variance: 1, season: 2018, round: 3},
          {mean: 1, variance: 1, season: 2018, round: 4},
        ],
        league,
        team,
      },
      type: SUCCESS_GET_TEAM_HISTORY,
    })
  };
};
