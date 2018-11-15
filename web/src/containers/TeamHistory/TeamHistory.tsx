import * as React from 'react';
import {
  CartesianGrid, Line, LineChart, Tooltip, XAxis,
} from 'recharts';

import { ITeamRating } from 'src/interfaces';

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

    return (
      <LineChart
        width={400}
        height={400}
        data={data}
        margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
      >
        <XAxis dataKey="i" />
        <Tooltip content={renderTooltip} />
        <CartesianGrid stroke="#f5f5f5" />
        <Line type="monotone" dataKey="mean" stroke="#387908" yAxisId={1} />
      </LineChart>
    );
  }
}
