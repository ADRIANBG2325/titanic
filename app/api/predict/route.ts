import { type NextRequest, NextResponse } from "next/server"

const DJANGO_API_URL = process.env.DJANGO_API_URL || "http://localhost:8000"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { pclass, sex, age, sibsp, parch, fare, embarked, name, ticket, cabin } = body

    try {
      const response = await fetch(`${DJANGO_API_URL}/api/predict/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          pclass: Number.parseInt(pclass),
          sex: sex,
          age: Number.parseFloat(age),
          sibsp: Number.parseInt(sibsp),
          parch: Number.parseInt(parch),
          fare: Number.parseFloat(fare),
          embarked: embarked,
          name: name || "",
          ticket: ticket || "",
          cabin: cabin || "",
        }),
      })

      if (response.ok) {
        const data = await response.json()
        console.log("[v0] Usando modelo de Django:", data.model_type)

        return NextResponse.json({
          survived: data.survived,
          probability: data.probability,
          message: data.survived
            ? `Tus probabilidades de supervivencia son ${data.survival_chance.toLowerCase()}: ${(data.probability * 100).toFixed(1)}%`
            : `Tus probabilidades de supervivencia eran ${data.survival_chance.toLowerCase()}: ${(data.probability * 100).toFixed(1)}%`,
          model_type: data.model_type,
          model_accuracy: data.model_accuracy,
        })
      }
    } catch (error) {
      console.log("[v0] Servidor Django no disponible, usando modelo fallback")
    }

    const sexNumeric = sex === "male" ? 1 : 0
    const ageNumeric = Number.parseFloat(age)
    const sibspNumeric = Number.parseInt(sibsp)
    const parchNumeric = Number.parseInt(parch)
    const fareNumeric = Number.parseFloat(fare)
    const pclassNumeric = Number.parseInt(pclass)

    const embarkedS = embarked === "S" ? 1 : 0
    const embarkedC = embarked === "C" ? 1 : 0
    const embarkedQ = embarked === "Q" ? 1 : 0

    const familySize = sibspNumeric + parchNumeric + 1
    const isAlone = familySize === 1 ? 1 : 0

    const coefficients = {
      intercept: 0.5,
      pclass: -1.2,
      sex: -2.5,
      age: -0.01,
      sibsp: -0.3,
      parch: -0.1,
      fare: 0.002,
      embarkedS: -0.3,
      embarkedC: 0.5,
      embarkedQ: -0.2,
      familySize: -0.2,
      isAlone: 0.1,
    }

    const logit =
      coefficients.intercept +
      coefficients.pclass * pclassNumeric +
      coefficients.sex * sexNumeric +
      coefficients.age * ageNumeric +
      coefficients.sibsp * sibspNumeric +
      coefficients.parch * parchNumeric +
      coefficients.fare * fareNumeric +
      coefficients.embarkedS * embarkedS +
      coefficients.embarkedC * embarkedC +
      coefficients.embarkedQ * embarkedQ +
      coefficients.familySize * familySize +
      coefficients.isAlone * isAlone

    const probability = 1 / (1 + Math.exp(-logit))
    const survived = probability > 0.5

    let message = ""
    if (survived) {
      if (probability > 0.8) {
        message = "Tus características te daban excelentes probabilidades de supervivencia."
      } else if (probability > 0.65) {
        message = "Tenías buenas probabilidades de conseguir un lugar en un bote salvavidas."
      } else {
        message = "Tus probabilidades eran moderadas, pero habrías tenido una oportunidad."
      }
    } else {
      if (probability < 0.2) {
        message = "Desafortunadamente, tus características indicaban muy bajas probabilidades de supervivencia."
      } else if (probability < 0.35) {
        message = "Las probabilidades estaban en tu contra, pero algunos con características similares sobrevivieron."
      } else {
        message = "Era una situación difícil con probabilidades casi iguales."
      }
    }

    return NextResponse.json({
      survived,
      probability,
      message,
      model_type: "fallback (JavaScript)",
    })
  } catch (error) {
    console.error("[v0] Error en predicción:", error)
    return NextResponse.json({ error: "Error al procesar la predicción" }, { status: 500 })
  }
}
