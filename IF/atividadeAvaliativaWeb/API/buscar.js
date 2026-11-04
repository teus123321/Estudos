const express = require('express');
const app = express();
app.use(express.json());

let dados = [
    {id : "1", nome : "black myth wokong"},
    {id : "2", nome : "Apex Legends"},
    {id : "3", nome : "Minecraft"},
    {id : "4", nome : "Free Fire"},
]

app.get("/itens", (req, res) => {
    res.send(dados).json();
})

app.get("/itens/:id", (req, res) => {
    const encontrado = dados.find(item => item.id === req.params.id); 
    if(!encontrado){
        return res.status(404).json({ erro: "Item não encontrado" });
    }else {
        res.json(encontrado);
    }
})


app.delete("/itens/delete/:id", (req, res) => {
    const {id} = req.params
    dados = dados.filter((item) => item.id !== id)
    res.status(200).json({ mensagem: 'Item removido com sucesso!', dados });
})

app.listen(3000, () => console.log("Servidor rodando na porta 3000"));
