import React, { useState, useEffect, useCallback } from "react";
import { HasResults } from './resultsView';
import { useParams } from 'react-router-dom';

/*
The Result table displays the entries yielded from a mySQL query with the search 
string from the search form
*/
function ResultTable(props) {
  const [results, setResults] = useState();

  const getResults = useCallback(() => {
    const built_string = 'http://localhost:4000/api/search/?Volume=' + props.volume;

    fetch(built_string)
      .then((response) => response.json())
      .then((json) => setResults(json));
  }, [props.volume]);

  useEffect(getResults, [getResults, props.volume]);

  if (results === undefined || results.length === 0) {
    return <div></div>
  }

  return <HasResults results={results} showVolume={false} />;
}

export default function VolumeViewer(props) {
  let { volume } = useParams();
  return (
    <div className="w3-container">
      <a href='/volumes'>
        <img src="/arrow-left-solid.svg" alt="" style={{width: "1em", height: "1em", marginRight: "0.25em" }}></img>
        Back to Volumes List
      </a>
      <h1>Volume {volume}</h1>
      <ResultTable volume={volume} />
    </div>
  );
}
