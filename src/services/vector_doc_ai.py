import asyncio
import logging
import os
from pathlib import Path

from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAIChat
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# BASE_DIR = Path(__file__).parent.parent.resolve().parent
# filename = 'stepik-certificate(2).pdf'
#
# path_to_file = str(BASE_DIR / "uploaded_files" / filename)
#
#
# print(path_to_file)


async def vector_func(path_file, question):
    loader = PyPDFLoader(path_file)
    documents = loader.load()
    print(f"vector_func{documents}")
    vectordb = Chroma.from_documents(
        documents,
        embedding=OpenAIEmbeddings(),
        persist_directory='./data'
    )
    vectordb.persist()

    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAIChat(),
        retriever=vectordb.as_retriever(search_kwargs={'k': 7}),
        return_source_documents=True
    )

    # we can now execute queries against our Q&A chain
    result = qa_chain({'query': question})
    print(f'result query: {result}')
    print(result['result'])

    return f'I: {question}\nFreeDoc-AI: {result["result"]}'

# while True:
#     a = input(f'>>>')
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(vector_func(path_to_file, a))
#     if a == '0':
#         break
