const express = require('express');
const app = express();

const dados = [{
    id : 1, nome : "black myth wokong"
}]

app.get("/itens", (req, res) => {
    res.send(dados).json();
})

app.get("/itens/:id", (res, req) => {
    res.status(404).json({ "erro": "Item não encontrado" });
})

app.delete("/itens/:id", (res, req) => {
    res.status(204).send();
    // 404 se o id não existir 
})

app.listen(3000, () => console.log("Servidor rodando na porta 3000"));
