# Calculadora de Salário para Professores

Este projeto é uma aplicação simples que permite a um professor calcular seu salário com base na taxa da hora-aula e nas horas semanais trabalhadas em diferentes campi. A aplicação é dividida em duas partes:

- **Backend:** Uma API construída com FastAPI que realiza os cálculos e retorna o salário semanal e mensal, tanto por campus quanto o total geral.
- **Frontend:** Uma interface web mobile-first, desenvolvida com HTML, CSS, JavaScript e Bootstrap, que consome a API para exibir os resultados de forma interativa.

---

## Tecnologias Utilizadas

- **Backend:**
  - Python 3.7+  
  - [FastAPI](https://fastapi.tiangolo.com/)  
  - [Pydantic](https://pydantic-docs.helpmanual.io/)
  - [Uvicorn](https://www.uvicorn.org/) (servidor ASGI)

- **Frontend:**
  - HTML5, CSS3 e JavaScript
  - [Bootstrap 5](https://getbootstrap.com/)

---

## Funcionalidades

- Cálculo do salário semanal e mensal por campus com base no valor da hora-aula e nas horas semanais.
- Exibição dos resultados formatados no padrão brasileiro (ex.: **R$ 7.796,52**).
- Interface responsiva, mobile-first, com a possibilidade de adicionar ou remover dinamicamente campos para diferentes campi.
- Comunicação entre o front-end e a API via requisições HTTP (fetch).

---

## Estrutura do Projeto

```plaintext
controle_salario/
├── app.py         # Código da API FastAPI
├── index.html     # Página principal do front-end
├── style.css      # Arquivo de estilos customizados (além do Bootstrap)
└── script.js      # Lógica JavaScript para interação e consumo da API
```

---

## Como Executar

### 1. Configurando e Executando a API (Backend)

#### Requisitos

- Python 3.7 ou superior

#### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/Hargenx/controle_salario
   cd controle_salario
   ```

2. Instale as dependências necessárias:

   ```bash
   pip install fastapi uvicorn
   ```

#### Execução

Inicie o servidor da API utilizando o Uvicorn:

```bash
uvicorn app:app --reload
```

A API ficará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 2. Executando o Front-end

1. Certifique-se de que a API está em execução.
2. Abra o arquivo `index.html` em seu navegador (você pode abrir diretamente ou utilizar um servidor web local, como o [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) do VSCode).

Ao acessar a página, você encontrará um formulário onde poderá:

- Informar o **Valor da Hora-Aula**.
- Adicionar um ou mais campi, inserindo o nome e as **Horas Semanais** de cada um.
- Enviar o formulário para calcular o salário, que será exibido na própria página.

---

## Configuração de CORS

A API utiliza o `CORSMiddleware` do FastAPI para permitir requisições de outras origens (como o front-end), evitando problemas com o pré-voo OPTIONS. Em ambiente de produção, ajuste o parâmetro `allow_origins` para restringir aos domínios desejados.

---

## Formatação de Valores Monetários

No front-end, o objeto `Intl.NumberFormat` é utilizado para formatar os valores conforme o padrão brasileiro, garantindo que os resultados sejam exibidos como, por exemplo, **R$ 7.796,52**.

---

## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar o projeto ou corrigir algum problema, sinta-se à vontade para:

1. Fazer um fork deste repositório.
2. Criar uma branch com suas alterações (`git checkout -b feature/nome-da-feature`).
3. Enviar um pull request explicando as modificações.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## Contato

Para dúvidas ou sugestões, entre em contato pelo e-mail: [hargenx@hotmail.com](mailto:hargenx@hotmail.com)
