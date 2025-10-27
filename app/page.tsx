import { PredictionForm } from "@/components/prediction-form"
import { TitanicFacts } from "@/components/titanic-facts"
import { StatsDisplay } from "@/components/stats-display"

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-serif text-3xl font-bold text-foreground">RMS Titanic</h1>
              <p className="text-sm text-muted-foreground">Análisis de Supervivencia con Machine Learning</p>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium text-foreground">15 de Abril, 1912</p>
              <p className="text-xs text-muted-foreground">02:20 AM</p>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-12">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="font-serif text-4xl font-bold text-foreground text-balance mb-4">
              ¿Habrías Sobrevivido al Hundimiento del Titanic?
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Utilizando Random Forest y datos históricos de los 2,224 pasajeros, este modelo predice tus probabilidades
              de supervivencia basándose en características como clase de ticket, género, edad y ubicación en el barco.
            </p>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="border-b border-border">
        <div className="container mx-auto px-4 py-12">
          <StatsDisplay />
        </div>
      </section>

      {/* Main Content */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          <div className="grid gap-8 lg:grid-cols-2">
            {/* Prediction Form */}
            <div>
              <PredictionForm />
            </div>

            {/* Facts Sidebar */}
            <div>
              <TitanicFacts />
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-card">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-sm text-muted-foreground">
            <p>Proyecto de Machine Learning - Dataset del Titanic</p>
            <p className="mt-2">Modelo: Random Forest Classifier | Precisión: ~82-85%</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
