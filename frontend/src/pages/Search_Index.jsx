/*
Gabriel Young
Spring 2022, Winter 2023
*/
import React, { useState, useEffect, useCallback } from "react";
import 'w3-css';
import { HasResults } from './resultsView';
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css'

const SLAVE_STATS_STEP = 10;
const DEFAULT_RESULTS_PER_PAGE = 25;
const SEARCH_MIN_YEAR = 1700;
const SEARCH_MAX_YEAR = 1900;
const PERSON_COUNT_MIN = 0;
const PERSON_COUNT_MAX = 999;
const DATE_START = "1700-01-01";
const DATE_END = "1900-01-01";


/**
 * This creates all the text and single-number input fields
 * @param {label, name, type, handleInputChange} props 
 * @returns input field of {type} sets state with {handleInputChange}
 */
function SearchFormInputField(props) {
  return (
    <div className="w3-quarter w3-border w3-padding">
      <label>{props.label}</label>
      <input
        className="w3-input"
        name={props.name}
        type={props.type}
        placeholder={props.type}
        onChange={props.handleInputChange} />
      <p className="w3-tiny w3-opac" style={{ opacity: "50%" }}>{props.note}</p>
    </div>
  );
}

/**
 * This creates all the date number input fields
 * @param {label, name, type, handleInputChange, default_val, min_year, max_year} props 
 * @returns input field of {type} sets state with {handleInputChange}
 */
function SearchFormDateInputField(props) {
  return (
    <div className="w3-quarter w3-border w3-padding">
      <label>{props.label}</label>
      <input
        className="w3-input"
        defaultValue={props.default_val}
        name={props.name}
        type={props.type}
        min={props.min_year}
        max={props.max_year}
        placeholder={props.type}
        onChange={props.handleInputChange} />
      <p className="w3-tiny w3-opac" style={{ opacity: "50%" }}>{props.note}</p>
    </div>
  );
}

function jsDate2mySQLDate(d) {
  if (typeof(d) == "string") {
    return d;
  }
  return d = d.getUTCFullYear() + '-' +
  ('00' + (d.getUTCMonth()+1)).slice(-2) + '-' +
  ('00' + d.getUTCDate()).slice(-2);
}

/**
 * This creates range silders (uses rc-slider)
 * @param {rangefield, field, step, note, onRangeChange} props 
 * @returns rc-slider with min and max of rangefield, sets parent state with
 * onRangeChange
 */
class SearchFormSliderInput extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
  }
  state = { sliderValues: this.props.rangefield }
  handleChange(val) {
    this.props.onRangeChange(this.props.field, val);
  }
  render() {
    const { sliderValues } = this.state;
    return (
      <div>
        <Slider
          range
          step={this.props.step}
          min={sliderValues[0]}
          max={sliderValues[1]}
          defaultValue={sliderValues}
          onChange={this.handleChange} />
        <p className="w3-tiny w3-opac" style={{ opacity: "50%" }}>{this.props.note}</p>
      </div>
    );
  }
}

/*
SearchForm: generates a search string according to form fields
*/
class SearchForm extends React.Component {
  
  constructor(props) {
    super(props);
    this.handleRangeChange = this.handleRangeChange.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleEnableChange = this.handleEnableChange.bind(this);
    this.handleEnableChangeDate = this.handleEnableChangeDate.bind(this);

    this.state = {
      Uniq: "", Volume: "", StartPage: "", EndPage: "",
      CaseN: "", Location: "", Captor: "", CaptureDate_s: new Date(DATE_START), 
      CaptureDate_e: new Date(DATE_END),
      Mixed: "", Court: "", Ocean: "", AdjudicationDate_s: new Date(DATE_START),
      AdjudicationDate_e: new Date(DATE_END),
      RedNumber: "", Notes: "", Men: "", Women: "",
      Children_m: "", Children_f: "", Total: "", Died: "",
      uniq_court_locations: [], uniq_mixed_commissions: []
    };
  }

  componentDidMount() {
    fetch('http://localhost:4000/api/distinct/?field=Court')
      .then((response) => response.json())
      .then((json) => this.setState({ uniq_court_locations:json })); 
    fetch('http://localhost:4000/api/distinct/?field=Mixed')
      .then((response) => response.json())
      .then((json) => this.setState({ uniq_mixed_commissions:json }));
    fetch('http://localhost:4000/api/distinct/?field=Volume')
      .then((response) => response.json())
      .then((json) => 
      {
        this.setState({volumes:json});
      }); 
  }

  handleInputChange(event) {
    const target = event.target;
    const name = target.name;
    this.setState({ [name]: target.value });
  }

  handleRangeChange(field, range) {
    this.setState({ [field]: range });
  }

  handleSubmit(event) {
    event.preventDefault();
    //list of search params:
    //most names map directly to mySQL columns. names starting with "max_" 
    //or "min" only directly map afterwards
    const search_params = [
      "Uniq", "Volume", "StartPage", "EndPage", "CaseN", "Location", "Captor",
      "Mixed", "Court", "Ocean",
      "Men", "Women", "Children_m", "Children_f", "Total", "Died", "RedNumber",
      "Notes"];

    //const [CaptureDate, onChange_cap_date] = useState([new Date(), new Date()]);
    //const [AdjudicationDate, onChange_adj_date] = useState([new Date(), new Date()]);

    let search_string = "?"
    let param_list = [];

    //convert native javascript date (garbage) to mysql date
    param_list.push("CaptureDate=" + encodeURIComponent(
      jsDate2mySQLDate(this.state["CaptureDate_s"])
      + "," + jsDate2mySQLDate(this.state["CaptureDate_e"]) ));
    param_list.push("AdjudicationDate=" + encodeURIComponent(
      jsDate2mySQLDate(this.state["AdjudicationDate_s"])
      + "," + jsDate2mySQLDate(this.state["AdjudicationDate_e"]) ));

    search_params.forEach(param => {
      let raw_param = this.state[param];
      if (raw_param !== "") {
        param_list.push(param + "="
          + encodeURIComponent(raw_param));
      }
    });

    search_string += param_list.join("&");

    this.props.handleChange("searchString", search_string);
    //set page to 1 after every search
    this.props.handleChange("page", 1);    
    event.preventDefault();
  }

  handleEnableChange(event) {
    let field = event.target.value;
    if (this.state[field] === "") {
      this.setState({ [field]: [PERSON_COUNT_MIN, PERSON_COUNT_MAX] });
    } else {
      this.setState({ [field]: "" });
    }
  }

  handleEnableChangeDate(event) {
    let field = event.target.value;

    if (this.state[field] === "") {
      this.setState({ [field]: [SEARCH_MIN_YEAR, SEARCH_MAX_YEAR] });
    } else {
      this.setState({ [field]: "" });
    }
  }

  render() {
    if (this.state.uniq_court_locations.length === 0 ||
      this.state.uniq_mixed_commissions.length === 0) {
      return (<div><p>loading...</p></div>)
    }
    return (
      <div className="w3-margin w3-padding w3-card">
        <form onSubmit={this.handleSubmit} className="w3-container">

          {/*group 1*/}
          <div className="w3-row-padding w3-left-align"><h5>Slave Ship:</h5></div>
            <SearchFormInputField label={"Name"} type={"text"}
              name={"CaseN"} handleInputChange={this.handleInputChange} />
            <SearchFormInputField label={"Notes"} type={"text"}
              name={"Notes"} handleInputChange={this.handleInputChange} />
            <SearchFormInputField label={"UniqueID"} type={"number"}
              name={"Uniq"} handleInputChange={this.handleInputChange} />

          {/*group 2*/}
          <div className="w3-row-padding w3-left-align"><h5>Record:</h5></div>
            <SearchFormInputField label={"Red number"} type={"text"}
              name={"RedNumber"} handleInputChange={this.handleInputChange} 
              />
            <div className="w3-quarter w3-border w3-padding w3-left-align">
              <label>Volume</label>
                <select className="w3-select" name="Volume" type="number"
                onChange={this.handleInputChange}>
                  <option value="">Any</option>
                  {this.state.volumes ? this.state.volumes.map(
                    (vol) => <option key={vol} value={vol}>
                      {vol}</option>
                  ) : null}
                </select>
            </div>
            <SearchFormInputField label={"Start Page"} type={"number"}
              name={"StartPage"} handleInputChange={this.handleInputChange} />
            <SearchFormInputField label={"End Page"} type={"number"}
              name={"EndPage"} handleInputChange={this.handleInputChange} />
 
          {/*group 3*/}
          <div className="w3-row-padding w3-left-align"><h5>Capture:</h5></div>
            <SearchFormDateInputField label={"Date start"} type={"date"} note="try typing in a date!"
              name={"CaptureDate_s"} handleInputChange={this.handleInputChange} 
              default_val={DATE_START} min_year={DATE_START} max_year={this.state.CaptureDate_e}/>
            <SearchFormDateInputField label={"Date end"} type={"date"} note="try typing in a date!"
              name={"CaptureDate_e"} handleInputChange={this.handleInputChange} 
              default_val={DATE_END} min_year={this.state.CaptureDate_s} max_year={DATE_END}/>
            <SearchFormInputField label={"Place of Capture"} type={"text"}
              name={"Location"} handleInputChange={this.handleInputChange} 
              note="may not have effect"/>
            <SearchFormInputField label={"Capturing Ship"} type={"text"}
              name={"Captor"} handleInputChange={this.handleInputChange} 
              note="may not have effect"/>
            
            <div className="w3-row-padding"></div>
            <div className="w3-quarter w3-border w3-padding ">
              <label>Ocean:</label>
              <select className="w3-select"name="Ocean" type="text"
                onChange={this.handleInputChange}>
                <option value="">Any</option>
                <option value="Atlantic">Atlantic</option>
                <option value="Indian">Indian</option>
                <option value="South China Sea">South China Sea</option>
              </select>
            </div>

          {/*group 4*/}
          <div className="w3-row-padding w3-left-align"><h5>Adjudication:</h5></div>
            <SearchFormDateInputField label={"Date start"} type={"date"} note="try typing in a date!"
              name={"AdjudicationDate_s"} handleInputChange={this.handleInputChange} 
              default_val={DATE_START} min_year={DATE_START} max_year={this.state.AdjudicationDate_e}/>
            <SearchFormDateInputField label={"Date end"} type={"date"} note="try typing in a date!"
              name={"AdjudicationDate_e"} handleInputChange={this.handleInputChange} 
              default_val={DATE_END} min_year={this.state.AdjudicationDate_s} max_year={DATE_END}/>
            <div className="w3-quarter w3-border w3-padding">
              <label>Mixed Commission:</label>
              <select className="w3-select" name="Mixed" type="text"
                onChange={this.handleInputChange}>
                <option value="">Any</option>
                {this.state.uniq_mixed_commissions.map(
                  (mixed) => <option key={mixed} value={mixed}>{mixed}</option>
                )}
              </select>
            </div>
            <div className="w3-quarter w3-border w3-padding">
              <label>Court Location:</label>
              <select className="w3-select" name="Court" type="text"
                onChange={this.handleInputChange}>
                <option value="">Any</option>
                {this.state.uniq_court_locations.map(
                  (court) => <option key={court} value={court}>{court}</option>
                )}
              </select>
            </div>

          {/*group 5*/}
          <div className="w3-row-padding w3-left-align"><h5>Population:</h5></div>
          <div className="w3-row-padding">
            <div className="w3-quarter w3-border w3-padding">
              Men<span className="w3-padding-small"></span>
              <input className="w3-check" type="checkbox" value="Men"
                onChange={this.handleEnableChange} />
              {((this.state.Men !== "") &&
                <div>
                  <SearchFormSliderInput
                    step={SLAVE_STATS_STEP}
                    field="Men"
                    onRangeChange={this.handleRangeChange}
                    rangefield={this.state.Men}
                    note="Using this field will filter out all entires without values for Men" />
                  {this.state.Men[0]}-{this.state.Men[1]}
                </div>)}
            </div>
            <div className="w3-quarter w3-border w3-padding">
              Women<span className="w3-padding-small"></span>
              <input className="w3-check" type="checkbox" value="Women"
                onChange={this.handleEnableChange} />
              {((this.state.Women !== "") &&
                <div>
                  <SearchFormSliderInput
                    step={SLAVE_STATS_STEP}
                    field="Women"
                    onRangeChange={this.handleRangeChange}
                    rangefield={this.state.Women}
                    note="Using this field will filter out all entires without values for Women" />
                  {this.state.Women[0]}-{this.state.Women[1]}
                </div>)}
            </div>
            <div className="w3-quarter w3-border w3-padding">
              Boys <span className="w3-padding-small"></span>
              <input className="w3-check" type="checkbox" value="Children_m"
                onChange={this.handleEnableChange} />
              {((this.state.Children_m !== "") &&
                <div>
                  <SearchFormSliderInput
                    step={SLAVE_STATS_STEP}
                    field="Children_m"
                    onRangeChange={this.handleRangeChange}
                    rangefield={this.state.Children_m}
                    note="Using this field will filter out all entires without values for Boys" />
                  {this.state.Children_m[0]}-{this.state.Children_m[1]}
                </div>)}
            </div>
            <div className="w3-quarter w3-border w3-padding">
              Girls <span className="w3-padding-small"></span>
              <input className="w3-check" type="checkbox" value="Children_f"
                onChange={this.handleEnableChange} />
              {((this.state.Children_f !== "") &&
                <div>
                  <SearchFormSliderInput
                    step={SLAVE_STATS_STEP}
                    field="Children_f"
                    onRangeChange={this.handleRangeChange}
                    rangefield={this.state.Children_f}
                    note="Using this field will filter out all entires without values for Girls" />
                  {this.state.Children_f[0]}-{this.state.Children_f[1]}
                </div>)}
            </div>
          </div>
          {/*row 5*/}
          <div className="w3-row-padding">
            <div className="w3-quarter w3-border w3-padding">
              Total <span className="w3-padding-small"></span>
              <input className="w3-check" type="checkbox" value="Total"
                onChange={this.handleEnableChange} />
              {((this.state.Total !== "") &&
                <div>
                  <SearchFormSliderInput
                    step={SLAVE_STATS_STEP}
                    field="Total"
                    onRangeChange={this.handleRangeChange}
                    rangefield={this.state.Total}
                    note="Using this field will filter out all entires without values for Total" />
                  {this.state.Total[0]}-{this.state.Total[1]}
                </div>)}
            </div>
            <div className="w3-quarter w3-border w3-padding">
              Died <span className="w3-padding-small"></span>
              <input className="w3-check" type="checkbox" value="Died"
                onChange={this.handleEnableChange} />
              {((this.state.Died !== "") &&
                <div>
                  <SearchFormSliderInput
                    step={SLAVE_STATS_STEP}
                    field="Died"
                    onRangeChange={this.handleRangeChange}
                    rangefield={this.state.Died}
                    note="Using this field will filter out all entires without values for Died" />
                  {this.state.Died[0]}-{this.state.Died[1]}
                </div>)}
            </div>
          </div>
          <br />
          <input className="w3-button w3-border w3-teal" type="submit" value="Submit" />
        </form>
      </div>
    )
  }
}

function ResultHeader(props) {
  const [count, setCount] = useState();
  const searchString = props.searchString;

  const getResults = useCallback(() => {
    const built_string = 'http://localhost:4000/api/count/' + searchString;
    fetch(built_string)
      .then((response) => response.json())
      .then((json) => setCount(json));
  }, [searchString]);

  useEffect(() => {
    // Note: This searches on page load.
    // This ensures that the user gets to see some results before typing
    // their query.
    getResults()
  }, [getResults, searchString]);
  
  return (
    <div>
      {(count === undefined ? <h1>Loading...</h1> :
        (count === 0 ? <h1>No Results</h1> :
        <div>
          <h2>Results (displaying {(props.page - 1) * props.resultsPerPage + 1}-{(props.page) * props.resultsPerPage} of {count}):</h2>
        </div>))}
    </div>
  );
}

/*
The Result table displays the entries yielded from a mySQL query with the search 
string from the search form
*/
function ResultTable(props) {
  const [results, setResults] = useState();
  const searchString = props.searchString;
  const startRow = (props.page - 1) * props.resultsPerPage

  const getResults = useCallback(() => {
    var joiner = '?'

    if (searchString) {
      joiner = "&"
    }

    const built_string = 'http://localhost:4000/api/search/' + searchString + joiner + "offset="
    + startRow + "&limit=" + props.resultsPerPage;

    fetch(built_string)
      .then((response) => response.json())
      .then((json) => {
        // clears results. not having this line results in subtle bug
        setResults([]);
        setResults(json);
      });
  }, [searchString, startRow, props.resultsPerPage]);

  useEffect(() => {
    // Note: This searches on page load.
    // This ensures that the user gets to see some results before typing
    // their query.
    getResults()
  }, [getResults, searchString]);

  if (results === undefined || results.length === 0) {
    // Note: The "results unavailable" message is displayed in ResultHeader
    return <div></div>
  }

  return <HasResults results={results} showVolume={true} />;
}

/**
 * set options for the result table: results per page and page number
 */
class TableOptions extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      numResult: { DEFAULT_RESULTS_PER_PAGE }
    }
    this.handleChangeTBSize = this.handleChangeTBSize.bind(this);
    this.handleChangePage = this.handleChangePage.bind(this);
  }

  handleChangeTBSize(event) {
    this.props.handleChange("resultsPerPage", event.target.value);
    this.props.handleChange("page", 1);
  }

  handleChangePage(event) {
    if (event.target.value === "down") {
      if (this.props.page > 1)
        this.props.handleChange("page", this.props.page - 1);
    }
    else {
      this.props.handleChange("page", this.props.page + 1);
    }
  }

  render() {
    return (
      <div className="w3-container w3-card w3-padding w3-margin">
        <h3>Table Options</h3>
        <div className="w3-row-padding w3-container">
          <div className="w3-half">
            <h5>Results per page (default {DEFAULT_RESULTS_PER_PAGE}):</h5>
            <div onChange={this.handleChangeTBSize}>
              <input className="w3-radio" type="radio" name="numResult" value="25" />
              <label className="w3-padding-small">25</label>
              <span className="w3-margin"></span>
              <input className="w3-radio" type="radio" name="numResult" value="50" />
              <label className="w3-padding-small">50</label>
              <span className="w3-margin"></span>
              <input className="w3-radio" type="radio" name="numResult" value="100" />
              <label className="w3-padding-small">100</label>
              <span className="w3-margin"></span>
              <input className="w3-radio" type="radio" name="numResult" value="200" />
              <label className="w3-padding-small">200</label>
            </div>
          </div>
          <div className="w3-half">
            <button onClick={this.handleChangePage}
              className="w3-button w3-teal w3-large" value="down">Previous</button>
            <span className="w3-large w3-padding"> Page: {this.props.page} </span>
            <button onClick={this.handleChangePage}
              className="w3-button w3-teal w3-large" value="up">Next</button>
          </div>
        </div>
      </div>
    );
  }
}

/*
Query Page
this class contains the search form that generates search strings and the
corrosponding result table.
The search string state is at the QueryPage level so it can be set by the search
form and used by the resultTable.
*/
export default class QueryPage extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange =
      this.handleChange.bind(this);
    this.state = {
      searchString: "",
      page: 1,
      resultsPerPage: 25,
      resultCount: 0
    };
  }

  handleChange(field, val) {
    this.setState({ [field]: val });
  }

  render() {
    const searchString = this.state.searchString;
    const page = this.state.page;
    const resultsPerPage = this.state.resultsPerPage;
    return (
      <div className="w3-container">
        <h1>Slave Ship Search</h1>
        <SearchForm handleChange={this.handleChange} />
        <TableOptions
          page={page}
          resultsPerPage={resultsPerPage}
          handleChange={this.handleChange} />
        <ResultHeader
          searchString={searchString}
          page={page}
          resultsPerPage={resultsPerPage}
        />
        <ResultTable
          searchString={searchString}
          page={page}
          resultsPerPage={resultsPerPage}
        />
      </div>
    );
  }
}