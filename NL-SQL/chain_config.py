from llama_index.core import SQLDatabase
from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.objects import ObjectIndex, SQLTableNodeMapping, SQLTableSchema

from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


table_details={
    "branches" : "Stores the branch id and branch name",
    "coupon_master": "Stores the details of coupon won by each customer",
    "customer_master": "Stores the customer details",
    "invoice_details": "Stores the details about the products purchased in each invoice",
    "invoice_master": "Stores the details about purchases made by each customer"
}

tables=['branches','customer_master','invoice_details','invoice_master']


def configure_db():
    try:
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_name = os.getenv("DB_NAME")
        if not all([db_user, db_password, db_host, db_name]):
            raise ValueError("Missing database configuration. Please check your .env file.")
        engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}")
        engine.connect()  # Test the connection
        logger.info("Database connection successful")
        sql_database = SQLDatabase(engine, include_tables=tables, sample_rows_in_table_info=2)
        return sql_database
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        raise

def setup_llm():
    try:
        Settings.llm = Ollama(model="llama3:8b-instruct-q4_K_M", request_timeout=60.0)
        Settings.embed_model = OllamaEmbedding(model_name="lama3:8b-instruct-q4_K_M")
        Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
        Settings.num_output = 512
        Settings.context_window = 3900
        
        sql_database = configure_db()
        
        system_prompt = """
        Instructions:
	    1.	Input: Receive natural language queries from the user.
	    2.	Output: Convert these queries into precise SQL commands.
	    3.	Validation: Ensure SQL queries are syntactically correct and optimized for performance.
	    4.	Date Format: dates are in YYYY-MM-DD HH:MM:SS.sss format. Handle edge cases and ambiguities logically.
        5.  Time Format: times are in HH:MM:SS.sss format. Handle edge cases and ambiguities logically
        6.  When query is made about a day only use the date for comparision do not use time
	    7.	Limitations: Only read operations are allowed. Do not create, update, or delete tables.
	    6.	Currency: Use INR (Indian Rupees) for monetary amounts. Do not use the $ symbol.
	    8.	Optimization: Ensure SQL queries are optimized and follow best practices.
	    9.	Joins: Use appropriate join conditions and always use id columns when joining tables, not names.
	    10.	Aliases: Use meaningful aliases for tables and columns to improve readability.
	    11.	ID Usage: When a name is given, convert it to the appropriate id.
	    12.	Use DATE(CURRENT_TIMESTAMP) instead of CURRENT_DATE.
        13. IMPORTANT: Only generate READ-ONLY queries (SELECT statements). Do not generate any queries that modify the database (INSERT, UPDATE, DELETE, etc.).
        14. If a user requests a query that would modify the database, politely explain that you can only provide read-only queries for security reasons.
        """
        
        query_engine = NLSQLTableQueryEngine(
            sql_database,
            service_context=Settings,
            synthesize_response=True,
            response_synthesizer_kwargs={
                "system_prompt": system_prompt
            }
        )
        logger.info("LLM setup completed successfully")
        return query_engine
    except Exception as e:
        logger.error(f"Error setting up LLM: {str(e)}")
        raise