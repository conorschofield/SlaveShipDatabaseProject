import React, { useState, useEffect, useCallback } from "react";

export default class VolumeList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      volumes: undefined
    };
  }

  componentDidMount() {
    fetch('http://localhost:4000/api/groups/Volume')
      .then((response) => response.json())
      .then((json) => this.setState({ volumes: json })); 
  }

  render() {
    const volumes = this.state.volumes;

    if (volumes === undefined) {
      return (<h1>Loading...</h1>);
    }

    return (
      <div className="w3-container">
        <h1>Available Volumes</h1>
        <ul style={{listStyleType: 'none'}}>
          {Object.entries(volumes).map(([volume, count]) =>
            <li key={volume}>
              <img src="/folder-open-solid.svg" alt="" style={{width: "1em", height: "1em", marginRight: "1em" }}></img>
              <a href={`/volume/${volume}`}>Volume {volume} ({count} entries)</a>
            </li>)}
        </ul>
      </div>
    );
  }
}
