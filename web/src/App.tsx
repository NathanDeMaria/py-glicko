import * as React from 'react';
import { BrowserRouter, Route } from 'react-router-dom';

import './App.css';
import WeeklyUpdate from './containers/WeeklyUpdate/';


// There's gotta be something that does this for you...
const l = (m: any) => (<WeeklyUpdate {...m.match.params} />)

class App extends React.Component {
  public render() {
    return (
      <BrowserRouter>
        <div>
          <div className="App">
            <header className="App-header">
              <h1 className="App-title">Welcome to React</h1>
            </header>
            <p className="App-intro">
              To get started, edit <code>src/App.tsx</code> and save to reload.
            </p>
          </div>
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
