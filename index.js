// Client-facing API
const express = require('express');
const http = require('http');

const bodyParser = require('body-parser');
const cors = require('cors');


const app = express();
const server = http.createServer(app);
app.use(cors())


app.use(express.static(__dirname));
app.use(bodyParser.json());



/*
// Client requests download
app.get('/download', async (req, res) => {
  
    try {
        var item = {
            
        }
        res.send()
    }
    catch (err) {
      console.error(err)
      res.status(500).send('An error occurred while fetching the data');
    }
  });
*/


server.listen(3002, () => console.log('Listening on port 3001'));
