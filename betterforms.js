//check if we alr have the input history file if so delete it
/*const fs = require('fs');
const path1 = require('path');

const filePath = path1.join(__dirname, 'input_history.json');


if (fs.existsSync(filePath)) {
  fs.unlinkSync(filePath); 
  console.log('File deleted.');
} else {
  console.log('No file to delete.');
}*/

//then get to server business
const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

app.get('/data', (req, res) => {
  const py = spawn('python', ['betterforms.py']);

  let data = '';
  py.stdout.on('data', chunk => data += chunk);

  py.stderr.on('data', err => console.error(`Python error: ${err}`));

  py.on('close', () => {
    try {
      res.json(JSON.parse(data));
    } catch (e) {
      res.status(500).send('Invalid data from Python');
    }
  });
});

app.post('/process', (req, res) => {
  const { spawn } = require('child_process');
  const py = spawn('python', ['betterforms.py']);

  let dataToSend = '';

  py.stdout.on('data', (data) => {
    dataToSend += data.toString();
  });

  py.stderr.on('data', (err) => {
    console.error(`stderr: ${err}`);
  });

  py.on('close', () => {
    res.json({ reply: dataToSend });
  });

  // Send input from user to Python
  py.stdin.write(JSON.stringify(req.body));
  py.stdin.end();
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});