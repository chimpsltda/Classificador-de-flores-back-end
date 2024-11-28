const functions = require('firebase-functions');
const { spawn } = require('child_process');

// Função para iniciar o servidor Flask
exports.api = functions.https.onRequest((req, res) => {
  const process = spawn('python', ['./flask_api/app.py']);
  
  // Captura a saída do servidor Flask
  process.stdout.on('data', (data) => {
    res.status(200).send(data.toString());
  });

  process.stderr.on('data', (data) => {
    console.error(data.toString());
    res.status(500).send('Error starting Flask server.');
  });
});
