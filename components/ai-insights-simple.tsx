"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Brain, Sparkles, Loader2, CheckCircle, XCircle, RefreshCw } from "lucide-react"
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

  const generateDataSummary = () => {
    const numericColumns = columns.filter((col) =>
      data.some((row) => {
        const value = row[col]
        return typeof value === "number" && !isNaN(value) && isFinite(value)
      }),
    )

    return {
      totalRecords: data.length,
      columns: columns.length,
      numericColumns: numericColumns.length,
      categoricalColumns: columns.length - numericColumns.length,
      sampleData: data.slice(0, 5),
    }
  }

  const callGeminiAPI = async (prompt: string, dataContext: any) => {
    console.log("🚀 Chamando API Gemini...")

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

    console.log("📡 Status da resposta:", response.status)

    const result = await response.json()
    console.log("📥 Resultado:", result)

    if (!response.ok) {
      throw new Error(result.error || `HTTP ${response.status}: ${result.details || "Erro na API"}`)
    }

    return result
  }

  const testConnection = async () => {
    setIsAnalyzing(true)
    setError("")
    console.log("🧪 Testando conexão com Gemini...")

    try {
      const result = await callGeminiAPI("Responda apenas: 'Conexão com Gemini estabelecida com sucesso!'", {
        test: true,
      })

      setConnectionStatus("connected")
      console.log("✅ Conexão estabelecida!")
    } catch (error: any) {
      console.error("❌ Erro na conexão:", error)
      setConnectionStatus("error")
      setError(error.message)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const analyzeWithAI = async () => {
    setIsAnalyzing(true)
    setError("")
    console.log("🔍 Iniciando análise com IA...")

    try {
      const summary = generateDataSummary()
      console.log("📊 Resumo dos dados:", summary)

      const prompt = `
        Analise este dataset de vendas e forneça insights de negócio:
        
        - ${summary.totalRecords} registros de vendas
        - ${summary.columns} colunas de dados
        - ${summary.numericColumns} colunas numéricas
        
        Forneça 3 insights principais sobre:
        1. Tendências de vendas
        2. Oportunidades de melhoria
        3. Recomendações estratégicas
      `

      const result = await callGeminiAPI(prompt, summary)
      const aiResponse = result.analysis

      setInsights({
        overview: {
          title: "Análise Completa com Gemini AI",
          description: aiResponse.overview || "Análise concluída com sucesso",
          timestamp: new Date().toLocaleString("pt-BR"),
          model: result.model,
        },
        insights: aiResponse.insights || [
          "Análise processada com sucesso",
          "Padrões identificados nos dados",
          "Recomendações disponíveis",
        ],
        rawResponse: aiResponse.rawResponse,
      })

      setConnectionStatus("connected")
      console.log("✅ Análise concluída!")
    } catch (error: any) {
      console.error("❌ Erro na análise:", error)
      setError(error.message)
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
      const result = await callGeminiAPI(customQuery, summary)

      setInsights((prev) => ({
        ...prev,
        customResponse: {
          question: customQuery,
          answer: result.analysis.overview || "Resposta processada",
          timestamp: new Date().toLocaleString("pt-BR"),
        },
      }))

      setCustomQuery("")
    } catch (error: any) {
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

            <Button variant="outline" size="sm" onClick={testConnection} disabled={isAnalyzing}>
              {isAnalyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
              Testar Conexão
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* AI Analysis */}
      <Card className="border-0 shadow-lg bg-gradient-to-r from-purple-50 to-blue-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-500" />
            Análise com Gemini AI
          </CardTitle>
          <CardDescription>Obtenha insights profundos usando Google Gemini AI</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Button
              onClick={analyzeWithAI}
              disabled={isAnalyzing || data.length === 0}
              className="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
            >
              {isAnalyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              {isAnalyzing ? "Analisando..." : "🚀 Gerar Análise Completa"}
            </Button>

            <div className="flex gap-2">
              <Textarea
                placeholder="Faça uma pergunta sobre seus dados..."
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
                {isAnalyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : "🤖"}
                Perguntar
              </Button>
            </div>

            {error && (
              <Alert variant="destructive">
                <AlertDescription>
                  <strong>Erro:</strong> {error}
                </AlertDescription>
              </Alert>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Data Context */}
      <Card>
        <CardHeader>
          <CardTitle>📊 Contexto dos Dados</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 p-3 rounded-lg">
              <div className="text-sm text-blue-600 font-medium">Registros</div>
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

      {/* Results */}
      {insights && (
        <div className="space-y-6">
          <Card className="border-l-4 border-l-green-500">
            <CardHeader>
              <CardTitle>🤖 Análise do Gemini AI</CardTitle>
              <CardDescription>Gerado em: {insights.overview.timestamp}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="whitespace-pre-wrap">{insights.rawResponse || insights.overview.description}</p>
              </div>
            </CardContent>
          </Card>

          {insights.customResponse && (
            <Card className="border-l-4 border-l-purple-500">
              <CardHeader>
                <CardTitle>💬 Resposta Personalizada</CardTitle>
                <CardDescription>Pergunta: "{insights.customResponse.question}"</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <p className="whitespace-pre-wrap">{insights.customResponse.answer}</p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  )
}
