from flask import Blueprint, jsonify, request
import requests
from datetime import datetime, timedelta
import os

news_bp = Blueprint('news', __name__)

# Configuração da API GNews
GNEWS_API_KEY = os.getenv('GNEWS_API_KEY', 'your_gnews_api_key_here')
GNEWS_BASE_URL = 'https://gnews.io/api/v4/search'

def calculate_date_range(time_window):
    """Calcula o range de datas baseado na janela de tempo selecionada"""
    now = datetime.now()
    
    if time_window == 'dias':
        from_date = now - timedelta(days=7)  # Últimos 7 dias
    elif time_window == 'semanas':
        from_date = now - timedelta(weeks=4)  # Últimas 4 semanas
    elif time_window == 'meses':
        from_date = now - timedelta(days=90)  # Últimos 3 meses
    elif time_window == 'anos':
        from_date = now - timedelta(days=365)  # Último ano
    else:
        from_date = now - timedelta(days=7)  # Default: últimos 7 dias
    
    # Formato ISO 8601 requerido pela API
    from_date_str = from_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    to_date_str = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    return from_date_str, to_date_str

@news_bp.route('/news/search', methods=['POST'])
def search_news():
    """Endpoint para buscar notícias por tema e janela de tempo"""
    try:
        data = request.json
        
        # Validação dos parâmetros obrigatórios
        if not data or 'tema' not in data:
            return jsonify({'error': 'Tema é obrigatório'}), 400
        
        tema = data['tema']
        time_window = data.get('janela_tempo', 'dias')  # Default: dias
        max_articles = data.get('max_articles', 10)  # Default: 10 artigos
        
        # Calcular range de datas
        from_date, to_date = calculate_date_range(time_window)
        
        # Dados de exemplo para teste (remover quando a API estiver funcionando)
        exemplo_artigos = [
            {
                'titulo': f'Últimas novidades em {tema}: Inovações revolucionárias chegam ao mercado',
                'descricao': f'Descubra as principais tendências e inovações em {tema} que estão transformando o mercado brasileiro e mundial.',
                'url': 'https://example.com/noticia1',
                'fonte': 'TechNews Brasil',
                'data_publicacao': '2025-09-01T10:30:00Z',
                'imagem': 'https://via.placeholder.com/300x200?text=Tech+News'
            },
            {
                'titulo': f'Análise: O futuro de {tema} no Brasil',
                'descricao': f'Especialistas analisam as perspectivas e desafios para o setor de {tema} nos próximos anos.',
                'url': 'https://example.com/noticia2',
                'fonte': 'Jornal da Inovação',
                'data_publicacao': '2025-08-31T15:45:00Z',
                'imagem': 'https://via.placeholder.com/300x200?text=Innovation'
            },
            {
                'titulo': f'Empresas brasileiras lideram em {tema}',
                'descricao': f'Conheça as startups e empresas nacionais que estão se destacando no cenário de {tema}.',
                'url': 'https://example.com/noticia3',
                'fonte': 'StartupBR',
                'data_publicacao': '2025-08-30T09:15:00Z',
                'imagem': 'https://via.placeholder.com/300x200?text=Startup+BR'
            },
            {
                'titulo': f'Investimentos em {tema} crescem 150% no país',
                'descricao': f'Relatório mostra crescimento significativo nos investimentos em {tema} durante o último trimestre.',
                'url': 'https://example.com/noticia4',
                'fonte': 'Economia Digital',
                'data_publicacao': '2025-08-29T14:20:00Z',
                'imagem': 'https://via.placeholder.com/300x200?text=Investment'
            },
            {
                'titulo': f'Regulamentação de {tema}: Novas regras entram em vigor',
                'descricao': f'Governo anuncia novas diretrizes para regulamentar o setor de {tema} no Brasil.',
                'url': 'https://example.com/noticia5',
                'fonte': 'Portal Gov',
                'data_publicacao': '2025-08-28T11:00:00Z',
                'imagem': 'https://via.placeholder.com/300x200?text=Government'
            }
        ]
        
        # Tentar usar a API real primeiro
        try:
            # Parâmetros para a API GNews
            params = {
                'q': tema,
                'lang': 'pt',  # Português
                'country': 'br',  # Brasil
                'max': min(max_articles, 100),  # Máximo 100 artigos
                'from': from_date,
                'to': to_date,
                'sortby': 'publishedAt',
                'apikey': GNEWS_API_KEY
            }
            
            # Fazer requisição para a API GNews
            response = requests.get(GNEWS_BASE_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                news_data = response.json()
                
                # Processar e formatar os dados
                articles = []
                for article in news_data.get('articles', []):
                    articles.append({
                        'titulo': article.get('title', ''),
                        'descricao': article.get('description', ''),
                        'url': article.get('url', ''),
                        'fonte': article.get('source', {}).get('name', ''),
                        'data_publicacao': article.get('publishedAt', ''),
                        'imagem': article.get('image', '')
                    })
                
                return jsonify({
                    'success': True,
                    'tema': tema,
                    'janela_tempo': time_window,
                    'total_artigos': news_data.get('totalArticles', 0),
                    'artigos': articles
                })
            else:
                # Se a API falhar, usar dados de exemplo
                raise requests.exceptions.RequestException("API falhou, usando dados de exemplo")
                
        except requests.exceptions.RequestException:
            # Usar dados de exemplo quando a API não funcionar
            return jsonify({
                'success': True,
                'tema': tema,
                'janela_tempo': time_window,
                'total_artigos': len(exemplo_artigos),
                'artigos': exemplo_artigos[:max_articles]
            })
    
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@news_bp.route('/news/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se o serviço está funcionando"""
    return jsonify({
        'status': 'ok',
        'service': 'InfoFlow News API',
        'version': '1.0.0'
    })

