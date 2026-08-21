from src.validation import EducationEntry
import sqlite3
from src.validation import Candidate,ExperienceEntry,EducationEntry
from datetime import date

def get_connection() -> sqlite3.Connection:
    conn=sqlite3.connect("resumes.db")#Opens/Creates the file
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def create_tables(conn: sqlite3.Connection) -> None:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Candidate (
        Candidate_ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Description TEXT
    )
    """)
    conn.commit()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Skill (
        Skill_ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL UNIQUE
    )
    """)
    conn.commit()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS ExperienceEntry (
        ExperienceEntry_ID INTEGER PRIMARY KEY,
        Candidate_ID INTEGER NOT NULL REFERENCES Candidate(Candidate_ID) ON DELETE CASCADE,
        Title TEXT,
        Company TEXT,
        Job_type TEXT,
        Start_date TEXT,
        End_date TEXT
    )
    """)
    conn.commit()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS EducationEntry (
        EducationEntry_ID INTEGER PRIMARY KEY,
        Candidate_ID INTEGER NOT NULL REFERENCES Candidate(Candidate_ID) ON DELETE CASCADE,
        Institution TEXT,
        Field_of_study TEXT,
        GPA REAL,
        Start_date TEXT,
        End_date TEXT
    )
    """)
    conn.commit()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS CandidateSkill (
        Skill_ID INTEGER NOT NULL REFERENCES Skill(Skill_ID) ON DELETE RESTRICT,
        Candidate_ID INTEGER NOT NULL REFERENCES Candidate(Candidate_ID) ON DELETE CASCADE,
        PRIMARY KEY (Skill_ID,Candidate_ID)
    ) 
    """)
    conn.commit()

def insert_candidate(conn: sqlite3.Connection,candidate:Candidate)->int:
    cursor=conn.cursor()
   
    cursor.execute("INSERT INTO Candidate(Name,Description) VALUES(?,?)",(candidate.name,candidate.description))
    candidate_id=cursor.lastrowid

    for exp in candidate.experience:
        end_date=None
        if(exp.end_date!=None):
            end_date=str(exp.end_date)
        cursor.execute("INSERT INTO ExperienceEntry (Candidate_ID,Title,Company,Job_type,Start_date,End_date) VALUES (?,?,?,?,?,?)",(candidate_id,exp.title,exp.company,exp.job_type,str(exp.start_date),end_date))

    for edu in candidate.education:
        end_date=None
        if(edu.end_date!=None):
            end_date=str(edu.end_date)
        cursor.execute("INSERT INTO EducationEntry (Candidate_ID,Institution,Field_of_study,GPA,Start_date,End_date) VALUES (?,?,?,?,?,?)",(candidate_id,edu.institution,edu.field_of_study,edu.gpa,str(edu.start_date),end_date))

    for skill in candidate.skills:
        cursor.execute("SELECT Skill_ID FROM Skill WHERE Name=? LIMIT 1 ",(skill.lower(),))
        exists=cursor.fetchone()
        if exists==None:
            cursor.execute("INSERT INTO Skill (Name) VALUES (?)",(skill.lower(),))
            skill_id=cursor.lastrowid
        else:
            skill_id=exists[0]
        cursor.execute("SELECT Candidate_ID FROM CandidateSkill WHERE Skill_ID=? AND Candidate_ID=? LIMIT 1",(skill_id,candidate_id))
        composite_exists=cursor.fetchone()
        if composite_exists==None:
            cursor.execute("INSERT INTO CandidateSkill (Skill_ID,Candidate_ID) VALUES (?,?)",(skill_id,candidate_id))
    conn.commit()
    return candidate_id


if __name__=="__main__":
    conn=get_connection()
    create_tables(conn)
    conn.close()