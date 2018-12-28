import * as React from 'react';
import {
  CartesianGrid, Scatter, ScatterChart, Tooltip, YAxis,
} from 'recharts';

import { ITeamRating } from 'src/interfaces';

import TeamPicker from './TeamPicker';

export interface IOwnProps {
  league: string,
  team: string,
}

export interface IStateProps {
  history: ITeamRating[],
};
     
interface IDispatchProps {
  getTeamHistory: () => void,
}
 
type Props = IStateProps & IDispatchProps & IOwnProps

function renderTooltip(props: any) {
  // Payload is a list of 1 when I want to display it I guess?
  const {payload: [datum]} = props;
  if (!datum) {
    return null;
  }
  const { payload: {season, round} } = datum;
  return (
    <div>
      <p>Season: {season}</p>
      <p>Round: {round}</p>
    </div>
  );
}

export default class extends React.Component<Props, {}> {
  public state = {
    selected: [],
  }

  public componentDidMount() {
    this.props.getTeamHistory();
  }

  public render() {
    if (!this.props.history) {
      return null;
    }
    const data = this.props.history.map((td, i) => ({
      i,
      mean: td.mean,
      round: td.round,
      season: td.season,
    }));

    // TODO: filter to time window w/ http://recharts.org/en-US/examples/HighlightAndZoomLineChart
    // Show mean in crosshair?
    // Multiple per chart?
    return (
      <div>
        <h1>{this.props.team}</h1>
        <TeamPicker league={this.props.league} />
        <ScatterChart
          width={800}
          height={400}
          margin={{ top: 5, right: 20, left: 30, bottom: 5 }}
          data={data}
          >
          {this.state.selected.map((team: any) => (
            <YAxis
            type="number"
            domain={[dataMin => Math.floor(dataMin / 100) * 100,
                     dataMax => Math.ceil(dataMax / 100) * 100]}
            dataKey="mean"
            allowDecimals={false}
            />
          ))}
          <Tooltip content={renderTooltip} />
          <CartesianGrid stroke="#f5f5f5" />
          <Scatter fill="#8884d8" line={true} />
        </ScatterChart>
      </div>
    );
  }
}
