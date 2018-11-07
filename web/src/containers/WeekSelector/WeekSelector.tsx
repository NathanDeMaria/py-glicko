import * as React from "react";

import Menu, { MenuItem, SubMenu } from 'rc-menu';
import { Link } from 'react-router-dom';

import 'rc-menu/assets/index.css';


export interface IStateProps {
  seasons: {
    [key: number]: number[],
  }
};

interface IDispatchProps {
  getSeasons: () => void,
};
 
type Props = IStateProps & IDispatchProps;


export class WeekSelector extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.getSeasons();
  }

  public render() {
    return (
      <Menu style={{width: 200}}>
        <SubMenu title="Pick Round">
        {Object.keys(this.props.seasons).map(s => (
          <SubMenu title={s}>
            {this.props.seasons[s].map((week: number) => (
              <MenuItem>
                <Link
                  style={{color: "black", textDecoration: "none"}}
                  to={`/weekly/season/${s}/round/${week}`}
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
