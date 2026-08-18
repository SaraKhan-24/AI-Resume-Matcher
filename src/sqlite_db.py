import sqlite3


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


if __name__=="__main__":
    conn=get_connection()
    create_tables(conn)
    conn.close()