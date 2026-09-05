from dotenv import load_dotenv
from groq import Groq, RateLimitError, BadRequestError
import json
from pydantic import ValidationError
from src.validation import Candidate
from src.resume_reader import extract_text
from get_random_resumes import get_random_resumes
import time
from src.sqlite_db import get_connection, create_tables, insert_candidate

load_dotenv()

client=Groq() #Automatically reads GROQ_API_KEY

def extract_candidate_from_text(raw_text: str) -> Candidate:
    system_prompt ="""You are an expert resume parser, your role is to read unstructured text that is extracted from resumes (orginally in docx or pdf format), organize this data into the Candidate Schema, so it can be stored into the database's fields.
    A Resume may not have all the fields required in that case, you should leave them out rather than inventing them, the Candidate Schema carefully handles potentially missing values by defaulting them to an empty string/ empty list or None. Only organize the data you find in the resume.
    Valid Dates are pydantic strings that follow the pattern: YYYY, YYYY-MM, YYYY-MM-DD, the dates extracted from the resumes must be written in this format.
    You are forbidden from fabrication, Never Guess any data field's value just try your best to extract the fields from the text, Use the Text's exactly words only.
    """
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "candidate",
            "schema": Candidate.model_json_schema()
        }
    }
    failures = 0
    while failures < 3:
        try:
            response = client.chat.completions.create(
                model = "openai/gpt-oss-20b",
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": raw_text}
                ],
                response_format = response_format,
                temperature = 0,
                max_completion_tokens = 8192
            )
            json_object = json.loads(response.choices[0].message.content)
            candidate = Candidate.model_validate(json_object)
            return candidate
        except (ValidationError, json.JSONDecodeError, BadRequestError, RateLimitError) as e:
            failures += 1
            print(f"Attempt {failures} failed: {e}")
            time.sleep(15)
    if (failures == 3):
        raise RuntimeError(f"Failed to extract candidate after {failures} attempts")
    

if __name__ == "__main__":
    resume_file_paths = get_random_resumes("testfiles/archive/data/data/")
    number = 0
    conn = get_connection()
    create_tables(conn)

    for file in resume_file_paths:
        print(file)
        raw_text = extract_text(file)
        try:
            candidate = extract_candidate_from_text(raw_text)
            print(f"Candidate {number}: {candidate.role}")
            number+=1
            insert_candidate(conn, candidate)
            time.sleep(10)
        except Exception as e:
            print(f"Candidate extraction from resume failed: {type(e).__name__}: {e}")
    conn.close()
    
   

