# Proyecto LangGraph

Este proyecto demuestra la implementación de agentes de IA usando LangGraph, un framework para construir aplicaciones basadas en flujos de trabajo con LLMs.

## ¿Qué es LangGraph?

LangGraph es un framework desarrollado por LangChain que permite crear sistemas que combinan múltiples modelos de lenguaje y herramientas en secuencias lógicas. Su principal característica es la capacidad de definir "estados" y "transiciones" entre ellos, facilitando la creación de agentes autónomos que pueden tomar decisiones complejas.

## Repositorio Oficial

El repositorio oficial de LangGraph se encuentra en:
[GitHub - langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/tree/main)

## Instalación

### Instalación para desarrollo

Para instalar LangGraph en modo desarrollo:

```bash
pip install langgraph
pip install -U "langgraph-cli[inmem]"  # Para debugging
```

Si estás usando Google Vertex AI, necesitarás instalar las siguientes dependencias:

```bash
pip install langgraph
pip install langchain_google_vertexai
pip install langgraph-cli
pip install python-dotenv
pip install google-cloud-aiplatform
```

## Estructura del Proyecto

El proyecto requiere los siguientes archivos:

### 1. langraph.json

Este archivo es necesario para manejar el entorno de desarrollo y despliegue:

```json
{
  "dependencies": ["."],
  "graphs":{
    "bushido3":"./agent.py:graph",
    "bushido4":"./agent_with_tools.py:graph"
  },
  "python_version": "3.11"
}
```

Donde:
- **dependencies**: Indica las dependencias a instalar
- **graphs**: Define los agentes disponibles (clave: nombre del agente, valor: ruta al archivo y variable)
- **python_version**: Versión de Python recomendada (se sugiere 3.11 por escalabilidad)

### 2. requirements.txt

```
langgraph
langchain_google_vertexai
langgraph-cli
python-dotenv
google-cloud-aiplatform
```

### 3. app.py (o como prefieras nombrarlo)

Este archivo contiene la implementación del agente:

```python
from typing import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_google_vertexai import ChatVertexAI

# Definimos la estructura del estado
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Configuramos el modelo de lenguaje
llm = ChatVertexAI(model="gemini-2.0-flash-001", temperature=0)

# Función del chatbot
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Construcción del grafo
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compilación del grafo
graph = graph_builder.compile()
```

## Explicación del Código

1. **Estado del Agente**:
   - Definimos una clase `State` que contiene la estructura de datos que fluirá por el grafo
   - La clave `messages` contendrá una lista de mensajes en formato de diccionario

2. **Modelo de Lenguaje**:
   - Configuramos el LLM que vamos a usar (en este caso Gemini de VertexAI)
   - Puedes cambiar el modelo según tus necesidades

3. **Nodo del Chatbot**:
   - La función `chatbot` recibe el estado actual y devuelve un nuevo estado
   - Utiliza el LLM para procesar los mensajes y generar una respuesta

4. **Construcción del Grafo**:
   - `StateGraph(State)` crea un constructor de grafo que maneja datos con la estructura definida
   - `add_node` añade un nodo al grafo con un nombre y una función asociada
   - `add_edge` define las conexiones entre nodos (START → chatbot → END)
   - Finalmente, `compile()` produce el grafo ejecutable

## Ejecución

Para ejecutar el agente en modo desarrollo:

1. Asegúrate de estar en la carpeta del proyecto
2. Ejecuta:
   ```bash
   langgraph dev
   ```

Esto abrirá una interfaz web donde podrás probar tu agente y ver el flujo de ejecución.

## Características

- **Debuging visual**: La interfaz permite ver por dónde está fluyendo el agente
- **Memoria preconstruida**: El entorno de cloud proporciona funcionalidades de memoria
- **Despliegue sencillo**: Se puede desplegar en Langgraph Cloud

## Notas Importantes

- Es recomendable revisar la documentación oficial para explorar todas las posibilidades de configuración
- No se recomienda usar las últimas versiones de Python por cuestiones de escalabilidad
- Para otros proveedores de LLM, consulta la documentación de LangChain

## Enlaces Útiles

- [Documentación del CLI de LangGraph](https://langchain-ai.github.io/langgraph/cloud/reference/cli/)
- [Documentación oficial de LangGraph](https://langchain-ai.github.io/langgraph/)
