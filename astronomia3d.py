import pyvista as pv
import numpy as np


def esfera(plotter, raio, posicao, cor, nome=None):
    posicao = tuple(float(v) for v in posicao)

    mesh = pv.Sphere(radius=raio,center=posicao,theta_resolution=64,phi_resolution=64)

    actor = plotter.add_mesh(mesh,color=cor,smooth_shading=True)

    if nome:
        plotter.add_point_labels([posicao],[nome],font_size=11,show_points=False)

    return actor


def orbita(plotter, distancia):
    theta = np.linspace(0, 2 * np.pi, 500)

    pontos = np.c_[distancia * np.cos(theta),np.zeros_like(theta),distancia * np.sin(theta)].astype(float)

    linha = pv.lines_from_points(pontos)

    plotter.add_mesh(linha,color="gray",opacity=0.25)


def criar_satelite(plotter, posicao):
    x, y, z = posicao

    corpo = pv.Cube(center=(x, y, z),x_length=0.12,y_length=0.12,z_length=0.20)

    painel1 = pv.Cube(center=(x - 0.25, y, z),x_length=0.35,y_length=0.015,z_length=0.12)
    painel2 = pv.Cube(center=(x + 0.25, y, z),x_length=0.35,y_length=0.015,z_length=0.12)

    satelite = pv.MultiBlock([corpo, painel1, painel2]).combine()

    return plotter.add_mesh(satelite,color="silver")


def criar_aneis_saturno(plotter, centro):

    atores = []
    theta = np.linspace(0, 2 * np.pi, 700)

    for raio, cor in [(2.3, "wheat"),(2.65, "gold"),(3.0, "khaki")]:
        pontos = np.c_[centro[0] + raio * np.cos(theta),centro[1] + np.zeros_like(theta),centro[2] + raio * np.sin(theta)].astype(float)

        anel = pv.lines_from_points(pontos)

        actor = plotter.add_mesh(anel,color=cor,line_width=3)
        atores.append(actor)
    return atores


def criar_cometa(plotter, posicao):

    x, y, z = posicao
    nucleo = esfera(plotter,0.28,(x, y, z),"white")
    cauda = []

    for i in range(1, 18):
        raio = 0.16 * (1 - i / 20)

        if raio <= 0:
            raio = 0.02

        parte = esfera(plotter,raio,(x - i * 0.45,y + np.random.uniform(-0.08, 0.08),z + np.random.uniform(-0.08, 0.08)),"cyan")
        cauda.append(parte)
    return nucleo, cauda


def criar_asteroides_meteoros(plotter, quantidade_asteroides=120, quantidade_meteoros=45):
    
    asteroides = []
    meteoros = []

    for _ in range(quantidade_asteroides):
        ang = np.random.uniform(0, 2 * np.pi)
        dist = np.random.uniform(26, 31)

        x = dist * np.cos(ang)
        y = np.random.uniform(-1.2, 1.2)
        z = dist * np.sin(ang)

        raio = np.random.uniform(0.07, 0.20)
        
        asteroide = pv.Sphere(radius=raio,center=(x, y, z),theta_resolution=9,phi_resolution=9)
        
        actor = plotter.add_mesh(asteroide,color=np.random.choice(["gray","dimgray","sienna"]),smooth_shading=False)
                
        asteroides.append(actor)


    for _ in range(quantidade_meteoros):
        ang = np.random.uniform(0, 2 * np.pi)
        dist = np.random.uniform(18, 75)

        x = dist * np.cos(ang)
        y = np.random.uniform(-4, 4)
        z = dist * np.sin(ang)

        raio = np.random.uniform(0.03, 0.10)

        meteoro = pv.Sphere(radius=raio,center=(x, y, z),theta_resolution=7,phi_resolution=7)

        actor = plotter.add_mesh(meteoro,color=np.random.choice(["darkgray","gray","sienna","dimgray"]),smooth_shading=False)

        meteoros.append(actor)

    return asteroides, meteoros


def abrir_astronomia3d(app_principal):

    plotter = pv.Plotter(title="🌌 Mundo Astronômico",window_size=[1200, 800])
    plotter.set_background("black")

    info_objetos = {
        "Sol": "☀ SOL\n\nTipo: Estrela\nComposição: Hidrogênio e hélio\nFunção: Centro gravitacional do Sistema Solar.",
        "Mercúrio": "☿ MERCÚRIO\n\nTipo: Planeta rochoso\nPosição: 1º planeta a partir do Sol\nCaracterísticas: Pequeno, rochoso e muito próximo do Sol.",
        "Vênus": "♀ VÊNUS\n\nTipo: Planeta rochoso\nPosição: 2º planeta a partir do Sol\nCaracterísticas: Atmosfera densa e temperatura extremamente alta.",
        "Terra": "🌍 TERRA\n\nTipo: Planeta rochoso\nPosição: 3º planeta a partir do Sol\nCaracterísticas: Possui água líquida, atmosfera e vida confirmada.",
        "Lua": "🌙 LUA\n\nTipo: Satélite natural da Terra\nCaracterísticas: Orbita a Terra e influencia as marés.",
        "ISS": "🛰 ISS\n\nNome: Estação Espacial Internacional\nTipo: Satélite artificial habitável\nFunção: Laboratório espacial em órbita.",
        "Hubble": "🔭 HUBBLE\n\nNome: Telescópio Espacial Hubble\nTipo: Telescópio espacial\nFunção: Observação astronômica fora da atmosfera.",
        "Marte": "♂ MARTE\n\nTipo: Planeta rochoso\nPosição: 4º planeta a partir do Sol\nCaracterísticas: Planeta vermelho, com calotas polares e sinais antigos de água.",
        "Júpiter": "♃ JÚPITER\n\nTipo: Gigante gasoso\nPosição: 5º planeta a partir do Sol\nCaracterísticas: Maior planeta do Sistema Solar.",
        "Saturno": "♄ SATURNO\n\nTipo: Gigante gasoso\nPosição: 6º planeta a partir do Sol\nCaracterísticas: Famoso por seus anéis.",
        "Urano": "♅ URANO\n\nTipo: Gigante gelado\nPosição: 7º planeta a partir do Sol\nCaracterísticas: Possui eixo de rotação extremamente inclinado.",
        "Netuno": "♆ NETUNO\n\nTipo: Gigante gelado\nPosição: 8º planeta a partir do Sol\nCaracterísticas: Ventos fortes e coloração azul intensa.",
        "Cometa": "☄ COMETA\n\nTipo: Corpo celeste de gelo, poeira e rocha\nCaracterísticas: Pode formar cauda ao se aproximar do Sol.",
        "Asteroides/Meteoros": "☄ ASTEROIDES / METEOROIDES\n\nAsteroides: corpos rochosos menores que planetas, encontrados principalmente entre Marte e Júpiter.",}

    painel_info = plotter.add_text("",position="upper_left",font_size=9,color="white")
    painel_info.SetText(2,info_objetos["Sol"])

    checkboxes = {}

    bloqueando_callback = {"ativo": False}

    def selecionar_objeto(nome):

        if bloqueando_callback["ativo"]:
            return

        bloqueando_callback["ativo"] = True

        for outro_nome, widget in checkboxes.items():
            estado = 1 if outro_nome == nome else 0

            widget.GetRepresentation().SetState(estado)

        painel_info.SetText(2,info_objetos[nome])

        plotter.render()

        bloqueando_callback["ativo"] = False


    nomes_menu = ["Sol","Mercúrio","Vênus","Terra","Lua","ISS","Hubble","Marte","Júpiter","Saturno","Urano","Netuno","Cometa", "Asteroides/Meteoros"]

    plotter.add_text("Selecionar objeto:",position=(10, 640),font_size=8,color="white")
    y = 600

    for nome in nomes_menu:
        widget = plotter.add_checkbox_button_widget(
            callback=lambda value, n=nome: selecionar_objeto(n) if value else None,
            value=True if nome == "Sol" else False,
            position=(10, y),
            size=18,
            color_on="cyan",
            color_off="gray")

        checkboxes[nome] = widget

        plotter.add_text(nome,position=(40, y - 2),font_size=7,color="white")
        y -= 28

    estrelas = np.random.uniform(-350,350,(18000, 3)).astype(float)

    plotter.add_points(estrelas,color="white",point_size=1,render_points_as_spheres=True)
    esfera(plotter,3.5,(0, 0, 0),"yellow","Sol")

    planetas = [
        ["Mercúrio", 8, 0.45, "gray", 4.5],
        ["Vênus", 12, 0.8, "orange", 3.4],
        ["Terra", 17, 1.05, "blue", 2.6],
        ["Marte", 23, 0.75, "red", 2.0],
        ["Júpiter", 32, 2.3, "orange", 1.2],
        ["Saturno", 45, 1.9, "gold", 0.9],
        ["Urano", 58, 1.35, "cyan", 0.65],
        ["Netuno", 70, 1.25, "darkblue", 0.5]]

    atores = {}
    angulos = {}

    for nome, distancia, raio, cor, velocidade in planetas:
        orbita(plotter, distancia)

        ang = np.random.uniform(0, 2 * np.pi)

        x = distancia * np.cos(ang)
        z = distancia * np.sin(ang)

        actor = esfera(plotter,raio,(x, 0, z),cor,nome)
        atores[nome] = {"actor": actor,"distancia": distancia,"velocidade": velocidade}

        angulos[nome] = ang

    terra_ang = angulos["Terra"]
    terra_pos = np.array([17 * np.cos(terra_ang),0,17 * np.sin(terra_ang)])

    saturno_ang = angulos["Saturno"]
    saturno_pos = np.array([45 * np.cos(saturno_ang),0,45 * np.sin(saturno_ang)])

    lua = esfera(plotter,0.22,terra_pos + np.array([3.5, 0.2, 0]),"lightgray")

    iss = criar_satelite(plotter,terra_pos + np.array([1.6, 0.45, 0]))

    hubble = criar_satelite(plotter,terra_pos + np.array([-2.0, -0.45, 0]))

    aneis = criar_aneis_saturno(plotter,saturno_pos)

    cometa, cauda_cometa = criar_cometa(plotter,(-55, 12, 25))

    asteroides, meteoros = criar_asteroides_meteoros(plotter)
    
    
    
    

    for _ in range(350):
        ang = np.random.uniform(0, 2 * np.pi)
        dist = np.random.uniform(26, 29)

        esfera(plotter,np.random.uniform(0.025, 0.06),(dist * np.cos(ang),np.random.uniform(-0.2, 0.2),dist * np.sin(ang)),"gray")

    tempo = {"t": 0}

    def animar(step):
        tempo["t"] += 0.02

        terra_atual = None
        saturno_atual = None

        for nome, dados in atores.items():
            angulos[nome] += 0.004 * dados["velocidade"]

            x = dados["distancia"] * np.cos(angulos[nome])
            z = dados["distancia"] * np.sin(angulos[nome])

            dados["actor"].SetPosition(x, 0, z)
            dados["actor"].RotateY(0.5)

            if nome == "Terra":
                terra_atual = np.array([x, 0, z])
                
            if nome == "Saturno":
                saturno_atual = np.array([x, 0, z])

        if terra_atual is not None:

            lua_ang = tempo["t"] * 4
            lua.SetPosition(*(terra_atual + np.array([3.5 * np.cos(lua_ang),0.2,3.5 * np.sin(lua_ang)])))

            iss_ang = tempo["t"] * 10
            iss.SetPosition(*(terra_atual + np.array([1.55 * np.cos(iss_ang),0.5 * np.sin(iss_ang),1.55 * np.sin(iss_ang)])))

            hubble_ang = tempo["t"] * 7
            hubble.SetPosition(*(terra_atual + np.array([2.0 * np.cos(hubble_ang),-0.45 * np.sin(hubble_ang),2.0 * np.sin(hubble_ang)])))

        if saturno_atual is not None:
            for anel in aneis:
                anel.SetPosition(*saturno_atual)

        plotter.render()

    plotter.add_timer_event(max_steps=100000,duration=30,callback=animar)
    plotter.camera_position = [(0, 85, 135),(0, 0, 0),(0, 1, 0)]
    plotter.show()

    app_principal.deiconify()