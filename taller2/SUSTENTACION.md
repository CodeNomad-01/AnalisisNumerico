# Sustentación del Taller 2 — Análisis Numérico

Este documento explica **por qué** y **para qué** se hizo cada parte del taller, como si no tuvieras experiencia previa en matemáticas aplicadas. Puedes leerlo junto con el notebook `Taller_2.ipynb`.

---

## ¿De qué trata el taller en general?

Tienes **datos medidos en un experimento** (pesos, longitudes, poblaciones, alturas…) y quieres:

1. **Ver** qué dicen esos datos (gráficas).
2. **Predecir** valores que no mediste (por ejemplo, peso a 60 cm de longitud).
3. **Simular** procesos que cambian en el tiempo (un salto, dos poblaciones que compiten).

Para eso usamos **métodos numéricos**: recetas en computadora que aproximan respuestas cuando no hay una fórmula simple o cuando la fórmula exacta es difícil de usar.

Los archivos `modelos.py`, `Ceros.py`, `ecuaciones.py` y `sel.py` son **cajas de herramientas** con esas recetas. El notebook solo las llama con tus datos.

---

## Palabras clave (en una frase)

| Término | Significado simple |
|--------|-------------------|
| **Interpolación** | Dibujar una curva que **pasa exactamente** por todos los puntos medidos. |
| **Ajuste / regresión** | Dibujar una curva que **sigue la tendencia** aunque no pase por cada punto. |
| **Mínimos cuadrados** | Elegir la recta (o modelo) que **comete el menor error global** respecto a los datos. |
| **Extrapolar** | Predecir **fuera** del rango donde mediste (más arriesgado que interpolar). |
| **EDO** | Ecuación que dice cómo cambia algo **con el tiempo** (velocidad, poblaciones…). |
| **Euler / RK4** | Formas de avanzar paso a paso en el tiempo para simular una EDO. |
| **Bisección** | Buscar un valor donde una función **se hace cero** (cambio de signo). |
| **R²** | Número entre 0 y 1: qué tan bien el modelo **explica** los datos (más cerca de 1, mejor). |

---

# Ejercicio 1 — Platija: longitud vs peso

**Problema de fondo:** A más longitud del pez, más peso. Queremos entender esa relación y estimar el peso si el pez mide 60 cm (aunque en la tabla solo hay datos hasta ~49.5 cm).

---

## 1-a) Gráfico de datos

**Qué se hizo:** Se graficaron puntos: eje horizontal = longitud (cm), eje vertical = peso (g).

**Para qué:** Antes de calcular nada, hay que **ver** si la relación parece recta, curva suave o algo raro. Un gráfico responde en segundos: “¿crece rápido al principio y luego se estabiliza?”.

**Por qué solo gráfica:** Es el paso más barato y el que evita errores tontos (datos mal copiados, unidades equivocadas).

---

## 1-b) Polinomio de Lagrange (pasa por todos los puntos)

**Qué se hizo:**

- Se construyó un polinomio con `lagrange` que **pasa exactamente** por los 27 puntos.
- Se evaluó en L = 60 cm para obtener un peso estimado.

**Para qué:** Cumplir el enunciado: “un polinomio que pase por cada dato”. También sirve de **contraste** con el método del ítem c.

**Por qué Lagrange:** Con n puntos, existe un único polinomio de grado n−1 que los une todos. Lagrange es una forma de construirlo.

**Problema que se descubre (y por eso importa la sustentación):** Fuera del rango medido (extrapolar a 60 cm), el polinomio puede dar **números enormes o sin sentido**. Eso se llama fenómeno de **Runge**: encaja perfecto dentro, pero se vuelve inestable fuera. **Conclusión del ítem b:** el modelo **no es coherente** para predecir 60 cm, aunque sea perfecto dentro del intervalo.

---

## 1-c) Modelo de ajuste (mínimos cuadrados, ley de potencia)

**Qué se hizo (en orden):**

1. **`escalas`** — Muchas gráficas probando transformar x e y (log, cuadrados, etc.).
2. **`coeficiente_determinacion`** — Se comparó qué tan bien encajan tres ideas: recta simple, usar L³, o log-log.
3. **`minimos_cuadrados`** en log-log — Se ajustó una recta entre log(longitud) y log(peso), y se pasó a la forma **w = a · L^b**.

**Para qué:** El enunciado pide un modelo de **tendencia**, no uno que pase por cada punto. Ese modelo debe poder estimar 60 cm de forma **razonable**.

**Por qué log-log:** En biología, peso vs longitud suele comportarse como “si duplicas la longitud, el peso se multiplica por algo” (ley de potencia). En papel log-log, una potencia se ve como **línea recta**, y la recta es fácil de ajustar con mínimos cuadrados.

**Por qué R²:** Para **elegir con número** entre “recta”, “L³” o “potencia”, no solo a ojo. El log-log dio el R² más alto → mejor explicación de los datos.

**Por qué w = a·L^b con b ≈ 3:** Un exponente cerca de 3 es plausible (el peso escala algo como el volumen). La predicción en 60 cm (~1900 g) es del mismo orden que la curva, no un número astronómico como en Lagrange.

**Conclusión del ítem c:** Modelo **coherente, pertinente y más adecuado** para extrapolar un poco, siempre diciendo que 60 cm está **fuera** de lo medido.

---

## 1-d) Gráficas separadas de a, b y c

**Qué se hizo:** Tres figuras: solo datos; datos + polinomio Lagrange hasta 60 cm; datos + curva de potencia hasta 60 cm.

**Para qué:** **Mostrar** lo que los números ya dijeron: el polinomio se dispara; la curva de potencia sigue la nube de puntos de forma suave.

**Por qué línea vertical en 60:** Marca visualmente “aquí estamos extrapolando”.

---

# Ejercicio 2 — Salto vertical de la bailarina

**Problema de fondo:** La gravedad frena la subida. Hay una ecuación que relaciona velocidad y tiempo. Queremos la **altura máxima** del salto y comparar métodos numéricos con la respuesta exacta.

---

## 2-a) y 2-b) Euler, RK4 y altura máxima exacta

**Qué se hizo:**

- Se escribió el problema como **sistema de dos ecuaciones** (altura y velocidad).
- Se simuló con **`Euler`** y **`Rk4`** (`ecuaciones.py`).
- Se calculó la altura máxima teórica: **H = g·T²/8**.

**Para qué:**

- **Euler:** método simple, didáctico; suele tener más error.
- **RK4:** método más preciso con el mismo paso de tiempo.
- **Exacta:** referencia para saber si la computadora “va bien”.

**Por qué convertir a sistema de primer orden:** Las herramientas del curso avanzan en el tiempo con variables (y, v), no con derivadas sueltas.

**Conclusión típica:** RK4 se acerca mucho más a H exacta que Euler con el mismo paso.

---

## 2-c) Error con distintos pasos h

**Qué se hizo:** Se repitió la simulación con distintos números de pasos (n = 5, 10, 20…) y se midió el error en la altura máxima.

**Para qué:** Ver **cómo mejora** la solución al hacer el paso más pequeño (más cálculos, más precisión).

**Por qué importa:** En la práctica siempre hay que elegir: ¿paso grande y rápido, o paso chico y más exacto? Euler mejora ~al doble de pasos; RK4 mejora mucho más rápido.

---

## 2-d) Gráficas altura y velocidad vs tiempo

**Qué se hizo:** Comparar curva exacta vs Euler vs RK4 en dos paneles: altura y velocidad.

**Para qué:** Entender el **movimiento**: sube, velocidad baja a cero en el punto más alto, baja acelerando. Las gráficas muestran si el método numérico “sigue” esa forma.

**Por qué convertir pulgadas a pies en un eje:** Solo para leer mejor las mismas unidades del enunciado.

---

# Ejercicio 3 — Cangrejo violinista: cuerpo vs tenaza

**Problema de fondo:** El cuerpo (x) y la tenaza (y) no crecen igual. Hay un umbral de “madurez sexual” (~1100 mg de cuerpo) y hay que comparar modelos simples vs modelos en dos fases.

---

## 3-a) Polinomio interpolante y umbral de madurez

**Qué se hizo:**

- Polinomio de Lagrange sobre todos los puntos (cuerpo vs tenaza).
- Se buscó **x\*** tal que **x + peso_tenaza(x) = 1100** usando **bisección** (`Ceros.py`).

**Para qué:**

- Tener un polinomio que reproduce los datos (como en ejercicio 1-b).
- Responder: “¿a qué peso de cuerpo la suma cuerpo+tenaza supera 1100 mg?” — criterio del enunciado de madurez.

**Por qué bisección:** La función “x + P(x) − 1100” cambia de signo en un intervalo; bisección encuentra el cero de forma segura sin derivadas complicadas.

**Gráfica datos vs modelo:** Ver si el polinomio es razonable **dentro** del rango medido.

---

## 3-b) Modelo en dos fases (joven / maduro)

**Qué se hizo:**

- Se partieron los datos en **antes** y **después** del umbral 1100 mg (usando x\* del ítem a).
- En cada grupo: ajuste **log-log** → **y = c · x^a** (dos leyes de potencia distintas).

**Para qué:** La biología sugiere que el crecimiento **no es igual** en juventud y en adultez. Un solo polinomio o una sola recta mezcla comportamientos distintos.

**Por qué dos modelos:** Cada fase tiene su propia “pendiente” en escala log-log (exponente **a**).

---

## 3-c) Alométrico vs isométrico

**Qué se hizo:** Explicación con texto (no mucho código): comparar **a = 1** (isométrico: partes crecen igual) vs **a ≠ 1** (alométrico: una parte crece más rápido en proporción).

**Para qué:** Conectar el taller con la **idea biológica** del enunciado, no solo con números.

**En simple:** Si a = 1, la tenaza y el cuerpo mantienen la misma proporción. Si a > 1, la tenaza gana proporción al crecer el cuerpo.

---

## 3-d) Comparar exponentes a por fase

**Qué se hizo:** Se imprimieron **a_joven** y **a_maduro** (típicamente ambos > 1, con a_joven mayor).

**Para qué:** Responder con evidencia numérica la pregunta de alometría por etapa.

**Interpretación:** En ambas fases la tenaza crece **más rápido en proporción** que el cuerpo; pero en la fase joven ese efecto es **más fuerte**.

---

## 3-e) ¿En qué etapa crece más la tenaza en proporción?

**Qué se hizo:** Comparar a_joven y a_maduro; concluir que **fase joven**.

**Para qué:** Pregunta directa del taller: el exponente **a** mide justamente la “tasa relativa” de crecimiento de la tenaza respecto al cuerpo.

---

## 3-f) Estimar tenaza para x = 500 mg y x = 2000 mg

**Qué se hizo:** Función que elige modelo joven o maduro según si x está antes o después de x\*, y evalúa y.

**Para qué:** Aplicar el modelo de dos fases a **casos concretos** del enunciado.

**Lógica:** 500 mg → aún “joven”; 2000 mg → ya en rama “madura”. Los valores salen del orden de magnitud de los datos, no absurdos.

---

## 3-g) Predicción para x = 3000 mg

**Qué se hizo:** Comparar predicción del **polinomio Lagrange** vs **modelo de dos fases**.

**Para qué:** Mostrar otra vez la lección del ejercicio 1: interpolación alta fuera del rango → **catastrófico**; modelo de tendencia por fases → **usable con cautela**.

**Conclusión:** Lagrange puede dar pesos negativos o gigantes; el modelo de dos fases da algo interpretable (y/x razonable).

---

# Ejercicio 4 — Lotka-Volterra: compradores y vendedores

**Problema de fondo:** Dos poblaciones (compradores x, vendedores v) que crecen, se limitan entre sí y compiten. Las ecuaciones dicen cómo cambian x y v en el tiempo. No hay solución con lápiz y papel fácil → se **simula** con Euler.

---

## Idea común a los cuatro casos (a, b, c, d)

**Qué se hizo siempre:**

- Definir las ecuaciones del modelo con unos parámetros (a, b, m, c, d, n).
- Integrar en el tiempo con **`Euler`** desde las poblaciones iniciales.
- Graficar **x(t)**, **v(t)** y a veces **v vs x** (retrato de fases).

**Para qué:** Ver si las dos poblaciones **conviven**, si una **muere**, si hay **oscilaciones**, etc., según cambian los parámetros.

**Por qué Euler aquí:** El taller pide simular el sistema; Euler es el método base del curso para EDOs. En el caso c se usa paso pequeño porque la dinámica es muy rápida.

---

## 4-a) Parámetros “suaves” (b y n pequeños)

**Qué se buscaba:** Comportamiento donde compradores y vendedores pueden **coexistir** en el tiempo (no se extingue uno de golpe).

**Para qué:** Caso de referencia “equilibrado” del modelo de competencia.

---

## 4-b) b grande (mucha competencia entre compradores)

**Qué cambia:** b = 0.2 hace que los compradores se **frenen mucho entre sí**.

**Para qué:** Ver cómo un solo parámetro puede hacer que una población **colapse** rápido.

**Interpretación simple:** “Demasiada competencia interna” → pocos compradores sobreviven.

---

## 4-c) n muy grande (compradores aplastan vendedores)

**Qué cambia:** n = 4.2 → los compradores afectan **muchísimo** a los vendedores.

**Para qué:** Caso extremo: los vendedores caen casi a cero; el sistema va hacia dominancia de compradores.

**Por qué paso h pequeño:** La curva cambia muy rápido; si el paso es grande, Euler “se pierde”.

---

## 4-d) Parámetros con equilibrio inestable

**Qué se hizo:** Simular y comentar que existe un punto donde ambas poblaciones podrían quedarse quietas, pero es **inestable** (cualquier perturbación aleja el sistema).

**Para qué:** Entender que “equilibrio en papel” no siempre significa “equilibrio en la realidad”. Las trayectorias pueden converger a un lado u otro según condiciones iniciales.

**Gráfica v vs x:** Muestra el “camino” conjunto de las dos poblaciones, no solo cada una contra el tiempo.

---

# Resumen: ¿qué método usar y cuándo?

| Situación | Herramienta del taller | Idea en una frase |
|-----------|------------------------|-------------------|
| Ver datos | Gráfica | Siempre primero. |
| Pasar exactamente por todos los puntos | Lagrange | Bueno **dentro** del rango; peligroso **fuera**. |
| Capturar tendencia y predecir | Mínimos cuadrados (+ transformaciones) | Curva simple que generaliza mejor. |
| Elegir mejor transformación | `escalas` + R² | Comparar antes de decidir. |
| Buscar un valor que cumple una condición | Bisección | “¿Dónde se cumple x + f(x) = 1100?” |
| Cambio en el tiempo (física, poblaciones) | Euler / RK4 | Simular paso a paso. |

---

# Cómo defender el taller en oral o por escrito (frases útiles)

1. **“Primero graficamos”** — demuestra que no se calculó a ciegas.
2. **“Probamos dos filosofías”** — interpolación exacta (1-b) vs ajuste de tendencia (1-c).
3. **“Elegimos log-log porque…”** — la biología sugiere potencias y el R² lo respaldó.
4. **“Extrapolar es arriesgado”** — por eso Lagrange falla y el modelo de potencia o dos fases se prefiere con cautela.
5. **“Euler vs RK4”** — no es solo calcular, es comparar calidad del método.
6. **“Dos fases en el cangrejo”** — porque un solo modelo mezcla etapas de vida distintas.

---

*Documento de apoyo al Taller 2. No reemplaza el notebook ni las definiciones formales del curso; sirve para entender el sentido de cada paso.*
