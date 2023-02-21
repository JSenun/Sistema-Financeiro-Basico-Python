from datetime import datetime


usuarios = [{'user': 'jvnsilva', 'password': '456123'}, {
    'user': 'jbres', 'password': '321654'}, {'user': 'bnmagalhaes', 'password': '123456'}, {'user': 'msnunes', 'password': '1234567'}, {'user': 'seis5', 'password': '555555'}]
acessos_negados = []
logins_confirmados = []
modificacoes = [['jvnsilva', 'Launch System', '20/02/2023', '20:45:11']]
fez_modificacao = False
saldo = 25500

# Decorator para capturar horário e dependendo da ação do usuário capturar o nome do user


def controle_horario(funcao):
    def wrapper(*args):
        horario = datetime.now()
        funcao(*args)
        if usuario_confirmado == True:
            logins_confirmados.append(
                (user, f'{horario.day}/{horario.month}/{horario.year}', f'{horario.hour}:{horario.minute}:{horario.second}'))
        elif acesso_negado == True:
            acessos_negados.append(horario)

        if fez_modificacao == True:
            modificacoes.append(
                [user, f'Tipo de Operação: {tipo_modificacao}', f'{horario.day}/{horario.month}/{horario.year}', f'{horario.hour}:{horario.minute}:{horario.second}'])
    return wrapper


@controle_horario
# Captura a entrado do user (username e senha) e verifica com os usuarios e senhas cadastrados
def faz_login(bd_usuarios=usuarios):
    global usuario_confirmado, acesso_negado, user
    user = input('\nDigite seu usuário: ')
    senha = input('\nDigite sua senha: ')
    tentativas = len(bd_usuarios)
    for usuario in bd_usuarios:
        nome_usuario = usuario.get('user')
        senha_usuario = usuario.get('password')
        if (user == nome_usuario and senha == senha_usuario):
            print('\nUsuário Confirmado\n')
            usuario_confirmado = True
            break
        elif (user != nome_usuario or senha != senha_usuario):
            tentativas -= 1
            if (tentativas == 0):
                print('\nAcesso negado\n')
                acesso_negado = True
                break


@controle_horario
def saque(valor):
    global fez_modificacao, tipo_modificacao, saldo
    if usuario_confirmado == True:
        if type(valor) == float or type(valor) == int:
            if valor <= saldo:
                fez_modificacao = True
                tipo_modificacao = 'Saque'
                saldo -= float(valor)
                print(f'Saque realizado no valor de R${valor:.2f}')
            else:
                print('Saldo insuficiente.')
        else:
            print('Valor inválido')
    else:
        print('Somente usuário autorizado')


@controle_horario
def deposito(valor):
    global fez_modificacao, tipo_modificacao, saldo
    if usuario_confirmado == True:
        if type(valor) == float or type(valor) == int:
            if valor > 0:
                fez_modificacao = True
                tipo_modificacao = 'Depósito'
                saldo += float(valor)
                print(f'Depósito realizado no valor de R${valor:.2f}')
            else:
                print('Valor insuficiente para depósito.')
        else:
            print('Valor inválido')
    else:
        print('Somente usuário autorizado')


def criar_linha(num=1, caracter='='):  # Função estética para criar linhas no CMD
    separador = caracter
    print(f'{separador*num}')


# Função estética para centralizar strings no CMD
def centralizar_linha(string, total_caracteres):
    total_string = int(len(string))
    espacos = total_caracteres - total_string
    separador = ' '
    print(f'{separador*(espacos//2)}{string}{separador*(espacos//2)}')


# Função estética para criar um header para a aplicação no CMD
def cria_header(string, separador):
    criar_linha(100, separador)
    centralizar_linha(
        string, 100)
    criar_linha(100, separador)


finalizar_programa = False
credencial_confirmada = False
usuario_confirmado = False

while finalizar_programa != True:
    if usuario_confirmado == False:
        cria_header('Sistema Financeiro A.C.M ', '=')
        centralizar_linha(
            'Para acessar o nosso sistema é necessário fazer o login.', 100)
        escolha_1 = input('\nRealizar o login? S / N\n')
        tentativas = 3
        if escolha_1 == 'S' or escolha_1 == "s":
            while tentativas > 0:
                faz_login()
                if usuario_confirmado == True:
                    credencial_confirmada = True
                    break
                else:
                    tentativas -= 1
                    criar_linha(100, '=')
                    print(
                        f'Usuário não reconhecido. Tentar novamente. {tentativas} Tentativas restantes')
        elif escolha_1 == 'N' or escolha_1 == "n":
            criar_linha(100, '=')
            print('Finalizando Programa.')
            finalizar_programa = True

    if credencial_confirmada == True:
        cria_header('Sistema Financeiro A.C.M ', '=')
        print('\nQual operação você deseja realizar: \n')
        print('1 - Verificar Saldo ')
        print('2 - Saque ')
        print('3 - Depósito ')
        print('4 - Verificar Log de Mudanças ')
        print('5 - Log Out / Trocar de User')
        print('6 - Finalizar programa')
        escolha_2 = input('\nDigite a operação: ')

        if escolha_2 == '1':
            cria_header(f'Saldo atual: R${saldo:.2f}', '=')
        elif escolha_2 == '2':
            cria_header('Sistema Financeiro A.C.M ', '=')
            print(f'Saldo para saques: R${saldo:.2f}')
            valor_saque = float(
                input('Insira o valor do saque a ser realizado: \n'))
            saque(valor_saque)
            print(f'Saldo atualizado: R${saldo:.2f}')
        elif escolha_2 == '3':
            cria_header('Sistema Financeiro A.C.M ', '=')
            print(f'Saldo atual: R${saldo:.2f}')
            valor_deposito = float(
                input('Insira o valor do depósito a ser realizado: \n'))
            deposito(valor_deposito)
            print(f'Saldo atualizado: R${saldo:.2f}')
        elif escolha_2 == '4':
            cria_header('Sistema Financeiro A.C.M ', '=')
            contador = 1
            for log in modificacoes:
                print(
                    f'{contador} - User: {log[0]} | {log[1]} | Data de modificação: {log[2]} | Horário de Modificação: {log[3]}')
                contador += 1
        elif escolha_2 == '5':
            print('\n\nRealizando Log Out e Reiniciando sistema...\n\n')
            usuario_confirmado = False
        elif escolha_2 == '6':
            print('\n\nFinalizando Programa.\n\n')
            finalizar_programa = True
        else:
            pass
    else:
        criar_linha(100, '=')
        print('\nAcesso Negado.')
        print('Finalizando Programa.')
        finalizar_programa = True
