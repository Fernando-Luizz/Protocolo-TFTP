## Arquitetura do sistema

Para representar a estrutura do projeto, usamos o modelo **C4**, dividido em três níveis: **contexto**, **containers** e **componentes**.  
Os diagramas foram elaborados no **draw.io**, com base na arquitetura definida e implementada pela equipe.

A ideia é partir de uma visão mais geral do sistema e chegar até a organização interna do servidor TFTP.

### Tecnologias utilizadas

- **Python 3**
- **socket**
- **argparse**
- **struct**
- **draw.io**
- **GitHub**
- **Modelo C4**

### Integrantes

- Fernando Luiz da Silva Freire
- Gabriel Pepes Moda
- Gustavo Morais De Almada
- Ryan Da Silva Marinho
- Wanderberg De Melo Santana


> **Tecnologias Utilizadas:** Todos os diagramas arquiteturais apresentados abaixo foram elaborados utilizando a ferramenta draw.io

---
### 1. Diagrama de Contexto (Nível 1)
O diagrama de contexto mostra o sistema de forma mais ampla. Nele, aparecem o usuário, o Sistema TFTP em Python, o cliente TFTP nativo do sistema operacional e o sistema de arquivos. Esse diagrama ajuda a visualizar quem interage com a aplicação e quais dependências externas existem.

![Diagrama de Contexto](./Imagens%20Diagramas/Diagrama%20Protocolo%20TFTP-System%20Context%20-%20Nivel%2001.png)

---

### 2. Diagrama de Containers (Nível 2)
Neste nível, o sistema foi dividido em duas partes principais:

* **Cliente TFTP em Python:** Responsável por iniciar as operações de envio e recebimento de arquivos.
* **Servidor TFTP em Python:** Recebe as requisições e processa a transferência.

Também demonstramos que tanto o cliente quanto o servidor acessam seus respectivos sistemas de arquivos. Fica mais clara a comunicação via protocolo **TFTP/UDP** entre os dois lados.

![Diagrama de Containers](./Imagens%20Diagramas/Diagrama%20Protocolo%20TFTP-Container%20-%20Nivel%202.png)

---

### 3. Diagrama de Componentes (Nível 3)
Aqui damos foco total ao **Servidor TFTP em Python**, detalhando os principais módulos internos e suas responsabilidades. Esse diagrama é fundamental para mostrar como o código do servidor foi organizado e o papel de cada parte na transferência de arquivos.

Os componentes representados são:

* **CLI / Argument Parser:** Processa os argumentos recebidos pelo terminal e inicia o servidor.
* **Transfer Manager:** Coordena o fluxo da transferência.
* **UDP Socket Adapter:** Cuida da comunicação pela rede usando o protocolo UDP.
* **File Access:** Realiza a leitura e a gravação dos arquivos no disco.
* **TFTP Packet API:** Centraliza a montagem e a interpretação dos pacotes do protocolo.
  * **Packet Builders:** Constroem os pacotes TFTP.
  * **Packet Parsers:** Interpretam os pacotes recebidos.
  * **TFTP Constants:** Armazenam constantes usadas no protocolo, como *opcodes* e tamanho de bloco.

![Diagrama de Componentes](./Imagens%20Diagramas/Diagrama%20Protocolo%20TFTP-Component%20-%20Nivel%203.png)

---

### Observação sobre os Testes Locais
Nos testes locais, o servidor foi executado na **porta 6969** para evitar problemas de permissão de administrador no sistema operacional (portas privilegiadas). Mesmo assim, a arquitetura e a lógica continuam totalmente baseadas no funcionamento padrão do protocolo TFTP, que utiliza oficialmente a **porta 69**.