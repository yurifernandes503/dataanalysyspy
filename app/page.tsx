"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Upload, BarChart3, Brain, Download, FileSpreadsheet } from "lucide-react"
import { DataUpload } from "@/components/data-upload"
import { DataVisualization } from "@/components/data-visualization"
import { AIInsights } from "@/components/ai-insights-simple"
import { DataStats } from "@/components/data-stats"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function HomePage() {
  const [data, setData] = useState<any[]>([])
  const [columns, setColumns] = useState<string[]>([])
  const [fileName, setFileName] = useState<string>("")
  const [activeTab, setActiveTab] = useState("upload")

  const handleDataLoad = (newData: any[], newColumns: string[], newFileName: string) => {
    setData(newData)
    setColumns(newColumns)
    setFileName(newFileName)
    setActiveTab("overview")
  }

  const generateSampleData = () => {
    const sampleData = Array.from({ length: 100 }, (_, i) => ({
      id: i + 1,
      vendas: Math.floor(Math.random() * 10000) + 1000,
      regiao: ["Norte", "Sul", "Leste", "Oeste"][Math.floor(Math.random() * 4)],
      produto: ["Produto A", "Produto B", "Produto C"][Math.floor(Math.random() * 3)],
      mes: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"][Math.floor(Math.random() * 6)],
      satisfacao: Math.floor(Math.random() * 5) + 1,
      custo: Math.floor(Math.random() * 5000) + 500,
      lucro: 0,
    }))

    // Calculate profit
    sampleData.forEach((item) => {
      item.lucro = item.vendas - item.custo
    })

    const sampleColumns = ["id", "vendas", "regiao", "produto", "mes", "satisfacao", "custo", "lucro"]
    handleDataLoad(sampleData, sampleColumns, "dados_exemplo.csv")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto p-6">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
              <BarChart3 className="w-8 h-8 text-white" />
            </div>
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
            DataInsight AI
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Plataforma avançada de análise de dados com inteligência artificial para insights profundos e visualizações
            interativas
          </p>
        </div>

        {/* Quick Actions */}
        {data.length === 0 && (
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <Card className="border-2 border-dashed border-blue-200 hover:border-blue-400 transition-colors">
              <CardHeader className="text-center">
                <Upload className="w-12 h-12 text-blue-500 mx-auto mb-2" />
                <CardTitle>Carregar Seus Dados</CardTitle>
                <CardDescription>Faça upload de arquivos CSV, Excel ou JSON para análise</CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-2 border-dashed border-green-200 hover:border-green-400 transition-colors">
              <CardHeader className="text-center">
                <FileSpreadsheet className="w-12 h-12 text-green-500 mx-auto mb-2" />
                <CardTitle>Dados de Exemplo</CardTitle>
                <CardDescription>Use nosso dataset de exemplo para explorar as funcionalidades</CardDescription>
              </CardHeader>
              <CardContent className="text-center">
                <Button onClick={generateSampleData} className="w-full">
                  Carregar Dados de Exemplo
                </Button>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Main Content */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-5 mb-6">
            <TabsTrigger value="upload" className="flex items-center gap-2">
              <Upload className="w-4 h-4" />
              Upload
            </TabsTrigger>
            <TabsTrigger value="overview" disabled={data.length === 0}>
              <BarChart3 className="w-4 h-4" />
              Visão Geral
            </TabsTrigger>
            <TabsTrigger value="visualization" disabled={data.length === 0}>
              <BarChart3 className="w-4 h-4" />
              Visualização
            </TabsTrigger>
            <TabsTrigger value="insights" disabled={data.length === 0}>
              <Brain className="w-4 h-4" />
              IA Insights
            </TabsTrigger>
            <TabsTrigger value="export" disabled={data.length === 0}>
              <Download className="w-4 h-4" />
              Exportar
            </TabsTrigger>
          </TabsList>

          <TabsContent value="upload">
            <DataUpload onDataLoad={handleDataLoad} />
          </TabsContent>

          <TabsContent value="overview">
            <DataStats data={data} columns={columns} fileName={fileName} />
          </TabsContent>

          <TabsContent value="visualization">
            <DataVisualization data={data} columns={columns} />
          </TabsContent>

          <TabsContent value="insights">
            <AIInsights data={data} columns={columns} />
          </TabsContent>

          <TabsContent value="export">
            <Card>
              <CardHeader>
                <CardTitle>Exportar Dados</CardTitle>
                <CardDescription>Baixe seus dados processados em diferentes formatos</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-3 gap-4">
                  <Button variant="outline" className="h-20 flex flex-col gap-2">
                    <FileSpreadsheet className="w-6 h-6" />
                    CSV
                  </Button>
                  <Button variant="outline" className="h-20 flex flex-col gap-2">
                    <FileSpreadsheet className="w-6 h-6" />
                    Excel
                  </Button>
                  <Button variant="outline" className="h-20 flex flex-col gap-2">
                    <FileSpreadsheet className="w-6 h-6" />
                    JSON
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
