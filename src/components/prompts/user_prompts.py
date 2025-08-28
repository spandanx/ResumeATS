
complete_resume_extraction_user_prompt = f"""
Extract resume information from the below raw resume data. 

** Resume Content **
{{resume_content}}
"""

resume_scoring_user_prompt = f"""
Calculate the score for different components present in the resume.

** Resume JSON Content **
{{resume_json}}
"""

job_description_user_prompt = f"""
You are a job description extracting agent. Your task is to extract information from the job description.
Extract different components from the below job description.

** Job description **
{{job_description}}
"""

similarity_score_user_prompt = f"""
Compare the below job description and resume data and calculate the similarity score on different components

** Job description **
{{job_description}}

** Resume JSON Content **
{{resume_json}}
"""