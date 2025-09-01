#!/usr/bin/env python3
"""
Testes automatizados para a API InfoFlow
"""

import requests
import json
import sys
import time

# Configurações
API_BASE_URL = "http://localhost:5000/api"
TIMEOUT = 10

def test_health_check():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/news/health", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "InfoFlow News API"
        print("✅ Health check passou")
        return True
    except Exception as e:
        print(f"❌ Health check falhou: {e}")
        return False

def test_search_news_valid():
    """Testa busca de notícias com parâmetros válidos"""
    print("🔍 Testando busca de notícias válida...")
    try:
        payload = {
            "tema": "tecnologia",
            "janela_tempo": "dias",
            "max_articles": 5
        }
        response = requests.post(
            f"{API_BASE_URL}/news/search",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["tema"] == "tecnologia"
        assert data["janela_tempo"] == "dias"
        assert len(data["artigos"]) > 0
        assert data["total_artigos"] > 0
        
        # Verificar estrutura dos artigos
        artigo = data["artigos"][0]
        required_fields = ["titulo", "descricao", "url", "fonte", "data_publicacao"]
        for field in required_fields:
            assert field in artigo
            assert artigo[field] is not None
        
        print("✅ Busca de notícias válida passou")
        return True
    except Exception as e:
        print(f"❌ Busca de notícias válida falhou: {e}")
        return False

def test_search_news_different_time_windows():
    """Testa busca com diferentes janelas de tempo"""
    print("🔍 Testando diferentes janelas de tempo...")
    time_windows = ["dias", "semanas", "meses", "anos"]
    
    for window in time_windows:
        try:
            payload = {
                "tema": "esportes",
                "janela_tempo": window,
                "max_articles": 3
            }
            response = requests.post(
                f"{API_BASE_URL}/news/search",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=TIMEOUT
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert data["janela_tempo"] == window
            print(f"  ✅ Janela de tempo '{window}' passou")
        except Exception as e:
            print(f"  ❌ Janela de tempo '{window}' falhou: {e}")
            return False
    
    print("✅ Teste de janelas de tempo passou")
    return True

def test_search_news_invalid_params():
    """Testa busca com parâmetros inválidos"""
    print("🔍 Testando parâmetros inválidos...")
    
    # Teste sem tema
    try:
        payload = {"janela_tempo": "dias"}
        response = requests.post(
            f"{API_BASE_URL}/news/search",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        print("  ✅ Teste sem tema passou")
    except Exception as e:
        print(f"  ❌ Teste sem tema falhou: {e}")
        return False
    
    # Teste com payload vazio
    try:
        response = requests.post(
            f"{API_BASE_URL}/news/search",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert response.status_code == 400
        print("  ✅ Teste com payload vazio passou")
    except Exception as e:
        print(f"  ❌ Teste com payload vazio falhou: {e}")
        return False
    
    print("✅ Teste de parâmetros inválidos passou")
    return True

def test_search_news_different_themes():
    """Testa busca com diferentes temas"""
    print("🔍 Testando diferentes temas...")
    themes = ["tecnologia", "esportes", "política", "economia", "saúde"]
    
    for theme in themes:
        try:
            payload = {
                "tema": theme,
                "janela_tempo": "dias",
                "max_articles": 3
            }
            response = requests.post(
                f"{API_BASE_URL}/news/search",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=TIMEOUT
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert data["tema"] == theme
            # Verificar se o tema aparece nos títulos das notícias
            found_theme = any(theme.lower() in artigo["titulo"].lower() or 
                            theme.lower() in artigo["descricao"].lower() 
                            for artigo in data["artigos"])
            assert found_theme, f"Tema '{theme}' não encontrado nas notícias"
            print(f"  ✅ Tema '{theme}' passou")
        except Exception as e:
            print(f"  ❌ Tema '{theme}' falhou: {e}")
            return False
    
    print("✅ Teste de diferentes temas passou")
    return True

def run_all_tests():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da API InfoFlow\n")
    
    tests = [
        test_health_check,
        test_search_news_valid,
        test_search_news_different_time_windows,
        test_search_news_invalid_params,
        test_search_news_different_themes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Linha em branco entre testes
    
    print(f"📊 Resultados: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram!")
        return True
    else:
        print("⚠️  Alguns testes falharam!")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

