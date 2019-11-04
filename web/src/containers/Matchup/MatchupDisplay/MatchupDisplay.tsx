import * as React from 'react';

import { IMatchup } from 'src/interfaces';

export interface IStateProps {
  team1: string,
  team2: string,
  matchup: IMatchup | null,
};


export default class extends React.Component<IStateProps, {}> {
  public render() {
    if (!this.props.matchup) {
      return null;
    }
    return (
      <div>
        <h2>{this.props.team1} over {this.props.team2}</h2>
        <p>{this.props.matchup.winProbability.toFixed(3)}</p>
      </div>
    );
  }
}
