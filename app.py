from datetime import datetime


usuarios = [{'user': 'jvnsilva', 'password': '456123'}, {
    'user': 'jbres', 'password': '321654'}, {'user': 'bnmagalhaes', 'password': '123456'}, {'user': 'msnunes', 'password': '1234567'}, {'user': 'seis5', 'password': '555555'}]
acessos_negados = []
logins_confirmados = []
modificacoes = []
fez_modificacao = False


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
                (user, f'Tipo de Operação: {tipo_modificacao}', f'{horario.day}/{horario.month}/{horario.year}', f'{horario.hour}:{horario.minute}:{horario.second}'))
            print(modificacoes)
    return wrapper


@controle_horario
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
def saque(saldo, valor):
    global fez_modificacao, tipo_modificacao
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
def deposito(saldo, valor):
    global fez_modificacao, tipo_modificacao
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


def criar_linha(num=1, caracter='='):
    separador = caracter
    print(f'{separador*num}')


def centralizar_linha(string, total_caracteres):
    total_string = int(len(string))
    espacos = total_caracteres - total_string
    separador = ' '
    print(f'{separador*(espacos//2)}{string}{separador*(espacos//2)}')


finalizar_programa = False
credencial_confirmada = False
usuario_confirmado = False

while finalizar_programa != True:
    if usuario_confirmado == False:
        criar_linha(100, '=')
        centralizar_linha(
            'Sistema Financeiro A.C.M ', 100)
        criar_linha(100, '=')
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
        criar_linha(100, '=')
        centralizar_linha(
            'Sistema Financeiro A.C.M ', 100)
        criar_linha(100, '=')
        print('\nQual operação você deseja realizar: \n')
        print('1 - Saque ')
        print('2 - Depósito ')
        print('3 - Verificar Log de Mudanças ')
        escolha_2 = input('\nDigite a operação: ')
    else:
        criar_linha(100, '=')
        print('\nAcesso Negado.')
        print('Finalizando Programa.')
        finalizar_programa = True
