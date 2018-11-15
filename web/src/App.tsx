import * as React from 'react';
import { BrowserRouter, Route } from 'react-router-dom';

import './App.css';
import TeamHistory from './containers/TeamHistory/';
import WeeklyUpdate from './containers/WeeklyUpdate/';
import WeekSelector from './containers/WeekSelector/';


// There's gotta be something that does this for you...
const l = (m: any) => (
  <WeeklyUpdate
    {...m.match.params}
    key={`${m.match.params.season}-${m.match.params.round}`}
  />
);

const s = (m: any) => (
  <WeekSelector
    {...m.match.params}
    key={m.match.params.league}
  />
);

const t = (m: any) => (
  <TeamHistory
    {...m.match.params}
    key={`${m.match.params.league}-${m.match.params.team}`}
  />
);

class App extends React.Component {
  public render() {
    return (
      <BrowserRouter>
        <div>
          <Route
            path="/:league"
            render={s}
          />
          <Route
            path="/:league/weekly/season/:season/round/:round"
            render={l}
          />
          <Route
            path="/:league/team/:team"
            render={t}
          />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
