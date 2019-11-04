import {
  ISeason,
  ITeamRating,
  IWeeklyResult,
} from './interfaces';

const API_ROOT = 'http://localhost:5000';


export class Api {
  public async getSeasons(league: string): Promise<ISeason> {
    return await this.get<ISeason>(`${league}/seasons`);
  }

  public async getWeeklyUpdate(league: string, season: number, week: number): Promise<IWeeklyResult>{
    return await this.get<IWeeklyResult>(`${league}/ratings/${season}/${week}`);
  }

  public async getTeamHistory(league: string, team: string): Promise<ITeamRating[]> {
    return await this.get<ITeamRating[]>(`${league}/team/${team}`);
  }

  public async getLeagues(): Promise<string[]> {
    return await this.get<string[]>('leagues');
  }

  public async getTeams(league: string): Promise<string[]> {
    return await this.get<string[]>(`${league}/teams`);
  }

  public async getWinProbability(league: string, team1: string, team2: string): Promise<number> {
    return await this.get<number>(`${league}/team1/${team1}/team2/${team2}`);
  }

  private async get<T>(path: string): Promise<T> {
    const response = await fetch(`${API_ROOT}/${path}`);
    if (!response.ok) {
      throw new Error(`GET: ${path} failed because: ${response.statusText}`);
    }
    return response.json();
  }
}
