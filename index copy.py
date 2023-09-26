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
# test_key = "nCemGMTrPM8bZpmC3jyze4gbAJJ6cmO7daualXlkyvU53ciuMeHr0AcKsB8Xva4c"
# test_key = "B8X6lDceXhDO5aVg86npbFavLcQtnNhII35GolV8HlDdY5Tj9jMvTViUBlotsXUc"  # articles 1
# test_key = "UANbeZQ2y06QPv9P7aKFujzPyi8hd79acaYLXPhl1FE18kAUUnL3BBmzJTojLgvM"  # articles 2
# test_key = "PZYdfvYo0NjH6juRrwCnV7YohszyVt0tt9UBKu4R1HwIMuqyI3LZVWmqvLouuzjv"  # articles 3
test_key = "ErzOMCZxLRKu7GhndfAValWizy5zNz0EKU1YCumfbKAWFu7E142oZlkv5l6XPfen"  # articles 3
# test_key = "lcG14E9wn0aNNp2whaRhcsbOGrYYJxLOhjGG4Pb2YEJZD7XCik5086cVhqwj7eCc"  # product
# test_key = "nCemGMTrPM8bZpmC3jyze4gbAJJ6cmO7daualXlkyvU53ciuMeHr0AcKsB8Xva4c"  # faq
default_page = 0
default_rows = 20

fields = "articles"

endpoint = "https://api.wordlift.io/graphql/"
headers = {
    "Authorization": f"Key {test_key}",
    "Content-Type": "application/json"
}

config_options = {
    "text_fields": ["headlines", "body"],
    "metadata_fields": ["url"],
}
query = """
query {
	articles(rows: 10){
		title: string(name: "schema:headline")
		body: string(name: "wordpress:content")
		address: string(name: "schema:url")
	}
}"""

# query = """
# query {
# 	entities(query: {
#         descriptionConstraint: {exists: {exists: true, excludeEmpty: true}},
# 		wordpressTitleConstraint: {exists: {exists: true, excludeEmpty: true}}
#     }) {
# 		headlines: string(name: "wordpress:title")
# 		description: string(name: "schema:description")
# 		url: string(name: "wordpress:permalink")
# 		body: string(name: "wordpress:content")
# 	}
# }"""
# query = """
# query {
#   articles(page: 0, rows: 25) {
#     id: iri
#     title: string(name: "schema:headline")
#     date: string(name: "schema:datePublished")
#     author_id: string(name: "schema:author")
#     article_author: resource(name: "schema:author") {
#       id: iri
#       name: string(name: "schema:name")
#     }
#     article_url: string(name: "schema:mainEntityOfPage")
#     article_about: resource(name: "schema:about") {
#       names: string(name: "schema:name")
#     }
#     article_desc: string(name: "schema:description")
#     mentions: resources(name: "schema:mentions") {
#       names: strings(name: "schema:name")
#     }
#     body: string(name: "wordpress:content")
#   }
# }
# """

# config_options = {
#     'text_fields': ['name', 'description'],
#     'metadata_fields': ['url', 'image.image']
# }
# query = """
# query {
#   products(page:0, rows:10) {
# 		url: strings(name: "schema:url")
# 		names: strings(name:"schema:name")
#     description: strings(name:"schema:description")
#     image: resource(name: "schema:image") {
#       image: string(name: "schema:url")
#     }
#   }
# }
# """


# config_options = {
#     'text_fields': ['questions.question'],
#     'metadata_fields': ['url', 'questions.answer.text', 'title']
# }
# query = """
# query{
#   faqPages(page:0, rows:30){
#     url: string(name: "schema:url")
# 		title: string(name: "schema:name")
#     questions: resources(name: "schema:mainEntity") {
# 			question: string(name: "schema:name")
# 			answer: resources(name: "schema:acceptedAnswer") {
#         text: string(name: "schema:text")
#       }
#     }
#   }
# }
# """


# logging.basicConfig(
#     level=logging.DEBUG
# )

# # Create a logger object
# logger = logging.getLogger()
# Create an instance of the WordLiftLoader
reader = WordLiftLoader(
    endpoint, headers, query, fields, config_options)

# Load the data
documents = reader.load_data()
# node_parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
# service_context = ServiceContext.from_defaults(node_parser=node_parser)
# print(documents)
# # Convert the documents
with open('documents.json', 'w') as f:
    json.dump([doc.__doc__ for doc in documents], f, indent=4)
converted_doc = []
for doc in documents:
    converted_doc_id = json.dumps(doc.doc_id)
    converted_doc.append(Document(text=doc.text, doc_id=converted_doc_id,
                         embedding=doc.embedding, doc_hash=doc.hash, extra_info=doc.extra_info))
with open('converted_doc.json', 'w') as f:
    json.dump([doc.__dict__ for doc in converted_doc], f, indent=4)

# Create the index and query engine

index = VectorStoreIndex.from_documents(converted_doc)
query_engine = index.as_query_engine()

# langchain_documents = [d.to_langchain_format() for d in documents]

# # initialize sample QA chain
# llm = OpenAI(temperature=0)
# qa_chain = load_qa_chain(llm)
# question = "What is WordLift?"
# answer = qa_chain.run(input_documents=langchain_documents, question=question)

# Perform a query
result = query_engine.query("How Does SEO Automation Work?")

# Process the result as needed
print("=============> result: ", result)
print(result.get_formatted_sources())
