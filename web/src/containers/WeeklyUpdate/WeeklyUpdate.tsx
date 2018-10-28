import * as React from 'react';

interface IOwnProps {
  season: number,
  round: number,
}

interface IResult {
  // Whatever will make a row in the "week results" table
  team: string,
  rating: number,
  variance: number,
}

interface IStateProps {
  weekResults: IResult[],
};
     
interface IDispatchProps {
  getWeeklyUpdate: () => void,
}
 
type Props = IStateProps & IDispatchProps & IOwnProps

export default class WeeklyUpdate extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.getWeeklyUpdate()
  }

  public render() {
    return (
      <div>
        <h1>{this.props.season} - {this.props.round}</h1>
        <p>Results will go here</p>
      </div>
    );
  }
}
