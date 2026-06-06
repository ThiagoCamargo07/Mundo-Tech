import customtkinter as ctk
import feedparser
import webbrowser


noticias_carregadas = []

def carregar_noticias():
    global noticias_carregadas

    caixa.delete("1.0", "end")
    noticias_carregadas = []

    caixa.insert("end", "Atualizando notícias de tecnologia...\n\n")

    feeds = [
        "https://tecnoblog.net/feed/",
        "https://www.inovacaotecnologica.com.br/rss/",
        "https://canaltech.com.br/rss/",
        "https://www.tudocelular.com/rss/"]

    palavras_tecnologia = [
        "tecnologia",
        "programação",
        "programador",
        "python",
        "javascript",
        "inteligência artificial",
        "ia",
        "chatgpt",
        "openai",
        "google",
        "microsoft",
        "apple",
        "meta",
        "nvidia",
        "computador",
        "software",
        "hardware",
        "cyber",
        "cibersegurança",
        "segurança",
        "dados",
        "robô",
        "robótica",
        "internet",
        "app",
        "aplicativo",
        "celular",
        "smartphone",
        "android",
        "ios",
        "windows",
        "linux",
        "cloud",
        "nuvem",
        "startup",
        "gadget",
        "chip",
        "processador",
        "gpu",
        "energia",
        "spacex",
        "tesla"]

    palavras_bloqueadas = ["mega-sena","loteria","aposta","bbb","futebol","novela","celebridade","horóscopo","signo","receita","culinária","crime","polícia"]

    total = 0
    
    caixa.delete("1.0", "end")

    for url in feeds:
        feed = feedparser.parse(url)

        if feed.bozo:
            continue

        for noticia in feed.entries:
            titulo = noticia.get("title", "")
            resumo = noticia.get("summary", "")
            link = noticia.get("link", "")
            texto_busca = f"{titulo} {resumo}".lower()

            if any(bloqueada in texto_busca for bloqueada in palavras_bloqueadas):
                continue

            if not any(palavra in texto_busca for palavra in palavras_tecnologia):
                continue

            noticias_carregadas.append(link)
            caixa.insert("end",f"{len(noticias_carregadas)} - {titulo}\n")

            if resumo:
                resumo_limpo = resumo.replace("<p>", "").replace("</p>", "")
                caixa.insert("end", f"{resumo_limpo[:250]}...\n")

            caixa.insert("end", f"Fonte: {url}\n")
            caixa.insert("end", "-" * 80 + "\n\n")

            total += 1
            
            if total >= 15:
                break

        if total >= 15:
            break

    if total == 0:
        caixa.insert("end","Nenhuma notícia tecnológica foi encontrada agora.\nTente atualizar novamente em alguns minutos.")


def abrir_link():
    try:
        numero = int(entrada_link.get())

        if numero <= 0 or numero > len(noticias_carregadas):
            caixa.insert("end", "\nNúmero inválido.\n")
            return
        
        webbrowser.open(noticias_carregadas[numero - 1])

    except:
        caixa.insert("end", "\nDigite o número da notícia corretamente.\n")


def abrir_tecnologia(app_principal):

    global caixa
    global entrada_link

    janela = ctk.CTkToplevel()
    janela.geometry("900x650")
    janela.title("💻 Mundo Tecnológico")


    def voltar():
        janela.destroy()
        app_principal.deiconify()


    janela.protocol("WM_DELETE_WINDOW", voltar)
   
    titulo = ctk.CTkLabel(janela,text="💻 Mundo Tecnológico",font=("Arial", 28, "bold"))
    titulo.pack(pady=15)

    subtitulo = ctk.CTkLabel(janela,text="Notícias sobre tecnologia atualizadas em tempo real",font=("Arial", 14))
    subtitulo.pack(pady=5)

    caixa = ctk.CTkTextbox(janela,width=820,height=420)
    caixa.pack(pady=20)

    # Botões e caixas de texto
    frame_botoes = ctk.CTkFrame(janela)
    frame_botoes.pack(pady=10)

    botao_carregar = ctk.CTkButton(frame_botoes,text="Carregar notícias",command=carregar_noticias)
    botao_carregar.grid(row=0, column=0, padx=10)
    
    entrada_link = ctk.CTkEntry(frame_botoes,width=120,placeholder_text="Nº notícia")
    entrada_link.grid(row=0, column=1, padx=10)

    botao_abrir = ctk.CTkButton(frame_botoes,text="Abrir notícia",command=abrir_link )
    botao_abrir.grid(row=0, column=2, padx=10)
    carregar_noticias()

    botao_voltar = ctk.CTkButton(janela,text="⬅ Voltar", command=voltar)
    botao_voltar.pack(pady=10)