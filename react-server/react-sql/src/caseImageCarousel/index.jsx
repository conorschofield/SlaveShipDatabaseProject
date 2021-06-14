import React from "react";
import {Carousel, Accordion, Button, Card, ListGroup, Container, Row, Jumbotron} from "react-bootstrap";
import {Table, TableBody, TableRow, TableCell} from "@material-ui/core";
import { useHistory } from "react-router-dom";
import ReactPanZoom from 'react-image-pan-zoom-rotate';
//import caseImg from "../assets/HCA-35-01/HCA35-01-1.JPG";
//require('../assets/HCA-35-01/' + entry.imageURL)

// -- add image manipulation (zoom and rotate)

export default function CaseImageCarousel({ data }) {
    console.log(data);
    return (
        <div align="left">
        {
            data.slice(0,1).map(entry => 
                <div>
                <div>
                <ListGroup>
                    <ListGroup.Item><b>Court:</b> {entry.Court}</ListGroup.Item>
                    <ListGroup.Item><b>Ship:</b> {entry.CaseN}</ListGroup.Item>
                    <ListGroup.Item><b>Capturing Ship:</b> {entry.Captor}</ListGroup.Item>
                    <ListGroup.Item><b>Place of Capture:</b> {entry.Location}</ListGroup.Item>
                    <ListGroup.Item><b>Mixed Commision:</b> {entry.Mixed}</ListGroup.Item>
                    <ListGroup.Item><b>Red Number:</b> {entry.RedNumber}</ListGroup.Item>
                    <ListGroup.Item><b>Men:</b> {entry.Men}</ListGroup.Item>
                    <ListGroup.Item><b>Women:</b> {entry.Women}</ListGroup.Item>
                    <ListGroup.Item><b>Boys:</b> {entry.Children_m}</ListGroup.Item>
                    <ListGroup.Item><b>Girls:</b> {entry.Children_f}</ListGroup.Item>
                    <ListGroup.Item><b>Total People:</b> {entry.Total}</ListGroup.Item>
                    <ListGroup.Item><b>Date of Capture:</b> {entry.RAW_DateOfCapture}</ListGroup.Item>
                    <ListGroup.Item><b>Date of Adjudication:</b> {entry.RAW_DateOfAdjudication}</ListGroup.Item>
                </ListGroup>
                </div>
                <div class="jumbotron bg-light">
                    <h3>Notes</h3>
                    <ListGroup horizontal='xl'>
                        <ListGroup.Item>{entry.Notes}</ListGroup.Item>
                    </ListGroup>
                </div>
                </div>
                // <Table>
                //     <TableBody>
                //         <TableRow>
                //             <TableCell variant="head">Court</TableCell>
                //             <TableCell>{entry.Court}</TableCell>
                //         </TableRow>
                //         <TableRow>
                //             <TableCell variant="head">Ship</TableCell>
                //             <TableCell>{entry.CaseN}</TableCell>
                //         </TableRow>
                //         <TableRow>
                //             <TableCell variant="head">Capturing Ship</TableCell>
                //             <TableCell>{entry.Captor}</TableCell>
                //         </TableRow>
                //         <TableRow>
                //             <TableCell variant="head">Place of Capture</TableCell>
                //             <TableCell>{entry.Location}</TableCell>
                //         </TableRow>
                //         <TableRow>
                //             <TableCell variant="head">Mixed Commision</TableCell>
                //             <TableCell>{entry.Mixed}</TableCell>
                //         </TableRow>
                //         <TableRow>
                //             <TableCell variant="head">Number of Men on Ship</TableCell>
                //             <TableCell>{entry.Men}</TableCell>
                //         </TableRow>
                //         <TableRow>
                //             <TableCell variant="head">Number of Women on Ship</TableCell>
                //             <TableCell>{entry.Women}</TableCell>
                //         </TableRow>
                //         <TableRow>
                //             <TableCell variant="head">Number of Boys on Ship</TableCell>
                //             <TableCell>{entry.Children_m}</TableCell>
                //         </TableRow>
                //         <TableRow>
                //             <TableCell variant="head">Number of Girls on Ship</TableCell>
                //             <TableCell>{entry.Children_f}</TableCell>
                //         </TableRow>
                //     </TableBody>
                // </Table>
                )
        }
        {/* {data === undefined ? 
            <div>
            <p>Court: {data[0].Court}</p>
            <p>Ship: {data[0].CaseN}</p>
            <p>Capturing Ship: {data[0].Captor}</p>
            <p>Place of Capture: {data[0].Location}</p>
            <p>Mixed Commision: {data[0].Mixed}</p>
            <p>Red Number: {data[0].RedNumber}</p>
            <p>Number of Men on Ship: {data[0].Men}</p>
            <p>Number of Women on Ship: {data[0].Women}</p>
            <p>Number of Boys on Ship: {data[0].Children_m}</p>
            <p>Number of Girls on Ship: {data[0].Chilren_f}</p>
            <p>Total Number of People on Ship: {data[0].Total}</p>
            <Accordion defaultActiveKey="0">
                <Card>
                    <Card.Header>
                    <Accordion.Toggle as={Button} variant="link" eventKey="0">
                        Notes
                    </Accordion.Toggle>
                    </Card.Header>
                    <Accordion.Collapse eventKey="0">
                    <Card.Body>{data[0].notes}</Card.Body>
                    </Accordion.Collapse>
                </Card>
            </Accordion>
            </div>
            : <p>no data</p>} */}
        <Carousel interval={1000000}>
            {
                data.map(entry => 
                <Carousel.Item>
                    <div class = "img">
                        <ReactPanZoom image={`${'../assets/HCA-35-' + entry.Volume + '/' + entry.imageURL}`} alt = {entry.Page}/>
                    </div> 
                        <Carousel.Caption>
                        <h3>Volume: {entry.Volume} Page: {entry.Page} </h3>
                        </Carousel.Caption>
                </Carousel.Item>)
            }
        </Carousel>
        </div>
    );
}