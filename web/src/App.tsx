import * as React from 'react';
import { BrowserRouter, Route } from 'react-router-dom';

import './App.css';
import WeeklyUpdate from './containers/WeeklyUpdate/';
import WeekSelector from './containers/WeekSelector/';


// There's gotta be something that does this for you...
const l = (m: any) => (<WeeklyUpdate {...m.match.params} />)

class App extends React.Component {
  public render() {
    return (
      <BrowserRouter>
        <div>
          <WeekSelector />
          <div>
            <Route
              path="/weekly/season/:season/round/:round"
              render={l}
            />
          </div>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
