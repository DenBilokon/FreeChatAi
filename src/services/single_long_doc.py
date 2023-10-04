import os
from pathlib import Path

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI


from src.conf.config import settings

BASE_DIR = Path(__file__).parent.parent.resolve().parent
filename = 'stepik-certificate(2).pdf'

path_to_file = str(BASE_DIR / "uploaded_files" / filename)


print(path_to_file)

# loader = PyPDFLoader(path_to_file)
# documents = loader.load()
# print(type(documents))
#
# # we split the data into chunks of 1,000 characters, with an overlap
# # of 200 characters between the chunks, which helps to give better results
# # and contain the context of the information between chunks
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# documents = text_splitter.split_documents(documents)
# print(type(documents))
# print(documents)
# # we create our vectorDB, using the OpenAIEmbeddings tranformer to create
# # embeddings from our text chunks. We set all the db information to be stored
# # inside the ./data directory, so it doesn't clutter up our source files
# vectordb = Chroma.from_documents(
#   documents,
#   embedding=OpenAIEmbeddings(),
#   persist_directory='./data'
# )
# vectordb.persist()
#
#
# qa_chain = RetrievalQA.from_chain_type(
#     llm=OpenAI(),
#     retriever=vectordb.as_retriever(search_kwargs={'k': 7}),
#     return_source_documents=True
# )
# while True:
#     question = input(f'>>> ')
#     # we can now execute queries against our Q&A chain
#     result = qa_chain({'query': question})
#     # print(result['result'])
#     # print(result)
#     if question == '0':
#         break

loader = PyPDFLoader(path_to_file)
documents = loader.load()
print(f"vector_func{documents}")
vectordb = Chroma.from_documents(
  documents,
  embedding=OpenAIEmbeddings(),
  persist_directory='./data'
)
vectordb.persist()

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=vectordb.as_retriever(search_kwargs={'k': 7}),
    return_source_documents=True
)


while True:
    question = input(f'>>> ')
    # we can now execute queries against our Q&A chain
    result = qa_chain({'query': question})
    print(result['result'])
    print(result)
    if question == '0':
        break
