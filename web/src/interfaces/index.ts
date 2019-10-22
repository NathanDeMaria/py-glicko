export interface IGameResult {
  opponent: string,
  score: number,
  opponentScore: number,
};

export interface ITeamRoundResult {
  team: string,
  
  rating: number,
  variance: number,
  previousRating: number,
  
  wins: number,
  losses: number,
  ties: number,
  
  ranking: number,
  previousRanking: number,
  gameResults: IGameResult[],
};

export interface ITeamRating {
  mean: number,
  variance: number,
  season: number,
  round: number,
};

export interface IWeeklyResult {
  [key: string]: {
    [key: number]: {
      [key: number]: ITeamRoundResult[],
    },
  },
};

export interface ISeason {
  [key: number]: number[],
}

export interface ISeasons {
  [key: string]: ISeason,
};

export interface ITeams {
  [key: string]: string[],
};

export interface ITeamHistories {
  [key: string]: {
    [key: string]: ITeamRating[],
  }
};

export interface IAppState {
  // has to match reducer name...for now
  weeklyUpdate: IWeeklyResult,
  weekSelector: ISeasons,
  teamHistory: ITeamHistories,
  leagueTeams: ITeams,
  leagueSelector: string[],
};
