import * as React from "react";

import { Link } from 'react-router-dom';

import { ChangeEvent } from 'react';


export interface IOwnProps {
  league: string,
};

export interface IStateProps {
  defaultWeeks: number[],
  seasons: {
    [key: number]: number[],
  },
};

interface IDispatchProps {
  getSeasons: (league: string) => void,
};
 
type Props = IStateProps & IDispatchProps & IOwnProps;

interface IComponentState {
  selectedSeason: string | null,
}


export class WeekSelector extends React.Component<Props, IComponentState> {
  public state = {
    selectedSeason: null,
  }

  public componentDidMount() {
    this.props.getSeasons(this.props.league);
  }

  public render() {
    if (!this.props.seasons) { return null };
    const seasons = Object.keys(this.props.seasons);
    return (
      <div style={{padding: "20px"}}>
        {this.renderSeasonList()}
        <select
          style={{display: "inline"}}
          onChange={this.handleChanged}
          defaultValue={this.getDefaultSeason()}
        >
          {seasons.map(s => (
            <option value={s}>{s}</option>
          ))}
        </select>
      </div>
    );
  }

  private handleChanged = (e: ChangeEvent<HTMLSelectElement>) => {
    const selectedSeason = e.currentTarget.value;
    this.setState({selectedSeason});
  }

  private renderSeasonList() {
    const season = this.state.selectedSeason || this.getDefaultSeason();
    const currentSeason = season == null ? this.props.defaultWeeks : this.props.seasons[season];
    return (
      <ul style={{display: "inline"}}>
        {currentSeason.map(w => (
          <li style={{display: "inline", padding: "5px"}}>
            <Link
              style={{color: "black", textDecoration: "none"}}
              to={`/${this.props.league}/weekly/season/${season}/round/${w}`}
            >
              {w}
            </Link>
          </li>
        ))}
      </ul>
    )
  }

  private getDefaultSeason(): number {
    const seasons = Object.keys(this.props.seasons).map(s => parseInt(s, 10));
    return Math.max(...seasons);
  }
}
