import customtkinter as ctk
import math
import re


def calcular_porcentagem(texto):
    texto = texto.lower().replace(",", ".").replace("%", "")

    padrao = r"([\d.]+)\s*(de|do|da)\s*([\d.]+)"
    resultado = re.search(padrao, texto)

    if not resultado:
        return "Formato inválido.\nUse exemplo: 5% de 1000"

    porcentagem = float(resultado.group(1))
    valor = float(resultado.group(3))

    calculo = (porcentagem / 100) * valor

    return f"""
Porcentagem: {porcentagem}%
Valor base: {valor}

Conta:
({porcentagem} / 100) × {valor}

Resultado:
{calculo}
"""


def atualizar_dica(event=None):
    if menu.get() == "Porcentagem":
        ajuda.configure(text="Exemplo porcentagem: 5% de 1000")
    else:
        ajuda.configure(text="")


def calcular():
    try:
        operacao = menu.get()
        texto = entrada.get().strip()

        if texto == "":
            resposta.configure(text="Digite um valor.")
            return
        
        if operacao == "Binário → Decimal":
            decimal = int(texto, 2)

            resposta.configure(
                text=f"""
                    Binário: {texto}

                    Decimal: {decimal}
                    """)

        elif operacao == "Decimal → Binário":
            valor = int(texto)
            binario = bin(valor).replace("0b", "")

            resposta.configure(
                text=f"""
                    Decimal: {valor}

                    Binário: {binario}
                    """) 

        elif operacao == "Potência":
            valor = float(texto)
            resultado = valor ** 2
            resposta.configure(text=f"{valor}² = {resultado}")

        elif operacao == "Raiz":
            valor = float(texto)

            if valor < 0:
                resposta.configure(text="Erro: não é possível calcular raiz real de número negativo.")
                return

            resultado = math.sqrt(valor)
            resposta.configure(text=f"√{valor} = {resultado}")

        elif operacao == "Porcentagem":
            resultado = calcular_porcentagem(texto)
            resposta.configure(text=resultado)

        else:
            resposta.configure(text="Selecione uma operação.")

    except ValueError:
        resposta.configure(text="Erro: valor inválido para essa operação.")

    except Exception as erro:
        resposta.configure(text=f"Erro inesperado: {erro}")


def abrir_calculos(app_principal):

    global entrada
    global resposta
    global menu
    global ajuda

    janela = ctk.CTkToplevel()

    janela.geometry("700x620")
    janela.title("Calculadora Mundo Tech")

    def voltar():
        janela.destroy()
        app_principal.deiconify()


    janela.protocol("WM_DELETE_WINDOW",voltar)
    
    titulo = ctk.CTkLabel(janela,text="🧮 Calculadora Mundo Tech",font=("Arial", 24, "bold"))
    titulo.pack(pady=20)

    menu = ctk.CTkComboBox(
        janela,
        width=300,
        values=[
            "Binário → Decimal",
            "Decimal → Binário",
            "Potência",
            "Raiz",
            "Porcentagem"],
        command=atualizar_dica)
    
    menu.pack(pady=10)
    menu.set("Binário → Decimal")

    # Botões e caixas de texto
    entrada = ctk.CTkEntry(janela,width=350,placeholder_text="Digite o valor")
    entrada.pack(pady=10)

    ajuda = ctk.CTkLabel(janela,text="",font=("Arial", 12))
    ajuda.pack(pady=5)

    botao = ctk.CTkButton(janela,text="Calcular",command=calcular)
    botao.pack(pady=10)

    resposta = ctk.CTkLabel(janela,text="",font=("Arial", 15),justify="left")
    resposta.pack(pady=20)

    botao_voltar = ctk.CTkButton(janela,text="⬅ Voltar",command=voltar)
    botao_voltar.pack(pady=30)