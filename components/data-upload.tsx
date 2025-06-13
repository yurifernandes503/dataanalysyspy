"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Upload, FileText, AlertCircle } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface DataUploadProps {
  onDataLoad: (data: any[], columns: string[], fileName: string) => void
}

export function DataUpload({ onDataLoad }: DataUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const parseCSV = (text: string): any[] => {
    const lines = text.trim().split("\n")
    const headers = lines[0].split(",").map((h) => h.trim().replace(/"/g, ""))

    return lines.slice(1).map((line) => {
      const values = line.split(",").map((v) => v.trim().replace(/"/g, ""))
      const obj: any = {}
      headers.forEach((header, index) => {
        const value = values[index] || ""
        // Try to parse as number
        const numValue = Number.parseFloat(value)
        obj[header] = isNaN(numValue) ? value : numValue
      })
      return obj
    })
  }

  const handleFile = useCallback(
    async (file: File) => {
      setIsLoading(true)
      setError(null)

      try {
        const text = await file.text()
        let data: any[] = []
        let columns: string[] = []

        if (file.name.endsWith(".csv")) {
          data = parseCSV(text)
          columns = Object.keys(data[0] || {})
        } else if (file.name.endsWith(".json")) {
          const jsonData = JSON.parse(text)
          data = Array.isArray(jsonData) ? jsonData : [jsonData]
          columns = Object.keys(data[0] || {})
        } else {
          throw new Error("Formato de arquivo não suportado. Use CSV ou JSON.")
        }

        if (data.length === 0) {
          throw new Error("O arquivo está vazio ou não contém dados válidos.")
        }

        onDataLoad(data, columns, file.name)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro ao processar arquivo")
      } finally {
        setIsLoading(false)
      }
    },
    [onDataLoad],
  )

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragging(false)

      const files = Array.from(e.dataTransfer.files)
      if (files.length > 0) {
        handleFile(files[0])
      }
    },
    [handleFile],
  )

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="w-5 h-5" />
            Upload de Dados
          </CardTitle>
          <CardDescription>Carregue seus dados em formato CSV ou JSON para começar a análise</CardDescription>
        </CardHeader>
        <CardContent>
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-gray-400"
            }`}
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
            onDragEnter={() => setIsDragging(true)}
            onDragLeave={() => setIsDragging(false)}
          >
            <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Arraste e solte seu arquivo aqui</h3>
            <p className="text-gray-600 mb-4">ou clique para selecionar um arquivo</p>
            <input
              type="file"
              accept=".csv,.json"
              onChange={handleFileInput}
              className="hidden"
              id="file-input"
              disabled={isLoading}
            />
            <Button asChild disabled={isLoading} className="cursor-pointer">
              <label htmlFor="file-input">{isLoading ? "Processando..." : "Selecionar Arquivo"}</label>
            </Button>
          </div>

          {error && (
            <Alert className="mt-4" variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Formatos Suportados</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center gap-3 p-3 border rounded-lg">
              <FileText className="w-8 h-8 text-green-500" />
              <div>
                <h4 className="font-semibold">CSV</h4>
                <p className="text-sm text-gray-600">Comma Separated Values</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 border rounded-lg">
              <FileText className="w-8 h-8 text-blue-500" />
              <div>
                <h4 className="font-semibold">JSON</h4>
                <p className="text-sm text-gray-600">JavaScript Object Notation</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
