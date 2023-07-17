import os
import json
import openai
import logging
from llama_index import GPTVectorStoreIndex
from llama_index.readers.schema.base import Document
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from base import WordLiftLoader

# Set up the necessary configuration options
openai.api_key = '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'
os.environ["OPENAI_API_KEY"] = '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'
# test_key = "nCemGMTrPM8bZpmC3jyze4gbAJJ6cmO7daualXlkyvU53ciuMeHr0AcKsB8Xva4c"
# test_key = "B8X6lDceXhDO5aVg86npbFavLcQtnNhII35GolV8HlDdY5Tj9jMvTViUBlotsXUc"  # articles
test_key = "lcG14E9wn0aNNp2whaRhcsbOGrYYJxLOhjGG4Pb2YEJZD7XCik5086cVhqwj7eCc"  # product
# test_key = "nCemGMTrPM8bZpmC3jyze4gbAJJ6cmO7daualXlkyvU53ciuMeHr0AcKsB8Xva4c"  # faq
default_page = 0
default_rows = 500

fields = "products"

endpoint = "https://api.wordlift.io/graphql"
headers = {
    "Authorization": f"Key {test_key}",
    "Content-Type": "application/json"
}

# config_options = {
#     'text_fields': ['article_url'],
#     'metadata_fields': ['title', 'article_url']
# }
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

config_options = {
    'text_fields': ['description'],
    'metadata_fields': ['url', 'names']
}
query = """
query {
  products(page:0, rows:20) {
    id: iri
		url: strings(name: "schema:url")
		gtin: strings(name: "schema:gtin")
		names: strings(name:"schema:name")
    description: strings(name:"schema:description")
    brand: resource(name:"schema:brand"){
        brand: string(name: "schema:name")
      }
		price: resource(name:"schema:offers"){
        price: string(name: "schema:price")}
	  image: string(name: "schema:image")
}
}
"""


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
print(documents)
# # Convert the documents
converted_doc = []
for doc in documents:
    converted_doc_id = json.dumps(doc.doc_id)
    converted_doc.append(Document(text=doc.text, doc_id=converted_doc_id,
                         embedding=doc.embedding, doc_hash=doc.doc_hash, extra_info=doc.extra_info))

# Create the index and query engine
index = GPTVectorStoreIndex.from_documents(converted_doc)
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
print(result)
print(result.get_formatted_sources())
