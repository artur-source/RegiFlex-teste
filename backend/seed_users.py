from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    # Verificar se já existem usuários
    existing_users = Usuario.query.count()
    
    if existing_users == 0:
        # Criar usuário admin
        admin = Usuario(
            username='admin',
            email='admin@regiflex.com',
            role='admin'
        )
        admin.set_password('password')
        
        # Criar psicólogo
        psicologo = Usuario(
            username='psicologo1',
            email='psicologo1@regiflex.com',
            role='psicologo'
        )
        psicologo.set_password('password')
        
        # Criar recepcionista
        recepcionista = Usuario(
            username='recepcionista1',
            email='recepcionista1@regiflex.com',
            role='recepcionista'
        )
        recepcionista.set_password('password')
        
        # Adicionar ao banco
        db.session.add(admin)
        db.session.add(psicologo)
        db.session.add(recepcionista)
        db.session.commit()
        
        print("✅ Usuários criados com sucesso!")
        print("   - admin / password")
        print("   - psicologo1 / password")
        print("   - recepcionista1 / password")
    else:
        print(f"ℹ️  Já existem {existing_users} usuários no banco de dados")
