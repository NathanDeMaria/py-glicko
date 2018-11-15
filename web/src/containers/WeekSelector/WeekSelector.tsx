import * as React from "react";

import Menu, { MenuItem, SubMenu } from 'rc-menu';
import { Link } from 'react-router-dom';

import 'rc-menu/assets/index.css';


export interface IOwnProps {
  league: string,
};

export interface IStateProps {
  seasons: {
    [key: number]: number[],
  },
};

interface IDispatchProps {
  getSeasons: (league: string) => void,
};
 
type Props = IStateProps & IDispatchProps & IOwnProps;


export class WeekSelector extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.getSeasons(this.props.league);
  }

  public render() {
    return (
      <Menu style={{width: 200}}>
        <SubMenu title="Pick Round">
        {Object.keys(this.props.seasons).map(s => (
          <SubMenu title={s} key={s}>
            {this.props.seasons[s].map((week: number) => (
              <MenuItem key={week}>
                <Link
                  style={{color: "black", textDecoration: "none"}}
                  to={`/${this.props.league}/weekly/season/${s}/round/${week}`}
                >
                  {week}
                </Link>
              </MenuItem>
            ))}
          </SubMenu>
        ))}
        </SubMenu>
      </Menu>
    );
  }
}
