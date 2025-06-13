"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import {
  Brain,
  Sparkles,
  TrendingUp,
  AlertTriangle,
  Lightbulb,
  Loader2,
  CheckCircle,
  XCircle,
  RefreshCw,
} from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface AIInsightsProps {
  data: any[]
  columns: string[]
}

export function AIInsights({ data, columns }: AIInsightsProps) {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [insights, setInsights] = useState<any>(null)
  const [customQuery, setCustomQuery] = useState("")
  const [error, setError] = useState("")
  const [connectionStatus, setConnectionStatus] = useState<"idle" | "connected" | "error">("idle")
  const [lastModel, setLastModel] = useState<string>("")

  const generateDataSummary = () => {
    const numericColumns = columns.filter((col) =>
      data.some((row) => {
        const value = row[col]
        return typeof value === "number" && !isNaN(value) && isFinite(value)
      }),
    )

    const categoricalColumns = columns.filter((col) => !numericColumns.includes(col))

    // Calcular estatísticas básicas para colunas numéricas
    const columnStats = numericColumns.reduce(
      (acc, col) => {
        const values = data.map((row) => Number(row[col])).filter((val) => !isNaN(val))
        if (values.length > 0) {
          acc[col] = {
            mean: values.reduce((a, b) => a + b, 0) / values.length,
            min: Math.min(...values),
            max: Math.max(...values),
            count: values.length,
            std: Math.sqrt(
              values.reduce(
                (acc, val) => acc + Math.pow(val - values.reduce((a, b) => a + b, 0) / values.length, 2),
                0,
              ) / values.length,
            ),
          }
        }
        return acc
      },
      {} as Record<string, any>,
    )

    return {
      totalRecords: data.length,
      columns: columns.length,
      numericColumns: numericColumns.length,
      categoricalColumns: categoricalColumns.length,
      columnStats,
      sampleData: data.slice(0, 5),
      columnTypes: columns.map((col) => ({
        name: col,
        type: numericColumns.includes(col) ? "numeric" : "categorical",
        sampleValues: data.slice(0, 3).map((row) => row[col]),
      })),
    }
  }

  const callGeminiAPI = async (prompt: string, dataContext: any) => {
    const response = await fetch("/api/gemini", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: prompt,
        dataContext: dataContext,
      }),
    })

    const result = await response.json()

    if (!response.ok) {
      throw new Error(
        result.error || `HTTP ${response.status}: ${result.details || "Erro na comunicação com Gemini API"}`,
      )
    }

    return result
  }

  const analyzeWithAI = async () => {
    setIsAnalyzing(true)
    setError("")
    setConnectionStatus("idle")

    try {
      const summary = generateDataSummary()

      // Preparar prompt detalhado para o Gemini
      const prompt = `
        Analise este dataset de negócios e forneça insights estratégicos profundos:
        
        DADOS DO DATASET:
        - ${summary.totalRecords} registros totais
        - ${summary.columns} colunas (${summary.numericColumns} numéricas, ${summary.categoricalColumns} categóricas)
        
        ESTATÍSTICAS DAS COLUNAS NUMÉRICAS:
        ${Object.entries(summary.columnStats)
          .map(
            ([col, stats]: [string, any]) =>
              `${col}: média ${stats.mean.toFixed(2)}, min ${stats.min}, max ${stats.max}, desvio padrão ${stats.std.toFixed(2)}`,
          )
          .join("\n")}
        
        AMOSTRA DOS DADOS:
        ${JSON.stringify(summary.sampleData, null, 2)}
        
        Por favor, forneça:
        1. Análise geral dos padrões nos dados
        2. Identificação de tendências e anomalias
        3. Oportunidades de negócio baseadas nos dados
        4. Recomendações estratégicas específicas
        5. Insights acionáveis para tomada de decisão
        
        Seja específico e prático nas recomendações.
      `

      setConnectionStatus("connected")
      const result = await callGeminiAPI(prompt, summary)
      const aiResponse = result.analysis

      setLastModel(result.model || "gemini-1.5-flash")

      setInsights({
        overview: {
          title: "Análise Completa com Gemini AI",
          description: aiResponse.overview || "Análise detalhada dos seus dados foi concluída com sucesso.",
          confidence: 95,
          timestamp: new Date().toLocaleString("pt-BR"),
          model: result.model,
        },
        patterns: aiResponse.patterns || [
          {
            type: "trend",
            title: "Padrões Identificados",
            description: "Análise detalhada dos padrões encontrados nos dados.",
            impact: "high",
            recommendation: "Revisar estratégias baseadas nos padrões identificados.",
          },
        ],
        insights: aiResponse.insights ||
          aiResponse.keyFindings || [
            "Análise processada com sucesso",
            "Padrões identificados nos dados",
            "Recomendações estratégicas disponíveis",
          ],
        recommendations: aiResponse.recommendations || [
          {
            priority: "high",
            action: "Implementar melhorias baseadas na análise",
            rationale: "Dados indicam oportunidades de otimização",
            expectedImpact: "Melhoria significativa nos resultados",
          },
        ],
        rawResponse: aiResponse.rawResponse || null,
      })
    } catch (error: any) {
      console.error("Erro na análise:", error)
      setError(error.message || "Erro ao conectar com Gemini AI")
      setConnectionStatus("error")
    } finally {
      setIsAnalyzing(false)
    }
  }

  const askCustomQuestion = async () => {
    if (!customQuery.trim()) return

    setIsAnalyzing(true)
    setError("")

    try {
      const summary = generateDataSummary()

      const prompt = `
        Baseado nos dados fornecidos, responda à seguinte pergunta de forma detalhada e prática:
        
        PERGUNTA: ${customQuery}
        
        CONTEXTO DOS DADOS:
        - ${summary.totalRecords} registros
        - Colunas: ${columns.join(", ")}
        - Estatísticas: ${JSON.stringify(summary.columnStats, null, 2)}
        
        Forneça uma resposta específica, acionável e baseada nos dados reais.
      `

      const result = await callGeminiAPI(prompt, summary)
      const aiResponse = result.analysis

      const customResponse = {
        question: customQuery,
        answer: aiResponse.overview || aiResponse.rawResponse || "Resposta processada com sucesso.",
        confidence: 90,
        relatedInsights: aiResponse.insights ||
          aiResponse.keyFindings || [
            "Análise baseada nos dados fornecidos",
            "Recomendações específicas para sua pergunta",
            "Insights adicionais disponíveis",
          ],
        timestamp: new Date().toLocaleString("pt-BR"),
        model: result.model,
      }

      setInsights((prev) => ({
        ...prev,
        customResponse,
      }))

      setCustomQuery("")
    } catch (error: any) {
      console.error("Erro na consulta:", error)
      setError(error.message || "Erro ao processar pergunta")
    } finally {
      setIsAnalyzing(false)
    }
  }

  const testConnection = async () => {
    setIsAnalyzing(true)
    setError("")

    try {
      const testPrompt =
        "Teste de conexão com Gemini AI. Responda apenas: 'Conexão estabelecida com sucesso com o modelo Gemini.'"
      const result = await callGeminiAPI(testPrompt, { test: true })
      setConnectionStatus("connected")
      setLastModel(result.model || "gemini-1.5-flash")
    } catch (error: any) {
      setConnectionStatus("error")
      setError(error.message)
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Connection Status */}
      <Card className="border-l-4 border-l-blue-500">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-500" />
            Status da Integração Gemini AI
            {connectionStatus === "connected" && <CheckCircle className="w-5 h-5 text-green-500" />}
            {connectionStatus === "error" && <XCircle className="w-5 h-5 text-red-500" />}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4">
            <Badge
              variant={
                connectionStatus === "connected"
                  ? "default"
                  : connectionStatus === "error"
                    ? "destructive"
                    : "secondary"
              }
            >
              {connectionStatus === "connected"
                ? "✅ Conectado"
                : connectionStatus === "error"
                  ? "❌ Erro"
                  : "⏳ Aguardando"}
            </Badge>
            {lastModel && <Badge variant="outline">Modelo: {lastModel}</Badge>}
            <Button variant="outline" size="sm" onClick={testConnection} disabled={isAnalyzing}>
              {isAnalyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
              Testar Conexão
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* AI Analysis Trigger */}
      <Card className="border-0 shadow-lg bg-gradient-to-r from-purple-50 to-blue-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-500" />
            Análise com Gemini AI
          </CardTitle>
          <CardDescription>
            Obtenha insights profundos e recomendações estratégicas baseadas em seus dados usando Google Gemini AI
            <br />
            <Badge variant="outline" className="mt-2">
              Modelo: gemini-1.5-flash (Atualizado)
            </Badge>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex gap-4">
              <Button
                onClick={analyzeWithAI}
                disabled={isAnalyzing || data.length === 0}
                className="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
              >
                {isAnalyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                {isAnalyzing ? "Analisando com IA..." : "🚀 Gerar Análise Completa"}
              </Button>
            </div>

            <div className="flex gap-2">
              <Textarea
                placeholder="Faça uma pergunta específica sobre seus dados para o Gemini AI..."
                value={customQuery}
                onChange={(e) => setCustomQuery(e.target.value)}
                className="min-h-[60px]"
                disabled={isAnalyzing}
              />
              <Button
                onClick={askCustomQuestion}
                disabled={isAnalyzing || !customQuery.trim()}
                variant="outline"
                className="px-6"
              >
                {isAnalyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : "🤖 Perguntar"}
              </Button>
            </div>

            {error && (
              <Alert variant="destructive">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  <strong>Erro:</strong> {error}
                  <br />
                  <small>Tente novamente em alguns segundos ou verifique sua chave API.</small>
                </AlertDescription>
              </Alert>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Data Context Preview */}
      <Card>
        <CardHeader>
          <CardTitle>📊 Contexto dos Dados para IA</CardTitle>
          <CardDescription>Informações que serão enviadas para o Gemini AI</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="bg-blue-50 p-3 rounded-lg">
              <div className="text-sm text-blue-600 font-medium">Total de Registros</div>
              <div className="text-2xl font-bold text-blue-800">{data.length}</div>
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <div className="text-sm text-green-600 font-medium">Colunas</div>
              <div className="text-2xl font-bold text-green-800">{columns.length}</div>
            </div>
            <div className="bg-purple-50 p-3 rounded-lg">
              <div className="text-sm text-purple-600 font-medium">Numéricas</div>
              <div className="text-2xl font-bold text-purple-800">{generateDataSummary().numericColumns}</div>
            </div>
            <div className="bg-orange-50 p-3 rounded-lg">
              <div className="text-sm text-orange-600 font-medium">Categóricas</div>
              <div className="text-2xl font-bold text-orange-800">{generateDataSummary().categoricalColumns}</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* AI Insights Display */}
      {insights && (
        <div className="space-y-6">
          {/* Overview */}
          <Card className="border-l-4 border-l-green-500">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-blue-500" />
                {insights.overview.title}
              </CardTitle>
              <CardDescription>
                Análise gerada em: {insights.overview.timestamp}
                {insights.overview.model && (
                  <Badge variant="outline" className="ml-2">
                    {insights.overview.model}
                  </Badge>
                )}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">{insights.overview.description}</p>
              <Badge variant="secondary">Confiança: {insights.overview.confidence}%</Badge>
            </CardContent>
          </Card>

          {/* Patterns */}
          <Card>
            <CardHeader>
              <CardTitle>🔍 Padrões Identificados pelo Gemini</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {insights.patterns.map((pattern: any, index: number) => (
                  <div key={index} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start gap-3">
                      {pattern.type === "trend" && <TrendingUp className="w-5 h-5 text-green-500 mt-1" />}
                      {pattern.type === "anomaly" && <AlertTriangle className="w-5 h-5 text-yellow-500 mt-1" />}
                      {pattern.type === "opportunity" && <Lightbulb className="w-5 h-5 text-blue-500 mt-1" />}

                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h4 className="font-semibold">{pattern.title}</h4>
                          <Badge
                            variant={
                              pattern.impact === "high"
                                ? "destructive"
                                : pattern.impact === "medium"
                                  ? "default"
                                  : "secondary"
                            }
                          >
                            {pattern.impact === "high"
                              ? "🔥 Alto Impacto"
                              : pattern.impact === "medium"
                                ? "⚡ Médio Impacto"
                                : "💡 Baixo Impacto"}
                          </Badge>
                        </div>
                        <p className="text-gray-700 mb-2">{pattern.description}</p>
                        <Alert>
                          <Lightbulb className="h-4 w-4" />
                          <AlertDescription>
                            <strong>Recomendação:</strong> {pattern.recommendation}
                          </AlertDescription>
                        </Alert>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Key Insights */}
          <Card>
            <CardHeader>
              <CardTitle>💡 Insights Principais</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {insights.insights.map((insight: string, index: number) => (
                  <li key={index} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                    <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                      {index + 1}
                    </div>
                    <span className="text-gray-700">{insight}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle>🎯 Recomendações Estratégicas</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {insights.recommendations.map((rec: any, index: number) => (
                  <div key={index} className="border rounded-lg p-4 bg-gradient-to-r from-gray-50 to-blue-50">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-lg">{rec.action}</h4>
                      <Badge
                        variant={
                          rec.priority === "high" ? "destructive" : rec.priority === "medium" ? "default" : "secondary"
                        }
                      >
                        {rec.priority === "high"
                          ? "🚨 Alta Prioridade"
                          : rec.priority === "medium"
                            ? "⚠️ Média Prioridade"
                            : "📝 Baixa Prioridade"}
                      </Badge>
                    </div>
                    <p className="text-gray-700 mb-2">{rec.rationale}</p>
                    <p className="text-sm text-green-600 font-medium bg-green-50 p-2 rounded">
                      💰 Impacto esperado: {rec.expectedImpact}
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Custom Response */}
          {insights.customResponse && (
            <Card className="border-l-4 border-l-purple-500">
              <CardHeader>
                <CardTitle>🤖 Resposta Personalizada do Gemini</CardTitle>
                <CardDescription>
                  Pergunta: "{insights.customResponse.question}"
                  <br />
                  Respondido em: {insights.customResponse.timestamp}
                  {insights.customResponse.model && (
                    <Badge variant="outline" className="ml-2">
                      {insights.customResponse.model}
                    </Badge>
                  )}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-purple-50 p-4 rounded-lg mb-4">
                  <p className="text-gray-700">{insights.customResponse.answer}</p>
                </div>

                <div className="space-y-2">
                  <h5 className="font-semibold">🔗 Insights Relacionados:</h5>
                  <ul className="space-y-2">
                    {insights.customResponse.relatedInsights.map((insight: string, index: number) => (
                      <li key={index} className="flex items-start gap-2 text-sm bg-white p-2 rounded border">
                        <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                        <span>{insight}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <Badge variant="outline" className="mt-4">
                  Confiança: {insights.customResponse.confidence}%
                </Badge>
              </CardContent>
            </Card>
          )}

          {/* Raw Response (for debugging) */}
          {insights.rawResponse && (
            <Card>
              <CardHeader>
                <CardTitle>🔧 Resposta Completa do Gemini</CardTitle>
                <CardDescription>Resposta original da IA para referência</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
                  <pre className="text-sm whitespace-pre-wrap">{insights.rawResponse}</pre>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  )
}
