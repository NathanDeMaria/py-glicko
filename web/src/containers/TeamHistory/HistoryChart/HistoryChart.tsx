import * as React from 'react';
import {
  Dot, Legend, Line, LineChart,
  ReferenceArea, Tooltip,
  XAxis, YAxis,
} from 'recharts';

import { ITeamRating } from 'src/interfaces/';

export interface IOwnProps {
  league: string,
}

interface ITeamHistory {
  team: string,
  ratings: ITeamRating[],
}

export interface IStateProps {
  histories: ITeamHistory[],
};
 
type Props = IStateProps & IOwnProps;


// rainbow(n = 10)
const colors = [
  "#FF0000FF", "#FF9900FF", "#CCFF00FF", "#33FF00FF", "#00FF66FF",
  "#00FFFFFF", "#0066FFFF", "#3300FFFF", "#CC00FFFF", "#FF0099FF",
];


interface IIndexLookup {
  // lookup[season][round] = index
  [key: number]: {
    [key: number]: number,
  },
}


function createTimeLookup(histories: ITeamHistory[]): IIndexLookup {
  // Give me a lookup from season/round to an index
  // Indices are increasing ints within a round, skip one between seasons.
  const ranges = {};
  histories.forEach(h => {
    h.ratings.forEach(r => {
      const soFar = ranges[r.season];
      if (soFar) {
        ranges[r.season] = [
          Math.min(soFar[0], r.round),
          Math.max(soFar[1], r.round),
        ];
      } else {
        ranges[r.season] = [r.round, r.round];
      }
    })
  });

  let i = 0;
  const lookup = {};
  Object.keys(ranges).sort().forEach(season => {
    const roundRange = ranges[season];
    // This can be less gross...
    lookup[season] = {};
    for(let j = roundRange[0]; j < roundRange[1] + 1; j++) {
      lookup[season][j] = i;
      i++;
    }
  });
  return lookup;
}

function renderTooltip(props: any) {
  // This is a bit broken b/c this doesn't seem to play nicely with
  // multiple lines in one chart. But it at least shows season/round.
  const {payload} = props;
  if (!payload) { return null; }
  const datum = payload[0];
  if (!datum) { return null };

  const { payload: {season, round} } = datum;
  return (
    <div>
      <p>Season: {season}</p>
      <p>Round: {round}</p>
    </div>
  )
}

export default class extends React.Component<Props, {}> {
  public state = {
    left: 'dataMin',
    refAreaLeft: '',
    refAreaRight: '',
    right: 'dataMax',
  }

  public render() {
    const timeLookup = createTimeLookup(this.props.histories);
    const teamDatas = this.props.histories.map(h => ({
      data: h.ratings.map(r => ({
        index: timeLookup[r.season][r.round],
        ...r
      })),
      team: h.team,
    }));
    const {
      left, right,

      refAreaLeft, refAreaRight,
    } = this.state;
    return (
      <div>
        <button onClick={this.zoomOut}>
          Zoom Out
        </button>
        <LineChart
          width={800}
          height={400}
          margin={{ top: 5, right: 20, left: 30, bottom: 5 }}
          onMouseDown={this.markLeft}
          onMouseMove={this.move}
          onMouseUp={this.zoom}
        >
          <XAxis
            dataKey="index"
            type="number"
            domain={[left, right]}
            allowDataOverflow={true}
            hide={true}
          />
          <YAxis
            allowDecimals={false}
            domain={["auto", "auto"]}
          />
          <Legend />
          {teamDatas.map((td, i) => (
            <Line
              data={td.data}
              dataKey="mean"
              name={td.team}
              key={td.team}
              connectNulls={true}
              stroke={colors[i]}
              dot={<Dot r={1} />}
            />
          ))}
          <Tooltip content={renderTooltip} />
          {
            (refAreaLeft && refAreaRight) ?
            (<ReferenceArea x1={refAreaLeft} x2={refAreaRight} strokeOpacity={0.3} /> )
            : null
          }            
        </LineChart>
      </div>
    );
  }

  private zoomOut = () => {
    this.setState({
      left: 'dataMin',
      refAreaLeft: '',
      refAreaRight: '',
      right: 'dataMax',
    });
  }

  // TODO: what's an e?
  private markLeft = (e: any) => {
    if (!e) { return; }
    this.setState({refAreaLeft:e.activeLabel});
  }

  private move = (e: any) => {
    if (!e) { return; }
    if (this.state.refAreaLeft) {
      this.setState({refAreaRight:e.activeLabel});
    }
  }

  // TODO: also zoom in the y axis?
  private zoom = () => {
  	let { refAreaLeft, refAreaRight } = this.state;

		if ( refAreaLeft === refAreaRight || refAreaRight === '' ) {
    	this.setState( () => ({
      	refAreaLeft : '',
        refAreaRight : ''
      }) );
    	return;
    }

		// xAxis domain
	  if (refAreaLeft > refAreaRight) {
      [ refAreaLeft, refAreaRight ] = [ refAreaRight, refAreaLeft ];
    }

    this.setState({
      left : refAreaLeft,
      refAreaLeft : '',
      refAreaRight : '',
      right : refAreaRight,
    });
  };
}
