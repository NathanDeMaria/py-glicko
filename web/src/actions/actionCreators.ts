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
  SUCCESS_GET_TEAMS,
  SUCCESS_GET_WEEKLY_UPDATE,
  SUCCESS_GET_WIN_PROBABILITY,
} from './actionTypes';

export interface IWeeklyUpdateAction {
  payload: {
    league: string,
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
          league,
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

// TODO: shouldGetTeamHistory??
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

export interface ITeamsPayload {
  payload: {
    league: string,
    teams: string[],
  },
  type: string,
}

export const getTeams = (league: string) => {
  return (dispatch: ThunkDispatch<IAppState, void, ITeamsPayload>) => {
    // TODO: don't re-get if it's already in there
    (new Api()).getTeams(league)
      .then(teams => dispatch({
        payload: {
          league,
          teams,
        },
        type: SUCCESS_GET_TEAMS,
      }));
  };
};

export interface IMatchupPayload {
  payload : {
    league: string,
    team1: string,
    team2: string,
    winProbability: number,
  },
  type: string,
}

export const getMatchup = (league: string, team1: string, team2: string) => {
  return (dispatch: ThunkDispatch<IAppState, void, IMatchupPayload>) => {
    (new Api()).getWinProbability(league, team1.replace(/\s/g, ''), team2.replace(/\s/g, ''))
      .then(winProbability => dispatch({
        payload: {
          league,
          team1,
          team2,
          winProbability,
        },
        type: SUCCESS_GET_WIN_PROBABILITY,
      }))
  }
}
