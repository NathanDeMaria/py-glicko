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
  getTeamHistory: (team: string) => void,
}
 
type Props = IStateProps & IDispatchProps & IOwnProps;


interface IOption {
  value: string,
  label: string,
}


export default class extends React.Component<Props, {}> {
  public state = {
    selected: []
  }

  public componentDidMount() {
    this.props.getTeams();
  }

  public render() {
    return (
      <div>
        <Select
          isMulti={true}
          options={this.props.teams.map(t => ({
            label: t,
            value: t.replace(/\s/g, ''),
          }))}
          onChange={this.handleChange}
        />
        <button onClick={this.loadTeams}>
          SHOW ME
        </button>
      </div>
    );
  }

  private handleChange = (selected: IOption[]) => {
    this.setState({selected});
  }

  private loadTeams = () => {
    this.state.selected.map((o: IOption) => this.props.getTeamHistory(o.value));
  }
}
