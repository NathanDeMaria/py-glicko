import { ISeasons, ITeamRating, IWeeklyResult } from './interfaces';

const API_ROOT = 'http://localhost:5000';


export class Api {
  public async getSeasons(league: string): Promise<ISeasons> {
    return await this.get<ISeasons>(`${league}/seasons`);
  }

  public async getWeeklyUpdate(league: string, season: number, week: number): Promise<IWeeklyResult>{
    return await this.get<IWeeklyResult>(`${league}/ratings/${season}/${week}`);
  }

  public async getTeamHistory(league: string, team: string): Promise<ITeamRating[]> {
    return [
        {mean: 1, variance: 1, season: 2018, round: 1},
        {mean: 2, variance: 1, season: 2018, round: 2},
        {mean: 3, variance: 1, season: 2018, round: 3},
        {mean: 4, variance: 1, season: 2018, round: 4},
      ];
  }

  private async get<T>(path: string): Promise<T> {
    const response = await fetch(`${API_ROOT}/${path}`);
    if (!response.ok) {
      throw new Error(`GET: ${path} failed because: ${response.statusText}`);
    }
    return response.json();
  }
}
