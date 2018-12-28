import * as React from 'react';
import {
  Line, LineChart, XAxis, YAxis,
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


export default class extends React.Component<Props, {}> {
  public render() {
    const timeLookup = createTimeLookup(this.props.histories);
    const teamDatas = this.props.histories.map(h => ({
      data: h.ratings.map(r => ({
        week: timeLookup[r.season][r.round],
        ...r
      })),
      team: h.team,
    }))
    return (
      <div>
        <LineChart
          width={800}
          height={400}
          margin={{ top: 5, right: 20, left: 30, bottom: 5 }}
        >
          <XAxis
            dataKey="week"
            type="number"
          />
          <YAxis />
          {teamDatas.map(td => (
            <Line
              data={td.data}
              dataKey="mean"
              name={td.team}
              key={td.team}
              connectNulls={true}
            />
          ))}
        </LineChart>
      </div>
    );
  }
}
