import React, { Component } from 'react';
import CaseImageCarousel from '../caseImageCarousel';
import {Accordion, Button, Card, Container} from "react-bootstrap";


class CasesDetail extends Component {
  constructor(props) {
    super(props);
  }

  state = {
    cases: []
  }


  componentDidMount() {
    this.getCases();
    //this.getCasesStats();
  }

  getCases = _ => {
    fetch('http://localhost:4000/cases/' + this.props.caseID)
    .then(response => response.json())
    .then(response => this.setState({ cases: response.data }))
    .catch(err => console.error(err))
  }

  // getCasesStats = _ => {
  //   fetch('http://localhost:4000/cases/stats' + this.props.caseID)
  //   .then(response => response.json())
  //   .then(response => this.setState({ stats: response.data }))
  //   .catch(err => console.error(err))
  // }

  render() {
    const {cases} = this.state;
    console.log(cases);

    return (
      <Container fluid>
        <h1>Case Detail</h1>
          <CaseImageCarousel data = {cases}/>
      </Container>
    )
  }
}

export default CasesDetail

