"use client"

import { useMemo } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { BarChart3, TrendingUp, Database, FileText } from "lucide-react"

interface DataStatsProps {
  data: any[]
  columns: string[]
  fileName: string
}

export function DataStats({ data, columns, fileName }: DataStatsProps) {
  const stats = useMemo(() => {
    if (!data || data.length === 0) return null

    const numericColumns = columns.filter((col) => data.some((row) => typeof row[col] === "number"))

    const categoricalColumns = columns.filter((col) => !numericColumns.includes(col))

    const missingValues = columns.reduce(
      (acc, col) => {
        acc[col] = data.filter((row) => row[col] === null || row[col] === undefined || row[col] === "").length
        return acc
      },
      {} as Record<string, number>,
    )

    const totalMissing = Object.values(missingValues).reduce((a, b) => a + b, 0)

    return {
      totalRows: data.length,
      totalColumns: columns.length,
      numericColumns: numericColumns.length,
      categoricalColumns: categoricalColumns.length,
      totalMissing,
      missingValues,
      numericStats: numericColumns.reduce(
        (acc, col) => {
          const values = data.map((row) => row[col]).filter((val) => typeof val === "number")
          if (values.length > 0) {
            acc[col] = {
              mean: values.reduce((a, b) => a + b, 0) / values.length,
              min: Math.min(...values),
              max: Math.max(...values),
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
      ),
    }
  }, [data, columns])

  if (!stats) return null

  return (
    <div className="space-y-6">
      {/* Overview Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-2">
              <Database className="w-5 h-5 text-blue-500" />
              <div>
                <p className="text-2xl font-bold">{stats.totalRows.toLocaleString()}</p>
                <p className="text-sm text-gray-600">Linhas</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-green-500" />
              <div>
                <p className="text-2xl font-bold">{stats.totalColumns}</p>
                <p className="text-sm text-gray-600">Colunas</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-purple-500" />
              <div>
                <p className="text-2xl font-bold">{stats.numericColumns}</p>
                <p className="text-sm text-gray-600">Numéricas</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-orange-500" />
              <div>
                <p className="text-2xl font-bold">{stats.categoricalColumns}</p>
                <p className="text-sm text-gray-600">Categóricas</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Data Preview */}
      <Card>
        <CardHeader>
          <CardTitle>Prévia dos Dados</CardTitle>
          <CardDescription>Arquivo: {fileName} | Primeiras 10 linhas</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-200">
              <thead>
                <tr className="bg-gray-50">
                  {columns.map((col) => (
                    <th key={col} className="border border-gray-200 p-2 text-left font-semibold">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.slice(0, 10).map((row, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    {columns.map((col) => (
                      <td key={col} className="border border-gray-200 p-2">
                        {typeof row[col] === "number" ? row[col].toLocaleString() : String(row[col] || "")}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Column Analysis */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Estatísticas Numéricas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(stats.numericStats).map(([col, stat]) => (
                <div key={col} className="border rounded-lg p-4">
                  <h4 className="font-semibold mb-2">{col}</h4>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>
                      Média: <Badge variant="secondary">{stat.mean.toFixed(2)}</Badge>
                    </div>
                    <div>
                      Desvio: <Badge variant="secondary">{stat.std.toFixed(2)}</Badge>
                    </div>
                    <div>
                      Mín: <Badge variant="outline">{stat.min.toLocaleString()}</Badge>
                    </div>
                    <div>
                      Máx: <Badge variant="outline">{stat.max.toLocaleString()}</Badge>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Qualidade dos Dados</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span>Total de valores ausentes:</span>
                <Badge variant={stats.totalMissing > 0 ? "destructive" : "secondary"}>{stats.totalMissing}</Badge>
              </div>

              {Object.entries(stats.missingValues).map(
                ([col, missing]) =>
                  missing > 0 && (
                    <div key={col} className="flex justify-between items-center text-sm">
                      <span>{col}:</span>
                      <Badge variant="outline">{missing} ausentes</Badge>
                    </div>
                  ),
              )}

              {stats.totalMissing === 0 && <p className="text-green-600 text-sm">✓ Nenhum valor ausente encontrado</p>}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
