const express = require('express');
const cors = require('cors');
const mysql = require('mysql');
var CnnPool = require('./CnnPool.js');

const app = express();

const SELECT_ALL_CASES_QUERY = "SELECT * FROM ImageConcordance " + 
"JOIN Images ON ImageConcordance.UniqID = Images.UniqID " +
"JOIN CaseImage ON Images.UniqID = CaseImage.UniqImage";

const SELECT_ALL_CASES_STATS_QUERY = "SELECT * " +
// "FORMAT(CaptureDates.DateOfCapture, 'MMM dd yyyy') as DateOfCapture , " +
// "FORMAT(AdjudicationDates.DateOfAdjudication, 'MMM dd yyyy') as DateOfAdjudication " +
"FROM Cases " +
"JOIN SlaveStats ON Cases.Uniq = SlaveStats.Uniq " +
"JOIN Captor ON Cases.Captor = Captor.CapID " +
"JOIN Location ON Cases.Location = Location.LocID " +
"LEFT JOIN AdjudicationDates ON AdjudicationDates.CaseId = Cases.Uniq " +
"LEFT JOIN CaptureDates ON CaptureDates.CaseId = Cases.Uniq " +
"ORDER BY Cases.Uniq";

const SELECT_CASE_WITH_IMG_QUERY = "SELECT * " +
"FROM ImageConcordance " +
"JOIN Images ON ImageConcordance.UniqID = Images.UniqID " +
"JOIN CaseImage ON Images.UniqID = CaseImage.UniqImage " +
"JOIN Cases ON UniqCase = Cases.Uniq " +
"JOIN SlaveStats ON Cases.Uniq = SlaveStats.Uniq " +
"JOIN Captor ON Cases.Captor = Captor.CapID " +
"JOIN Location ON Cases.Location = Location.LocID " +
"WHERE UniqCase = ? " +
"ORDER BY Page";

const SELECT_FULL_CASE_WITH_IMG_QUERY = "SELECT * " +
"FROM Cases " +
"JOIN SlaveStats ON Cases.Uniq = SlaveStats.Uniq " +
"JOIN Captor ON Cases.Captor = Captor.CapID " +
"JOIN Location ON Cases.Location = Location.LocID " +
"LEFT JOIN AdjudicationDates ON AdjudicationDates.CaseId = Cases.Uniq " +
"LEFT JOIN CaptureDates ON CaptureDates.CaseId = Cases.Uniq " +
"LEFT JOIN CaseImage ON CaseImage.UniqCase = Cases.Uniq " +
"LEFT JOIN Images ON Images.UniqID = CaseImage.UniqImage " +
"LEFT JOIN ImageConcordance ON ImageConcordance.UniqID = Images.UniqID " +
"WHERE CASES.Uniq = ? " +
"ORDER BY Page";


const SELECT_CASE_STAT_QUERY = "SELECT * " +
"FROM Cases " +
"JOIN SlaveStats ON Cases.Uniq = SlaveStats.Uniq " +
"JOIN Captor ON Cases.Captor = Captor.CapID " +
"JOIN Location ON Cases.Location = Location.LocID " +
"WHERE Cases.Uniq = ?";

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'SeniorProject2021',
    database: 'SeniorProject'
});

connection.connect(err => {
    if(err) {
        return err
    }
});

// app.use(function(req, res, next) {
//     console.log("Handling " + req.path + '/' + req.method);
//     res.header("Access-Control-Allow-Origin", "http://localhost:3000");
//     res.header("Access-Control-Allow-Credentials", true);
//     res.header("Access-Control-Allow-Headers", "Content-Type, Location");
//     res.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE, PUT");
//     res.header("Access-Control-Expose-Headers", "Location");
//     res.header("Access-Control-Allow-Request-Headers", "Content-Type, Location");
//     next();
//  });

// // Add DB connection, with smart chkQry method, to |req|
// app.use(CnnPool.router);

app.use(cors());

app.get('/', (req, res) => {
    res.send('go to /cases to see cases')
});

// get all cases
app.get('/cases', (req, res) => {
    connection.query(SELECT_ALL_CASES_QUERY, (err, results) => {
        if(err) {
            return res.send(err)
        }
        else {
            return res.json({
                data: results
            })
        }
    });
});

// get all cases
app.get('/cases/stats', (req, res) => {
    connection.query(SELECT_ALL_CASES_STATS_QUERY, (err, results) => {
        if(err) {
            return res.send(err)
        }
        else {
            return res.json({
                data: results
            })
        }
    });
});

app.get('/cases/:id', (req, res) => {
    var caseId = parseInt(req.params.id);
    connection.query(SELECT_FULL_CASE_WITH_IMG_QUERY, [caseId], (err, results) => {
        if(err) {
            return res.send(err)
        }
        else {
            return res.json({
                data: results
            })
        }
    });
});

app.get('/cases/stats/:id', (req, res) => {
    var caseId = parseInt(req.params.id);
    connection.query(SELECT_CASE_STAT_QUERY, [caseId], (err, results) => {
        if(err) {
            return res.send(err)
        }
        else {
            return res.json({
                data: results
            })
        }
    });
});


app.get('/')

app.listen(4000, () => {
    console.log('server listening on port 4000')
});