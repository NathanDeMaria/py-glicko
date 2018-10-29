import * as React from 'react';

import { ITeamRoundResult } from 'src/interfaces';


export interface IOwnProps {
  season: number,
  round: number,
}

export interface IStateProps {
  weekResults: ITeamRoundResult[],
};
     
interface IDispatchProps {
  getWeeklyUpdate: (season: number, round: number) => void,
}
 
type Props = IStateProps & IDispatchProps & IOwnProps

function renderRoundResult(teamRoundResult: ITeamRoundResult) {
  return (
    <li key={teamRoundResult.team}>{teamRoundResult.team}</li>
  );
}

export class WeeklyUpdate extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.getWeeklyUpdate(this.props.season, this.props.round);
  }

  public render() {
    return (
      <div>
        <h1>{this.props.season} - {this.props.round}</h1>
        <ul>
          {this.props.weekResults ? this.props.weekResults.map(renderRoundResult) : null}
        </ul>
        <p>Results will go here</p>
      </div>
    );
  }
}
