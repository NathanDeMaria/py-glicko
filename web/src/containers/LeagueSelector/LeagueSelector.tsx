import * as React from "react";

import { Link } from 'react-router-dom';


export interface IStateProps {
  leagues: string[],
};

interface IDispatchProps {
  getLeagues: () => void,
};
 
type Props = IStateProps & IDispatchProps;


export class LeagueSelector extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.getLeagues();
  }

  public render() {
    return (
      <ul>
        {this.props.leagues.map((league: string) => (
          <li>
            <Link
              to={`/${league}`}
            >
              {league.toUpperCase()}
            </Link>
          </li>          
        ))}
      </ul>
    );
  }
}
