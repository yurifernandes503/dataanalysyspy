import { type NextRequest, NextResponse } from "next/server"
import { GoogleGenerativeAI } from "@google/generative-ai"

export async function POST(request: NextRequest) {
  try {
    console.log("🚀 Iniciando chamada para Gemini API...")

    const { prompt, dataContext } = await request.json()
    console.log("📝 Prompt recebido:", prompt?.substring(0, 100) + "...")

    // Verificar se a chave API existe
    const apiKey = process.env.GEMINI_API_KEY
    console.log("🔑 API Key existe:", !!apiKey)
    console.log("🔑 API Key primeiros chars:", apiKey?.substring(0, 10) + "...")

    if (!apiKey) {
      console.error("❌ GEMINI_API_KEY não encontrada")
      return NextResponse.json(
        {
          error: "GEMINI_API_KEY não configurada",
          details: "Verifique se a variável de ambiente está definida corretamente",
        },
        { status: 500 },
      )
    }

    // Inicializar Gemini AI
    console.log("🤖 Inicializando Gemini AI...")
    const genAI = new GoogleGenerativeAI(apiKey)

    const model = genAI.getGenerativeModel({
      model: "gemini-1.5-flash",
      generationConfig: {
        temperature: 0.7,
        topP: 0.8,
        topK: 40,
        maxOutputTokens: 1024,
      },
    })

    // Criar prompt simples e direto
    const simplePrompt = `
Analise estes dados de negócio em português brasileiro:

DADOS:
- Total de registros: ${dataContext?.totalRecords || 0}
- Colunas: ${dataContext?.columns || 0}
- Dados de exemplo: ${JSON.stringify(dataContext?.sampleData?.slice(0, 3) || [])}

PERGUNTA: ${prompt}

Responda de forma clara e objetiva com insights práticos para negócios.
Máximo 500 palavras.
`

    console.log("📤 Enviando para Gemini...")

    // Fazer chamada para Gemini
    const result = await model.generateContent(simplePrompt)
    const response = await result.response
    const text = response.text()

    console.log("📥 Resposta recebida:", text.substring(0, 100) + "...")

    // Resposta simplificada
    const analysis = {
      overview: text,
      insights: [
        "Análise processada com sucesso",
        "Dados analisados pelo Gemini AI",
        "Insights baseados nos padrões identificados",
      ],
      patterns: [
        {
          type: "trend",
          title: "Análise Completa",
          description: text.substring(0, 200) + "...",
          impact: "high",
          recommendation: "Revisar insights detalhados na resposta completa",
        },
      ],
      recommendations: [
        {
          priority: "high",
          action: "Implementar melhorias baseadas na análise",
          rationale: "Baseado na análise do Gemini AI",
          expectedImpact: "Melhoria nos resultados de negócio",
        },
      ],
      rawResponse: text,
      modelUsed: "gemini-1.5-flash",
      timestamp: new Date().toISOString(),
    }

    console.log("✅ Análise processada com sucesso")

    return NextResponse.json({
      analysis,
      success: true,
      timestamp: new Date().toISOString(),
      model: "gemini-1.5-flash",
    })
  } catch (error: any) {
    console.error("❌ Erro detalhado na API Gemini:", error)
    console.error("❌ Stack trace:", error.stack)

    let errorMessage = "Erro desconhecido"
    let statusCode = 500

    if (error.message?.includes("API_KEY")) {
      errorMessage = "Chave API inválida ou expirada"
      statusCode = 401
    } else if (error.message?.includes("quota") || error.message?.includes("limit")) {
      errorMessage = "Limite de quota excedido"
      statusCode = 429
    } else if (error.message?.includes("SAFETY")) {
      errorMessage = "Conteúdo bloqueado por filtros de segurança"
      statusCode = 400
    } else {
      errorMessage = error.message || "Erro na comunicação com Gemini API"
    }

    return NextResponse.json(
      {
        error: errorMessage,
        details: error.message,
        suggestion: "Verifique sua chave API e tente novamente",
        timestamp: new Date().toISOString(),
      },
      { status: statusCode },
    )
  }
}
