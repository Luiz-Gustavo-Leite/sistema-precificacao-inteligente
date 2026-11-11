const perfil = localStorage.getItem('perfil');


// ======================================
// ESCONDE ÁREA ADMIN DO COLABORADOR
// ======================================

if(perfil === 'colaborador'){

    const adminArea = document.getElementById('admin-area');

    if(adminArea){
        adminArea.style.display = 'none';
    }
}


// ======================================
// LOGOUT
// ======================================

function logout(){

    localStorage.clear();

    window.location.href = '/logout';
}


// ======================================
// CONFIG
// ======================================

// mesmo host do backend
const API_BASE = '';


// ======================================
// ELEMENTOS
// ======================================

const form = document.getElementById('form');

const statusDiv = document.getElementById('status');

const historyDiv = document.getElementById('history');

const filterInput = document.getElementById('filterInput');

const downloadBtn = document.getElementById('downloadReport');

let cachedRecent = [];


// ======================================
// BUSCA HISTÓRICO
// ======================================

async function fetchRecent(){

  try {

    const res = await fetch(API_BASE + '/api/items');

    const j = await res.json();

    const recent = j.recent || [];

    cachedRecent = recent;

    renderHistory(recent);

  } catch(e){

    console.warn('fetchRecent error', e);

    historyDiv.innerHTML = `
      <div class="entry">
        Não foi possível carregar histórico.
      </div>
    `;
  }
}


// ======================================
// RENDER HISTÓRICO
// ======================================

function renderHistory(items){

  historyDiv.innerHTML = '';

  if (!items || items.length === 0){

    historyDiv.innerHTML = `
      <div class="entry">
        Nenhum registro encontrado.
      </div>
    `;

    return;
  }

  items.forEach(r => {

    const div = document.createElement('div');

    div.className = 'entry';

    const ts = r.timestamp || '';

    const precoFormatted =
      (typeof r.preco === 'number')
      ? r.preco.toFixed(2)
      : r.preco;

    div.textContent =
      `${ts} — Canal ${r.canal}: ${r.nome} — R$ ${precoFormatted}`;

    historyDiv.appendChild(div);
  });
}


// ======================================
// FILTRO
// ======================================

filterInput && filterInput.addEventListener('input', (ev) => {

  const q = (ev.target.value || '')
    .toLowerCase()
    .trim();

  if (!q) {

    renderHistory(cachedRecent);

    return;
  }

  const filtered = cachedRecent.filter(r => {

    const fields =
      `${r.canal} ${r.nome} ${r.timestamp || ''} ${r.preco}`;

    return fields
      .toString()
      .toLowerCase()
      .includes(q);
  });

  renderHistory(filtered);
});


// ======================================
// ENVIO FORM
// ======================================

form.addEventListener('submit', async (ev) => {

  ev.preventDefault();

  const canal =
    Number(document.getElementById('canal').value);

  const nome =
    document.getElementById('nome').value.trim();

  let preco =
    document.getElementById('preco').value.trim();

  if (!nome || !preco){

    statusDiv.textContent =
      'Preencha nome e preço.';

    return;
  }

  // normaliza
  preco = preco
    .replace(/\./g,'')
    .replace(',','.');

  const payload = {

    canal,
    nome,
    preco: Number(preco)
  };

  statusDiv.textContent = 'Enviando...';

  try {

    const res = await fetch(API_BASE + '/api/update', {

      method: 'POST',

      headers: {
        'Content-Type': 'application/json'
      },

      body: JSON.stringify(payload)
    });

    if (res.ok) {

      statusDiv.textContent =
        'Enviado com sucesso!';

      form.reset();

      await fetchRecent();

      setTimeout(() => {

        statusDiv.textContent = '';

      }, 2000);

    } else {

      const j =
        await res.json().catch(() => ({}));

      statusDiv.textContent =
        'Erro: ' +
        (j.detail || j.error || res.statusText);
    }

  } catch (err) {

    statusDiv.textContent =
      'Falha ao conectar: ' + err;

    console.error(err);
  }
});


// ======================================
// BAIXAR RELATÓRIO
// ======================================

downloadBtn &&
downloadBtn.addEventListener('click', async () => {

  downloadBtn.disabled = true;

  downloadBtn.textContent = 'Gerando...';

  try {

    const res =
      await fetch(API_BASE + '/api/relatorio');

    if (!res.ok)
      throw new Error('Falha ao gerar relatório');

    const blob = await res.blob();

    const url =
      window.URL.createObjectURL(blob);

    const a = document.createElement('a');

    a.href = url;

    a.download =
      'relatorio_solicitacoes.xlsx';

    document.body.appendChild(a);

    a.click();

    a.remove();

    window.URL.revokeObjectURL(url);

  } catch (err) {

    alert(
      'Erro ao gerar relatório: ' + err.message
    );

    console.error(err);

  } finally {

    downloadBtn.disabled = false;

    downloadBtn.textContent =
      '📊 Baixar Relatório (.xlsx)';
  }
});


// ======================================
// INIT
// ======================================

fetchRecent();

// ======================================
// ÁREA ADMIN - USUÁRIOS
// ======================================

const adminUsersArea = document.getElementById('admin-users-area');


// ======================================
// ESCONDER ÁREA ADMIN DO COLABORADOR
// ======================================

if(perfil !== 'admin'){

    if(adminUsersArea){

        adminUsersArea.style.display = 'none';
    }
}


// ======================================
// LISTAR USUÁRIOS
// ======================================

async function loadUsers(){

    if(perfil !== 'admin') return;

    try{

        const response = await fetch('/api/users');

        const users = await response.json();

        const usersList = document.getElementById('usersList');

        usersList.innerHTML = '';

        users.forEach(user => {

            const div = document.createElement('div');

            div.className = 'entry';

            div.innerHTML = `
                <strong>${user.username}</strong>
                - ${user.perfil}

                <button
                    onclick="deleteUser(${user.id})"
                    style="margin-left:15px;"
                >
                    Excluir
                </button>
            `;

            usersList.appendChild(div);
        });

    }catch(err){

        console.error(err);
    }
}


// ======================================
// CRIAR USUÁRIO
// ======================================

async function createUser(){

    const username = document.getElementById('newUsername').value;

    const password = document.getElementById('newPassword').value;

    const perfilNovo = document.getElementById('newPerfil').value;

    if(!username || !password){

        alert('Preencha todos os campos');

        return;
    }

    try{

        const response = await fetch('/api/users', {

            method:'POST',

            headers:{
                'Content-Type':'application/json'
            },

            body:JSON.stringify({

                username,
                password,
                perfil:perfilNovo
            })
        });

        const data = await response.json();

        if(data.success){

            alert('Usuário criado com sucesso');

            document.getElementById('newUsername').value = '';

            document.getElementById('newPassword').value = '';

            loadUsers();

        }else{

            alert(data.error || 'Erro ao criar usuário');
        }

    }catch(err){

        console.error(err);

        alert('Erro ao criar usuário');
    }
}


// ======================================
// EXCLUIR USUÁRIO
// ======================================

async function deleteUser(userId){

    const confirmar = confirm(
        'Deseja realmente excluir este usuário?'
    );

    if(!confirmar) return;

    try{

        const response = await fetch(

            `/api/users/${userId}`,

            {
                method:'DELETE'
            }
        );

        const data = await response.json();

        if(data.success){

            loadUsers();
        }

    }catch(err){

        console.error(err);

        alert('Erro ao excluir usuário');
    }
}


// ======================================
// INICIALIZA USUÁRIOS
// ======================================

loadUsers();