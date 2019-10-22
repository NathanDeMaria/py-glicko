import * as React from 'react';
import { BrowserRouter, Link, Route } from 'react-router-dom';

import './App.css';
import LeagueSelector from './containers/LeagueSelector/';
import Matchup from './containers/Matchup/';
import TeamHistory from './containers/TeamHistory/';
import WeeklyUpdate from './containers/WeeklyUpdate/';
import WeekSelector from './containers/WeekSelector/';


// There's gotta be something that does this for you...
const h = () => (
  <LeagueSelector />
);

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
    key={m.match.params.league}
  />
);

const wp = (m: any) => (
  <Matchup
    {...m.match.params}
    key={m.match.params.league}
  />
);

const menu = (m: any) => (
  <div key={m.match.params.league}>
    <Link to={`/${m.match.params.league}/history`}>
      History
    </Link>
    <br />
    <Link to={`/${m.match.params.league}/weekly`}>
      Weekly
    </Link>
    <br />
    <Link to={`/${m.match.params.league}/matchup`}>
      Matchup
    </Link>
  </div>
)

class App extends React.Component {
  public render() {
    return (
      <BrowserRouter>
        <div>
          <Route
            path="/"
            render={h}
          />
          <Route
            path="/:league/weekly"
            render={s}
          />
          <Route
            path="/:league"
            exact={true}
            render={menu}
          />
          <Route
            path="/:league/weekly/season/:season/round/:round"
            render={l}
          />
          <Route
            path="/:league/history"
            render={t}
          />
          <Route
            path="/:league/matchup"
            render={wp}
          />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
