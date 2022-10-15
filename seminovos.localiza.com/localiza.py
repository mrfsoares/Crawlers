# -*- coding: utf-8 -*-
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


def trata_duplicatas(df):
    '''
    Algumas informações estão vindo dupicadas por sequência de coleta devido
    ao formado de sua disposição. Essa função é responsável por corrigir esse 
    problema.
    '''
    for num in df.index:
        if num % 2 != 0:
            df.drop([num], inplace=True)
    df.reset_index(inplace=True, drop=True)

    return df


def BuscarDados(pages=2):
    # Criando dataframes que receberão os valores
    links = []
    nomes = []
    preco = []
    km = []
    cambio = []
    combustivel = []
    ano = []
    cor = []
    marca = []

    for pag in range(1, pages):
        print("PÁGINA ATUAL:", str(pag))

        url = "https://seminovos.localiza.com/seminovo?map=tipo&order=OrderByPriceASC&page=" + \
            str(pag)
        print(url)

        PARAMS = {
            "authority": 'seminovos.localiza.com',
            "method": 'GET',
            "path": '/seminovo/s?map=tipo&order=OrderByPriceASC&page=1&__pickRuntime=appsEtag%2Cblocks%2CblocksTree%2Ccomponents%2CcontentMap%2Cextensions%2Cmessages%2Cpage%2Cpages%2Cquery%2CqueryData%2Croute%2CruntimeMeta%2Csettings&__device=tablet',
            "scheme": 'https',
            "accept": 'application/json',
            "accept-encoding": 'gzip, deflate, br',
            "accept-language": 'pt-BR,pt-PT;q=0.9,pt;q=0.8,en-US;q=0.7,en;q=0.6',
            "cache-control": 'no-cache',
            "cookie": 'VtexWorkspace=master%3A-; cookieOpt=.rand; _gaexp=.rand; _gcl_au=1.1.1219588870.1665704816; vtex_segment=eyJjYW1wYWlnbnMiOm51bGwsImNoYW5uZWwiOiIxIiwicHJpY2VUYWJsZXMiOm51bGwsInJlZ2lvbklkIjpudWxsLCJ1dG1fY2FtcGFpZ24iOm51bGwsInV0bV9zb3VyY2UiOm51bGwsInV0bWlfY2FtcGFpZ24iOm51bGwsImN1cnJlbmN5Q29kZSI6IkJSTCIsImN1cnJlbmN5U3ltYm9sIjoiUiQiLCJjb3VudHJ5Q29kZSI6IkJSQSIsImN1bHR1cmVJbmZvIjoicHQtQlIiLCJjaGFubmVsUHJpdmFjeSI6InB1YmxpYyJ9; _gid=GA1.2.273039745.1665704820; blueID=e0f7cd71-0a4f-4b72-88cf-4b6f730be8a0; biggy-anonymous=gzSKoiyT6NyKG1FC8l825; VtexRCMacIdv7=107b8a3f-9360-491c-9960-9ef15b879f43; analytic_id=1665704823717293; checkout.vtex.com=__ofid=430523decf5b4188b84cf3d8e221e2b4; .ASPXAUTH=CDCBAE1DBBE8813056F3CD7F80BD0CFA5AD5EE816F5183AEF1086EB4EDE65752AC16C43FA72F9F66C750EF24D5217EBCEA47FA120EA3E265FF0576DE67BCC98EDF2718A9AC209F6F2A516BF28564C663FF4C03F5D2BF17C69E0978C514767FE51AE50FBCAAB027029AB6571CABE43E72036D8082D5DABC2D877A47F0A5D3B31265B248BE4953782F72F61008F31EC9A062BA99C657FE5E5828A6C92ABA48D79DF0BA2C96; _fbp=fb.1.1665704827383.1359057934; _tt_enable_cookie=1; _ttp=008264cd-385a-4666-8ea0-a3350a154225; _hjSessionUser_2184053=eyJpZCI6IjZiMDQ3OTFmLWI4NGYtNWNkYy1hZDdiLWZlYWJhYzg2ZTI5NSIsImNyZWF0ZWQiOjE2NjU3MDQ4MTk3NjcsImV4aXN0aW5nIjp0cnVlfQ==; vtex_session=eyJhbGciOiJFUzI1NiIsImtpZCI6IjM5NEYyNzAyNzBERDRDMzI5MTA3QTEwMjI0MDI1NjJENTMyMkQwODUiLCJ0eXAiOiJqd3QifQ.eyJhY2NvdW50LmlkIjoiZGRjZjUyMjAtYzcxMi00ZTYzLTg1ZTAtNTRmNzRjMmZhMDQ5IiwiaWQiOiJlY2NlYjBlZC04NWNlLTQyZmYtOTAyMy1mMmEzZmQ3MTA0NzUiLCJ2ZXJzaW9uIjozLCJzdWIiOiJzZXNzaW9uIiwiYWNjb3VudCI6InNlc3Npb24iLCJleHAiOjE2NjYzOTY0NzQsImlhdCI6MTY2NTcwNTI3NCwiaXNzIjoidG9rZW4tZW1pdHRlciIsImp0aSI6IjA5YTI4MGYyLThlYTAtNDk1Ni04MGMzLTVmMDQ1Mjg5NDExZCJ9.cfZDyfUuhLRSczz1X1tRf1ufe14fk24wNDBze7U7Hv2mP0A30NcqFq8-Tj70ttdT2zw61gh9wALxksq31u8_RQ; vtex_binding_address=localizaseminovos.myvtex.com/; biggy-session-localizaseminovos=gPTozGCgYuSgYSO68yvTo; VtexRCSessionIdv7=deb37756-cf72-4001-bf63-56568bb04b2e; _hjIncludedInSessionSample=0; _hjSession_2184053=eyJpZCI6IjZjOWU1YTk0LTc5YWQtNDI5MS04OTU1LWU5MGQyNDQ5Y2JlZCIsImNyZWF0ZWQiOjE2NjU3NTQxNjQ2NjQsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; _gaexp=GAX1.2.m44DmhfkS0O-dcqQ2nvcQw.19362.1; _uetsid=54eca4f04b5111edbb45af7d5817c6b9; _uetvid=54eccd404b5111ed9c1a45e2a5c0a8ac; _ga=GA1.1.1335803798.1665704820; cto_bundle=FsZmTV9hREp6MElYZWFBJTJCeGhndFJFNUVhUW1QWE54RXZyTzZENWNab2dqU2RFTkNpcHJKVEFHQzM0Smc0dVBLV1pPb3VPbGk3UzdTaklBaGlPMFlPdmR2aE5oSld5MFY0b09tUCUyRiUyRnJpcG9tV3Y3ZG1qVm1OQlowdWVGb01pZ2Y2VmVuTkFHUEgzdWdFUFY4a2lheUFNSmxodFElM0QlM0Q; _ga_36RRJKE9VS=GS1.1.1665754165.2.1.1665755103.52.0.0; biggy-event-queue=; _dd_s=rum=0&expire=1665756706685',
            "pragma": 'no-cache',
            "referer": 'https://seminovos.localiza.com/seminovo?map=tipo&order=OrderByPriceASC&page='+str(pag),
            "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            "sec-ch-ua-mobile": '?0',
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": 'empty',
            "sec-fetch-mode": 'cors',
            "sec-fetch-site": 'same-origin',
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }

        # faz conexão com a página
        page = requests.get(url=url, headers=PARAMS)

        # pega conteúdo da página
        soup = BeautifulSoup(page.text, 'html.parser')

        # PEGANDO INFORMAÇÕES:
        # Links
        for link in re.findall(r'"linkText":"(.*?)"', str(soup)):
            link = "https://seminovos.localiza.com/" + link + "\p"
            links.append(link)

        # Nome veículos
        for valor in re.findall(r'"originalName":"Modelo","values":{"type":"json","json":\["(.*?)"]', str(soup)):
            nomes.append(valor)

        # Preço veículos
        for valor in re.findall(r'"Price":(.*?),', str(soup)):
            preco.append(valor)

        # Quilometragem dos veículos
        for valor in re.findall(r'"originalName":"Quilometragem","values":{"type":"json","json":\["(.*?)"]', str(soup)):
            km.append(valor)

        # Cambio dos veículos
        for valor in re.findall(r'"originalName":"Cambio","values":{"type":"json","json":\["(.*?)"]', str(soup)):
            cambio.append(valor)

        # Combustivel dos veículos
        for valor in re.findall(r'"originalName":"Combust(.*?)]', str(soup)):
            valor = str(re.findall(r'\["(.*?)"', valor)
                        ).replace("\\u002F", "").replace("['", "").replace("']", "")
            combustivel.append(valor)

        # Ano dos veículos
        for valor in re.findall(r'"originalName":"Ano fabrica(.*?)"]', str(soup)):
            valor = str(re.findall(r'\d+', valor)
                        ).replace("['", "").replace("']", "")
            ano.append(valor)

        # Cor dos veículos
        for valor in re.findall(r'"originalName":"Cor Completa","values":{"type":"json","json":\["(.*?)"]', str(soup)):
            cor.append(valor)

        # Marca dos veículos
        for valor in re.findall(r'"originalName":"Marca","values":{"type":"json","json":\["(.*?)"]', str(soup)):
            marca.append(valor)

    # Criando dataframe final com todas as informações e salvando na memória local
    links = pd.DataFrame(links).rename(columns={0: 'Link'})
    nomes = pd.DataFrame(nomes).rename(columns={0: 'Nome'})
    preco = pd.DataFrame(preco).rename(columns={0: 'Preco'})
    km = pd.DataFrame(km).rename(columns={0: 'Quilometragem'})
    cambio = pd.DataFrame(cambio).rename(columns={0: 'Cambio'})
    combustivel = pd.DataFrame(combustivel).rename(columns={0: 'Combustivel'})
    ano = pd.DataFrame(ano).rename(columns={0: 'Ano'})
    cor = pd.DataFrame(cor).rename(columns={0: 'Cor'})
    marca = pd.DataFrame(marca).rename(columns={0: 'Marca'})

    nomes = trata_duplicatas(nomes)
    km = trata_duplicatas(km)
    cambio = trata_duplicatas(cambio)
    combustivel = trata_duplicatas(combustivel)
    ano = trata_duplicatas(ano)
    cor = trata_duplicatas(cor)
    marca = trata_duplicatas(marca)

    df = pd.concat([nomes, preco, km, cambio, combustivel, ano, cor, marca, links],
                   axis=1)

    df.to_csv('veiculos_localiza.csv', index=False,
              sep=';', encoding='latin-1')


BuscarDados(51)  # 50
