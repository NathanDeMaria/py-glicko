import { ISeasons, IWeeklyResult } from './interfaces';

const API_ROOT = 'http://localhost:5000';


export class Api {
  public async getSeasons(): Promise<ISeasons> {
    return await this.get<ISeasons>('seasons');
  }

  public async getWeeklyUpdate(season: number, week: number): Promise<IWeeklyResult>{
    return await this.get<IWeeklyResult>(`ratings/${season}/${week}`);
  }

  private async get<T>(path: string): Promise<T> {
    const response = await fetch(`${API_ROOT}/${path}`);
    if (!response.ok) {
      throw new Error(`GET: ${path} failed because: ${response.statusText}`);
    }
    return response.json();
  }
}
