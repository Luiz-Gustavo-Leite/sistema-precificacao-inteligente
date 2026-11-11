# Sistema de Precificação Inteligente

Projeto de sistema de precificação com interface web, backend desenvolvido em Python/Flask, armazenamento de dados SQLite e integração com displays OLED.

## Estrutura do Projeto

```text
projeto_oled/
│
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── create_admin.py
│   ├── database.py
│   ├── oled_display.py
│   ├── precificacao.py
│   └── relatorio.py
│
├── frontend/
│   ├── login.html
│   ├── login.js
│   ├── index.html
│   ├── script.js
│   ├── display.html
│   ├── display.js
│   ├── style.css
│   └── theme.js
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Tecnologias Utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Pandas
- Displays OLED SSD1306
- Multiplexador I2C TCA9548A

## Funcionalidades

- Gerenciamento de preços por canais.
- Atualização de informações dos produtos.
- Histórico de solicitações e preços.
- Interface web com modo claro e escuro.
- Tela OLED virtual com atualização automática.
- Integração com displays OLED físicos.
- Sistema de autenticação de usuários.
- Gerenciamento de usuários e perfis.
- Geração e exportação de relatórios Excel.
- Modo simulado para desenvolvimento sem hardware.

## Observações

Os bancos de dados SQLite, relatórios gerados, ambientes virtuais e arquivos temporários não estão incluídos neste repositório.

O banco de dados é inicializado pela aplicação conforme o código do projeto.

Este repositório preserva os arquivos-fonte da aplicação, sem alterações nas funcionalidades existentes.

## Instalação e Configuração

### 1. Instalar as dependências

Na raiz do projeto, execute:

```bash
pip install -r requirements.txt
```

### 2. Configurar a chave secreta do Flask

Por segurança, a chave de sessão do Flask não fica escrita diretamente no código.

1. Na raiz do projeto, copie o arquivo `.env.example`.
2. Crie uma cópia chamada `.env`.
3. Gere uma chave forte e exclusiva com Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

4. Copie o valor gerado para dentro do arquivo `.env`, após `FLASK_SECRET_KEY=`.

Exemplo:

```env
FLASK_SECRET_KEY=sua_chave_secreta_aqui
```

**Importante:** nunca publique o arquivo `.env` no GitHub. Ele já está listado no `.gitignore`.

Cada instalação deve utilizar sua própria chave. Caso ela seja alterada, as sessões de login existentes serão invalidadas.

### 3. Criar o primeiro administrador

O projeto não utiliza contas com senhas padrão, como `admin123` ou `colab123`.

Em uma instalação nova, depois de configurar o arquivo `.env`, execute:

```bash
python backend/create_admin.py
```

O programa solicitará:

- Nome de usuário do administrador.
- Senha com pelo menos 12 caracteres.
- Confirmação da senha.

A senha não aparece durante a digitação e é armazenada no banco de dados utilizando hash.

Depois da criação, entre no sistema com as credenciais cadastradas e utilize o gerenciamento de usuários para adicionar colaboradores.

**Atenção para bancos de dados antigos:** a remoção de contas padrão do código não exclui automaticamente usuários já existentes no SQLite. Verifique se existem contas antigas utilizando senhas padrão e altere ou exclua essas contas antes de disponibilizar o sistema.

## Executar a Aplicação

Na raiz do projeto, execute:

```bash
python backend/app.py
```

O servidor Flask será iniciado na porta `5000`.

Acesse pelo navegador:

- Login: http://localhost:5000
- Sistema: http://localhost:5000/system
- OLED virtual: http://localhost:5000/display

Para acessar pelo celular na mesma rede Wi-Fi, utilize o endereço IP do computador no lugar de `localhost`.

## Modo Simulado

Quando as bibliotecas ou o hardware necessário para os displays OLED não estiverem disponíveis, o sistema poderá utilizar o modo simulado.

Nesse modo, as operações são apresentadas no terminal, permitindo testar parte do funcionamento sem os displays físicos.

## Segurança

- Não compartilhar arquivos `.env`.
- Não publicar senhas ou chaves de acesso.
- Não incluir bancos de dados locais com informações privadas.
- Utilizar senhas fortes para as contas.
- Configurar o servidor adequadamente antes de disponibilizá-lo pela internet.

## Projeto em Desenvolvimento

O Sistema de Precificação Inteligente está em desenvolvimento contínuo, com perspectivas de expansão para integração com aplicativo móvel Flutter e comunicação remota com dispositivos Raspberry Pi.