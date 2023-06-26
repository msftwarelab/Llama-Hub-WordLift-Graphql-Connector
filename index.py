import os
import json
import openai
import logging
from llama_index import GPTVectorStoreIndex
from llama_index.readers.schema.base import Document
from base import WordLiftGraphQLReader

# Set up the necessary configuration options
openai.api_key = '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'
os.environ["OPENAI_API_KEY"] = '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'
# test_key = "nCemGMTrPM8bZpmC3jyze4gbAJJ6cmO7daualXlkyvU53ciuMeHr0AcKsB8Xva4c"
test_key = "B8X6lDceXhDO5aVg86npbFavLcQtnNhII35GolV8HlDdY5Tj9jMvTViUBlotsXUc"
default_page = 0
default_rows = 25

fields = "articles"

endpoint = "https://api.wordlift.io/graphql/graphql"
headers = {
    "Authorization": f"Key {test_key}",
    "Content-Type": "application/json"
}
config_options = {
    'text_fields': ['article_desc'],
    'metadata_fields': ['article_url']
}
query = """
query {
  articles(page: 0, rows: 25) {
    id: iri
    title: string(name: "schema:headline")
    date: string(name: "schema:datePublished")
    author_id: string(name: "schema:author")
    article_author: resource(name: "schema:author") {
      id: iri
      name: string(name: "schema:name")
    }
    article_url: string(name: "schema:mainEntityOfPage")
    article_about: resource(name: "schema:about") {
      names: string(name: "schema:name")
    }
    article_desc: string(name: "schema:description")
    mentions: resources(name: "schema:mentions") {
      names: strings(name: "schema:name")
    }
    body: string(name: "wordpress:content")
  }
}
"""
# config_options = {
#     # 'text_fields': ['name'],
#     # 'metadata_fields': ['frameShape']
# }
# query = """
# query {
#   products(page: 1, rows: 30) {
#           id:iri
#         brand: string(name: "schema:brand")
#           name: string(name: "schema:name")
#         type: string(name: "rdf:type")
#         category: string(name: "eyewear:category")
#         productGroup: string(name: "eyewear:eyewearProductGroup")
#         bridgeType: string(name: "eyewear:bridgeType")
#         frameShape: string(name: "eyewear:frameShape")
#         faceShape: string(name: "eyewear:faceShape")
#         frameFitting: string(name: "eyewear:frameFitting")
#         frontColorFinish: string(name: "eyewear:frontColorFinish")
#         macroAgeRange: string(name: "eyewear:macroAgeRange")
#         ageGroupEnumeration: string(name: "eyewear:ageGroupEnumeration")
#         lensAssemblyTypeOnFrame: string(name: "eyewear:lensAssemblyTypeOnFrame")
#         frameType: string(name: "eyewear:frameType")
#         eyewearLensMaterial: string(name: "eyewear:eyewearLensMaterial")
#         eyewearTempleMaterial: string(name: "eyewear:eyewearTempleMaterial")
#         nosepadType: string(name: "eyewear:nosepadType")
#         release: string(name: "eyewear:release")
#         specialProjectCollection: string(name: "eyewear:specialProjectCollection")
#         specialProjectSponsor: string(name: "eyewear:specialProjectSponsor")
#         specialProjectType: string(name: "eyewear:specialProjectType")
#         specialProjectFeaturesFlag: string(name: "eyewear:specialProjectFeaturesFlag")
#         lensTreatment: string(name: "eyewear:lensTreatment")
#         lensColor: string(name: "eyewear:lensColor")
#         productStyleName: string(name: "eyewear:productStyleName")
#         productFamilyModel: string(name: "eyewear:productFamilyModel")
#         frameFoldability: string(name: "eyewear:frameFoldability")
#         roXability: string(name: "eyewear:roXability")
#         isLensPhotochromic: string(name: "eyewear:isLensPhotochromic")
#         isLensPolar: string(name: "eyewear:isLensPolar")
#         modelCodeDisplay: string(name: "eyewear:modelCodeDisplay")
#         progressiveFriendly: string(name: "eyewear:progressiveFriendly")
#         materialType: string(name: "eyewear:materialType")
#         maskShield: string(name: "eyewear:maskShield")
#         strassPresence: string(name: "eyewear:strassPresence")
#         strassPosition: string(name: "eyewear:strassPosition")
#         lensContrastEnhancement: string(name: "eyewear:lensContrastEnhancement")
#         lensBaseCurve: string(name: "eyewear:lensBaseCurve")
#         isLensGradient: string(name: "eyewear:isLensGradient")
#         isLensMirror: string(name: "eyewear:isLensMirror")
#         modelFit: string(name: "eyewear:modelFit")
#         modelName: string(name: "eyewear:modelName")
#         frontMaterial: string(name: "eyewear:frontMaterial")
#         lensProtection: string(name: "eyewear:lensProtection")
#         templeColor: string(name: "eyewear:templeColor")
#           frontColor: string(name: "eyewear:templeColor")
#           isLensBlueLightFiltered: string(name: "eyewear:isLensBlueLightFiltered")
#         genderType: string(name: "eyewear:genderType")
#         lensProtection: string(name: "eyewear:lensProtection")
#         channelAttributes: resources(name: "eyewear:channelAttributes") {
#             channel: string(name: "eyewear:channel")
#             styleName: string(name: "eyewear:styleName")
#         }
#   }
# }
# """
# config_options = {
#     # 'text_fields': ['questions'],
#     'metadata_fields': ['url']
# }
# query = """
# {
#  faqPages(page: 0, rows: 25){
#    url: string(name: "schema:url")
#    questions: resources(name: "schema:mainEntity") {
#      question: string(name: "schema:name")
#      answer: resources(name: "schema:acceptedAnswer") {
#        answer: string(name: "schema:text")
#      }
#    }
#  }
# }
# """
logging.basicConfig(
    level=logging.DEBUG
)

# Create a logger object
logger = logging.getLogger()
# Create an instance of the WordLiftGraphQLReader
reader = WordLiftGraphQLReader(
    endpoint, headers, query, fields, config_options)

# Load the data
documents = reader.load_data()

# Convert the documents
converted_doc = []
for doc in documents:
    converted_doc_id = json.dumps(doc.doc_id)
    converted_doc.append(Document(text=doc.text, doc_id=converted_doc_id,
                         embedding=doc.embedding, doc_hash=doc.doc_hash, extra_info=doc.extra_info))
logging.info("documents: %s", documents)

# Create the index and query engine
index = GPTVectorStoreIndex.from_documents(converted_doc)
query_engine = index.as_query_engine()

# Perform a query
result = query_engine.query("What did the author do growing up?")

# Process the result as needed
logging.info("Result: %s", result)
