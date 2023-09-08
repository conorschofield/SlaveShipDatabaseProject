import React, { Component } from 'react';
import './App.css';
import SEARCH_INDEX from './pages/Search_Index';
import CasesDetail from './pages/casesDetail';
import About from './pages/about';
import VolumeList from './pages/volumeList';
import VolumeViewer from './pages/volumeViewer';

import Contact from './pages/contact';
import Home from './pages/home';
import {
  Route,
  Switch,
} from "react-router-dom";
import { Navbar, Nav} from 'react-bootstrap';

export default class App extends Component {

  render() {
    return (
      <section className="App">
        <Navbar collapseOnSelect bg="light" expand="md" className="mb-3">
          <Navbar.Brand href="/home" className="font-weight-bold text-muted">
            HCA Index
          </Navbar.Brand>
          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-middle">
            <Nav>
              <Nav.Link href="/volumes">Available Volumes</Nav.Link>
              <Nav.Link href="/search">Search Index</Nav.Link>
              <Nav.Link href="/contact">Contact</Nav.Link>
              <Nav.Link href="/about">About</Nav.Link>

            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <Switch>
          <Route path='/home'>
            <Home></Home>
          </Route>
          <Route path='/volumes'>
            <VolumeList />
          </Route>
          <Route path='/volume/:volume'>
            <VolumeViewer />
          </Route>
          <Route path='/search'>
            <SEARCH_INDEX></SEARCH_INDEX>
          </Route>
          <Route path='/contact'>
            <Contact></Contact>
          </Route>
          <Route path='/about'>
            <About></About>
          </Route>
          <Route path='/cases/:id' render={(props) =>
            <CasesDetail caseID={parseInt(props.match.params.id)} {...this.props} />} />
          <Route>
            <Home></Home>
          </Route>

        </Switch>
        <hr />
        <div className="d-flex flex-column">
          <footer className="footer">
            <div>
              <span>Ryan Linard, Conor Schofield, Gabriel Young</span>
            </div>
            <div className="ml-auto">
              <span>For Professor Matthew Hopper</span>
            </div>
          </footer>
        </div>
      </section>
    );
  }
}
