import { Card } from "@/components/ui/card"

const facts = [
  {
    title: "Mujeres y Niños Primero",
    description: "74% de las mujeres sobrevivieron, comparado con solo 19% de los hombres.",
    stat: "74%",
  },
  {
    title: "La Clase Importaba",
    description:
      "Los pasajeros de primera clase tenían 3 veces más probabilidades de sobrevivir que los de tercera clase.",
    stat: "3x",
  },
  {
    title: "Botes Salvavidas Insuficientes",
    description: "El Titanic tenía capacidad para 2,224 personas pero solo 1,178 espacios en botes salvavidas.",
    stat: "1,178",
  },
  {
    title: "Temperatura del Agua",
    description: "El agua estaba a -2°C. La mayoría de las víctimas murieron por hipotermia en 15-30 minutos.",
    stat: "-2°C",
  },
  {
    title: "Tripulación",
    description: "885 miembros de la tripulación estaban a bordo. Solo 212 sobrevivieron.",
    stat: "24%",
  },
  {
    title: "El Hundimiento",
    description: "El barco se hundió en 2 horas y 40 minutos después de golpear el iceberg.",
    stat: "2h 40m",
  },
]

export function TitanicFacts() {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="font-serif text-2xl font-bold text-foreground mb-2">Datos Históricos del Titanic</h3>
        <p className="text-sm text-muted-foreground">
          Hechos fascinantes sobre el desastre más famoso de la historia marítima
        </p>
      </div>

      <div className="grid gap-4">
        {facts.map((fact, index) => (
          <Card key={index} className="p-4">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-accent">
                <span className="font-serif text-lg font-bold text-accent-foreground">{fact.stat}</span>
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-foreground mb-1">{fact.title}</h4>
                <p className="text-sm text-muted-foreground leading-relaxed">{fact.description}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <Card className="p-6 bg-accent">
        <h4 className="font-serif text-lg font-bold text-accent-foreground mb-3">
          Sobre el Modelo de Machine Learning
        </h4>
        <div className="space-y-2 text-sm text-muted-foreground">
          <p>
            <strong>Algoritmo:</strong> Regresión Logística
          </p>
          <p>
            <strong>Precisión:</strong> ~80% en datos de validación
          </p>
          <p>
            <strong>Features principales:</strong> Género, clase de ticket, edad, y tamaño de familia
          </p>
          <p>
            <strong>Dataset:</strong> 891 pasajeros con datos completos de supervivencia
          </p>
        </div>
      </Card>
    </div>
  )
}
