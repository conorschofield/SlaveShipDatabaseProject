import React, { useState, useEffect } from "react";
import Datatable from "../datatable";
import {Form, Button, Accordion, Card, 
    InputGroup, FormControl,
    Container, Row, Col, Modal} from "react-bootstrap";
import {
      MuiPickersUtilsProvider,
      KeyboardTimePicker,
      KeyboardDatePicker,
    } from '@material-ui/pickers';
import TextField from '@material-ui/core/TextField';
//import DateFnsUtils from '@date-io/date-fns';

import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';

require("es6-promise").polyfill();
require("isomorphic-fetch");

function valuetext(value) {
    return `${value}`;
}

export default function TableTest() {
    const [data, setData] = useState([]);
    const [q, setQ] = useState("");
    const [searchColumns, setSearchColumns] = useState(["CaseN", "Court","Location"]);
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const [value, setValue] = React.useState([0, 50]);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    // const [selectedDate, setSelectedDate] = React.useState(new Date('1772-08-18T21:11:54'));
    // const handleDateChange = (date) => {
    //     setSelectedDate(date);
    // };


    useEffect(() => {
        fetch('http://localhost:4000/cases/stats')
        .then((response) => response.json())
        .then((json) => setData(json.data));
    }, []);

    function search(rows) {
        return rows.filter((row) =>
            searchColumns.some(
                (column) => row[column].toString().toLowerCase().indexOf(q.toLowerCase()) > -1
            )
        );
    }

    const columnsMap = new Map([
        ["CaseN", "Ship"],
        ["Court", "Court"],
        ["Volume", "Volume"], 
        ["StartPage", "Start Page"], 
        ["EndPage", "End Page"], 
        ["Captor", "Capturing Ship"], 
        ["Location", "Place of Capture"], 
        ["RAW_DateOfCapture", "Date of Capture"],
        ["RAW_DateOfAdjudication", "Date of Adjudication"],
        ["Men", "Men"], 
        ["Women", "Women"], 
        ["Children_m", "Boys"], 
        ["Children_f", "Girls"],
        ["Total", "Total"]]);

    const columns = ["Volume", "StartPage", "EndPage", "CaseN", "Court", "Captor", "Location", "RAW_DateOfCapture", "RAW_DateOfAdjudication","Men", "Women", "Children_m", "Children_f", "Total"];
    return (
        <div>
            <Container fluid>
            <Row>
                <Col>
            <InputGroup>
                    <FormControl
                        placeholder={`Search:${searchColumns.map((column) => " " + columnsMap.get(column))}`}
                        aria-label="Search Bar"
                        aria-describedby="search-bar"
                        value = {q} 
                        onChange={(e) => setQ(e.target.value)}
                        />
                <InputGroup.Append>
                <Accordion>
                    <Card>
                        <Accordion.Toggle as={Button} variant="link" eventKey="0">
                            Columns to Search
                        </Accordion.Toggle>
                        <Accordion.Collapse eventKey="0">
                        <Card.Body>
                            <Container fluid>
                        {
                            columns && columns.map((column) => 
                            <Row>
                            <label>
                                <input type="checkbox" checked={searchColumns.includes(column)}
                                    onChange={(e) => {
                                        const checked = searchColumns.includes(column)
                                        setSearchColumns(prev => checked
                                            ? prev.filter(sc => sc !== column)
                                            : [...prev, column])
                                    }}
                                />
                                {columnsMap.get(column)}
                            </label>
                            </Row>)
                        }
                        </Container>
                        </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                </Accordion>
                </InputGroup.Append>
                <Button variant="primary" onClick={handleShow}>
                    Advanced Search
                </Button>
            </InputGroup>
            </Col>
            </Row>
                {/* <input type="text" value = {q} onChange={(e) => setQ(e.target.value)}/>
                {
                    columns && columns.map((column) => 
                    <label>
                        <input type="checkbox" checked={searchColumns.includes(column)}
                            onChange={(e) => {
                                const checked = searchColumns.includes(column)
                                setSearchColumns(prev => checked
                                    ? prev.filter(sc => sc !== column)
                                    : [...prev, column])
                            }}
                        />
                        {columnsMap.get(column)}
                    </label>)
                } */}
            <Row>
                <Col>
                <Datatable data = {search(data)} />
                </Col>
            </Row>
            </Container>
            
            {/*Advanced Search Modal*/}
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                <Modal.Title>Advanced Search (Coming Soon)</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Container fluid>
                        <Row>
                            <Col>
                            <TextField
                                id="date"
                                label="Date of Capture"
                                type="date"
                                defaultValue="1876-05-24"
                                InputLabelProps={{
                                shrink: true,
                                }}
                            />
                            </Col>
                            <Col>
                            <TextField
                                id="date"
                                label="Date of Adjudication"
                                type="date"
                                defaultValue="1876-05-24"
                                InputLabelProps={{
                                shrink: true,
                                }}
                            />
                            </Col>
                        </Row>
                        <hr />
                        <Row>
                            <Typography id="range-slider" gutterBottom>
                                Total People Between {value[0]} and {value[1]}
                            </Typography>
                            <Slider
                                value={value}
                                onChange={handleChange}
                                valueLabelDisplay="auto"
                                aria-labelledby="range-slider"
                                getAriaValueText={valuetext}
                                max="500"
                            />
                        </Row>
                        <hr />

                        <Row>
                            <Accordion>
                            <Card>
                            <Accordion.Toggle as={Button} variant="link" eventKey="0">
                                Specific sliders
                            </Accordion.Toggle>
                            <Accordion.Collapse eventKey="0">
                            <Card.Body>
                                <Container fluid>
                                <Row>
                            <Typography id="range-slider" gutterBottom>
                                Number of Men Between {value[0]} and {value[1]}
                            </Typography>
                            <Slider
                                value={value}
                                onChange={handleChange}
                                valueLabelDisplay="auto"
                                aria-labelledby="range-slider"
                                getAriaValueText={valuetext}
                                max="500"
                            />
                            </Row>
                            <hr />
                            <Row>
                                <Typography id="range-slider" gutterBottom>
                                    Number of Women Between {value[0]} and {value[1]}
                                </Typography>
                                <Slider
                                    value={value}
                                    onChange={handleChange}
                                    valueLabelDisplay="auto"
                                    aria-labelledby="range-slider"
                                    getAriaValueText={valuetext}
                                    max="500"
                                />
                            </Row>
                            <hr />
                            <Row>
                                <Typography id="range-slider" gutterBottom>
                                    Number of Girls Between {value[0]} and {value[1]}
                                </Typography>
                                <Slider
                                    value={value}
                                    onChange={handleChange}
                                    valueLabelDisplay="auto"
                                    aria-labelledby="range-slider"
                                    getAriaValueText={valuetext}
                                    max="500"
                                />
                            </Row>
                            <hr />
                            <Row>
                                <Typography id="range-slider" gutterBottom>
                                    Number of Boys Between {value[0]} and {value[1]}
                                </Typography>
                                <Slider
                                    value={value}
                                    onChange={handleChange}
                                    valueLabelDisplay="auto"
                                    aria-labelledby="range-slider"
                                    getAriaValueText={valuetext}
                                    max="500"
                                />
                            </Row>
                                </Container>
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                            </Accordion>
                        </Row>
                    </Container>
                </Modal.Body>
                <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
                <Button variant="disable">
                    Search
                </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}