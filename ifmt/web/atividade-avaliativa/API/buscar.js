const express = require('express');
const app = express();
app.use(express.json());

let dados = [
    {id : "1", nome : "black myth wokong"},
    {id : "2", nome : "Apex Legends"},
    {id : "3", nome : "Minecraft"},
    {id : "4", nome : "Free Fire"},
]

app.get("/", (req, res) => {
    res.json(dados);
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
    const { id } = req.params;

    const encontrado = dados.find(item => item.id === id);

    if (!encontrado) {
        return res.status(404).json({
            erro: "Item não encontrado"
        });
    }

    dados = dados.filter(item => item.id !== id);

    res.status(200).json({
        mensagem: "Item removido com sucesso!",
        dados
    });
});

app.listen(3000, () => console.log("Servidor rodando na porta 3000"));

###############################################################################################################################################################################
// CRUD  

const express = require('express');
const app = express();
app.use(express.json());

let dados = [
    {id : 1, nome : "black myth wokong"},
    {id : 2, nome : "Apex Legends"},
    {id : 3, nome : "Minecraft"},
    {id : 4, nome : "Free Fire"},
];

let proximoId = 3;

app.get("/dados", (req, res) => {
    res.status(200).json(dados);
});

app.get("/dados/:id", (req, res) => {
    const id = Number(req.params.id);
    const dado = dados.find(item => item.id === id);
    if (!dado) {
        return res.status(404).json({erro : "Aluno não encontrado"});
    }
    res.status(200).json(dado);
});
    /*
    const encontrado = dados.find(item => item.id === req.params.id); 
    if(!encontrado){
        return res.status(404).json({ erro: "Item não encontrado" });
    }else {
        res.json(encontrado);
    }
})
    */

app.post("/dados/postar", (req, res) => {
    const {nome, jogo} = req.body;
    const noNovoJogo = {id: proximoId++, nome, curso};
    dados.push(noNovoJogo);
    res.status(201).json(noNovoJogo)
})



app.delete("/itens/delete/:id", (req, res) => {
    const { id } = req.params;

    const encontrado = dados.find(item => item.id === id);

    if (!encontrado) {
        return res.status(404).json({
            erro: "Item não encontrado"
        });
    }

    dados = dados.filter(item => item.id !== id);

    res.status(200).json({
        mensagem: "Item removido com sucesso!",
        dados
    });
});

app.listen(3000, () => console.log("Servidor rodando na porta 3000"));

