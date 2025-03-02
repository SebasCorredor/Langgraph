from typing import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END

''' 
Definimos el estado de los datos que van a fluir por el grafo
en este caso un diccionario con una clave llamada messages que 
contendra una lista de mensajes (que a su vez son diccionarios) con la forma 


state = {
    "messages": [
        {
            "role": "user",
            "content": "Hola, ¿cómo estás?"
        },
        {
            "role": "assistant",
            "content": "Estoy bien, ¿en qué puedo ayudarte?"
        },
        {
            "role": "user",
            "content": "Explícame cómo funciona LangGraph"
        }
    ]
}

''' 

class State(TypedDict):
    messages: Annotated[list, add_messages]


''' 
Cuando ejecutas esta línea:

Creas un nuevo constructor de grafo (un objeto StateGraph)
Le dices a este constructor que los datos que fluirán por el grafo tendrán la forma definida en la clase State
El constructor ahora sabe que debe esperar un diccionario con una clave messages que contendrá una lista

Es como preparar el lienzo antes de empezar a dibujar.
'''

graph_builder = StateGraph(State)


''' 
Definimos el LLM que vamos a usar en nuestro caso Gemini de VertexAI

Aqui usamos langchain para definir el modelo que vamos a usar

para cada LLM se importa de diferente manera en nuestro caso usamos ChatVertexAI

from langchain_google_vertexai import ChatVertexAI

''' 
from langchain_google_vertexai import ChatVertexAI
llm = ChatVertexAI(model="gemini-2.0-flash-001",temperature=0)


''' 
La línea def chatbot(state: State): está definiendo una función llamada "chatbot" que espera recibir un parámetro llamado "state".
La parte state: State es una "anotación de tipo" en Python, y hace lo siguiente:

state es el nombre del parámetro que recibirá la función
Los dos puntos : indican que estamos especificando el tipo de este parámetro
State (que definimos anteriormente como una TypedDict) indica que el parámetro debe tener la estructura especificada en la clase State

Es como poner una etiqueta en una caja que dice: "Esta función espera recibir una caja (state) que debe tener exactamente la forma descrita en el plano State".

'''

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


'''
Creamos nuestro primer todo (primer nuestro tercero de langgraph)
START Y END vienen por defecto 

"chatbot" - Este es el nombre o etiqueta que le estás dando al nodo. 
Es como ponerle un cartel a una estación de trabajo para identificarla. 
Cuando quieras referirte a este nodo más adelante (por ejemplo, para conectarlo con otros), usarás este nombre.

chatbot - Esta es la función que definiste anteriormente. Le estás diciendo al grafo: 
"Cuando el flujo llegue a este nodo, ejecuta esta función". Es la tarea específica que se realizará en esta estación.
'''

graph_builder.add_node("chatbot", chatbot)


''' 
START - Este es un nodo especial predefinido en LangGraph que representa el punto de inicio del flujo. Es como la puerta de entrada a tu diagrama.
'chatbot' - Este es el nombre del nodo al que quieres conectar el inicio. Debe ser un nodo que ya hayas añadido con add_node().
'''

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

''' 
La diferencia entre graph_builder y graph es importante:

graph_builder es la herramienta de diseño (el plano)
graph es el producto final listo para usar (la fábrica construida)
'''

graph = graph_builder.compile()