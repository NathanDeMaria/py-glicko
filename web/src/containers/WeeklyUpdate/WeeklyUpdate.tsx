import * as React from 'react';

import { IGameResult, ITeamRoundResult } from 'src/interfaces';


export interface IOwnProps {
  league: string,
  season: number,
  round: number,
}

export interface IStateProps {
  weekResults: ITeamRoundResult[],
};
     
interface IDispatchProps {
  getWeeklyUpdate: (league: string, season: number, round: number) => void,
}
 
type Props = IStateProps & IDispatchProps & IOwnProps

function renderRoundResult(teamRoundResult: ITeamRoundResult, i: number) {
  const rankChange = teamRoundResult.previousRanking - teamRoundResult.ranking;
  const rankChangeText = rankChange > 0 ? `+${rankChange}` : (rankChange < 0 ? rankChange : '');

  let record = `${teamRoundResult.wins}-${teamRoundResult.losses}`;
  if (teamRoundResult.ties) {
    record += `-${teamRoundResult.ties}`;
  }

  const ratingChange = teamRoundResult.rating - teamRoundResult.previousRating;

  return (
    <tr key={i}>
      <td>{i+1}</td>
      <td>{teamRoundResult.team} ({record})</td>
      <td>{teamRoundResult.rating.toFixed(2)}</td>
      <td>{teamRoundResult.variance.toFixed(2)}</td>
      <td>{rankChangeText} ({ratingChange.toFixed(2)})</td>
      <td>
        <ul>
          {teamRoundResult.gameResults.map(renderGame)}
        </ul>
      </td>
    </tr>
  );
}

function renderGame(game: IGameResult, i: number) {
  const resultText = game.score > game.opponentScore ? 'Win' : (game.score < game.opponentScore ? 'Loss' : 'Tie');
  return <li key={i}>
    {resultText} vs. {game.opponent} {game.score}-{game.opponentScore}
  </li>
}

export class WeeklyUpdate extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.getWeeklyUpdate(this.props.league, this.props.season, this.props.round);
  }

  public render() {
    return (
      <div>
        <h1>{this.props.season} - {this.props.round}</h1>
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Team</th>
              <th>Rating</th>
              <th>Variance</th>
              <th>Change</th>
              <th>Results</th>
            </tr>
          </thead>
          <tbody>
            {this.props.weekResults ? this.props.weekResults.map(renderRoundResult) : null}
          </tbody>
        </table>
      </div>
    );
  }
}
