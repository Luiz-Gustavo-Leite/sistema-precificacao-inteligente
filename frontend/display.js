
async function atualizarDisplay() {

    try {

        const response = await fetch('/api/items');
        const data = await response.json();

        const historico = data.recent;

// Mostrar a última atualização realizada no sistema
if (historico.length > 0) {

    const ultimaAtualizacao = historico[0];

    document.getElementById('ultimo-canal').innerText =
        `CANAL ${ultimaAtualizacao.canal}`;

    document.getElementById('ultimo-produto').innerText =
        ultimaAtualizacao.nome.toUpperCase();

    document.getElementById('ultimo-preco').innerText =
        Number(ultimaAtualizacao.preco).toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });

} else {

    document.getElementById('ultimo-canal').innerText =
        'Nenhuma atualização';

    document.getElementById('ultimo-produto').innerText =
        'Aguardando dados...';

    document.getElementById('ultimo-preco').innerText =
        'R$ 0,00';
}

        const seletor = document.getElementById('selecionar-canal');
        const canalSelecionado = Number(seletor.value);

      const produto = historico.find(
        item => Number(item.canal) === canalSelecionado
    );

        document.getElementById('display-canal').innerText =
            `CANAL ${canalSelecionado}`;

        if (produto) {

            document.getElementById('display-produto').innerText =
                produto.nome.toUpperCase();

           document.getElementById('display-preco').innerText =
            Number(produto.preco).toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL'
    });

        } else {

            document.getElementById('display-produto').innerText =
                'SEM PRODUTO';

            document.getElementById('display-preco').innerText =
                'R$ 0,00';
        }

    } catch (error) {

        console.error('Erro ao atualizar display:', error);

    }
}

document.getElementById('selecionar-canal').addEventListener(
    'change',
    atualizarDisplay
);

atualizarDisplay();

setInterval(atualizarDisplay, 2000);
