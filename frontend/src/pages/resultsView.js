import 'w3-css';

/*
Display results returned by JSON from backend server
*/
export function HasResults(props) {
  const data = props.results;
  const showVolume = props.showVolume;

  return (
    <table className="w3-hoverable w3-table-all">
      <thead>
        <tr>
          <th></th>
          <th>Unique ID</th>
          {showVolume ? <th>Volume</th> : null}
          <th>Start Page</th>
          <th>End Page</th>
          <th>Slave Ship</th>
          <th>Place of Capture</th>
          <th>Capturing Ship</th>
          <th>Date of Capture</th>
          <th>Mixed Commission</th>
          <th>Court Location</th>
          <th>Ocean</th>
          <th>Date of Adjudication</th>
          <th>Total Captives</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item, i) => {
          let captureDate, adjudicationDate;
          if (item.CaptureDatesVerbatim.length !== 0) {
            captureDate = item.CaptureDatesVerbatim[0]
          } else {
            captureDate = item.CaptureDates.join(", ")
          }
        
          if (item.AdjudicationDatesVerbatim.length !== 0) {
            adjudicationDate = item.AdjudicationDatesVerbatim[0]
          } else {
            adjudicationDate = item.AdjudicationDates.join(", ")
          }
          
          return (
          <tr key={item.Uniq} onClick={() => window.open("/cases/" + item.Uniq)}>
            <td>
              <img src="/external-link.svg" alt="Link opens in new tab" style={{width: "1em", height: "1em", marginRight: "1em" }}></img>
            </td>
            <td>
              <a href={"/cases/" + item.Uniq} target="_blank" rel="noopener noreferrer" onClick={e => e.stopPropagation()}>{item.Uniq}</a>
            </td>
            {showVolume ? <td>{item.Volume}</td> : null}
            <td>{item.StartPage}</td>
            <td>{item.EndPage}</td>
            <td>{item.CaseN}</td>
            <td>{item.Location}</td>
            <td>{item.Captor}</td>
            <td>{captureDate}</td>
            <td>{item.Mixed}</td>
            <td>{item.Court}</td>
            <td>{item.Ocean}</td>
            <td>{adjudicationDate}</td>
            <td>{item.Total}</td>
          </tr>)})}
      </tbody>
    </table>
  );
}
