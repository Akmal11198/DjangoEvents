import './App.css';
import "bootstrap/dist/css/bootstrap.min.css";
import {BrowserRouter,Route,Switch} from "react-router-dom";
import {Container} from "react-bootstrap"

import Login from "./components/Login";
import Events from "./components/Events";
function App() {
  return (
    <div className="App">
        <Container className="my-3">
      <BrowserRouter>
        <Switch>
          <Route path="/events" exact component={Events} />
          <Route path="/" component={Login} />
        </Switch>
      </BrowserRouter>
      </Container>
    </div>
  );
}

export default App;
