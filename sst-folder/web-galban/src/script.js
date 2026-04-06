const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;
const HTMLFILE = "index.html";

app.use(express.static(path.join(__dirname, '../public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, `../public/${HTMLFILE}`));
});

app.listen(PORT, () => {
    console.log(`Servidor escuchando en http://localhost:${PORT}`);
});
