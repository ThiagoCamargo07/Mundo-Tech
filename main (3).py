import customtkinter as ctk
from calculos import abrir_calculos
from astronomia3d import abrir_astronomia3d
from tecnologia import abrir_tecnologia


# Configurações do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Janela principal
app = ctk.CTk()

app.geometry("900x600")
app.title("🌎 Mundo Tech")

#Funçoes para os voltar a janela principal
def abrir_tela_calculos():
    app.withdraw()
    abrir_calculos(app)


def abrir_tela_astronomia():
    app.withdraw()
    abrir_astronomia3d(app)


def abrir_tela_tecnologia():
    app.withdraw()
    abrir_tecnologia(app)


# Título
titulo = ctk.CTkLabel(app,text="🌎 Mundo Tech",font=("Arial",30,"bold"))
titulo.pack(pady=30)

subtitulo = ctk.CTkLabel(app,text="Matemática • Astronomia • Tecnologia",font=("Arial",16))
subtitulo.pack()


# Botões
btn1 = ctk.CTkButton(app,text="🧮 Cálculos Númericos",width=250,height=50,command=abrir_tela_calculos)
btn1.pack(pady=20)

btn2 = ctk.CTkButton(app,text="🌌 Observação Astronômica",width=250,height=50,command=abrir_tela_astronomia)
btn2.pack(pady=20)

btn3 = ctk.CTkButton(app,text="💻 Notícias Tecnológicas",width=250,height=50,command=abrir_tela_tecnologia)
btn3.pack(pady=20)

rodape = ctk.CTkLabel(app,text=" Desenvolvido por: Thiago Camargo ",font=("Arial",10))
rodape.pack(side="bottom",pady=10)


app.mainloop()