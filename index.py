import os
import json
import openai
import logging
import nltk
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.readers.schema.base import Document
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from base import WordLiftLoader
from llama_index.node_parser import SimpleNodeParser
from llama_index.text_splitter import TokenTextSplitter

# Set up the necessary configuration options
openai.api_key = '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'
os.environ["OPENAI_API_KEY"] = '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'
test_key = "ErzOMCZxLRKu7GhndfAValWizy5zNz0EKU1YCumfbKAWFu7E142oZlkv5l6XPfen"  # articles 3
default_page = 0
default_rows = 20

fields = "articles"

endpoint = "https://api.wordlift.io/graphql/"
headers = {
    "Authorization": f"Key {test_key}",
    "Content-Type": "application/json"
}

config_options = {
    "text_fields": ["body"],
    "metadata_fields": ["address"],
}
query = """
query {
	articles(rows: 10){
		title: string(name: "schema:headline")
		body: string(name: "wordpress:content")
		address: string(name: "schema:url")
	}
}"""

reader = WordLiftLoader(
    endpoint, headers, query, fields, config_options)

documents = reader.load_data()

with open('documents.json', 'w') as f:
    json.dump([doc.__doc__ for doc in documents], f, indent=4)
converted_doc = []
for doc in documents:
    converted_doc_id = json.dumps(doc.doc_id)
    converted_doc.append(Document(text=doc.text, doc_id=converted_doc_id,
                         embedding=doc.embedding, doc_hash=doc.hash, extra_info=doc.extra_info))
with open('converted_doc.json', 'w') as f:
    json.dump([doc.__dict__ for doc in converted_doc], f, indent=4)


index = VectorStoreIndex.from_documents(converted_doc)
query_engine = index.as_query_engine()

result = query_engine.query("How Does SEO Automation Work?")

print("=============> result: ", result)
print(result.get_formatted_sources())
