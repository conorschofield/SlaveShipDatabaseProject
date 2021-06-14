import React from "react";
import Table from "react-bootstrap/Table";
import { useHistory } from "react-router-dom"

export default function Datatable({ data }) {
    const headers = ["Volume", "Start Page", "End Page", "Ship", "Court", "Capturing Ship", "Place of Capture","Date of Adjudication" , "Date of Capture", "Men", "Women", "Boys", "Girls", "Total"]
    const columns = ["Volume", "StartPage", "EndPage", "CaseN", "Court", "Captor", "Location", "RAW_DateOfAdjudication", "RAW_DateOfCapture","Men", "Women", "Children_m", "Children_f", "Total"];
    const history = useHistory();
    const handleRowClick = (row) => {
        history.push(`/cases/${row.Uniq}`);
    }  

    return (
        <Table striped bordered hover size="sm" responsive = "xl">
            <thead key = "table head">
                <tr>{data[0] && headers.map((heading) => <th>{heading}</th>)}</tr>
            </thead>
            <tbody key = "table body">
                {data.map(row => <tr key = {row.Uniq} onClick={() => handleRowClick(row)}>
                        {
                            columns.map(column => <td>{row[column]}</td>)
                        }
                        </tr>)}
            </tbody>
        </Table>
    );
}