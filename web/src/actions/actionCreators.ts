import { ITeamRoundResult } from 'src/interfaces';
import { SUCCESS_GET_WEEKLY_UPDATE } from './actionTypes';

export interface IWeeklyUpdateAction {
  payload: {
    results: ITeamRoundResult[],
    round: number,
    season: number,
  },
  type: string,
};

export const getWeeklyUpdate = (season: number, round: number): IWeeklyUpdateAction => ({
  payload: {
    results: [{
      team: "Nebraska Cornhuskers",
      rating: 2000,
      variance: 1,
      wins: 12,
      losses: 0,
      ties: 0,
      ranking: 1,
      previousRanking: 1,
      gameResults: [{
        opponent: "Ohio State Buckeyes",
        score: 100,
        opponentScore: 1,
      }],
    }],
    round,
    season,
  },
  type: SUCCESS_GET_WEEKLY_UPDATE,
});
