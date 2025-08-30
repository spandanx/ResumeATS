import hmac
import hashlib

class HashHandler:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.hashname = hashlib.sha256

    def generate_hash(self, message):
        hash_object = hmac.new(self.secret_key, message, self.hashname)
        hexa_hash = hash_object.hexdigest()
        return hexa_hash

if __name__ == "__main__":

    secret_key = b"my_secret_key"  # Key must be bytes
    message = b"This is the message to be authenticated." # Message must be bytes
    message = b'Spandan Maity\n\n+917407684252 | spandanmaity58@gmail.com | linkedin.com/in/spandan-maity | github.com/spandanx |\nmedium.com/@spandanmaity58 | kaggle.com/spandanx\n\nSUMMARY\n\n Generative AI and ML enthusiast with 5+ years of experience in software development. Experienced in building end-to-end\napplications using LLMs, LangChain, LangGraph, RAG, and LST M. Skilled in prompt engineering, NLP, vector search, and\nimproving model performance.\n\nTECHNICAL SKILLS\n\nProgramming Languages: Python, Java, Javascript, DataWeave\n\nLLM & N LP Frameworks:: LangChain, LangGraph, TensorFlow, Keras, RAG, LSTM, Transformers, LLM, NLTK, BERT, Fine Tuning\n\nDatabases and Messaging: Oracle SQL, QDrant (Vector DB), Cassandra , Apache Kafka\n\nTools & Libraries: Apache Air\xef\xac\x82ow, ML\xef\xac\x82ow, Docker, NumPy, Pandas, FastAPI, Scikit-learn\n\nEXPERIENCE\n\nDigital Engineering Senior Engineer\n NTT Data\n\nOctober 2023 \xe2\x80\x93 Present\nIndia, Remote\n\n\xe2\x80\xa2 Working on a POC to automate business work\xef\xac\x82ows by analyzing email using LangGraph, LangChain \n\n\xe2\x80\xa2 Boosted RAG model recall by 15% using dense re-ranking with a cross-encoder architecture\n\n\xe2\x80\xa2 Increased the answer relevancy score by 10% by using self- corrective RAG pattern using feedback loops\n\n\xe2\x80\xa2 Developed robust retry mechanism in MuleSoft, reducing Salesforce errors by 90%\n\nSenior Software Engineer\nApisero Inc . (part of NTT Data)\n\nOctober 2021 \xe2\x80\x93 October 2023\nIndia, Remote\n\n\xe2\x80\xa2 Led Kafka-based optimizations that improved throughput 3x using parallel consumers and  message partitioning\n\n\xe2\x80\xa2 Minimized MDM account creation errors by 99% and handled IDOC sequence issues through partial child account creation\n\n\xe2\x80\xa2 Reduced r edundant salesforce upsert calls by 75% through message \xef\xac\x81ltering with DataWeave\n\nSystems Engineer\nInfosys Limited\n\n\xe2\x80\xa2 Designed scalable Cassandra schema t o store 300GB+ data for a cybersecurity product.\n\n\xe2\x80\xa2 Developed Python-based data ingestion programs to ef\xef\xac\x81ciently populate Cassandra tables\n\nNovember 2019 \xe2\x80\x93 October 2021\nIndia, Remote\n\nPERSONAL PROJECTS\n\nYoutube Comment Analyzer\nGen AI Project | \xc2\xa7 | \xc2\xaf\n\nMay 2024 \xe2\x80\x93 Present\nLangChain, TensorF low, Python, FastAPI, QDrant, Llama3.2\n\xe2\x80\xa2 Built a GenAI platform to summarize YouTube content by combining transcripts, comments, and replies, using a custom RAG-based Q A\npipeline with LangChain and Llama3.2.\n\nStockDoc\nMachine Learning Project | \xc2\xa7\n\nDecember 2024 \xe2\x80\x93 Present\nLSTM, FastAPI, React.js\n\n\xe2\x80\xa2 Built a ful l-stack stock prediction app using LSTM on historical data, automated daily forecasts with Air\xef\xac\x82ow DAGs, and developed an\ninteractive React.js frontend for visualizing c harts and predictions.\n\nEDUCATION\n\nCollege of Engineering and Management, Kolaghat (MAKAUT)\nB.Tech in Computer Science and Engineering\n\nKolaghat, West Bengal\nAug 2015 \xe2\ x80\x93 May 2019\n\nCERTIFICATIONS\n\n\xe2\x80\xa2 Introduction to Transformer-Based Natural Language Processing, NVIDIA\n\n\xe2\x80\xa2 Machine Learning: Natural Language Processing in Python (V2), Udemy\n\n\x0c'
    hashHandler = HashHandler(secret_key=secret_key)
    # Create an HMAC object using SHA256 and the secret key
    # h = hmac.new(secret_key, message, hashlib.sha256)
    # Get the hexadecimal representation of the HMAC digest
    # hmac_digest = h.hexdigest()
    hash = hashHandler.generate_hash(message)
    print(hash)

    # print(f"HMAC-SHA256 digest: {hmac_digest}")