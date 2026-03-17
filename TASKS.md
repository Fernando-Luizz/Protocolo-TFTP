# Divisão de tarefas da equipe

Para evitar conflitos no repositório e deixar a participação de cada integrante bem definida, o projeto foi dividido por áreas de responsabilidade. Cada integrante ficará responsável por uma parte principal do sistema e fará suas alterações em branch própria, sempre enviando por pull request.

## Fernando — Infraestrutura, diagramas e documentação

Responsável pela organização inicial do projeto.

**Atividades:**
- criar o repositório no GitHub e adicionar os integrantes da equipe;
- configurar o arquivo `.gitignore`;
- montar a estrutura inicial do `README.md`;
- produzir os diagramas que serão colocados na documentação:
  - um diagrama de containers, mostrando a visão geral do sistema;
  - um diagrama de componentes, mostrando a estrutura interna da aplicação.

**Arquivos principais:**
- `README.md`
- `.gitignore`
- imagens dos diagramas

## Pessoa 2 — Base do protocolo

Responsável pela parte fundamental da comunicação TFTP: a criação e interpretação dos pacotes enviados pela rede.

**Atividades:**
- usar a biblioteca `struct` do Python;
- implementar as funções de montagem e leitura dos pacotes TFTP;
- tratar os pacotes:
  - `RRQ` (leitura),
  - `WRQ` (escrita),
  - `DATA` (dados),
  - `ACK` (confirmação),
  - `ERROR` (erro).

**Arquivo principal:**
- `tftp_packets.py`

## Pessoa 3 — Servidor

Responsável pelo desenvolvimento do servidor TFTP.

**Atividades:**
- importar o módulo `tftp_packets.py`;
- implementar a interface de linha de comando com `argparse`;
- usar `socket` UDP para escutar a porta do serviço;
- permitir uso da porta `69` ou, em testes locais, de uma porta alta como `6969`;
- tratar requisições `RRQ` e `WRQ`;
- controlar envio e recebimento de blocos, `ACKs` e retransmissão simples em caso de timeout;
- criar um socket efêmero após a requisição inicial, conforme o funcionamento do protocolo.

**Arquivo principal:**
- `server.py`

## Gabriel Pepes — Cliente

Responsável pela implementação do cliente TFTP.

**Atividades:**
- importar o módulo `tftp_packets.py`;
- criar a interface de linha de comando com `argparse`;
- permitir comandos de envio e recebimento de arquivos;
- enviar requisições `RRQ` e `WRQ` via UDP;
- tratar a troca de blocos de dados, `ACKs` e timeout simples durante a comunicação com o servidor.

**Arquivo principal:**
- `client.py`

## Pessoa 5 — Testes, padronização e revisão final

Responsável pela validação do projeto e pelos ajustes finais.

**Atividades:**
- revisar o código com foco no padrão PEP 8;
- usar ferramentas como `black` ou `flake8`;
- realizar testes sem concentrar grandes alterações nos arquivos dos colegas;
- fazer apenas ajustes pequenos e combinados em `server.py` e `client.py`, quando necessário;
- testar o servidor com um cliente TFTP nativo do Windows, Linux ou Mac;
- registrar os testes com capturas de tela;
- adicionar os prints e a parte final da documentação no repositório.

**Pastas principais:**
- `tests/`
- `prints/`
