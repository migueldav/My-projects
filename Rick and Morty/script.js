const personagens = [
    { imagem: document.querySelector('#img1'), nome: document.querySelector('#nome1'), especie: document.querySelector('#especie1'), condicao: document.querySelector('#status1') },
    { imagem: document.querySelector('#img2'), nome: document.querySelector('#nome2'), especie: document.querySelector('#especie2'), condicao: document.querySelector('#status2') },
    { imagem: document.querySelector('#img3'), nome: document.querySelector('#nome3'), especie: document.querySelector('#especie3'), condicao: document.querySelector('#status3') }
];

gerarValor = () => {
    return Math.floor(Math.random() * 671);
}

pegarPersonagem = (indice) => {
    let numero = gerarValor();
    return fetch(`https://rickandmortyapi.com/api/character/${numero}`, {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            "Content-type": 'application/json'
        }
    }).then((response) => response.json()).then((data) => {
        personagens[indice].imagem.src = `https://rickandmortyapi.com/api/character/avatar/${numero}.jpeg`;
        personagens[indice].imagem.alt = `https://rickandmortyapi.com/api/character/avatar/${numero}.jpeg`;
        personagens[indice].nome.innerHTML = data.name;
        personagens[indice].especie.innerHTML = data.species;
        personagens[indice].condicao.innerHTML = data.status;
    });
}

const botao = document.querySelector('#button');
botao.addEventListener('click', () => {
    for (let i = 0; i < personagens.length; i++) {
        pegarPersonagem(i);
    }
});
