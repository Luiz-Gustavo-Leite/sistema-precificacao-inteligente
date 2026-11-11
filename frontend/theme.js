
function aplicarTema() {

    const tema = localStorage.getItem('tema') || 'dark';

    document.body.classList.remove('dark-mode', 'light-mode');
    document.body.classList.add(`${tema}-mode`);

    const botoesTema = document.querySelectorAll('.theme-toggle');

    botoesTema.forEach(botao => {

        if (tema === 'dark') {

        botao.innerHTML = `
            <svg width="30" height="30" viewBox="0 0 32 32"
                xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M23 3.5
                        A13 13 0 1 0 28.5 24
                        A11 11 0 0 1 23 3.5Z"
                    fill="#FFD43B"
                />
            </svg>
        `;            
        
        botao.setAttribute('aria-label', 'Ativar modo claro');

        } else {

            botao.innerHTML = `
    <svg width="30" height="30" viewBox="0 0 32 32"
         xmlns="http://www.w3.org/2000/svg">
        <g fill="none" stroke="#FFD43B" stroke-width="2.5"
           stroke-linecap="round">
            <path d="M16 2 V6 M16 26 V30
                     M2 16 H6 M26 16 H30
                     M6.1 6.1 L9 9
                     M23 23 L25.9 25.9
                     M25.9 6.1 L23 9
                     M9 23 L6.1 25.9"/>
        </g>
        <circle cx="16" cy="16" r="7" fill="#FFD43B"/>
    </svg>
`;
            botao.setAttribute('aria-label', 'Ativar modo escuro');
        }
    });
}

function alternarTema() {

    const temaAtual = localStorage.getItem('tema') || 'dark';

    const novoTema = temaAtual === 'dark' ? 'light' : 'dark';

    localStorage.setItem('tema', novoTema);

    aplicarTema();
}

document.addEventListener('DOMContentLoaded', aplicarTema);
