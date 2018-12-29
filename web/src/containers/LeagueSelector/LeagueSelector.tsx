import * as React from "react";

import { Link } from 'react-router-dom';

import './styles.css';

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
      <ul className='navbar'>
        {this.props.leagues.map((league: string, i: number) => (
          <li className='league' key={i}>
            <Link
              className='leagueLink'
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
