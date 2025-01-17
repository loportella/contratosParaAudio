from azure.storage.blob import ContainerClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from PyPDF2 import PdfReader, PdfWriter
import os
import time
import requests
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
from tqdm import tqdm

# Função para baixar o arquivo blob
def baixar_blob(blob_url, caminho_download):
    response = requests.get(blob_url)
    with open(caminho_download, 'wb') as file:
        file.write(response.content)

# Função para extrair texto de cada página do PDF
def extrair_texto_do_pdf(caminho_pdf, caminho_saida_txt, cliente_computervision):
    # Abrir o arquivo PDF
    leitor_pdf = PdfReader(caminho_pdf)  # Usar PdfReader para ler o PDF
    

    # Criar/limpar o arquivo de saída
    with open(caminho_saida_txt, "w", encoding="utf-8") as arquivo_saida:
        arquivo_saida.write("")  # Limpa o arquivo de saída, se existir

    linhas_vistas = set()  # Conjunto para armazenar linhas vistas anteriormente

    # Processar cada página individualmente
    for num_pagina, pagina in enumerate(leitor_pdf.pages):
        escritor_pdf = PdfWriter()
        escritor_pdf.add_page(pagina)

        # Salvar a página atual em um arquivo temporário
        caminho_temp_pdf = f"temp_pagina_{num_pagina}.pdf"
        with open(caminho_temp_pdf, "wb") as arquivo_temp_pdf:
            escritor_pdf.write(arquivo_temp_pdf)

        # Enviar a página para a API
        with open(caminho_temp_pdf, "rb") as arquivo_temp_pdf:
            resposta_leitura = cliente_computervision.read_in_stream(arquivo_temp_pdf, raw=True)

        # Obter a localização da operação
        localizacao_operacao_leitura = resposta_leitura.headers["Operation-Location"]
        id_operacao = localizacao_operacao_leitura.split("/")[-1]

        # Aguardar o processamento da API
        while True:
            resultado_leitura = cliente_computervision.get_read_result(id_operacao)
            if resultado_leitura.status not in ["notStarted", "running"]:
                break
            time.sleep(1)

        # Escrever o texto retornado no arquivo de saída
        if resultado_leitura.status == OperationStatusCodes.succeeded:
            with open(caminho_saida_txt, "a", encoding="utf-8") as arquivo_saida:  # Abrir no modo "append"
                for resultado_texto in resultado_leitura.analyze_result.read_results:
                    for linha in resultado_texto.lines:
                        if linha.text not in linhas_vistas and len(linha.text.strip()) > 2:
                            arquivo_saida.write(linha.text + "\n")
                            linhas_vistas.add(linha.text)

        # Remover o arquivo temporário
        os.remove(caminho_temp_pdf)

        # Esperar
        print(f"Página {num_pagina + 1} processada. Aguardando ...")
        time.sleep(10)

# Função para dividir o texto em partes menores
def dividir_texto(texto, comprimento_max=5000):
    return [texto[i:i + comprimento_max] for i in range(0, len(texto), comprimento_max)]

# Função para concatenar os arquivos de áudio usando pydub
def concatenar_audio_pydub(caminhos_clips_audio, caminho_saida):
    combinado = AudioSegment.empty()
    for caminho_clip in tqdm(caminhos_clips_audio, "Lendo arquivos de áudio"):
        audio = AudioSegment.from_mp3(caminho_clip)
        combinado += audio
    combinado.export(caminho_saida, format="mp3")
    print(f"Áudio combinado salvo em: {caminho_saida}")

# Parte principal do script
if __name__ == "__main__":
    # URL do contêiner público
    url_container = "https://arquivosocraudio.blob.core.windows.net/contratos"

    # Criar cliente para o contêiner (sem autenticação, pois é público)
    cliente_container = ContainerClient.from_container_url(url_container)

    # Listar os blobs no contêiner
    lista_blobs = cliente_container.list_blobs()

    # Exibir os URLs completos de cada blob
    print("Blobs disponíveis publicamente:")
    urls_blobs = []
    for i, blob in enumerate(lista_blobs):
        url_blob = f"{url_container}/{blob.name}"
        urls_blobs.append(url_blob)
        print(f"[{i}] {url_blob}")

    # Verificar se há blobs disponíveis
    if not urls_blobs:
        print("Nenhum blob disponível.")
        exit()

    # Solicitar ao usuário que escolha um blob que seja um arquivo .pdf
    while True:
        indice_blob = int(input("Escolha o índice do blob que deseja usar (deve ser um arquivo .pdf): "))
        if indice_blob < 0 or indice_blob >= len(urls_blobs):
            print("Índice inválido.")
        elif not urls_blobs[indice_blob].lower().endswith('.pdf'):
            print("O blob escolhido não é um arquivo .pdf. Tente novamente.")
        else:
            break
    print(f"Blob escolhido: {urls_blobs[indice_blob]}")
    # Autenticação
    chave_assinatura = os.getenv("VISION_KEY")
    endpoint = os.getenv("VISION_ENDPOINT")

    if not chave_assinatura or not endpoint:
        print("As variáveis de ambiente VISION_KEY e VISION_ENDPOINT devem estar definidas.")
        exit()

    cliente_computervision = ComputerVisionClient(endpoint, CognitiveServicesCredentials(chave_assinatura))

    # Caminho do arquivo .txt de saída
    dir_script = os.path.dirname(os.path.abspath(__file__))
    caminho_saida_txt = os.path.join(dir_script, "texto_extraido.txt")

    # Baixar o blob escolhido
    url_escolhido_blob = urls_blobs[indice_blob]
    caminho_temp_pdf = os.path.join(dir_script, "temp_blob.pdf")
    baixar_blob(url_escolhido_blob, caminho_temp_pdf)

    # Extrair texto do PDF baixado e salvar no arquivo .txt
    extrair_texto_do_pdf(caminho_temp_pdf, caminho_saida_txt, cliente_computervision)

    # Remover o arquivo PDF temporário
    os.remove(caminho_temp_pdf)

    print("Texto extraído e salvo em", caminho_saida_txt)

    # Configuração do serviço de síntese de fala
    config_fala = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    config_fala.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3)
    config_fala.speech_synthesis_voice_name = 'pt-BR-FranciscaNeural'

    # Caminho do arquivo de entrada
    caminho_arquivo = caminho_saida_txt

    # Lendo o conteúdo do arquivo de texto
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        texto = arquivo.read()

    # Dividindo o texto em partes menores
    partes_texto = dividir_texto(texto, comprimento_max=5000)

    # Lista para armazenar os arquivos de áudio gerados
    arquivos_audio = []

    # Síntese de fala para cada parte do texto
    for i, parte in enumerate(partes_texto):
        nome_arquivo_audio = f"output_audio_part_{i}.mp3"
        config_audio = speechsdk.audio.AudioOutputConfig(filename=nome_arquivo_audio)
        sintetizador_fala = speechsdk.SpeechSynthesizer(speech_config=config_fala, audio_config=config_audio)

        resultado_sintese_fala = sintetizador_fala.speak_text_async(parte).get()
        sintetizador_fala = None  # Release the synthesizer to close the file

        if resultado_sintese_fala.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f'Audio processado: {nome_arquivo_audio}')
            arquivos_audio.append(nome_arquivo_audio)
        elif resultado_sintese_fala.reason == speechsdk.ResultReason.Canceled:
            detalhes_cancelamento = resultado_sintese_fala.cancellation_details
            print(f"Síntese de fala cancelada: {detalhes_cancelamento.reason}")
            if detalhes_cancelamento.reason == speechsdk.CancellationReason.Error:
                if detalhes_cancelamento.error_details:
                    print(f"Detalhes do erro: {detalhes_cancelamento.error_details}")
                    print("Você configurou a chave de recurso de fala e os valores da região?")

    # Função para juntar os arquivos de áudio gerados
    if arquivos_audio:
        caminho_audio_saida = "contrato_em_audio.mp3"
        concatenar_audio_pydub(arquivos_audio, caminho_audio_saida)
        
        # Remover os arquivos de áudio gerados anteriormente
        for arquivo_audio in arquivos_audio:
            os.remove(arquivo_audio)
        print("Arquivos temorários removidos:")
    else:
        print("Nenhum áudio gerado para combinar.")
