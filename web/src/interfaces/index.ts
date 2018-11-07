interface IGameResult {
  opponent: string,
  score: number,
  opponentScore: number,
};

export interface ITeamRoundResult {
  team: string,
  
  rating: number,
  variance: number,
  
  wins: number,
  losses: number,
  ties: number,
  
  ranking: number,
  previousRanking: number,
  gameResults: IGameResult[],
};

export interface IWeeklyResultState {
  [key: number]: {
    [key: number]: ITeamRoundResult[],
  },
};

export interface IWeekSelectorState {
  [key: number]: number[],
};

export interface IAppState {
  // has to match reducer name...for now
  weeklyUpdate: IWeeklyResultState,
  weekSelector: IWeekSelectorState,
};
