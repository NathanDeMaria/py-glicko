import * as React from 'react';

import HistoryChart from './HistoryChart';
import TeamPicker from './TeamPicker';

interface IProps {
  league: string,
  team: string,
}

export default class extends React.Component<IProps, {}> {
  public render() {
    return (
      <div>
        <TeamPicker league={this.props.league} />
        <HistoryChart league={this.props.league} />
      </div>
    );
  }
}
