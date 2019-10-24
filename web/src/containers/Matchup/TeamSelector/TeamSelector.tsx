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

interface IComponentState {
  team1: string | null,
  team2: string | null,
}

interface ISelectedTeams {
  team1: string,
  team2: string,
}

export default class extends React.Component<Props, IComponentState> {
  public state = {
    team1: null,
    team2: null,
  }

  public componentDidMount() {
    this.props.getTeams();
  }

  public render() {
    console.log(this.teamsAreSelected());
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
        { this.teamsAreSelected() ? 
          <button onClick={this.getMatchup}>
            GET MATCHUP
          </button>
          : null
        }
      </div>
    );
  }

  private handleTeam1Change = (selected: IOption) => {
    this.setState({team1: selected.value});
  }

  private handleTeam2Change = (selected: IOption) => {
    this.setState({team2: selected.value});
  }

  private getMatchup = () => {
    const selected = this.teamsAreSelected();
    if (selected) {
      const { team1, team2 } = selected;
      this.props.getMatchup(team1, team2);
    }
  }

  private teamsAreSelected = (): ISelectedTeams | null => {
    if (this.state.team1 !== null && this.state.team2 !== null) {
      return {
        team1: this.state.team1!,
        team2: this.state.team2!,
      }
    }
    return null;
  }
}
