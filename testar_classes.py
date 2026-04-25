# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:56:33 2026

@author: Laura
"""

# Importar as nossas classes que estão dentro da pasta 'classes'
from classes.agency import Agency
from classes.project import Project
from classes.officer import Officer
from classes.transaction import Transaction

def executar_testes():
    print("--- A INICIAR O TESTE DAS CLASSES ---\n")

    # TESTE 1: Criar uma Agência
    print("1. A testar a classe Agency...")
    ag1 = Agency(9901, "Agência de Teste Norte")
    print(f"   -> SUCESSO: Agência '{ag1.name}' criada com o ID {ag1.id}.")

    # TESTE 2: Criar um Projeto
    print("\n2. A testar a classe Project...")
    proj1 = Project(9902, "Projeto X", "Investigação", "2026-04-01")
    print(f"   -> SUCESSO: Projeto '{proj1.name}' criado com o ID {proj1.id}.")

    # TESTE 3: Criar um Oficial (Vamos testar o 'segurança')
    print("\n3. A testar a classe Officer...")
    # O Oficial precisa do ID de uma agência que já exista (vamos usar o 9901)
    off1 = Officer(9903, "Diretor", 9901)
    print(f"   -> SUCESSO: Oficial criado! Cargo: {off1.role}, Agência: {off1.agency_id}.")

    # TESTE 4: Criar uma Transação
    print("\n4. A testar a classe Transaction...")
    # A transação precisa da Agência 9901 e do Projeto 9902
    trans1 = Transaction(9904, 9901, 9902, "2026-04-01", 50000.50)
    print(f"   -> SUCESSO: Transação criada! Valor: {trans1.amount}€, Data: {trans1.payment_date}.")
    
    # TESTE 5: Testar as listas de memória (Gclass)
    print("\n--- RESUMO DA MEMÓRIA ---")
    print(f"Total de Agências em memória: {len(Agency.lst)}")
    print(f"Total de Projetos em memória: {len(Project.lst)}")
    print(f"Total de Oficiais em memória: {len(Officer.lst)}")
    print(f"Total de Transações em memória: {len(Transaction.lst)}")
    
    print("\n--- TESTES CONCLUÍDOS COM SUCESSO! ---")

# Esta linha garante que o teste só corre se executarmos este ficheiro diretamente
if __name__ == '__main__':
    executar_testes()