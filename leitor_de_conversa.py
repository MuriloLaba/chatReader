#Formato das mensagens que eu estou lendo foram feitos para o padrao americano EX: 5/3/2024


import os
import re
import pandas as pd
import matplotlib.pyplot as plt

def limpar_console():
    os.system('cls')

def listar_arquivos_txt():
    arquivos_txt = [f for f in os.listdir() if f.endswith('.txt')]
    return arquivos_txt

def carregar_conversa(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    dados = []
    padrao = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2} (?:AM|PM)?|\d{2}:\d{2}) - ([^:]+): (.+)'
    
    for linha in linhas:
        resultado = re.match(padrao, linha)
        if resultado:
            data, hora, remetente, mensagem = resultado.groups()
            dados.append([data, hora, remetente, mensagem])
        else:
            continue

    if len(dados) == 0:
        print("Não foi possível encontrar conversas no arquivo. Verifique o formato do arquivo.")
        return pd.DataFrame(columns=['Data', 'Hora', 'Remetente', 'Mensagem'])

    df = pd.DataFrame(dados, columns=['Data', 'Hora', 'Remetente', 'Mensagem'])
    return df

def resumo_conversas(df):
    limpar_console()
    if df.empty:
        print("Nenhuma conversa foi encontrada.")
        return

    resumo = df['Remetente'].value_counts().reset_index()
    resumo.columns = ['Remetente', 'Total de Mensagens']
    print(resumo)
    return resumo

def historico_remetente(df, remetente):
    limpar_console()
    if df.empty:
        print("Nenhuma conversa foi encontrada.")
        return

    historico = df[df['Remetente'] == remetente]
    if historico.empty:
        print(f"Nenhuma mensagem encontrada para o remetente: {remetente}")
    else:
        print(historico[['Data', 'Hora', 'Mensagem']])
    return historico

def grafico_pizza(df):
    limpar_console()
    if df.empty:
        print("Nenhuma conversa foi encontrada.")
        return

    resumo = df['Remetente'].value_counts()
    if resumo.empty:
        print("Nenhuma conversa encontrada para gerar o gráfico de pizza.")
        return

    plt.figure(figsize=(4, 4))
    plt.pie(resumo, labels=resumo.index, autopct='%1.1f%%', startangle=90)
    plt.title('Percentual de Mensagens por Remetente')
    plt.axis('equal') 
    plt.show()

def grafico_histograma(df, remetente):
    limpar_console()
    if df.empty:
        print("Nenhuma conversa foi encontrada.")
        return

    historico = df[df['Remetente'] == remetente]
    if historico.empty:
        print(f"Nenhuma mensagem encontrada para o remetente: {remetente}")
        return

    historico['Data'] = pd.to_datetime(historico['Data'], dayfirst=True, errors='coerce')

    historico = historico.dropna(subset=['Data'])
    
    if historico.empty:
        print("Falha ao converter as datas. Todas as datas estão inválidas ou em um formato incorreto.")
        return

    # Agrupar as mensagens por mês
    mensagens_por_mes = historico.groupby(historico['Data'].dt.to_period('M')).size()

    if mensagens_por_mes.empty:
        print(f"Nenhuma mensagem disponível por mês para o remetente {remetente}.")
        return

    # Gerar o gráfico de barras
    mensagens_por_mes.plot(kind='bar', figsize=(10, 5))
    plt.title(f'Histograma de Mensagens por Mês - {remetente}')
    plt.xlabel('Mês')
    plt.ylabel('Quantidade de Mensagens')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def grafico_linhas(df):
    limpar_console()
    if df.empty:
        print("Nenhuma conversa foi encontrada.")
        return

    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')

    df = df.dropna(subset=['Data'])

    if df.empty:
        print("Falha ao converter as datas. Verifique o formato das datas no arquivo.")
        return

    mensagens_por_dia_remetente = df.groupby(['Data', 'Remetente']).size().unstack(fill_value=0)

    if mensagens_por_dia_remetente.empty:
        print("Não há mensagens suficientes para gerar o gráfico de linhas.")
        return

    mensagens_por_dia_remetente.plot(kind='line', figsize=(10, 5))
    plt.title('Quantidade de Mensagens ao Longo do Tempo por Remetente')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de Mensagens')
    plt.legend(title='Remetente', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def menu():
    limpar_console()
    print("Análise de Conversas do WhatsApp")

    arquivos_txt = listar_arquivos_txt()
    
    if not arquivos_txt:
        print("Não há arquivos .txt no diretório atual.")
        return
    
    print("Arquivos disponíveis no diretório atual:")
    for i, arquivo in enumerate(arquivos_txt):
        print(f"{i + 1} - {arquivo}")
    
    escolha = int(input("\nEscolha o número do arquivo que deseja carregar: ")) - 1
    
    if escolha < 0 or escolha >= len(arquivos_txt):
        print("Escolha inválida!")
        return
    
    arquivo_escolhido = arquivos_txt[escolha]
    
    df = carregar_conversa(arquivo_escolhido)
    if df.empty:
        return 

    limpar_console()
    print(f"\nConversa carregada do arquivo: {arquivo_escolhido}\n")
    print(df)
    
    while True:
        print("\nEscolha uma opção para análise:")
        print("1 - Resumo das conversas")
        print("2 - Histórico de mensagens de um remetente")
        print("3 - Gráfico de pizza (percentual de mensagens por remetente)")
        print("4 - Histograma de mensagens por dia de um remetente")
        print("5 - Gráfico de linhas (mensagens ao longo do tempo por remetente)")
        print("0 - Sair")
        
        opcao = input("Opção: ")
        
        if opcao == '1':
            resumo_conversas(df)
        
        elif opcao == '2':
            remetente = input("Informe o nome do remetente: ")
            historico_remetente(df, remetente)
        
        elif opcao == '3':
            grafico_pizza(df)
        
        elif opcao == '4':
            remetente = input("Informe o nome do remetente: ")
            grafico_histograma(df, remetente)
        
        elif opcao == '5':
            grafico_linhas(df)
        
        elif opcao == '0':
            limpar_console()
            print("Saindo...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()