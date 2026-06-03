
from classes.agency import Agency
from classes.project import Project
from classes.officer import Officer
from classes.transaction import Transaction

def executar_testes():
   
    Agency.reset(); Project.reset(); Officer.reset(); Transaction.reset()

    print("Teste do sistema\n")

    ag = Agency(1, "Sede Central")
    pr = Project(1, "Expansão 2026", "Infraestrutura", "2026-01-01")

   
    print("A verificar o bloqueio de dados inválidos:")
    

    
   
    Transaction(99, 1, 888, "2026-04-25", 100.0) 


    print("\nControlo de Qualidade (Memória):")

    print(f"Oficiais registados: {len(Officer.lst)}") 
    print(f"Transações registadas: {len(Transaction.lst)}")

    print("\nA testar inserção de dados válidos:")
    Transaction(1, 1, 1, "2026-04-25", 5000.0)
    print(f"Transações após dado válido: {len(Transaction.lst)}")

if __name__ == '__main__':
    executar_testes()
    
    print("\n Teste de Alteração de Dados (Setters)")

    t1 = Transaction.obj[1] 
    t1.amount = 9999.99
    print(f"Novo valor da transação: {t1.amount}€ (Esperado: 9999.99)")

   
    print("Teste para tentar mudar para agência que não existe:")
    t1.agency_id = 5000 

