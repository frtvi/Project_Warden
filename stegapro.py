from PIL import Image
import tkinter as tk
from tkinter import filedialog
import base64

# Code by V. Barbosa

# Função para esconder um texto em uma imagem usando base64
def esconder_texto(imagem_path, texto, imagem_saida_path):
    # Codificar o texto em base64
    texto_codificado = base64.b64encode(texto.encode('utf-8')).decode('utf-8')

    # Adicionar a marcação de início e fim para identificar o texto codificado
    marca_inicio = b'---BEGIN_TEXT---'
    marca_fim = b'---END_TEXT---'

    # Converter a imagem em uma bytearray
    with open(imagem_path, 'rb') as imagem_arquivo:
        imagem_binario = bytearray(imagem_arquivo.read())

    # Encontrar a marcação de início e fim no binário da imagem
    pos_inicio = imagem_binario.find(marca_inicio)
    pos_fim = imagem_binario.find(marca_fim)

    # Se a marcação já existe, removê-la
    if pos_inicio != -1 and pos_fim != -1:
        imagem_binario = imagem_binario[:pos_inicio] + imagem_binario[pos_fim + len(marca_fim):]

    # Converter o texto codificado para bytes
    texto_codificado_completo = marca_inicio + texto_codificado.encode('utf-8') + marca_fim

    # Adicionar o texto codificado à imagem
    imagem_binario.extend(texto_codificado_completo)

    # Salvar a imagem resultante
    with open(imagem_saida_path, 'wb') as imagem_saida:
        imagem_saida.write(imagem_binario)

# Função para extrair texto de uma imagem e decodificar usando base64
def extrair_texto_e_salvar(imagem_path, arquivo_saida_path="extração.txt"):
    # Converter a imagem em uma bytearray
    with open(imagem_path, 'rb') as imagem_arquivo:
        imagem_binario = imagem_arquivo.read()

    # Encontrar a marcação de início e fim no binário da imagem
    marca_inicio = b'---BEGIN_TEXT---'
    marca_fim = b'---END_TEXT---'
    pos_inicio = imagem_binario.find(marca_inicio) + len(marca_inicio)
    pos_fim = imagem_binario.find(marca_fim)

    # Extrair o texto codificado entre as marcações de início e fim
    texto_codificado_completo = imagem_binario[pos_inicio:pos_fim]

    # Decodificar o texto usando base64
    texto_decodificado = base64.b64decode(texto_codificado_completo).decode('utf-8', errors='ignore')

    # Salvar o texto extraído automaticamente no arquivo "extração.txt"
    with open(arquivo_saida_path, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto_decodificado)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Esconder e Extrair Texto em Imagem")

# Função chamada quando o botão "Esconder Texto" é pressionado
def on_esconder_click():
    texto = texto_entry.get("1.0", tk.END).strip()  # Obter texto da caixa de texto
    if not texto:
        resultado_label.config(text="Por favor, insira um texto para esconder.")
        return

    imagem_path = filedialog.askopenfilename(title="Selecione a imagem")
    imagem_saida_path = "wownice.png"

    esconder_texto(imagem_path, texto, imagem_saida_path)
    resultado_label.config(text="Texto escondido na imagem com sucesso!")

# Função chamada quando o botão "Extrair Texto" é pressionado
def on_extrair_click():
    imagem_path = filedialog.askopenfilename(title="Selecione a imagem")

    try:
        extrair_texto_e_salvar(imagem_path)
        resultado_label.config(text="Texto extraído e salvo em 'extração.txt' com sucesso!")
    except Exception as e:
        resultado_label.config(text=f"Erro ao extrair texto: {str(e)}")

# Caixa de texto para inserir o texto
texto_entry = tk.Text(root, height=5, width=50)
texto_entry.pack(pady=10)

# Botão para esconder o texto na imagem
button_esconder = tk.Button(root, text="Esconder Texto na Imagem", command=on_esconder_click)
button_esconder.pack(pady=5)

# Botão para extrair texto
button_extrair = tk.Button(root, text="Extrair Texto", command=on_extrair_click)
button_extrair.pack(pady=5)

# Rótulo para exibir o resultado
resultado_label = tk.Label(root, text="")
resultado_label.pack()

# Executar a interface gráfica
root.mainloop()
