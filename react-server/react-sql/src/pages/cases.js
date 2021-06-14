import React from 'react'
import {Component} from 'react'

class Cases extends Component {
  constructor(props) {
    super(props);
 }

    state = {
      stats: []
    }
  
    componentDidMount() {
      this.getCasesStats();
    }
  
    getCases = _ => {
      fetch('http://localhost:4000/cases')
      .then(response => response.json())
      .then(response => this.setState({ cases: response.data }))
      .catch(err => console.error(err))
    }

    getCasesStats = _ => {
        fetch('http://localhost:4000/cases/stats')
        .then(response => response.json())
        .then(response => this.setState({ stats: response.data }))
        .catch(err => console.error(err))
    }
  
    renderCases = ({UniqID, Volume, Page, imageURL, UniqImage, UniqCase}) => <div key={(UniqID, Page, UniqImage, UniqCase)}>{Page}</div>
    renderStats = ({Uniq, RedNumber, Volume, StartPage, EndPage, Men, Women, Children_m, Children_f, Total, Captor, Location}) => <div key={(Uniq)}>{StartPage}</div>

    render () {
      console.log(this.props);
      const { stats } = this.state;
      return (
        <div className="Cases">
          {stats.map(this.renderStats)}
        </div>
      );
    }
  }

export default Cases


