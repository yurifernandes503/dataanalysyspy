"use client"

import { useState, useMemo, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  ScatterChart,
  Scatter,
} from "recharts"
import {
  BarChart3,
  LineChartIcon,
  PieChartIcon,
  ScatterChartIcon as ScatterIcon,
  TrendingUp,
  RefreshCw,
} from "lucide-react"

interface DataVisualizationProps {
  data: any[]
  columns: string[]
}

const COLORS = ["#3B82F6", "#EF4444", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#06B6D4", "#84CC16"]

export function DataVisualization({ data, columns }: DataVisualizationProps) {
  const [chartType, setChartType] = useState<"bar" | "line" | "pie" | "scatter">("bar")
  const [xAxis, setXAxis] = useState<string>("")
  const [yAxis, setYAxis] = useState<string>("")
  const [groupBy, setGroupBy] = useState<string>("none")
  const [isLoading, setIsLoading] = useState(false)

  // Separate numeric and categorical columns
  const { numericColumns, categoricalColumns } = useMemo(() => {
    if (!data || data.length === 0) return { numericColumns: [], categoricalColumns: [] }

    const numeric: string[] = []
    const categorical: string[] = []

    columns.forEach((col) => {
      // Check first few non-null values to determine type
      const sampleValues = data
        .slice(0, 10)
        .map((row) => row[col])
        .filter((val) => val != null)

      if (sampleValues.length > 0) {
        const isNumeric = sampleValues.every((val) => {
          const num = Number(val)
          return !isNaN(num) && isFinite(num)
        })

        if (isNumeric) {
          numeric.push(col)
        } else {
          categorical.push(col)
        }
      } else {
        categorical.push(col) // Default to categorical if no valid values
      }
    })

    return { numericColumns: numeric, categoricalColumns: categorical }
  }, [data, columns])

  // Auto-select initial values
  useEffect(() => {
    if (categoricalColumns.length > 0 && !xAxis) {
      setXAxis(categoricalColumns[0])
    }
    if (numericColumns.length > 0 && !yAxis) {
      setYAxis(numericColumns[0])
    }
  }, [categoricalColumns, numericColumns, xAxis, yAxis])

  // Process data for charts
  const chartData = useMemo(() => {
    if (!data || data.length === 0 || !xAxis) {
      return []
    }

    console.log("Processing chart data:", { chartType, xAxis, yAxis, groupBy })

    try {
      if (chartType === "pie") {
        // For pie charts, group by X axis and sum Y values or count
        const grouped: Record<string, number> = {}

        data.forEach((item) => {
          const key = String(item[xAxis] || "Unknown")
          if (yAxis && yAxis !== "count") {
            const value = Number(item[yAxis]) || 0
            grouped[key] = (grouped[key] || 0) + value
          } else {
            grouped[key] = (grouped[key] || 0) + 1
          }
        })

        return Object.entries(grouped)
          .map(([name, value]) => ({ name, value }))
          .sort((a, b) => b.value - a.value)
          .slice(0, 10) // Top 10 for readability
      }

      if (chartType === "scatter") {
        // For scatter plots, we need both X and Y to be numeric
        if (!yAxis || !numericColumns.includes(xAxis) || !numericColumns.includes(yAxis)) {
          return []
        }

        return data
          .filter((item) => {
            const x = Number(item[xAxis])
            const y = Number(item[yAxis])
            return !isNaN(x) && !isNaN(y) && isFinite(x) && isFinite(y)
          })
          .map((item) => ({
            [xAxis]: Number(item[xAxis]),
            [yAxis]: Number(item[yAxis]),
          }))
          .slice(0, 100) // Limit for performance
      }

      // For bar and line charts
      if (groupBy && groupBy !== "none") {
        // Group by both X axis and groupBy column
        const grouped: Record<string, Record<string, number>> = {}

        data.forEach((item) => {
          const xKey = String(item[xAxis] || "Unknown")
          const groupKey = String(item[groupBy] || "Unknown")

          if (!grouped[xKey]) {
            grouped[xKey] = {}
          }

          if (yAxis && yAxis !== "count") {
            const value = Number(item[yAxis]) || 0
            grouped[xKey][groupKey] = (grouped[xKey][groupKey] || 0) + value
          } else {
            grouped[xKey][groupKey] = (grouped[xKey][groupKey] || 0) + 1
          }
        })

        return Object.entries(grouped).map(([xKey, groups]) => ({
          [xAxis]: xKey,
          ...groups,
        }))
      } else {
        // Simple grouping by X axis
        const grouped: Record<string, { values: number[]; count: number }> = {}

        data.forEach((item) => {
          const key = String(item[xAxis] || "Unknown")

          if (!grouped[key]) {
            grouped[key] = { values: [], count: 0 }
          }

          if (yAxis && yAxis !== "count") {
            const value = Number(item[yAxis])
            if (!isNaN(value) && isFinite(value)) {
              grouped[key].values.push(value)
            }
          }
          grouped[key].count++
        })

        return Object.entries(grouped)
          .map(([key, data]) => {
            const result: any = { [xAxis]: key }

            if (yAxis && yAxis !== "count" && data.values.length > 0) {
              // Use average for line/bar charts
              result[yAxis] = data.values.reduce((a, b) => a + b, 0) / data.values.length
            } else {
              result.count = data.count
            }

            return result
          })
          .slice(0, 20) // Limit for readability
      }
    } catch (error) {
      console.error("Error processing chart data:", error)
      return []
    }
  }, [data, chartType, xAxis, yAxis, groupBy, numericColumns])

  const refreshData = () => {
    setIsLoading(true)
    // Simulate data refresh
    setTimeout(() => {
      setIsLoading(false)
    }, 1000)
  }

  const renderChart = () => {
    if (!chartData || chartData.length === 0) {
      return (
        <div className="h-64 flex flex-col items-center justify-center text-gray-500">
          <TrendingUp className="w-12 h-12 mb-4 text-gray-400" />
          <p className="text-lg font-medium">Nenhum dado para visualizar</p>
          <p className="text-sm">Configure os eixos acima para gerar o gráfico</p>
        </div>
      )
    }

    const dataKey = yAxis && yAxis !== "count" ? yAxis : "count"

    switch (chartType) {
      case "bar":
        return (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xAxis} />
              <YAxis />
              <Tooltip />
              <Legend />
              {groupBy && groupBy !== "none" ? (
                // Multiple bars for grouped data
                data
                  .reduce((acc: string[], item) => {
                    const groupValue = String(item[groupBy])
                    if (!acc.includes(groupValue)) acc.push(groupValue)
                    return acc
                  }, [])
                  .slice(0, 5)
                  .map((group, index) => <Bar key={group} dataKey={group} fill={COLORS[index % COLORS.length]} />)
              ) : (
                <Bar dataKey={dataKey} fill={COLORS[0]} />
              )}
            </BarChart>
          </ResponsiveContainer>
        )

      case "line":
        return (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xAxis} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey={dataKey} stroke={COLORS[0]} strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        )

      case "pie":
        return (
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(1)}%)`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        )

      case "scatter":
        return (
          <ResponsiveContainer width="100%" height={400}>
            <ScatterChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xAxis} type="number" />
              <YAxis dataKey={yAxis} type="number" />
              <Tooltip />
              <Scatter fill={COLORS[0]} />
            </ScatterChart>
          </ResponsiveContainer>
        )

      default:
        return null
    }
  }

  return (
    <div className="space-y-6">
      {/* Chart Type Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            Tipo de Visualização
            <Button variant="outline" size="sm" onClick={refreshData} disabled={isLoading}>
              <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-4 gap-4">
            {[
              { type: "bar" as const, icon: BarChart3, label: "Barras" },
              { type: "line" as const, icon: LineChartIcon, label: "Linha" },
              { type: "pie" as const, icon: PieChartIcon, label: "Pizza" },
              { type: "scatter" as const, icon: ScatterIcon, label: "Dispersão" },
            ].map(({ type, icon: Icon, label }) => (
              <Button
                key={type}
                variant={chartType === type ? "default" : "outline"}
                className="h-20 flex flex-col gap-2"
                onClick={() => setChartType(type)}
              >
                <Icon className="w-6 h-6" />
                {label}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Chart Configuration */}
      <Card>
        <CardHeader>
          <CardTitle>Configuração do Gráfico</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium mb-2 block">
                Eixo X {chartType === "scatter" ? "(deve ser numérico)" : ""}
              </label>
              <Select value={xAxis} onValueChange={setXAxis}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione coluna X" />
                </SelectTrigger>
                <SelectContent>
                  {(chartType === "scatter" ? numericColumns : columns).map((col) => (
                    <SelectItem key={col} value={col}>
                      {col}
                      <Badge variant="outline" className="ml-2">
                        {numericColumns.includes(col) ? "Numérica" : "Categórica"}
                      </Badge>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {chartType !== "pie" && (
              <div>
                <label className="text-sm font-medium mb-2 block">Eixo Y</label>
                <Select value={yAxis} onValueChange={setYAxis}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione coluna Y" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="count">Contagem</SelectItem>
                    {numericColumns.map((col) => (
                      <SelectItem key={col} value={col}>
                        {col}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}

            {chartType === "pie" && (
              <div>
                <label className="text-sm font-medium mb-2 block">Valores</label>
                <Select value={yAxis} onValueChange={setYAxis}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione valores" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="count">Contagem</SelectItem>
                    {numericColumns.map((col) => (
                      <SelectItem key={col} value={col}>
                        {col}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}

            {chartType === "bar" && (
              <div>
                <label className="text-sm font-medium mb-2 block">Agrupar por</label>
                <Select value={groupBy} onValueChange={setGroupBy}>
                  <SelectTrigger>
                    <SelectValue placeholder="Opcional" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">Nenhum</SelectItem>
                    {categoricalColumns.map((col) => (
                      <SelectItem key={col} value={col}>
                        {col}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Chart Display */}
      <Card>
        <CardHeader>
          <CardTitle>Visualização</CardTitle>
          {chartData.length > 0 && <CardDescription>Mostrando {chartData.length} pontos de dados</CardDescription>}
        </CardHeader>
        <CardContent>{renderChart()}</CardContent>
      </Card>

      {/* Quick Stats */}
      {chartData.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Estatísticas Rápidas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold text-blue-800">Total de Pontos</h4>
                <p className="text-2xl font-bold text-blue-600">{chartData.length}</p>
              </div>

              {yAxis && yAxis !== "count" && numericColumns.includes(yAxis) && (
                <>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <h4 className="font-semibold text-green-800">Valor Máximo</h4>
                    <p className="text-2xl font-bold text-green-600">
                      {Math.max(...chartData.map((d) => Number(d[yAxis]) || 0)).toLocaleString()}
                    </p>
                  </div>

                  <div className="p-4 bg-purple-50 rounded-lg">
                    <h4 className="font-semibold text-purple-800">Média</h4>
                    <p className="text-2xl font-bold text-purple-600">
                      {(chartData.reduce((acc, d) => acc + (Number(d[yAxis]) || 0), 0) / chartData.length).toFixed(2)}
                    </p>
                  </div>
                </>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
