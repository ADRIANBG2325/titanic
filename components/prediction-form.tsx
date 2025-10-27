"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface PredictionResult {
  survived: boolean
  probability: number
  message: string
}

export function PredictionForm() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)

  const [formData, setFormData] = useState({
    pclass: "3",
    sex: "male",
    age: "30",
    sibsp: "0",
    parch: "0",
    fare: "15",
    embarked: "S",
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error("[v0] Error al hacer predicción:", error)
      setResult({
        survived: false,
        probability: 0,
        message: "Error al procesar la predicción. Por favor intenta de nuevo.",
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="p-6">
      <div className="mb-6">
        <h3 className="font-serif text-2xl font-bold text-foreground mb-2">Ingresa tus Datos de Pasajero</h3>
        <p className="text-sm text-muted-foreground">
          Completa el formulario para calcular tu probabilidad de supervivencia
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Clase de Ticket */}
        <div className="space-y-2">
          <Label htmlFor="pclass">Clase de Ticket</Label>
          <Select value={formData.pclass} onValueChange={(value) => setFormData({ ...formData, pclass: value })}>
            <SelectTrigger id="pclass">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1">Primera Clase (£870)</SelectItem>
              <SelectItem value="2">Segunda Clase (£21)</SelectItem>
              <SelectItem value="3">Tercera Clase (£7-8)</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Género */}
        <div className="space-y-2">
          <Label htmlFor="sex">Género</Label>
          <Select value={formData.sex} onValueChange={(value) => setFormData({ ...formData, sex: value })}>
            <SelectTrigger id="sex">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="male">Masculino</SelectItem>
              <SelectItem value="female">Femenino</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Edad */}
        <div className="space-y-2">
          <Label htmlFor="age">Edad (años)</Label>
          <Input
            id="age"
            type="number"
            min="0"
            max="100"
            value={formData.age}
            onChange={(e) => setFormData({ ...formData, age: e.target.value })}
            required
          />
        </div>

        {/* Hermanos/Cónyuges */}
        <div className="space-y-2">
          <Label htmlFor="sibsp">Hermanos/Cónyuges a Bordo</Label>
          <Input
            id="sibsp"
            type="number"
            min="0"
            max="10"
            value={formData.sibsp}
            onChange={(e) => setFormData({ ...formData, sibsp: e.target.value })}
            required
          />
        </div>

        {/* Padres/Hijos */}
        <div className="space-y-2">
          <Label htmlFor="parch">Padres/Hijos a Bordo</Label>
          <Input
            id="parch"
            type="number"
            min="0"
            max="10"
            value={formData.parch}
            onChange={(e) => setFormData({ ...formData, parch: e.target.value })}
            required
          />
        </div>

        {/* Tarifa */}
        <div className="space-y-2">
          <Label htmlFor="fare">Tarifa del Ticket (£)</Label>
          <Input
            id="fare"
            type="number"
            min="0"
            step="0.01"
            value={formData.fare}
            onChange={(e) => setFormData({ ...formData, fare: e.target.value })}
            required
          />
        </div>

        {/* Puerto de Embarque */}
        <div className="space-y-2">
          <Label htmlFor="embarked">Puerto de Embarque</Label>
          <Select value={formData.embarked} onValueChange={(value) => setFormData({ ...formData, embarked: value })}>
            <SelectTrigger id="embarked">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="S">Southampton</SelectItem>
              <SelectItem value="C">Cherbourg</SelectItem>
              <SelectItem value="Q">Queenstown</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Button type="submit" className="w-full" disabled={loading}>
          {loading ? "Calculando..." : "Predecir Supervivencia"}
        </Button>
      </form>

      {/* Resultado */}
      {result && (
        <div
          className={`mt-6 rounded-lg border-2 p-6 ${
            result.survived
              ? "border-green-500 bg-green-50 dark:bg-green-950"
              : "border-red-500 bg-red-50 dark:bg-red-950"
          }`}
        >
          <div className="text-center">
            <div className="mb-2 text-4xl">{result.survived ? "✓" : "✗"}</div>
            <h4
              className={`font-serif text-2xl font-bold mb-2 ${
                result.survived ? "text-green-700 dark:text-green-300" : "text-red-700 dark:text-red-300"
              }`}
            >
              {result.survived ? "¡Habrías Sobrevivido!" : "No Habrías Sobrevivido"}
            </h4>
            <p className="text-lg font-medium mb-2">
              Probabilidad de Supervivencia: {(result.probability * 100).toFixed(1)}%
            </p>
            <p className="text-sm text-muted-foreground">{result.message}</p>
          </div>
        </div>
      )}
    </Card>
  )
}
