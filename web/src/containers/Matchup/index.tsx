import * as React from 'react';

import MatchupDisplay from './MatchupDisplay';
import TeamSelector from './TeamSelector';

interface IProps {
  league: string,
}

export default class extends React.Component<IProps, {}> {
  public render() {
    return (
      <div>
        <TeamSelector league={this.props.league} />
        <MatchupDisplay />
      </div>
    );
  }
}
