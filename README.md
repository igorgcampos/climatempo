# climatempo-monolito

Esse projeto automatiza a contrução do mapa da previsão do tempo (na versão impresa do jornal OGlobo), assim utilizando a AWS como o provedor de infraestrutura e o Climatempo como o provedor de informação sobre a previsão do tempo.

Estamos consumindo os 2 endpoints da api do Climatempo para realizar a consulta da previsão do tempo.

- ``` /api-manager/user-token/<api_token>/locales ```
  - Aqui listamos as cidades cadastradas em nossa conta
<br>

- ``` /api/v1/forecast/locale/<city_id>/days/15?token=<api_token> ```
  - Usamos esse endpoitn para consultar a previsão do tempo de cada cidade registrada em nossa conta
<br>

#### Configurando o ambiente de Produção:

- As variaveis de ambiente serão configuradas em um arquivo .env
<br>

- Certifique-se que a variavel "ENV" esteja com o valor "prod"
<br>

- Obtenha a API Key no [dashboard do Climatempo](https://advisor.climatempo.com.br/login) e coloque na variavel "CLIMATEMPO_API_KEY"
<br>

- Atualmente a api do Climatempo está nos fornecendo um limite de 60 requisições por minuto (1 requisição por segundo), ou seja, a variavel "CLIMATEMPO_MAX_REQUEST_PER_SECOND" deve estar com valor 1 caso contrario a api irá responder com um status 429
<br>

- Ao configurar as credenciais da AWS certifique-se de apagar as variaveis "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY" e "AWS_REGION". 
<br>

- Verificar se já está configurado o AWS CLI ou se ja foi definida as veriaveis de ambiente (fora do arquivo .env) "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION". Aqui está a [documentação](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/cli-configure-envvars.html) de como fazer
<br>

~~~Bash
ENV="prod"
CLIMATEMPO_API_KEY="<api-key>"
CLIMATEMPO_URL="http://apiadvisor.climatempo.com.br"
CLIMATEMPO_MAX_REQUEST_PER_SECOND="1"
AWS_CLIMATEMPO_BUCKET="infoglobo-climatempo-forecast-bucket"
TIDE_TABLE_ZIP="tide/tide-table.zip"
~~~
<br>

#### Configurando o ambiente local:

- Confirme que tenha instalado docker e docker-compose em sua maquina!
<br>

- Nesse primeiro passo iremos executar os serviços de mock para a AWS e Climatempo, execute esse comando no terminal ```docker-compose -f ./docker/docker-compose.yml up --build```
<br>

- Temos algumas mudanças nas variaveis de ambiente (em nosso arquivo .env), mas não muitas. Na primeira alteração precisamos adicionar a variavel "LOCALSTACK_URL", ela contem o endereço do Localstack, ou seja, adicione o valor "http://localhost:4566", "CLIMATEMPO_URL" para "http://localhost:1080" e "CLIMATEMPO_API_KEY" para "a3dcb4d229de6fde0db5686dee47145d"
<br>

- Ainda no arquivo .env, troque o valor da "ENV" para "local" e adicione as credenciais da AWS nesse arquivo, sendo "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY" e "AWS_REGION".
<br>

- Ao executar o Localstack será criado um bucket com o nome de "climatempo-cities-bucket"
<br>

~~~Bash
ENV="local"
LOCALSTACK_URL="http://localhost:4566"
CLIMATEMPO_API_KEY="a3dcb4d229de6fde0db5686dee47145d"
CLIMATEMPO_URL="http://localhost:1080"
CLIMATEMPO_MAX_REQUEST_PER_SECOND="1"
AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXXXXXX"
AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
AWS_REGION="us-east-1"
AWS_CLIMATEMPO_BUCKET=""
TIDE_TABLE_ZIP="tide/tide-table.zip"
~~~

#### Instalar dependências

- Certifique-se de ter o poetry instalado, caso não tenha aqui está o [tutorial](https://python-poetry.org/docs/#installation)
<br>

- O proximo passo é instalar as dependecias, execute o seguinte comando na raiz do projeto ```poetry install```

#### Executar o projeto

- Antes de executar o projeto, assegure que a pasta assets esteja atualizada e presente na raiz do projeto com os arquivos "template.xml" e "tide-table.zip"
<br>


- Para rodar o projeto basta executar esse comando na raiz do projeto ```poetry run python ./climatempo/main.py```
