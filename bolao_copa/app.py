import streamlit as st
import gspread
import pandas as pd


st.set_page_config(
    page_title="Bolão Copa 2026 🏆", 
    page_icon="⚽", 
    layout="centered"
)


resultados_reais = {
    1: {"gols_a": 2, "gols_b": 0}, 2: {"gols_a": 2, "gols_b": 1}, 3: {"gols_a": 1, "gols_b": 1}, 
    4: {"gols_a": 4, "gols_b": 1}, 5: {"gols_a": 1, "gols_b": 1}, 6: {"gols_a": 1, "gols_b": 1}, 
    7: {"gols_a": 0, "gols_b": 1}, 8: {"gols_a": 2, "gols_b": 0}, 9: {"gols_a": 7, "gols_b": 1},
    10: {"gols_a": 2, "gols_b": 2}, 11: {"gols_a": 1, "gols_b": 0}, 12: {"gols_a": 5, "gols_b": 1}, 
    13: {"gols_a": 0, "gols_b": 0}, 
    16: {"gols_a": 2, "gols_b": 2}, 18: {"gols_a": 1, "gols_b": 4}, 
    19: {"gols_a": 3, "gols_b": 0}
}

jogos_grupos = [
            {"id": 1, "data": "11/06 - 16h00", "time_A": "México", "time_B": "África do Sul"},
            {"id": 2, "data": "11/06 - 23h00", "time_A": "Coréia do Sul", "time_B": "República Tcheca"},
            {"id": 3, "data": "12/06 - 16h00", "time_A": "Canadá", "time_B": "Bósnia e Herzegovina"},
            {"id": 4, "data": "12/06 - 22h00", "time_A": "Estados Unidos", "time_B": "Paraguai"},
            {"id": 5, "data": "13/06 - 16h00", "time_A": "Catar", "time_B": "Suíça"},
            {"id": 6, "data": "13/06 - 19h00", "time_A": "Brasil", "time_B": "Marrocos"},
            {"id": 7, "data": "13/06 - 22h00", "time_A": "Haiti", "time_B": "Escócia"},
            {"id": 8, "data": "13/06 - 01h00", "time_A": "Austrália", "time_B": "Turquia"},
            {"id": 9, "data": "14/06 - 14h00", "time_A": "Alemanha", "time_B": "Curaçau"},
            {"id": 10, "data": "14/06 - 17h00", "time_A": "Holanda", "time_B": "Japão"},
            {"id": 11, "data": "14/06 - 20h00", "time_A": "Costa do Marfim", "time_B": "Equador"},
            {"id": 12, "data": "14/06 - 23h00", "time_A": "Suécia", "time_B": "Tunísia"},
            {"id": 13, "data": "15/06 - 13h00", "time_A": "Espanha", "time_B": "Cabo Verde"},
            {"id": 14, "data": "15/06 - 16h00", "time_A": "Bélgica", "time_B": "Egito"},
            {"id": 15, "data": "15/06 - 19h00", "time_A": "Arábia Saudita", "time_B": "Uruguai"},
            {"id": 16, "data": "15/06 - 22h00", "time_A": "Irã", "time_B": "Nova Zelândia"},
            {"id": 17, "data": "16/06 - 16h00", "time_A": "França", "time_B": "Senegal"},
            {"id": 18, "data": "16/06 - 19h00", "time_A": "Iraque", "time_B": "Noruega"},
            {"id": 19, "data": "16/06 - 22h00", "time_A": "Argentina", "time_B": "Argélia"},
            {"id": 20, "data": "17/06 - 01h00", "time_A": "Áustria", "time_B": "Jordânia"},
            {"id": 21, "data": "17/06 - 14h00", "time_A": "Portugal", "time_B": "RD Congo"},
            {"id": 22, "data": "17/06 - 17h00", "time_A": "Inglaterra", "time_B": "Croácia"},
            {"id": 23, "data": "17/06 - 20h00", "time_A": "Gana", "time_B": "Panamá"},
            {"id": 24, "data": "17/06 - 23h00", "time_A": "Uzbequistão", "time_B": "Colômbia"},
            {"id": 25, "data": "18/06 - 13h00", "time_A": "República Tcheca", "time_B": "África do Sul"},
            {"id": 26, "data": "18/06 - 16h00", "time_A": "Suíça", "time_B": "Bósnia e Herzegovina"},
            {"id": 27, "data": "18/06 - 19h00", "time_A": "Canadá", "time_B": "Catar"},
            {"id": 28, "data": "18/06 - 22h00", "time_A": "México", "time_B": "Coréia do Sul"},
            {"id": 29, "data": "19/06 - 16h00", "time_A": "Estados Unidos", "time_B": "Austrália"},
            {"id": 30, "data": "19/06 - 19h00", "time_A": "Escócia", "time_B": "Marrocos"},
            {"id": 31, "data": "19/06 - 21h30", "time_A": "Brasil", "time_B": "Haiti"},
            {"id": 32, "data": "19/06 - 01h00", "time_A": "Turquia", "time_B": "Paraguai"},
            {"id": 33, "data": "20/06 - 14h00", "time_A": "Holanda", "time_B": "Suécia"},
            {"id": 34, "data": "20/06 - 17h00", "time_A": "Alemanha", "time_B": "Costa do Marfim"},
            {"id": 35, "data": "20/06 - 21h00", "time_A": "Equador", "time_B": "Curaçau"},
            {"id": 36, "data": "20/06 - 01h00", "time_A": "Tunísia", "time_B": "Japão"},
            {"id": 37, "data": "21/06 - 13h00", "time_A": "Espanha", "time_B": "Arábia Saudita"},
            {"id": 38, "data": "21/06 - 16h00", "time_A": "Bélgica", "time_B": "Irã"},
            {"id": 39, "data": "21/06 - 19h00", "time_A": "Uruguai", "time_B": "Cabo Verde"},
            {"id": 40, "data": "21/06 - 22h00", "time_A": "Nova Zelândia", "time_B": "Egito"},
            {"id": 41, "data": "22/06 - 14h00", "time_A": "Argentina", "time_B": "Áustria"},
            {"id": 42, "data": "22/06 - 18h00", "time_A": "França", "time_B": "Iraque"},
            {"id": 43, "data": "22/06 - 21h00", "time_A": "Noruega", "time_B": "Senegal"},
            {"id": 44, "data": "22/06 - 00h00", "time_A": "Jordânia", "time_B": "Argélia"},
            {"id": 45, "data": "23/06 - 14h00", "time_A": "Portugal", "time_B": "Uzbequistão"},
            {"id": 46, "data": "23/06 - 17h00", "time_A": "Inglaterra", "time_B": "Gana"},
            {"id": 47, "data": "23/06 - 20h00", "time_A": "Panamá", "time_B": "Croácia"},
            {"id": 48, "data": "23/06 - 23h00", "time_A": "Colômbia", "time_B": "RD Congo"},
            {"id": 49, "data": "24/06 - 16h00", "time_A": "Suíça", "time_B": "Canadá"},
            {"id": 50, "data": "24/06 - 16h00", "time_A": "Bósnia e Herzegovina", "time_B": "Catar"},
            {"id": 51, "data": "24/06 - 19h00", "time_A": "Marrocos", "time_B": "Haiti"},
            {"id": 52, "data": "24/06 - 19h00", "time_A": "Escócia", "time_B": "Brasil"},
            {"id": 53, "data": "24/06 - 22h00", "time_A": "África do Sul", "time_B": "Coréia do Sul"},
            {"id": 54, "data": "24/06 - 22h00", "time_A": "República Tcheca", "time_B": "México"},
            {"id": 55, "data": "25/06 - 17h00", "time_A": "Equador", "time_B": "Alemanha"},
            {"id": 56, "data": "25/06 - 17h00", "time_A": "Curaçau", "time_B": "Costa do Marfim"},
            {"id": 57, "data": "25/06 - 20h00", "time_A": "Tunísia", "time_B": "Holanda"},
            {"id": 58, "data": "25/06 - 20h00", "time_A": "Japão", "time_B": "Suécia"},
            {"id": 59, "data": "25/06 - 23h00", "time_A": "Turquia", "time_B": "Estados Unidos"},
            {"id": 60, "data": "25/06 - 23h00", "time_A": "Paraguai", "time_B": "Austrália"},
            {"id": 61, "data": "26/06 - 16h00", "time_A": "Senegal", "time_B": "Iraque"},
            {"id": 62, "data": "26/06 - 16h00", "time_A": "Noruega", "time_B": "França"},
            {"id": 63, "data": "26/06 - 21h00", "time_A": "Cabo Verde", "time_B": "Arábia Saudita"},
            {"id": 64, "data": "26/06 - 21h00", "time_A": "Uruguai", "time_B": "Espanha"},
            {"id": 65, "data": "26/06 - 00h00", "time_A": "Egito", "time_B": "Irã"},
            {"id": 66, "data": "26/06 - 00h00", "time_A": "Nova Zelândia", "time_B": "Bélgica"},
            {"id": 67, "data": "27/06 - 18h00", "time_A": "Croácia", "time_B": "Gana"},
            {"id": 68, "data": "27/06 - 18h00", "time_A": "Panamá", "time_B": "Inglaterra"},
            {"id": 69, "data": "27/06 - 20h30", "time_A": "RD Congo", "time_B": "Uzbequistão"},
            {"id": 70, "data": "27/06 - 20h30", "time_A": "Colômbia", "time_B": "Portugal"},
            {"id": 71, "data": "27/06 - 23h00", "time_A": "Jordânia", "time_B": "Argentina"},
            {"id": 72, "data": "27/06 - 23h00", "time_A": "Argélia", "time_B": "Áustria"}
        ]

mapa_bandeiras = {
    "Brasil": "br", "México": "mx", "Alemanha": "de", "Argentina": "ar", 
    "Portugal": "pt", "Inglaterra": "gb-eng", "Espanha": "es", "França": "fr", 
    "Holanda": "nl", "Bélgica": "be", "Japão": "jp", "Catar": "qa", 
    "Austrália": "au", "Canadá": "ca", "Estados Unidos": "us", "Marrocos": "ma", 
    "África do Sul": "za", "Arábia Saudita": "sa", "Argélia": "dz", "Áustria": "at", 
    "Bósnia e Herzegovina": "ba", "Cabo Verde": "cv", "Colômbia": "co", 
    "Costa do Marfim": "ci", "Croácia": "hr", "Curaçau": "cw", "Egito": "eg", 
    "Equador": "ec", "Escócia": "gb-sct", "Gana": "gh", "Haiti": "ht", 
    "Iraque": "iq", "Jordânia": "jo", "Noruega": "no", "Nova Zelândia": "nz", 
    "Panamá": "pa", "Paraguai": "py", "RD Congo": "cd", "Coréia do Sul": "kr", 
    "Irã": "ir", "Senegal": "sn", "Suécia": "se", "Suíça": "ch", "República Tcheca": "cz", 
    "Tunísia": "tn", "Turquia": "tr", "Uruguai": "uy", "Uzbequistão": "uz" 
}

# ==========================================
# 1. FUNÇÕES DO GOOGLE SHEETS, PONTUAÇÃO, BANDEIRAS
# ==========================================

@st.cache_resource
def get_google_client():
    # CORREÇÃO AQUI: Em vez de buscar o arquivo, puxamos do painel Secrets do Streamlit
    credenciais_toml = st.secrets["gcp_service_account"]
    return gspread.service_account_from_dict(credenciais_toml)

def conectar_sheets():
    # Pega o cliente já conectado (ou cria se for a primeira vez)
    gc = get_google_client()
    return gc.open('dados_bolao').worksheet('Palpites')


@st.cache_data(ttl=600)
def carregar_palpites():
    try:
        sh = conectar_sheets()
        data = sh.get_all_records()
        return data if data else []
    except Exception as e:
        st.error(f"Erro ao carregar do Sheets: {e}")
        return []


def salvar_palpite(usuario, jogo_id, gols_a, gols_b):
    sh = conectar_sheets()
    registros = carregar_palpites() 
    df = pd.DataFrame(registros)
    
    # Verifica se já existe um palpite desse jogador para esse jogo
    # Nota: Certifique-se de que sua coluna na planilha se chame 'Jogo_ID' e 'Jogador'
    if not df.empty and 'Jogador' in df.columns and 'Jogo_ID' in df.columns:
        mask = (df['Jogador'] == usuario) & (df['Jogo_ID'].astype(int) == int(jogo_id))
    else:
        mask = pd.Series([False] * len(df))

    if mask.any():
        linha_idx = df[mask].index[0] + 2
        sh.update(f"C{linha_idx}:D{linha_idx}", [[gols_a, gols_b]])
    else:
        sh.append_row([usuario, jogo_id, gols_a, gols_b])


def calcular_pontos(palpite_a, palpite_b, real_a, real_b):
    if palpite_a == real_a and palpite_b == real_b:
        return 2
    
    if palpite_a == palpite_b:
        palpite = "E"
    elif palpite_a > palpite_b:
        palpite = "A"
    else:
        palpite = "B"
        
    if real_a == real_b:
        real = "E"
    elif real_a > real_b:
        real = "A"
    else:
        real = "B"
        
    if palpite == real:
        return 1
    
    return 0


def calcular_ranking():
    todos_palpites = carregar_palpites()
    pontos = {"Peterson": 0, "Kathy": 0}
    
    for p in todos_palpites:
        jogador = str(p['Jogador'])
        jogo_id = int(p['Jogo_ID'])
        
        # Só calcula se o resultado real do jogo já tiver sido inserido no dicionário
        if jogo_id in resultados_reais:
            real = resultados_reais[jogo_id]
            pts = calcular_pontos(int(p['Gols_A']), int(p['Gols_B']), real['gols_a'], real['gols_b'])
            if jogador in pontos:
                pontos[jogador] += pts
    return pontos


def calcular_evolucao_ranking():
    todos_palpites = carregar_palpites()
    
    # O gráfico começa na estaca zero (Jogo 0)
    historico = {
        'Jogo': [0], # Agora o eixo X será o ID do Jogo
        'Peterson': [0],
        'Kathy': [0]
    }
    
    acumulado_peterson = 0
    acumulado_kathy = 0
    
    # Pega apenas os IDs dos jogos que já acabaram (que estão no resultados_reais) e ordena
    jogos_finalizados = sorted(list(resultados_reais.keys()))
    
    # Passa jogo por jogo, linha do tempo real
    for jogo_id in jogos_finalizados:
        real = resultados_reais[jogo_id]
        
        # Pontos do Peterson neste jogo específico
        p_peterson = next((p for p in todos_palpites if str(p['Jogador']) == "Peterson" and int(p['Jogo_ID']) == jogo_id), None)
        pts_peterson = calcular_pontos(int(p_peterson['Gols_A']), int(p_peterson['Gols_B']), real['gols_a'], real['gols_b']) if p_peterson else 0
            
        # Pontos da Kathy neste jogo específico
        p_kathy = next((p for p in todos_palpites if str(p['Jogador']) == "Kathy" and int(p['Jogo_ID']) == jogo_id), None)
        pts_kathy = calcular_pontos(int(p_kathy['Gols_A']), int(p_kathy['Gols_B']), real['gols_a'], real['gols_b']) if p_kathy else 0
            
        # Soma os pontos da partida ao total acumulado
        acumulado_peterson += pts_peterson
        acumulado_kathy += pts_kathy
        
        # Registra a "foto" do momento após esse jogo
        historico['Jogo'].append(jogo_id)
        historico['Peterson'].append(acumulado_peterson)
        historico['Kathy'].append(acumulado_kathy)
        
    return pd.DataFrame(historico).set_index('Jogo')


def get_flag_url(nome_pais):
    codigo = mapa_bandeiras.get(nome_pais, "xx") # "xx" retorna uma bandeira genérica se não achar
    return f"https://flagcdn.com/w40/{codigo}.png"


# ==========================================
# CONTROLE DE SESSÃO (MEMÓRIA DO APP)
# ==========================================
# Se a variável 'logado' não existir na memória, começamos como False
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = None


# ==========================================
# PÁGINA 1: TELA INICIAL (HOME / LOGIN)
# ==========================================
if not st.session_state.logado:
    # Centraliza o título com um visual legal
    st.markdown("<h1 style='text-align: center;'>🏆 Bolão dos Mos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Faça seus palpites, acompanhe o ranking e ganhe prêmios!</p>", unsafe_allow_html=True)
    
    st.write("")
    
    # Caixa de seleção de usuário
    opcoes_usuarios = ["Qual mo é você...", "Peterson", "Kathy"]
    usuario_escolhido = st.selectbox("Qual mo está acessando o Bolão?", opcoes_usuarios)
    
    st.write("")
    
    # Botão para entrar
    if st.button("Entrar", use_container_width=True):
        if usuario_escolhido != "Qual mo é você...":
            # Guarda na memória que o usuário logou com sucesso
            st.session_state.logado = True
            st.session_state.usuario_atual = usuario_escolhido
            st.success(f"Bem-vindo(a), {usuario_escolhido}!")
            st.rerun() # Reinicia o app já na tela interna
        else:
            st.error("Por favor, selecione um usuário válido para continuar.")


# ==========================================
# PÁGINA 2: O APLICATIVO REAL (APÓS LOGIN)
# ==========================================
else:
    # Pega o usuário que ficou salvo na memória
    usuario_atual = st.session_state.usuario_atual
    
    # ==========================================
    # CONFIGURAÇÃO DA BARRA LATERAL (SIDEBAR)
    # ==========================================
    with st.sidebar:
        st.markdown(f"### 👤 Olá, {usuario_atual}!")
        st.write("Escolha uma opção abaixo:")

        menu = st.sidebar.radio(
            "Menu de Navegação",
            ["🏠 Início", "📝 Palpites", "📈 Ranking", "🎁 Prêmios"],
            label_visibility="collapsed" # Esconde o título do rádio para ficar mais limpo
        )
        
        st.divider()
        
        if st.button("🚪 Sair / Trocar Conta", use_container_width=True):
            st.session_state.logado = False
            st.session_state.usuario_atual = None
            st.rerun()

    # ==========================================
    # SEÇÃO 0: TELA INICIAL (HOME) - NOVO!
    # ==========================================
    if menu == "🏠 Início":
        st.title("Início")
        st.subheader(f"Bem-vindo(a) ao bolão, {usuario_atual}!")
        
        # Espaço reservado em branco (com um container temporário)
        st.write("")
        st.info("Bem-vindo ao Bolão da Copa do Mundo de 2026 dos mos. Faça seus palpites para cada jogos, acumule pontos e ganhe recompensas :)")
        
        # Você pode deixar linhas vazias ou um container vazio por enquanto:
        placeholder_futuro = st.container()

    # ==========================================
    # SEÇÃO 1: PALPITES
    # ==========================================
    elif menu == "📝 Palpites":
        st.header(f"Seus Palpites")
        aba_grupos, aba_eliminatorias = st.tabs(["⚽ Fase de Grupos", "🔥 Eliminatórias (Mata-Mata)"])
            
        with aba_grupos:
            st.header(f"Palpites de {usuario_atual}")
            
            # Carrega todos os palpites da planilha uma única vez
            todos_palpites = carregar_palpites()
                
            # Divisão dos jogos em rodadas
            rodadas = {
                "Rodada 1": jogos_grupos[0:24],
                "Rodada 2": jogos_grupos[24:48],
                "Rodada 3": jogos_grupos[48:72]
            }
                
            for nome_rodada, jogos_da_rodada in rodadas.items():
                with st.expander(nome_rodada, expanded=(nome_rodada == "Rodada 1")):
                    for jogo in jogos_da_rodada:
                        st.markdown(f"**{jogo['data']}**")
                            
                        # Verifica se o jogo já terminou para travar o input
                        jogo_finalizado = jogo['id'] in resultados_reais
                            
                        # Busca palpite salvos
                        palpites_usuario = [p for p in todos_palpites if str(p['Jogador']) == usuario_atual]
                        palpite_salvo = next((p for p in palpites_usuario if int(p['Jogo_ID']) == jogo['id']), None)
                            
                        gols_a_salvo = int(palpite_salvo['Gols_A']) if palpite_salvo else None
                        gols_b_salvo = int(palpite_salvo['Gols_B']) if palpite_salvo else None
                                                    
                        col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 2, 3])
                            
                        with col1:
                            col_bandeira, col_nome = st.columns([1, 4])
                            with col_bandeira:
                                st.image(get_flag_url(jogo['time_A']), width=25)
                            with col_nome:
                                st.markdown(f"<p style='font-size: 14px; margin-top: 5px;'>{jogo['time_A']}</p>", unsafe_allow_html=True)
                            with col2:
                                st.number_input("Gols A", min_value=0, max_value=20, step=1, value=gols_a_salvo, placeholder="0", disabled=jogo_finalizado, key=f"gols_a_{jogo['id']}_{usuario_atual}", label_visibility="collapsed")
                        with col3:
                            st.markdown("<h4 style='text-align: center; color: gray;'>X</h4>", unsafe_allow_html=True)
                        with col4:
                            st.number_input("Gols B", min_value=0, max_value=20, step=1, value=gols_b_salvo, placeholder="0", disabled=jogo_finalizado, key=f"gols_b_{jogo['id']}_{usuario_atual}", label_visibility="collapsed")
                        with col5:
                            col_nome, col_bandeira = st.columns([4, 1])
                            with col_nome:
                                Geist_texto = f"<p style='font-size: 14px; margin-top: 5px; text-align: right;'>{jogo['time_B']}</p>"
                                st.markdown(Geist_texto, unsafe_allow_html=True)
                            with col_bandeira:
                                st.image(get_flag_url(jogo['time_B']), width=25)
                        
                        if jogo_finalizado:

                            real_a = resultados_reais[jogo['id']]['gols_a']
                            real_b = resultados_reais[jogo['id']]['gols_b']
                            
                            if palpite_salvo is None:
                                st.info(f"🤷 **Nenhum palpite feito.**")
                            
                            else:
                                pts = calcular_pontos(gols_a_salvo, gols_b_salvo, real_a, real_b)
                                
                                if pts == 2:
                                    st.warning(f"🎯 **Cravou o placar!**")
                                elif pts == 1:
                                    st.success(f"✅ **Acertou o resultado!**")
                                else:
                                    st.error(f"❌ **Errou.**")
                        
                        st.write("")

            st.divider()
            
            if st.button("💾 Salvar Meus Palpites", use_container_width=True):
                houve_mudanca = False 
                
                with st.spinner("Salvando palpites..."):
                    for j in jogos_grupos:
                        if j['id'] not in resultados_reais:
                            v_a = st.session_state.get(f"gols_a_{j['id']}_{usuario_atual}")
                            v_b = st.session_state.get(f"gols_b_{j['id']}_{usuario_atual}")
                            
                            if v_a is not None and v_b is not None:
                                palpite_salvo = next((p for p in todos_palpites if int(p['Jogo_ID']) == j['id'] and str(p['Jogador']) == usuario_atual), None)
                                
                                is_novo_palpite = not palpite_salvo
                                is_palpite_editado = palpite_salvo and (int(palpite_salvo['Gols_A']) != v_a or int(palpite_salvo['Gols_B']) != v_b)
                                
                                if is_novo_palpite or is_palpite_editado:
                                    salvar_palpite(usuario_atual, j['id'], v_a, v_b)
                                    houve_mudanca = True
                        
                if houve_mudanca:
                    st.cache_data.clear()
                    st.success("Palpites salvos e atualizados com sucesso!")
                else:
                    st.info("Nenhuma alteração nova foi detectada.")
                    
                st.rerun()

            st.divider()
                
        with aba_eliminatorias:
            st.header("Mata-Mata")
            st.info("Os jogos desta fase ainda serão decididos.")

    # ==========================================
    # SEÇÃO 2: RANKING
    # ==========================================

    elif menu == "📈 Ranking":
        st.header("Desempenho no Bolão")
        
        # Calcula o ranking dinamicamente a partir dos palpites e resultados reais
        ranking = calcular_ranking()
        
        # Placar geral com componentes visuais limpos
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Pontuação Peterson", value=f"{ranking['Peterson']} pts")
        with col2:
            st.metric(label="Pontuação Kathy", value=f"{ranking['Kathy']} pts")
        
        st.write("")
        st.subheader("📊 Evolução do Placar no Tempo")
        
        # Gera o DataFrame com o histórico real baseado nas rodadas finalizadas
        dados_grafico_real = calcular_evolucao_ranking()
        
        # Desenha o gráfico de linha oficial
        st.line_chart(dados_grafico_real)
        
        st.caption("O gráfico rastreia os pontos acumulados do zero até o encerramento da Rodada 3.")

    # ==========================================
    # SEÇÃO 3: PRÊMIOS
    # ==========================================
    elif menu == "🎁 Prêmios":
        st.header(f"Trilha de Recompensas")
        
        ranking = calcular_ranking()
        pontos_atuais = ranking[usuario_atual]
        
        meta_maxima = 100
        progresso = min(pontos_atuais / meta_maxima, 1.0)
        st.progress(progresso, text=f"Progresso: {pontos_atuais}/{meta_maxima} pontos")
        
        premios = {
            25: "Vale uma massagem",
            50: "Vale um doce ou sobremesa da sua escolha.",
            75: "Vale um jantar especial.",
            100: "Prêmio Máximo Secreto"
        }
        
        st.write("")
        
        for meta, descricao in premios.items():
            if pontos_atuais >= meta:
                st.success(f"✅ **{meta} Pontos:** {descricao} (DESBLOQUEADO!)")
            else:
                st.info(f"🔒 **{meta} Pontos:** {descricao}")
                
        faltam = [meta for meta in premios.keys() if meta > pontos_atuais]
        if faltam:
            proxima_meta = min(faltam)
            pontos_faltantes = proxima_meta - pontos_atuais
            st.caption(f"Faltam {pontos_faltantes} pontos para desbloquear a próxima recompensa!")
        else:
            st.balloons()
            st.success("Parabéns! Todas as recompensas foram desbloqueadas!")
