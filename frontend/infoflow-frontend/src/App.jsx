import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Loader2, Search, Calendar, ExternalLink, Clock } from 'lucide-react'
import './App.css'

function App() {
  const [tema, setTema] = useState('')
  const [janelaTempoSelecionada, setJanelaTempoSelecionada] = useState('dias')
  const [noticias, setNoticias] = useState([])
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState('')
  const [totalArtigos, setTotalArtigos] = useState(0)

  const opcoesJanelaTempo = [
    { value: 'dias', label: 'Últimos 7 dias' },
    { value: 'semanas', label: 'Últimas 4 semanas' },
    { value: 'meses', label: 'Últimos 3 meses' },
    { value: 'anos', label: 'Último ano' }
  ]

  const buscarNoticias = async () => {
    if (!tema.trim()) {
      setErro('Por favor, digite um tema para buscar')
      return
    }

    setCarregando(true)
    setErro('')
    setNoticias([])

    try {
      const response = await fetch('/api/news/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tema: tema.trim(),
          janela_tempo: janelaTempoSelecionada,
          max_articles: 20
        })
      })

      const data = await response.json()

      if (response.ok && data.success) {
        setNoticias(data.artigos)
        setTotalArtigos(data.total_artigos)
      } else {
        setErro(data.error || 'Erro ao buscar notícias')
      }
    } catch (error) {
      setErro('Erro de conexão com o servidor')
      console.error('Erro:', error)
    } finally {
      setCarregando(false)
    }
  }

  const formatarData = (dataString) => {
    try {
      const data = new Date(dataString)
      return data.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return 'Data não disponível'
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      buscarNoticias()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            InfoFlow
          </h1>
          <p className="text-lg text-gray-600">
            Descubra as principais notícias sobre qualquer tema
          </p>
        </div>

        {/* Search Form */}
        <Card className="max-w-2xl mx-auto mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              Buscar Notícias
            </CardTitle>
            <CardDescription>
              Digite um tema e selecione o período de tempo para encontrar as notícias mais relevantes
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <Input
                  placeholder="Ex: tecnologia, esportes, política..."
                  value={tema}
                  onChange={(e) => setTema(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="w-full"
                />
              </div>
              <div className="sm:w-48">
                <Select value={janelaTempoSelecionada} onValueChange={setJanelaTempoSelecionada}>
                  <SelectTrigger>
                    <Calendar className="h-4 w-4 mr-2" />
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {opcoesJanelaTempo.map((opcao) => (
                      <SelectItem key={opcao.value} value={opcao.value}>
                        {opcao.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <Button 
              onClick={buscarNoticias} 
              disabled={carregando || !tema.trim()}
              className="w-full"
            >
              {carregando ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Buscando...
                </>
              ) : (
                <>
                  <Search className="mr-2 h-4 w-4" />
                  Buscar Notícias
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Error Message */}
        {erro && (
          <Card className="max-w-2xl mx-auto mb-8 border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-600 text-center">{erro}</p>
            </CardContent>
          </Card>
        )}

        {/* Results Header */}
        {noticias.length > 0 && (
          <div className="max-w-4xl mx-auto mb-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-semibold text-gray-900">
                Resultados para "{tema}"
              </h2>
              <Badge variant="secondary" className="text-sm">
                {noticias.length} de {totalArtigos} artigos
              </Badge>
            </div>
            <p className="text-gray-600 mt-1">
              {opcoesJanelaTempo.find(o => o.value === janelaTempoSelecionada)?.label}
            </p>
          </div>
        )}

        {/* News Results */}
        <div className="max-w-4xl mx-auto grid gap-6">
          {noticias.map((noticia, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex flex-col lg:flex-row gap-4">
                  {noticia.imagem && (
                    <div className="lg:w-48 flex-shrink-0">
                      <img
                        src={noticia.imagem}
                        alt={noticia.titulo}
                        className="w-full h-32 lg:h-24 object-cover rounded-lg"
                        onError={(e) => {
                          e.target.style.display = 'none'
                        }}
                      />
                    </div>
                  )}
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                      {noticia.titulo}
                    </h3>
                    <p className="text-gray-600 mb-3 line-clamp-3">
                      {noticia.descricao}
                    </p>
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span className="font-medium">{noticia.fonte}</span>
                        <div className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          {formatarData(noticia.data_publicacao)}
                        </div>
                      </div>
                      <Button variant="outline" size="sm" asChild>
                        <a 
                          href={noticia.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="flex items-center gap-1"
                        >
                          Ler mais
                          <ExternalLink className="h-3 w-3" />
                        </a>
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Empty State */}
        {!carregando && noticias.length === 0 && !erro && tema && (
          <Card className="max-w-2xl mx-auto">
            <CardContent className="pt-6 text-center">
              <p className="text-gray-500">
                Nenhuma notícia encontrada para "{tema}" no período selecionado.
                Tente outro tema ou período de tempo.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default App

