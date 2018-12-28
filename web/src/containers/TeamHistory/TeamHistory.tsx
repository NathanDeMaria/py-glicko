import * as React from 'react';

import { ITeamRating } from 'src/interfaces';

import HistoryChart from './HistoryChart';
import TeamPicker from './TeamPicker';

export interface IOwnProps {
  league: string,
  team: string,
}

export interface IStateProps {
  history: ITeamRating[],
};
 
type Props = IStateProps & IOwnProps

export default class extends React.Component<Props, {}> {
  public render() {
    return (
      <div>
        <h1>{this.props.team}</h1>
        <TeamPicker league={this.props.league} />
        <HistoryChart league={this.props.league} />
      </div>
    );
  }
}
