from typing import List

from langchain.prompts import PromptTemplate


binary_prompt_str = """
Analiza el siguiente artículo y determina si la noticia está relacionada con la sequía climática.
Texto:
{text}
Por ejemplo, si el artículo está relacionado con la sequía climática, responde únicamente la palabra "True" y si no lo está, responde "False". No añadas ningún signo de puntuación ni proporciones ninguna explicación adicional. Sólo True/False.
"""

impact_prompt_str = """
Analiza el siguiente artículo relacionado con la sequía climática. Determina si esta noticia menciona un impacto de la sequía en %s.
Texto:
{text}
Por ejemplo, si el artículo menciona un impacto en %s, responde únicamente la palabra "True" y si no lo está, responde "False". No añadas ningún signo de puntuación ni proporciones ninguna explicación adicional. Sólo True/False.
"""


def get_binary_prompt() -> PromptTemplate:
    prompt = PromptTemplate(template=binary_prompt_str, input_variables=["text"])
    return prompt


def get_impact_prompt(impact: str) -> PromptTemplate:
    impact_prompt_str % (impact, impact)
    prompt = PromptTemplate(template=impact_prompt_str, input_variables=["text"])
    return prompt
