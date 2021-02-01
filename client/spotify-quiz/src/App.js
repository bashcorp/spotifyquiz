import React from 'react';
import './App.css';
import Quiz from './components/Main/Quiz/Quiz';
import Home from './components/Home/Home';
import Results from './components/Results/Results';
import Dashboard from './components/Dashboard/Dashboard';


import {BrowserRouter, Route, Link} from 'react-router-dom';

class App extends React.Component {

  render() {
    return (
      <div className="App">
        
      <BrowserRouter>
        <Route exact path="/" component={Home} />
        <Route path="/quiz" component={Quiz} />
        <Route exact path="/dashboard" component={Dashboard} />
        <Route exact path="/results" component={Results} />
</BrowserRouter>
      </div>

      );
    }

}

export default App;