import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Path to your CSV file
csv_file_path = "C://Users//ARYA SHARMA//Desktop//Langchain//Data//CARS_1.csv"
# Read the CSV file using pandas
df = pd.read_csv(csv_file_path)

# SQLite database file path
db_file_path = "C://Users//ARYA SHARMA//Desktop//Langchain//Data//CARS_1.sqlite"

# Create a connection to the SQLite database
engine = create_engine(f"sqlite:///{db_file_path}")

# Convert the DataFrame to an SQLite database table
# Replace 'table_name' with the desired table name
df.to_sql("cars", engine, if_exists="replace", index=False)

# Once the data is inserted, the SQLite database is created with the given data

# Load Langchain components
dburi = "sqlite:///Data/CARS_1.sqlite"
db = SQLDatabase.from_uri(dburi)
llm = OpenAI(temperature=0)
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

# Streamlit app starts here
st.title("Analyse your data")

# Define functions for Langchain queries
def run_langchain_query(query):
    response = db_chain.run(query)
    return response

# Main Streamlit app
if __name__ == "__main__":
    st.write("Ask questions to your cars data!")

    # User input for Langchain queries
    user_input = st.text_input("Enter your question:", "What is the most popular car in the dataset?")

    if st.button("Run Query"):
        response = run_langchain_query(user_input)
        st.write(f"Query: {user_input}")
        st.write(f"Response: {response}")
