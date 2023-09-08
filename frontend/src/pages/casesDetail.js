import React, { useState, useEffect, useCallback  } from 'react';
import {Carousel} from "react-bootstrap";
import ReactPanZoom from 'react-image-pan-zoom-rotate';

import 'w3-css';
import './extra.css'

export default function CasesDetail(props) {
  const [result, setResult] = useState();
  const caseId = props.caseID;

  const getCase = useCallback(() => {
    fetch('http://localhost:4000/api/cases/' + caseId)
      .then((response) => response.json())
      .then((json) => setResult(json));
  },[caseId]);

  useEffect(() => {
    getCase()
  },[getCase]);

  return (
    <div>
    <h1>Case Detail</h1>
    {(result === undefined ? <h1>Loading...</h1> :
      (result.error !== undefined ? <h1>Error! could not find Case</h1> : 
      <HasResults results={result} caseImages={result.CaseImages} />))}
    </div>
  )
}

function CaseImages(props) {
  if (props.urls.length === 0) {
    return <p>Corresponding images for this case have not yet been uploaded to the website. Check OneDrive for up-to-date images.</p>
  }

  console.log(props)
  return (
        <Carousel interval={1000000}>
        {
            props.urls.caseImages.map(entry => 
            <Carousel.Item>
                <div class = "img">
                    <ReactPanZoom image={".." + entry} src={".." + entry} alt = {entry}/>
                </div> 
            </Carousel.Item>)
        }
      </Carousel> )
}

function Notes(props) {
  const notes = props.notes;

  if (notes == null) {
    return <i>(none)</i>
  } else {
    return <p>{notes}</p>
  }
}

function HasResults(props) {
  const data = props.results;

  let captureDate, adjudicationDate;
  if (data.CaptureDateVerbatim != null) {
    captureDate = data.CaptureDateVerbatim
  } else {
    captureDate = data.CaptureDates.join(", ")
  }

  if (data.AdjudicationDateVerbatim != null) {
    adjudicationDate = data.AdjudicationDateVerbatim
  } else {
    adjudicationDate = data.AdjudicationDates.join(", ")
  }

  return (
    <div className="w3-container w3-border">
      <div className="w3-row-padding w3-border">
        <div className="w3-col w3-cyan" style={{ width: "20%" }}>
          <h5>Unique ID</h5><p>{data.Uniq}</p></div>
        <div className="w3-col" style={{ width: "10%" }}>
          <h5>Volume</h5><p>{data.Volume}</p></div>
        <div className="w3-col" style={{ width: "15%" }}>
          <h5>Start Page</h5><p>{data.StartPage}</p></div>
        <div className="w3-col" style={{ width: "15%" }}>
          <h5>End Page</h5><p>{data.EndPage}</p></div>
        <div className="w3-col" style={{ width: "40%" }}>
          <h5>Red Number</h5><p>{data.RedNumber}</p></div>
      </div>
      <div className="w3-row-padding w3-border">
        <div className="w3-col" style={{ width: "33%" }}>
          <h5>Date Of Capture</h5>{captureDate}</div>
        <div className="w3-col" style={{ width: "33%" }}>
          <h5>Location</h5><p>{data.Location}</p></div>
        <div className="w3-col" style={{ width: "33%" }}>
          <h5>Ocean</h5><p>{data.Ocean}</p></div>
      </div>
      <div className="w3-row-padding w3-border">
        <div className="w3-col" style={{ width: "50%" }}>
          <h5>Slave Ship Info</h5>
          <h6>Ship Name:</h6><p>{data.CaseN}</p>
          <table className="w3-table w3-bordered">
            <thead>
              <tr>
                <th>Total</th>
                <th>Died</th>
                <th>Men</th>
                <th>Women</th>
                <th>Boys</th>
                <th>Girls</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{data.Total}</td>
                <td>{data.Died}</td>
                <td>{data.Men}</td>
                <td>{data.Women}</td>
                <td>{data.Children_m}</td>
                <td>{data.Children_f}</td>
              </tr>
            </tbody>
          </table>
          </div>
        <div className="w3-col" style={{ width: "50%", textAlign: "center" }}>
        <h5>Capture Info</h5>
          <table className="vtable" style={{ margin: "auto" }}>
            <tbody>
              <tr>
                <th>Captor Ship Name</th>
                <td>{data.Captor}</td>
              </tr>
              <tr>
                <th>Court Location</th>
                <td>{data.Court}</td>
              </tr>
              <tr>
                <th>Date of Adjudication</th>
                <td>{adjudicationDate}</td>
              </tr>
              <tr>
                <th>Mixed Court?</th>
                <td>{data.Mixed}</td>
              </tr>
            </tbody>
          </table>
          </div>
        </div>
        <div className="w3-row-padding w3-border">
        <h5>Notes</h5>
          <Notes notes={data.Notes} />
        </div>
        <div className="w3-row-padding">
        <h5>Case Images</h5>
          <CaseImages urls={props} />
        </div>
    </div>
  );
}

