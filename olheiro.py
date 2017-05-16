import json
from urllib.request import urlopen


def VerificaAproveitamento(aproveitamento):
    aproveitamento.reverse()
    dados = []

    if aproveitamento.count("v") == 0:
        return (str(len(aproveitamento)) + ' jogos sem vencer')

    ultima_vitoria = aproveitamento.index("v")

    if ultima_vitoria == 0:
        return ('Vem de vitória')
    else:
        return ('Não vence a '+ str(ultima_vitoria) + ' jogos')


def VerificaRodadaAnterior(time,rodada_anterior):
    for confronto in rodada_anterior['partidas']:
        if confronto['clube_casa_id'] == time:
            placar_time = confronto['placar_oficial_mandante']
            placar_adversario = confronto['placar_oficial_visitante']
            adversario = rodada_anterior['clubes'][str(confronto['clube_visitante_id'])]['nome']
            local = ' em casa'

        elif confronto['clube_visitante_id'] == time:
            placar_time = confronto['placar_oficial_visitante']
            placar_adversario = confronto['placar_oficial_mandante']
            adversario = rodada_anterior['clubes'][str(confronto['clube_casa_id'])]['nome']
            local = ' fora de casa'

    diferenca_gols = placar_time - placar_adversario

    if diferenca_gols >= 3:
        resultado = 'Goleou o '
    elif diferenca_gols > 0:
        resultado = 'Ganhou do '
    elif diferenca_gols == 0:
        resultado = 'Empatou com o '
    elif diferenca_gols > -3:
        resultado = 'Perdeu para o '
    else:
        resultado = 'Foi goleado pelo '

    return (resultado + adversario + local)


def MaisEscalados(codigo_html):
    url_destaques = "https://api.cartolafc.globo.com/mercado/destaques"
    response = urlopen(url_destaques).read().decode('utf8')
    destaques = json.loads(response)

    codigo_html = codigo_html + '''
        <div class="colunaJogadores">
            <h3>Jogadores mais escalados</h3>
    '''
    for jogador in destaques:
        jogador_analisado = """
            <p>{escalacoes}: {nome_jogador}, {clube_jogador} - {posicao_jogador} </p>
        """.format(
            escalacoes = str(jogador['escalacoes']),
            nome_jogador = jogador['Atleta']['apelido'],
            clube_jogador = jogador['clube'],
            posicao_jogador = jogador['posicao']
        )
        codigo_html = codigo_html + jogador_analisado

    return codigo_html + "</div>"

def AnaliseRodada(codigo_html):
    url_rodada_atual = "https://api.cartolafc.globo.com/partidas"
    response = urlopen(url_rodada_atual).read().decode('utf8')
    rodada_atual = json.loads(response)

    url_rodada_anterior = "https://api.cartolafc.globo.com/partidas/"+str(rodada_atual['rodada']-1)
    response = urlopen(url_rodada_anterior).read().decode('utf8')
    rodada_anterior = json.loads(response)

    codigo_html = codigo_html + '''
            <div class="colunaJogos">
            <h2> Rodada {rodada} </h2>
    '''.format(rodada = str(rodada_atual['rodada']))

    for confronto in rodada_atual['partidas']:
        partida_analisada = """
        </h3><b> {mandante} ({posicao_mandante}o) x {visitante} ({posicao_visitante}o) </b></h3>
        <p> Aproveitamento {mandante}: {aproveitamento_mandante} [ {ult_mandante} ] </p>
        <p> Aproveitamento {visitante}: {aproveitamento_visitante} [ {ult_visitante} ] </p>
        """.format(mandante = rodada_atual['clubes'][str(confronto['clube_casa_id'])]['nome'],
                   visitante = rodada_atual['clubes'][str(confronto['clube_visitante_id'])]['nome'],
                   posicao_mandante = confronto['clube_casa_posicao'], posicao_visitante = confronto['clube_visitante_posicao'],
                   aproveitamento_mandante = VerificaAproveitamento(confronto['aproveitamento_mandante']),
                   aproveitamento_visitante = VerificaAproveitamento(confronto['aproveitamento_visitante']),
                   ult_mandante = VerificaRodadaAnterior(confronto['clube_casa_id'],rodada_anterior),
                   ult_visitante = VerificaRodadaAnterior(confronto['clube_visitante_id'],rodada_anterior)
                   )

        codigo_html = codigo_html  + partida_analisada
    return codigo_html + "</div>"


def GerarHTML():
    # string com o código HTML
    codigo_html = '''
    <html>
    	<head>
    		<meta charset="utf-8">
            <title>Sem Tempo FC</title>
            <link rel="stylesheet" type="text/css" href="style.css">
            <meta name="viewport" content="width=device-width, initial-scale=1">
      </head>

      <body>
        <h1>Cartola 2017</h1>
        <header>
                <p>Esta pág foi gerada por um script em Python que analisa os times do BR17</p>
                <p>Se você, assim como eu, não tem tempo para acompanhar todos os times do campeonato, sinta-se em casa para consultar algumas coisas!
                Análises mais legais serão feitas com o passar das rodadas (estou sem tempo :D ), por isso, caso não encontre nenhum dado relevante, volte outro dia.</p>
                <p>Fique a vontade para enviar alguma sugestão para: semtempofc [dot] gmail [dot] com</p>
                <p>Não espalha não :p Espero que te ajude! []'s</p>
        </header>
        <div class="conteudo">
    '''
    codigo_html = AnaliseRodada(codigo_html)
    codigo_html = MaisEscalados(codigo_html)
    '''
      	</div>
        <footer>
      		<p>Jones</p>
      	</footer>
      </body>
    </html>
    '''
    return codigo_html

arq_html = open('index.html', 'w')
arq_html.write(GerarHTML())
arq_html.close()
