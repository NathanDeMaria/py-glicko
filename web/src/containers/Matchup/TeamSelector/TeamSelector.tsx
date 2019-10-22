import * as React from 'react';
import Select from 'react-select';


export interface IOwnProps {
  league: string,
}

export interface IStateProps {
  teams: string[],
};
     
interface IDispatchProps {
  getTeams: () => void,
  getMatchup: (team1: string, team2: string) => void,
}
 
type Props = IStateProps & IDispatchProps & IOwnProps;


interface IOption {
  value: string,
  label: string,
}


export default class extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.getTeams();
  }

  public render() {
    return (
      <div>
        <Select
          options={this.props.teams.map(t => ({
            label: t,
            value: t.replace(/\s/g, ''),
          }))}
          onChange={this.handleTeam1Change}
        />
        <Select
          options={this.props.teams.map(t => ({
            label: t,
            value: t.replace(/\s/g, ''),
          }))}
          onChange={this.handleTeam2Change}
        />
        {/* <button onClick={this.getMatchup}>
          GET MATCHUP
        </button> */}
      </div>
    );
  }

  private handleTeam1Change = (selected: IOption) => {
    this.setState({team1: selected.value});
  }

  private handleTeam2Change = (selected: IOption) => {
    this.setState({team2: selected.value});
  }

//   private getMatchup = () => {
//     this.props.getMatchup(this.props.team1, this.state.team2);
//   }
}
