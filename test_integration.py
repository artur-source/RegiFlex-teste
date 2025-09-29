#!/usr/bin/env python3
"""
Script de teste para verificar a integração entre frontend e backend do RegiFlex.
"""

import requests
import json
import time
import sys

# Configurações
BACKEND_URL = "http://localhost:5000/api"
FRONTEND_URL = "http://localhost:5173"

def test_backend_health():
    """Testa se o backend está respondendo."""
    try:
        # Teste de login
        response = requests.post(f"{BACKEND_URL}/login", 
                               json={"username": "admin", "password": "password"},
                               timeout=5)
        
        if response.status_code == 200:
            print("✅ Backend está funcionando - Login bem-sucedido")
            data = response.json()
            return data.get('token')
        else:
            print(f"❌ Erro no login: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão com o backend: {e}")
        return None

def test_api_endpoints(token):
    """Testa os principais endpoints da API."""
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        ("/me", "GET", "Informações do usuário atual"),
        ("/pacientes", "GET", "Lista de pacientes"),
        ("/relatorios/dashboard", "GET", "Dados do dashboard"),
        ("/ia/alertas", "GET", "Alertas de IA")
    ]
    
    for endpoint, method, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BACKEND_URL}{endpoint}", headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: Erro de conexão - {e}")

def test_frontend_health():
    """Testa se o frontend está respondendo."""
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend está funcionando")
            return True
        else:
            print(f"❌ Frontend retornou status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão com o frontend: {e}")
        return False

def main():
    print("🔍 Testando integração RegiFlex...")
    print("=" * 50)
    
    # Teste do backend
    print("\n📡 Testando Backend...")
    token = test_backend_health()
    
    if token:
        test_api_endpoints(token)
    else:
        print("❌ Não foi possível obter token de autenticação")
    
    # Teste do frontend
    print("\n🌐 Testando Frontend...")
    test_frontend_health()
    
    print("\n" + "=" * 50)
    print("✅ Testes de integração concluídos!")
    print("\n📋 Para testar manualmente:")
    print(f"   Frontend: {FRONTEND_URL}")
    print(f"   Backend API: {BACKEND_URL}")
    print("\n🔑 Credenciais de teste:")
    print("   Admin: admin / password")
    print("   Psicólogo: psicologo1 / password")
    print("   Recepcionista: recepcionista1 / password")

if __name__ == "__main__":
    main()
