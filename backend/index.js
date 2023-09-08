const express = require('express');
const cors = require('cors');
const mysql2 = require('mysql2');
const { promisify } = require('util');

const app = express();

const DATE_START = "1700-01-01";
const DATE_END = "1900-01-01";

// note: use a Pool to automatically reconnect on DB timeout.
const connection = mysql2.createPool({
  host: process.env["DB_HOST"] || '127.0.0.1',
  user: 'root',
  password: 'SeniorProject2021!',
  database: 'SeniorProject2'
});

const queryInternal = promisify(connection.query).bind(connection);
async function query(sql) {
  console.log(`SQL Query: ${sql}`);
  return queryInternal(sql);
}

app.use(cors());

//map each search field to a table
const tbwith = {
  "Uniq": "Cases", "Volume": "Cases", "StartPage": "Cases",
  "EndPage": "Cases", "Men": "SlaveStats", "Women": "SlaveStats",
  "Children_m": "SlaveStats", "Children_f": "SlaveStats",
  "Total": "SlaveStats", "Died": "SlaveStats", "CaseN": "Cases",
  "Location": "Cases", "Captor": "Cases", "CaptureDate": "CaptureDates",
  "Mixed": "Cases", "Court": "Cases", "Ocean": "Cases",
  "AdjudicationDate": "AdjudicationDates", "RedNumber": "Cases",
  "Notes": "Cases"
}

app.get('/api/distinct/', (req, res) => {
  const field = req.query.field;

  if (tbwith[field] === undefined) {
    res.status(400).json({
      error: `Bad field ${field}`
    });
    return;
  }

  return query(`SELECT DISTINCT Cases.${field} `
    + `FROM Cases ORDER BY Cases.${field}`)
    .then(results => results.map(record => record[field]))
    .then(results => res.json(results));
})

app.get('/api/groups/:field', (req, res) => {
  const field = req.params.field;

  if (tbwith[field] === undefined) {
    res.status(400).json({
      error: `Bad field ${field}`
    });
    return;
  }

  return query(`SELECT Cases.${field}, count(*) as Num `
    + `FROM Cases GROUP BY Cases.${field} ORDER BY Cases.${field}`)
    .then(results => 
      results.reduce((obj, record) => {
        obj[record[field]] = record['Num'];
        return obj;
      }, {}))
    .then(results => res.json(results));
})

const text_search_params = [
  "CaseN", "Location", "Captor", "Mixed", "Court",
  "Ocean", "RedNumber", "Notes"];

const date_search_params = ["CaptureDate", "AdjudicationDate"];
//start and end page are single nums because they are separate fields in the 
//mySQL database
const num_search_params = ["Uniq", "StartPage", "EndPage", "Volume"];
const num_range_search_params = [
  "Men", "Women", "Children_m", "Children_f", "Total", "Died"];

let valid_params = []
valid_params.push(...text_search_params)
valid_params.push(...date_search_params)
valid_params.push(...num_search_params)
valid_params.push(...num_range_search_params)

for (key in tbwith) {
  if (!valid_params.includes(key)) {
    throw Error("Internal error: search param " + key + " is not mapped to a type");
  }
}

function fixMysqlDate(d) {
  return d.toISOString().split('T')[0];
}

const dateTables = [
  ['CaptureDates', 'CaptureDate', fixMysqlDate, false],
  ['AdjudicationDates', 'AdjudicationDate', fixMysqlDate, false],
  ['CaptureDatesVerbatim', 'CaptureDateVerbatim', d => d, true],
  ['AdjudicationDatesVerbatim', 'AdjudicationDateVerbatim', d => d, true],
]

/*
return array to query search field varibles
*/
function getSearchVarList(req) {

  let var_params = []
  text_search_params.forEach(param => {
    let val = req.query[param];
    //if val found, add to conditions
    if (val !== undefined)
      var_params.push(tbwith[param] + "." +
        param + " LIKE " 
        + connection.escape('%' + decodeURIComponent(val) + '%'));
  });
  //numeric params must be parsed
  num_search_params.forEach(param => {
    //need to cast these to numbers
    let val = Number(decodeURIComponent(req.query[param]));
    if (!isNaN(val)) 
      var_params.push(tbwith[param] + "." + param + "=" + val);
  });
  
  num_range_search_params.forEach(param => {
    let val = req.query[param];
    if (val !== undefined) {
      val = decodeURIComponent(val).split(',').map(Number);
      var_params.push(tbwith[param] + "." + param + ">=" + val[0]);
      var_params.push(tbwith[param] + "." + param + "<=" + val[1]);
    }
  });

  date_search_params.forEach(param => {
    let val = req.query[param];
    if (val !== undefined) {
      val = decodeURIComponent(val).split(',');
      let date_str = "";

      if (val[0] != DATE_START) {
        date_str += "(" + tbwith[param] + "." + param; //col from table
        date_str += " >= ";
        date_str += "DATE(\'" + val[0] + "\')"; //low date bound
        //get edge cases
        date_str += " OR ";
        date_str += tbwith[param] + "." + param; //col from table
         //capture with same yr and month, but no day
        date_str += " = DATE(\'" + val[0].substring(0,8) + "00'\)";
        date_str += " OR "
        date_str += tbwith[param] + "." + param; //col from table
        //capture with same yr, but no month or day
        date_str += " = DATE(\'" + val[0].substring(0,5) + "00-00'\))"; 
      }

      if (!(val[0] == DATE_START || val[1] == DATE_END)) {
        date_str += " AND " //connect low and hi query
      }
      if (val[1] != DATE_END) {
        date_str += "(" + tbwith[param] + "." + param; //col from table
        date_str += " <= DATE(\'" + val[1] + "\')"; //hi date bound
        //get edge cases
        date_str += " OR "
        date_str += tbwith[param] + "." + param; //col from table
        //capture with same yr and month, but no day
        date_str += " = DATE(\'" + val[1].substring(0,8) + "00'\)"; 
        date_str += " OR ";
        date_str += tbwith[param] + "." + param; //col from table
        //capture with same yr, but no month or day
        date_str += " = DATE(\'" + val[1].substring(0,5) + "00-00'\))"; 
      }
      if (val[0] != DATE_START || val[1] != DATE_END) {
        var_params.push(date_str);
      }
    }
  });

  return var_params;

}

app.get('/api/search/', async (req, res) => {
  for (param in res.query) {
    if (param === 'limit' || param === 'offset') {
      continue;
    }

    if (tbwith[param] === undefined) {
      throw Error("Frontend sent an unrecognized search parameter to the backend");
    }
  }

  let query_string = `SELECT * FROM Cases `
    + "LEFT JOIN SlaveStats ON Cases.Uniq = SlaveStats.Uniq "
    + "LEFT JOIN Captor ON Cases.Captor = Captor.CapID "
    + "LEFT JOIN Location ON Cases.Location = Location.LocID "
    + "LEFT JOIN CaptureDates ON Cases.Uniq = CaptureDates.CaseId "
    + "LEFT JOIN AdjudicationDates ON Cases.Uniq = AdjudicationDates.CaseId "
    + "LEFT JOIN CaptureDatesVerbatim ON Cases.Uniq = CaptureDatesVerbatim.CaseId "
    + "LEFT JOIN AdjudicationDatesVerbatim ON Cases.Uniq = AdjudicationDatesVerbatim.CaseId "

  let var_params = getSearchVarList(req);
    
  if (var_params.length > 0)
    query_string += "WHERE " + var_params.join(" AND ") + " ";

  query_string += " ORDER BY Volume, StartPage ";

  if ('limit' in req.query) {
    query_string += `LIMIT ${req.query.limit} `
  }

  if ('offset' in req.query) {
    query_string += `OFFSET ${req.query.offset} `
  }

  const ungrouped = await query(query_string);
  let grouped = new Map();

  ungrouped.forEach(record => {
    existing = grouped.get(record['Uniq'])

    // Merge different field values for the date fields,
    // as cases with multiple dates will return
    // the cartesian products of those dates. This is easier than issuing
    // multiple queries for now.
    dateTables
      .map(([table, field, fixer, singular]) => {
        let existingList = []
        if (existing) {
          existingList = existing[table];
        }

        if (record[field] != null) {
          let proposed = fixer(record[field]);
          // This isn't efficient, but as N < 5 and N is almost always 1,
          // it's not a problem.
          if (existingList.indexOf(proposed) == -1) {
            existingList.push(proposed);
          }
        }

        delete record[field];
        record[table] = existingList;
      })
    
    grouped.set(record['Uniq'], record);
  })

  let finalResult = Array.from(grouped.values())

  res.json(finalResult);
});

app.get('/api/count/', (req, res) => {
  for (param in res.query) {
    if (tbwith[param] === undefined) {
      throw Error("Frontend sent an unrecognized search parameter to the backend");
    }
  }

    let query_string = "SELECT COUNT (DISTINCT Cases.Uniq) as Total FROM Cases "
      + "LEFT JOIN SlaveStats ON Cases.Uniq = SlaveStats.Uniq "
      + "LEFT JOIN Captor ON Cases.Captor = Captor.CapID "
      + "LEFT JOIN Location ON Cases.Location = Location.LocID "
      + "LEFT JOIN CaptureDates ON Cases.Uniq = CaptureDates.CaseId "
      + "LEFT JOIN AdjudicationDates ON Cases.Uniq = AdjudicationDates.CaseId "

    let var_params = getSearchVarList(req);
    
    if (var_params.length > 0)
      query_string += "WHERE " + var_params.join(" AND ") + " ";

  console.log(query_string);
  connection.query(query_string, (err, results) => {
    return (err ? res.send(err) : res.json(results[0]["Total"]))
  });
});

function imageConcordance(volume, startPage, endPage, onFail, onSuccess) {
  let query_string =
    `select PageNumber, ImagePath, Weight, OtherPageNumber ` +
    `from ImageConcordance ` +
    `where Volume=${volume} and PageNumber>=${startPage} and PageNumber<=${endPage}`
  
  connection.query(query_string, (err, records) => {
    if (err) {
      return onFail(err)
    }

    var groupedRecords = new Map()
    records.forEach(record => {
      let abbreviated = {
        'ImagePath': record['ImagePath'],
        'Weight': record['Weight'],
        'OtherPageNumber': record['OtherPageNumber']
      }
  
      let pageNumber = record['PageNumber']
      if (!groupedRecords.has(pageNumber)) {
        groupedRecords.set(pageNumber, [])
      }
      groupedRecords.get(pageNumber).push(abbreviated)
    })

    var coveredUnique = new Set()
    var pages = new Map()

    groupedRecords.forEach((candidates, pageNumber) => {
      if (candidates.length === 1) {
        let candidate = candidates[0]
        let otherPageNumber = candidate['OtherPageNumber']
        let path = candidate['ImagePath']

        coveredUnique.add(pageNumber)
        coveredUnique.add(otherPageNumber)

        pages.set(
          Math.min(pageNumber, otherPageNumber),
          path
        )
      }
    })

    var needed = new Set()
    groupedRecords.forEach((candidates, pageNumber) => {
      if (!coveredUnique.has(pageNumber)) {
        needed.add(pageNumber);
      }
    })

    singles = []

    needed.forEach(pageNumber => {
      candidates = groupedRecords.get(pageNumber)
      var selected

      candidates.forEach(candidate => {
        if (pageNumber === candidate['OtherPageNumber']) {
          selected = candidate
        }
      })

      pages.set(pageNumber, selected['ImagePath'])
    })

    finalPageList = [...pages]
      .sort((p1, p2) => p1[0] - p2[0])
      .map(pair => pair[1])
      .map(path => `/case-images/${path}`)

    onSuccess(finalPageList)
  })
}

app.get('/api/cases/:id', async (req, res) => {
  let caseId = parseInt(req.params.id);

  let caseData = await query("SELECT * FROM Cases "
    + "LEFT JOIN SlaveStats ON Cases.Uniq = SlaveStats.Uniq "
    + "LEFT JOIN Captor ON Cases.Captor = Captor.CapID "
    + "LEFT JOIN Location ON Cases.Location = Location.LocID "
    + "WHERE Cases.Uniq=" + Number(caseId));

  if (caseData.length === 0) {
    res.status(404).json({'error': 'No such case'});
    return;
  }

  let result = caseData[0]

  dateTables.forEach(async entry => {
    let [table, field, fixer, singular] = entry;
    let dates = await query(`SELECT ${field} FROM ${table} WHERE CaseId=${Number(caseId)}`);
    let fixed = dates.map(record => fixer(record[field]));

    if (singular) {
      result[field] = fixed.length > 0 ? fixed[0] : null;
    } else {
      result[table] = fixed;
    }
  })

  imageConcordance(result['Volume'], result['StartPage'], result['EndPage'], err => {
    res.status(500).send(err)
  }, finalPageList => {
    result['CaseImages'] = finalPageList;
    res.json(result)
  })
});

app.get('/api/concordance/:volume/:range', (req, res) => {
  let range = req.params.range.split('-');
  var startPage, endPage
  if (range.length === 1) {
    startPage = endPage = parseInt(range[0])
  } else {
    startPage = parseInt(range[0])
    endPage = parseInt(range[1])
  }
  volume = parseInt(req.params.volume)

  imageConcordance(volume, startPage, endPage, err => {
    res.send(err)
  }, finalPageList => {
    res.json(finalPageList)
  })
});

app.get('/api', (req, res) => {
  res.send('Backend API is operational.\n')
});

app.listen(4000, () => {
  console.log('server listening on port 4000')
});
