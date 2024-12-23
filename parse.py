from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import asyncio

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3.2")


def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        print(f"Parsing batch: {i} of {len(dom_chunks)}")
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        parsed_results.append(response)

    print('Done!')
    return "\n".join(parsed_results)

async def async_parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    async def process_chunk(chunk, idx):
        print(f"Parsing batch: {idx} of {len(dom_chunks)}")
        response = await chain.ainvoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        return response

    tasks = [
        process_chunk(chunk, idx) for idx, chunk in enumerate(dom_chunks, start=1)
        ]
    parsed_results = await asyncio.gather(*tasks)

    print('Done!')
    return "\n".join(parsed_results)
