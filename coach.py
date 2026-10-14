from llm import ask_ai_json

#number from 0 to 100

def analyze_profile(Resume_text,job_description):
    prompt=f"""
    You are an expert technical recruiter.
    Compare to candidates resume with job description.
    
    RESUME:
    {Resume_text}
    
    JOB DESCRIPTION
    {job_description}
    
    Return json with exactly these keys:
    -"Candidate's Name":string
    -"Role":job title from the job description
    -"Matching Skills":List of required skills the candidate has
    -"Missing Skills":List of required skills not found in the candidate's resume
    -"Matching score":0
    -"Summary":2-3 sentences about how well the candidate fits in the role
    Only use information that is actually in the resume don't invent skills
    """
    return ask_ai_json(prompt)
    
#to generate questions according to JD
def generate_questions(analysis,Resume_text,job_description,num_questions=5):
    prompt=f"""
    You are an experienced interviewer hiring for the role of 
    {analysis.get('Role','this job')}.
    write{num_questions} interview questions for this candidate.
    use this mix:
    -Technical questions on the skills the candidate has.
    -Atleast one question about specific project from their resume.
    -Atleast one question about a missing skill.
    -One behavioural question about team work, challenges or deadlines.
    every question must be specific to this candidate, not a generic text book questions.
    
    RESUME:
    {Resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    MATCHING SKILLS:
    {analysis.get('Matching Skills',[])}
    
    MISSING SKILSS:
    {analysis.get('Missing Skills',[])}
    
    Return JSON in this format:
    {{
        "questions":[
            {{
                "question":"...",
                "type":"technical | behavioural | project | missing skill",
                "Skill":"..."
            }}
        ]
    }} 
    """
    return ask_ai_json(prompt)
    