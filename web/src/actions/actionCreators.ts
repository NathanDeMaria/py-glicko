import { Api } from 'src/api';
import { ITeamRoundResult } from 'src/interfaces';
import {
  SUCCESS_GET_SEASONS,
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

export interface IWeekSelectorAction {
  payload: {
    seasons: {
      [key: number]: number[],
    },
  }
  type: string,
};

export const getWeeklyUpdate = (league: string, season: number, round: number) => {
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

export const getSeasons = (league: string) => {
  return (dispatch: any) => {
    (new Api()).getSeasons(league)
      .then(seasons => dispatch({
        payload: {
          seasons,
        },
        type: SUCCESS_GET_SEASONS,
      }));
  }
};
