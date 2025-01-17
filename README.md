# Leitor de Contratos em Áudio

Este projeto foi desenvolvido como parte do projeto final do **Bootcamp CAIXA - IA Generativa com Microsoft Copilot**. Ele oferece uma solução para tornar acessível a leitura de contratos digitalizados no formato PDF, convertendo o texto em áudio de maneira automática.

O código-fonte está disponível neste repositório e pode ser acessado para exploração, testes e melhorias.

---

## 🌟 Contexto e Motivação

Existem diversas tecnologias no mercado que realizam a transcrição de texto para áudio, o que é útil tanto para pessoas que preferem ouvir a ler quanto para aquelas com dificuldades visuais. Inspirado por essas ferramentas, este projeto implementa um algoritmo capaz de:

- **Extrair texto** de contratos digitalizados em PDF.
- **Converter o texto extraído em áudio** no formato MP3.

A solução utiliza ferramentas apresentadas no bootcamp e outras tecnologias complementares, entregando um resultado funcional e satisfatório, disponível para uso por qualquer pessoa que configure corretamente o ambiente.

---

## 🔧 Ferramentas Utilizadas

As tecnologias e ferramentas usadas para o desenvolvimento incluem:

- **[Visual Studio Code](https://code.visualstudio.com/)**: Ambiente de desenvolvimento integrado (IDE).
- **Python 3.12.8 (ou superior)**: Linguagem de programação.
- **[Microsoft Copilot](https://github.com/features/copilot)**: Assistente de desenvolvimento baseado em IA.
- **ChatGPT**: Para suporte na geração e refinamento do código.
- **[Azure Computer Vision](https://azure.microsoft.com/services/cognitive-services/computer-vision/)**: Para extração de texto via OCR.
- **[Azure Speech Service](https://azure.microsoft.com/services/cognitive-services/speech-services/)**: Para conversão de texto em áudio.
- **[Azure Blob Storage](https://azure.microsoft.com/services/storage/blobs/)**: Para armazenamento dos arquivos PDF.
- **[Chocolatey](https://chocolatey.org/)**: Gerenciador de pacotes utilizado para instalar o FFmpeg, necessário para a biblioteca Python `pydub`.

---

## ⚙️ Configuração do Ambiente

Para executar o projeto, você precisará:

1. **Conta verificada na Azure**: As ferramentas da Azure exigem uma conta configurada.
2. **Configuração do sistema operacional**: O projeto foi desenvolvido em **Windows**. Caso utilize outro SO, podem ser necessários ajustes específicos.
3. **Instalação do Chocolatey**: Para garantir o funcionamento correto da biblioteca `pydub`, siga as instruções no [site oficial do Chocolatey](https://chocolatey.org/).

### Variáveis de Ambiente

Configure corretamente as variáveis de ambiente necessárias para o uso das ferramentas da Azure. Consulte os links abaixo para detalhes:

- [Azure Computer Vision](https://learn.microsoft.com/azure/cognitive-services/computer-vision/)
- [Azure Text-to-Speech](https://learn.microsoft.com/azure/cognitive-services/speech-service/)

---

## 🛠️ Processo de Desenvolvimento

O código foi desenvolvido de forma iterativa, utilizando:

- **Microsoft Copilot**: Para sugestões e geração de código.
- **ChatGPT**: Para suporte em prompts e refinamento.

Prompts variaram entre simples e complexos, conforme a funcionalidade desejada.

---

## 🚀 Fluxo do Algoritmo

O algoritmo segue os seguintes passos:

1. **Importação dos Arquivos PDF**:  
   Os arquivos são carregados a partir de uma pasta no **Azure Blob Storage**. Estes documentos referem-se a contratos disponíveis publicamente.

2. **Extração de Texto (OCR)**:  
   Utilizando o **Azure Computer Vision**, o texto dos PDFs é extraído página por página e armazenado em um arquivo TXT temporário. Este método evita exceder os limites de requisições gratuitas.

3. **Conversão de Texto em Áudio**:  
   O texto extraído é processado pelo **Azure Speech Service**, gerando arquivos de áudio por página. Ao final, os áudios são combinados em um único arquivo MP3.

4. **Armazenamento e Finalização**:  
   O arquivo final é salvo no mesmo diretório onde o programa foi executado. Arquivos temporários são utilizados para garantir a confiabilidade do resultado.

### Detalhes Técnicos

- O arquivo final é gerado em formato **MP3**, otimizando o armazenamento.
- O sintetizador básico da Microsoft foi utilizado, mas outras vozes podem ser configuradas no código, conforme a preferência do programador.

---

## 🌍 Aplicações e Usos

A principal finalidade do projeto é tornar a leitura de contratos mais acessível. Exemplos de aplicação:

- **Apresentação ao Cliente**: Empresas podem utilizar o sistema para explicar contratos de forma dinâmica e inclusiva.
- **Uso Interno**: Profissionais com dificuldades visuais podem acessar contratos de forma independente.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Se você deseja melhorar o projeto, siga os passos abaixo:

1. Faça um fork deste repositório.
2. Crie uma branch para suas alterações (`git checkout -b feature/nova-funcionalidade`).
3. Envie suas mudanças por meio de um pull request.

---

Este projeto exemplifica como tecnologias acessíveis, como o Microsoft Copilot, ferramentas da Azure e bibliotecas Python, podem simplificar processos e aumentar a inclusão digital.

**Explore, teste e colabore!**
