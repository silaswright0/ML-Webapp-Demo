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
  const py = spawn('python', ['betterforms.py']);

  let dataToSend = '';

  py.stdout.on('data', (data) => {
    dataToSend += data.toString();
  });

  py.stderr.on('data', (err) => {
    console.error(`stderr: ${err}`);
  });

  py.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: 'Python script failed to execute correctly' });
    }

    try {
      const parsedData = JSON.parse(dataToSend);
      res.json(parsedData);  // Send the valid JSON back
    } catch (e) {
      console.error('Failed to parse data:', e);
      res.status(500).send('Invalid data from Python');
    }
  });

  // Send input from user to Python
  py.stdin.write(JSON.stringify(req.body));
  py.stdin.end();
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});