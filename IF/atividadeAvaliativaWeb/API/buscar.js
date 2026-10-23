async function buscarDados(dd){
    url = `https://brasilapi.com.br/api/ddd/v1/${dd}`;
    Resposta = await fetch(url);
    dados = await Resposta.json();
    estado = dados.state;
    cidades = dados.cities;
    console.log(`O estado é : ${estado}.`);
    console.log("As cidades são : ");
    for (i = 1; i < cidades.length; i++){
        console.log(i, cidades[i])
    }
}

buscarDados(65)