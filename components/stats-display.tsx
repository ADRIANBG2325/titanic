import { Card } from "@/components/ui/card"

const stats = [
  {
    label: "Total de Pasajeros",
    value: "2,224",
    description: "A bordo del RMS Titanic",
  },
  {
    label: "Sobrevivientes",
    value: "706",
    description: "32% de los pasajeros",
  },
  {
    label: "Víctimas",
    value: "1,518",
    description: "68% de los pasajeros",
  },
  {
    label: "Botes Salvavidas",
    value: "20",
    description: "Capacidad para 1,178 personas",
  },
]

export function StatsDisplay() {
  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat, index) => (
        <Card key={index} className="p-6 text-center">
          <div className="mb-2">
            <div className="font-serif text-3xl font-bold text-foreground">{stat.value}</div>
          </div>
          <div className="text-sm font-medium text-foreground mb-1">{stat.label}</div>
          <div className="text-xs text-muted-foreground">{stat.description}</div>
        </Card>
      ))}
    </div>
  )
}
