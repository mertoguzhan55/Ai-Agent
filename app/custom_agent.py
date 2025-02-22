from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from typing import Dict, List, Optional, Union
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.groq import GroqModel
from app.dependency import Dependency
import xml.etree.ElementTree as ET
import random
import requests
import psycopg2


@dataclass
class CustomAgent():

    logger: any

    def __post_init__(self):
        self.model = GroqModel('llama-3.3-70b-versatile')

    def run(self, dep):

        agent = Agent(
            model = self.model,  
            deps_type = dep,  
            system_prompt=(
                "You are a versatile AI assistant capable of handling multiple tasks. "
                "When the user asks for job-related information, extract the relevant keyword and use the appropriate tool "
                "to fetch job postings from the provided XML feed. If the user requests to store or update information, "
                "extract the necessary details such as user name and job title, and insert them into the specified PostgreSQL table. "
                "Always choose the correct tool based on the context of the prompt and provide clear, concise responses."
            ),
        )


        @agent.tool
        def get_job(ctx: RunContext[Dependency]) -> List[Dict[str, str]]:
            """
            This function is designed to take the job-related keyword in the entered prompt and list the job postings related to this keyword from the given URL. 
            """
            
            job_keyword = ctx.deps
            if not job_keyword:
                return [{"error": "No job keyword provided"}]
            
            print(f"get_job fonksiyonu çağrıldı ve keyword: {job_keyword}")

            # XML verisini çekelim
            url = "https://devitjobs.uk/job_feed.xml"
            response = requests.get(url)
            if response.status_code != 200:
                return [{"error": f"Failed to fetch job data. HTTP Code: {response.status_code}"}]

            print("response code is 200")

            # XML verisini parse edelim
            root = ET.fromstring(response.content)
            jobs = []

            # İş ilanlarını filtreleyelim
            for job in root.findall(".//item"):
                title = job.find("title").text if job.find("title") is not None else "Unknown"
                company = job.find("company").text if job.find("company") is not None else "Unknown"
                location = job.find("location").text if job.find("location") is not None else "Unknown"
                description = job.find("description").text if job.find("description") is not None else "No description"

                # Anahtar kelimeyi başlık veya açıklamada arayalım
                if job_keyword.lower() in title.lower() or job_keyword.lower() in description.lower():
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": description[:200] + "..."
                    })

            return jobs if jobs else [{"message": f"No jobs found for keyword: {job_keyword}"}]


        @agent.tool
        def database_conn(ctx: RunContext[Dependency], name:str, job:str) -> str:
            """
            Inserts a new record into the specified database table using the provided user_name and job information.
            This tool extracts the user name and job from the prompt and performs an INSERT operation on the database.
            
            Parameters:
            - user_name: The username to be inserted.
            - job: The job title or role associated with the user.
            
            Returns:
            A confirmation message indicating that the record has been successfully inserted into the table.
            """

            self.logger.info("the database tool is invoked.")
            conn_params = {
                "database": '',
                "user": "",
                "password": "",
                "host": "",
                "port": 1234,
            }
            
            try:
                self.logger.info("trying connection to database")
                
                conn = psycopg2.connect(**conn_params)
                cursor = conn.cursor()
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    job VARCHAR(255)
                );
                """
                cursor.execute(create_table_query)
                conn.commit()
                
                insert_query = f"INSERT INTO users (name, job) VALUES (%s, %s);"
                cursor.execute(insert_query, (name, job))
                conn.commit()
                
                cursor.close()
                conn.close()
                return f"Record inserted into table 'users' for user '{name}' with job '{job}'."
            except Exception as e:
                self.logger.info("connection error")
                return f"An error occurred: {str(e)}"


        prompt = input("Give a prompt!\n")
        result = agent.run_sync(str(prompt))
        self.logger.info(f"Agent: {result.data}")
        print("Agent:", result.data)



if __name__ == "__main__":
    pass