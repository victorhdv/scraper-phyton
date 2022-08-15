from bs4 import BeautifulSoup
import requests

# pagina trabalhada
url = 'https://rn.olx.com.br/rio-grande-do-norte/natal/imoveis/venda/apartamentos'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

cabecalho = ('Titulo do anuncio' + ';' + 'Endereco' + ';' +
             'Quantidade de quartos' + ';' + 'Area ' + ';' + 'Condominio' + ';' + 'Vagas' + ';' + 'Preco do apartamento ' + '\n')
# escrevendo o cabecalho
f = open('lista_apartamento.csv', 'a', newline='', encoding='UTF-8')
f.write(cabecalho)
# Requisição GET
data = requests.get(url, headers=headers)
# Testando objeto Response
if data.status_code == 200:
    print('Requisição bem sucedida!')
# Criação de objeto para salvar documento html
soup = BeautifulSoup(data.content, 'html.parser')

ultimaPagina = 20
for i in range(1, ultimaPagina+1):
    urlBusca = f'https://rn.olx.com.br/rio-grande-do-norte/natal/imoveis/venda/apartamentos?o={i}'
    # Requisição GET
    data = requests.get(urlBusca, headers=headers)
    # Criação de objeto para salvar documento html
    soup = BeautifulSoup(data.content, 'html.parser')
    # Utilizando o método find_all para acessar o objeto
    aparts = soup.find_all('a', class_='sc-12rk7z2-1 huFwya sc-giadOv dXANPZ')

    with open('lista_apartamento.csv', 'a', newline='', encoding='UTF-8')as f:

        for apart in aparts:

            endereco = apart.find(
                'span', class_='sc-1c3ysll-1 iDvjkv sc-fzsDOv dTHJIA').get_text().strip()

            try:
                preco = apart.find(
                    'span', class_='m7nrfa-0 eJCbzj sc-fzsDOv kHeyHD').get_text().strip()
            except:
                preco = '0'

            detalhes = apart.find(
                'div', class_='sc-1ftm7qz-2 ilPFvN').get_text()
            lista = detalhes.replace('\xa0', ' ').split(' | ')
            # print(lista)
            if lista[0].find('quartos') == -1:
                checkQuarto = lista[0].replace('quarto', '')
            elif lista[0].find('quartos') != -1:
                checkQuarto = lista[0].replace('quartos', '')
            if checkQuarto != "":
                quarto = checkQuarto
            else:
                quarto = "0"
            # print(quarto)
            checkArea = lista[1].replace('m²', '')
            if checkArea != "":
                area = checkArea
            else:
                area = "0"
            # print(area)
            checkCondominio = lista[2].replace('Condomínio: R$ ', '')
            if checkCondominio == "" or checkCondominio.find('vaga') != -1:
                condominio = "0"
            else:
                condominio = checkCondominio
            # print(condominio)
            if lista[3].find('vagas') == -1:
                checkVagas = lista[3].replace('vaga', '')
            elif lista[3].find('vagas') != -1:
                checkVagas = lista[3].replace('vagas', '')
            if checkVagas != "":
                vagas = checkVagas
            else:
                vagas = "0"

            try:
                titulo = apart.find(
                    'h2', class_='kgl1mq-0 eFXRHn sc-fzsDOv jiCiNE').get_text().strip()
            except:
                titulo = apart.find(
                    'h2', class_='kgl1mq-0 eFXRHn sc-fzsDOv dKgwlm').get_text().strip()

            teste = titulo + ';' + endereco + ';' + quarto + ';' + area + ';' + \
                condominio + ';' + vagas + ';' + preco + '\n'
            print(teste)
            f.write(teste)
    print(urlBusca)
