import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import Example from './Example';
import TableTest from './pages/tableTest';
import CasesDetail from './pages/casesDetail';
import {
  BrowserRouter as Router,
  Route,
  Switch,
  Redirect,
  Link,
  useRouteMatch,
} from "react-router-dom";
import Cases from './pages/cases';
import Contact from './pages/contact';
import {Navbar, Nav, Container, Row} from 'react-bootstrap';

class App extends Component {

  render () {
    return (
      <section className ="App">
        <Navbar collapseOnSelect bg="light" expand="md" className="mb-3">
          <Navbar.Brand href="/" className="font-weight-bold text-muted">
            HCA Index
          </Navbar.Brand>
          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-middle">
            <Nav>
              <Nav.Link href="/tableTest">Cases</Nav.Link>
              <Nav.Link href="/contact">Contact</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <Switch>
          <Route path = '/tableTest'>
            <TableTest></TableTest>
          </Route>
          <Route path = '/contact'>
            <Contact></Contact>
          </Route>
          <Route path = '/cases/:id' render = {(props) => 
                <CasesDetail caseID = {parseInt(props.match.params.id)} {...this.props}/>}/>
          <Route path='/cases' 
                render={() => <Cases {...this.props} />} />
        </Switch>
        <hr />
        <div class="d-flex flex-column">
          <footer class="footer">
            <div>
              <span>2021 California Polytechnic State University</span>
            </div>
            <div class="ml-auto">
              <span>San Luis Obispo</span>
            </div>
          </footer>
        </div>
      </section>
    );
  }
}

export default App;
