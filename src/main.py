import asyncio
import json

from components.agents.JDExtractionAgent import JDExtractionAgent
from components.agents.ResumeScoringAgent import ResumeScoringAgent
from components.agents.ResumeExtractionAgent import ResumeDataExtractingAgent
from components.utils.ResumeScoreCalculator import ResumeScoreCalculator

from components.exceptions.CustomExceptions import ResumeExtractionException, ResumeScoringException, JDExtractionException
# from components.exceptions.CustomExceptions import

'''
Extracts the job description data
'''
async def extract_job_description(job_description):
    jdExtractionAgent = JDExtractionAgent()
    job_description_raw_input = {
        "job_description": job_description
    }
    try:
        extracted_jd_data = await jdExtractionAgent.extract_job_description(job_description_raw_input)
        jd_json = json.loads(extracted_jd_data.messages[-1].content)
        return jd_json
    except Exception as e:
        raise JDExtractionException()

'''
Adds the component weights to the results
'''
def update_weightage_info(resume_score_json, component_wise_score):
    updated_map = dict()
    for key, val in resume_score_json.items():
        val.update(component_wise_score[key])
        updated_map[key] = val
    return updated_map

'''
Extracts the resume data
'''
async def extract_resume_description(raw_resume_data):
    resume_extractor = ResumeDataExtractingAgent()
    resume_scorer = ResumeScoringAgent()
    resume_data_raw_input = {
        "resume_content": raw_resume_data
    }
    try:
        # extracted_resume_data = await resume_extractor.extract_resume(resume_data_raw_input)
        # resume_json = json.loads(extracted_resume_data.messages[-1].content)
        resume_json = {'achievements': [], 'candidate_information': {'contact_number': '+91-xxxxxxxx',
                                                                     'email_id': 'prashantxxxxx@gmail.com',
                                                                     'github_profile_link': 'GitHub Profile',
                                                                     'linkedin_profile_link': 'LinkedIn Profile',
                                                                     'name': 'Prashant Singh',
                                                                     'other_information': 'Roll No.: xxxxxxx'},
                       'certifications': [], 'company_projects': [], 'education': [
                {'duration': '2020-24', 'institution_name': 'Shri Ramdeobaba College of Engineering and Management',
                 'location': 'Nagpur', 'marks': 'CGPA: xx',
                 'other_information': 'Bachelor of Technology in Computer Science and Engineering(Cyber Security)'}],
                       'experience': [{'company_name': 'AICTE-Eduskills', 'contributions': [
                           'In-depth understanding of AWS cloud computing services, including EC2, S3, RDS, Lambda, IAM, VPC, and more.',
                           'Proficient in designing, deploying, and managing fault-tolerant, highly available, and scalable AWS solutions.',
                           'Strong knowledge of architectural best practices, such as AWS Well-Architected Framework, security, performance, and cost optimization.',
                           'Hands-on experience in cloud infrastructure provisioning, monitoring, and automation using AWS Management Console and AWS CLI.'],
                                       'designation': 'AWS Cloud Virtual Internship', 'duration': 'May - July 2023',
                                       'technology': []}, {'company_name': 'AICTE-Eduskills', 'contributions': [
                           'Learned the fundamentals of Security Operations Center (SOC).',
                           'Learned basics of Network & Cloud Security.'],
                                                           'designation': 'Palo Alto Cybersecurity Virtual Internship',
                                                           'duration': 'Dec 2022 - Feb 2023', 'technology': []}],
                       'personal_projects': [{'complete_description': [
                           'Facilitating users’ logins to websites without having to remember their credentials',
                           'Used Live detection techniques to create high order security.'], 'duration': 'NOT FOUND',
                                              'project_description': 'A website based facial authentication system, implemented using a Chrome Extension.',
                                              'project_name': 'Web Based Facial Authentication(Liveness Detection)',
                                              'technology': ['Python', 'Reactjs', 'Bootstrap']}, {
                                                 'complete_description': [
                                                     'Used Firebase Authentication(SDK) to facilitate authentication & Cloud Firestore to store data.'],
                                                 'duration': 'NOT FOUND',
                                                 'project_description': 'A react based web application which allow users to chat in real time.',
                                                 'project_name': 'Realtime Chat App',
                                                 'technology': ['Reactjs', 'Firebase', 'Bootstrap', 'HTML']}, {
                                                 'complete_description': [
                                                     'Tracking world-wide cases using google maps and live API stats and datasets.'],
                                                 'duration': 'NOT FOUND',
                                                 'project_description': 'Daily and weekly updated statistics tracking the number of COVID-19 cases, recovered, and deaths.',
                                                 'project_name': 'Covid-19 Tracker',
                                                 'technology': ['JavaScript', 'CSS', 'HTML', 'API']}],
                       'skills': ['C/C++', 'Python', 'Javascript', 'HTML+CSS', 'C++ STL', 'Python Libraries', 'ReactJs',
                                  'Nodejs', 'VScode', 'Git', 'Github', 'MongoDb', 'Firebase',
                                  'Relational Database(mySql)', 'Data Structures & Algorithms', 'Operating Systems',
                                  'Object Oriented Programming', 'Database Management System', 'Software Engineering']}
        return resume_json
    except Exception as e:
        raise ResumeExtractionException()

'''
Calculate resume score
'''
async def calculate_resume_score(resume_json):
    weights = {
        "candidate_information": 5,
        "education": 6,
        "company_projects": 3,
        "personal_projects": 7,
        "skills": 9,
        "experience": 9,
        "achievements": 4,
        "certifications": 4,
    }
    resume_scoring_input = {
        "resume_json": resume_json
    }
    try:
        # resume_scores = await resume_scorer.score_resume(resume_scoring_input)
        # resume_score_json = json.loads(resume_scores.messages[-1].content)
        resume_score_json = {"candidate_information": {"score": 8.0,
                                                       "justification": "The candidate information is mostly complete, including name, contact details, and links to professional profiles. However, it lacks more in-depth personal information that could enhance identification, such as address or a short personal statement.",
                                                       "improvement_suggestions": [
                                                           "Add a brief summary or objective statement that outlines career goals and aspirations.",
                                                           "Include a full address or at least city and state for geographical context.",
                                                           "Ensure that GitHub and LinkedIn profile links are actual URLs instead of placeholders."]},
                             "education": {"score": 7.5,
                                           "justification": "The education section contains relevant details about the degree, institution, duration, and field of study. However, the marks are not clearly presented, using a placeholder instead of an actual value.",
                                           "improvement_suggestions": [
                                               "Replace placeholder marks with actual CGPA or percentage if available.",
                                               "Include any relevant coursework or projects that highlight skills learned during the education."]},
                             "company_projects": {"score": 2.0,
                                                  "justification": "There are no entries in the company projects section, resulting in a low score. Company projects can significantly showcase practical experience and contributions.",
                                                  "improvement_suggestions": [
                                                      "Add at least one project from a company, detailing the project goals, your role, technologies used, and outcomes."]},
                             "personal_projects": {"score": 8.5,
                                                   "justification": "The personal projects section is detailed with project names, descriptions, technologies used, and implementation methods. However, the 'duration' is marked as 'NOT FOUND' for all projects, which isn’t informative.",
                                                   "improvement_suggestions": [
                                                       "Provide the actual durations for each project, even if it's just the approximate time taken.",
                                                       "Highlight the impact or results of these projects, such as user adoption or performance improvements."]},
                             "skills": {"score": 9.0,
                                        "justification": "The skills section is extensive and covers a broad range of relevant technologies and programming languages, showcasing versatility. There are no apparent typos or errors.",
                                        "improvement_suggestions": [
                                            "Consider grouping skills into categories (e.g., programming languages, frameworks, databases) for clarity.",
                                            "Prioritize or rank skills based on proficiency or relevance to the desired job."]},
                             "experience": {"score": 8.5,
                                            "justification": "The experience section is informative, outlining roles, contributions, and technologies. It effectively demonstrates relevant internships and the skills acquired during those roles. However, inclusion of technology used is missing in job details.",
                                            "improvement_suggestions": [
                                                "List any tools or technologies used in each internship role to enhance specificity and context.",
                                                "Quantify achievements or contributions when possible (e.g., 'Improved system efficiency by 20%')."]},
                             "achievements": {"score": 1.0,
                                              "justification": "The achievements section is currently empty, leading to a low score. This section should ideally highlight awards or recognitions that complement professional experience.",
                                              "improvement_suggestions": [
                                                  "Include any academic honors, scholarships, or relevant personal achievements that demonstrate expertise and motivation.",
                                                  "Consider adding certifications or recognitions, especially those related to technology or programming."]},
                             "certifications": {"score": 1.0,
                                                "justification": "The certifications section is empty, reflecting no formal certifications listed. Certifications can significantly validate skills, especially in technical fields.",
                                                "improvement_suggestions": [
                                                    "Add any relevant certifications completed, such as AWS Certified Solutions Architect or other IT-related credentials.",
                                                    "Consider pursuing and highlighting certifications that are industry-recognized."]}}

        resumeScoreCalculator = ResumeScoreCalculator(weights)
        max_score_per_category = 10
        resume_score, component_wise_score = resumeScoreCalculator.calculate_score(resume_score_json,
                                                                                   max_score_per_category)
        ## Update scoring data and include weights for those
        return resume_score, component_wise_score
    except Exception as e:
        raise ResumeScoringException()

'''
Extract the resume data, job description and calculate resume and similarity score 
'''
async def process_resume(raw_resume_data, raw_job_description):
    extracted_resume_json = await extract_resume_description(raw_resume_data=raw_resume_data)
    calculated_resume_score_json = await calculate_resume_score(resume_json = extracted_resume_json)
    updated_map = update_weightage_info(extracted_resume_json, calculated_resume_score_json)
    extracted_jd = extract_job_description(job_description=raw_job_description)
    scoring_result = {
        "total_score": calculated_resume_score_json,
        "component_wise_score_and_justification": updated_map
    }
    return scoring_result

if __name__ == "__main__":
    resume_data = """
    Prashant Singh
    Roll No.: xxxxxxx
    Bachelor of Technology
    Shri Ramdeobaba College of Engineering and Management, Nagpur

    (cid:131) +91-xxxxxxxx
    # prashantxxxxx@gmail.com
    § GitHub Profile
    (cid:239) LinkedIn Profile

    Education

    •Bachelor of Technology in Computer Science and Engineering(Cyber Security)
    Shri Ramdeobaba College of Engineering and Management, Nagpur

    2020-24

    CGPA: xx

    Personal Projects

    •Web Based Facial Authentication(Liveness Detection)
    A website based facial authentication system, implemented using a Chrome Extension.

    – Facilitating users’ logins to websites without having to remember their credentials
    – Used Live detection techniques to create high order security.
    – Technology Used: Python, Reactjs, Bootstrap.

    •Realtime Chat App
    A react based web application which allow users to chat in real time.

    – Used Firebase Authentication(SDK) to facilitate authentication & Cloud Firestore to store data.
    – Technology Used: Reactjs, Firebase, Bootstrap, HTML.

    •Covid-19 Tracker
    Daily and weekly updated statistics tracking the number of COVID-19 cases, recovered, and deaths.

    – Tracking world-wide cases using google maps and live API stats and datasets.
    – Technology Used : JavaScript , CSS, HTML, API.

    Experience

    •AWS Cloud Virtual Internship
    Online
    AICTE-Eduskills
    – In-depth understanding of AWS cloud computing services, including EC2, S3, RDS, Lambda, IAM, VPC, and

    May - July 2023

    more.

    – Proficient in designing, deploying, and managing fault-tolerant, highly available, and scalable AWS solutions.
    – Strong knowledge of architectural best practices, such as AWS Well-Architected Framework, security, performance,

    and cost optimization.

    – Hands-on experience in cloud infrastructure provisioning, monitoring, and automation using AWS Management

    Console and AWS CLI.

    •Palo Alto Cybersecurity Virtual Internship
    AICTE-Eduskills
    – Learned the fundamentals of Security Operations Center (SOC).
    – Learned basics of Network & Cloud Security.

    Technical Skills and Interests

    Dec 2022 - Feb 2023

    Online

    Languages: C/C++, Python, Javascript, HTML+CSS
    Libraries : C++ STL, Python Libraries, ReactJs
    Web Dev Tools: Nodejs, VScode, Git, Github
    Frameworks: ReactJs
    Cloud/Databases:MongoDb, Firebase, Relational Database(mySql)
    Relevent Coursework: Data Structures & Algorithms, Operating Systems, Object Oriented Programming, Database
    Management System, Software Engineering.
    Areas of Interest: Web Design and Development, Cloud Security.
    Soft Skills: Problem Solving, Self-learning, Presentation, Adaptability

    Positions of Responsibility

    •On Desk Registrations Volunteer Aarhant Cyber Week Event - RCOEM, Nagpur

    Oct - Dec 2022

    – Helped to attract close to 300 attendees to the event.
    – Collected over Rs. 20,000 in entry fees for different activities.

    """
    asyncio.run(process_resume(resume_data))