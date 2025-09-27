import asyncio
import json
import inspect
import os
import sys

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_caller_file_name():
    call_stack = inspect.stack()
    call_filenames = [stack.filename for stack in call_stack if stack.filename.endswith(".py")]
    # print("Caller filename stack")
    logger.info("Caller filename stack")
    for fname in call_filenames:
        logger.info(fname)
        # print(fname)
    common_file_name = "resume-ats-app"
    filtered_filenames = [filename for filename in call_filenames if filename.endswith(".py") and common_file_name in filename]
    if len(filtered_filenames)==0:
        return "Not Found"
    caller_filename = os.path.basename(filtered_filenames[-1])
    return caller_filename

source_file_name = get_caller_file_name()
# print("source_file_name")
# print(source_file_name)
logger.info("source_file_name")
logger.info(source_file_name)

current_working_directory = os.getcwd()
logger.info(f"Current working directory (using os.getcwd()): {current_working_directory}")

if source_file_name == "ui.py":
    # sys.path.append("src")
    config_file_path = 'config.properties'
    # print("configuring for ui.py caller")
    logger.info("configuring for ui.py caller")
    sys.path.append("src")
elif source_file_name == "main.py":
    config_file_path = '../config.properties'
    logger.info("configuring for main.py caller")
else:
    config_file_path = 'config.properties'
    logger.info("configuring for other callers")



# from src.components.agents.JDExtractionAgent import JDExtractionAgent
# from src.components.agents.ResumeScoringAgent import ResumeScoringAgent
# from src.components.agents.ResumeExtractionAgent import ResumeDataExtractingAgent
# from src.components.agents.SimilarityScoreCalculationAgent import SimilarityScoreCalculationAgent
# from src.components.utils.ResumeScoreCalculator import ResumeScoreCalculator
# from src.components.utils.JDResumeSimilarityScoreCalculator import JDResumeSimilarityScoreCalculator
# from src.components.utils.HashHandler import HashHandler
# from src.components.utils.CacheHandler import CacheHandler
#
# from src.components.exceptions.CustomExceptions import ResumeExtractionException, ResumeScoringException, JDExtractionException, SimilarityCalculationException
# from src.components.DataExtraction.PDFContentReader import PDFContentReader


from components.agents.JDExtractionAgent import JDExtractionAgent
from components.agents.ResumeScoringAgent import ResumeScoringAgent
from components.agents.ResumeExtractionAgent import ResumeDataExtractingAgent
from components.agents.SimilarityScoreCalculationAgent import SimilarityScoreCalculationAgent
from components.utils.ResumeScoreCalculator import ResumeScoreCalculator
from components.utils.JDResumeSimilarityScoreCalculator import JDResumeSimilarityScoreCalculator
from components.utils.HashHandler import HashHandler
from components.utils.CacheHandler import CacheHandler

from components.exceptions.CustomExceptions import ResumeExtractionException, ResumeScoringException, JDExtractionException, SimilarityCalculationException
from components.DataExtraction.PDFContentReader import PDFContentReader


from datetime import timedelta
from configparser import ConfigParser

parser = ConfigParser()

with open(config_file_path) as f:
    file_content = f.read()

parser.read_string(file_content)
hashHandler = HashHandler(parser['CACHE']['cache_key'].encode('utf-8'))


cacheHandler = CacheHandler(redis_url=parser['CACHE']['cache_url'], redis_port=parser['CACHE']['cache_port'],
                            redis_db=parser['CACHE']['cache_db'], redis_password=parser['CACHE']['cache_password'],
                            db_hostname=parser['MONGODB']['mongodb_hostname'], db_port=parser['MONGODB']['mongodb_port'],
                            db_username=parser['MONGODB']['mongodb_username'], db_password=parser['MONGODB']['mongodb_password'],
                            db_database=parser['MONGODB']['mongodb_database'], db_keyspace=parser['MONGODB']['mongodb_keyspace'])
expire_time = timedelta(minutes=180)
# print(parser['CACHE']['url'])

'''
Reads PDF content from file
'''
async def read_pdf(file_path):
    pdfContentReader = PDFContentReader()
    content_pdfminer = pdfContentReader.read_pdf_with_pdfminer(file_path)
    return content_pdfminer

'''
Extracts the job description data
'''
async def extract_job_description(job_description, username, expiry):
    jdExtractionAgent = JDExtractionAgent()
    job_description_raw_input = {
        "job_description": job_description
    }

    try:
        content_hash = hashHandler.generate_hash(job_description.encode('utf-8'))
        print("content_hash", content_hash)

        cache_key = "extract_jd_description:" + username + ":" + content_hash
        cached_jd_json = cacheHandler.get_from_cache(cache_key, username, expiry)
        if cached_jd_json:
            print("Found cached extracted job description")
            return cached_jd_json
        else:
            extracted_jd_data = await jdExtractionAgent.extract_job_description(job_description_raw_input)
            jd_json = json.loads(extracted_jd_data.messages[-1].content)
            # jd_json = {"responsibilities":["Develop, test, and maintain web applications using Java and Spring Boot.","Collaborate with cross-functional teams to define and implement new features.","Ensure the performance, quality, and responsiveness of applications.","Identify and correct bottlenecks and fix bugs.","Document development processes, coding standards, and project requirements.","Participate in code reviews to ensure adherence to best practices and coding standards.","Stay up-to-date with emerging technologies and industry trends."],"skills":["Java","Spring Boot","Hibernate","RESTful APIs","SQL","Git","Maven","Unit Testing"],"qualifications":["Bachelor's degree in Computer Science, Information Technology, or related field.","Proven experience as a Java Developer, with expertise in Spring Boot.","Strong understanding of object-oriented programming principles and design patterns.","Experience with databases such as MySQL, PostgreSQL, or MongoDB.","Knowledge of front-end technologies like HTML, CSS, and JavaScript is a plus.","Excellent problem-solving skills and attention to detail.","Good communication and teamwork abilities."],"experience":[],"salary":"Not Mentioned","certifications":[]}
            cache_response = cacheHandler.cache_data(data=jd_json, key=cache_key, expiry=expire_time,
                                                     username=username)
            print("Cached extracted resume for id", cache_key, cache_response)
            return jd_json
    except Exception as e:
        raise JDExtractionException()


'''
Extracts the resume data
'''
async def extract_resume_description(raw_resume_data, username, expiry):
    resume_extractor = ResumeDataExtractingAgent()
    resume_data_raw_input = {
        "resume_content": raw_resume_data
    }
    try:
        content_hash = hashHandler.generate_hash(raw_resume_data.encode('utf-8'))
        print("content_hash", content_hash)

        cache_key = "extract_resume_description:" + username + ":" + content_hash
        cached_resume_json = cacheHandler.get_from_cache(cache_key, username, expiry)
        if cached_resume_json:
            print("Found cached extracted resume")
            return cached_resume_json
        else:
            extracted_resume_data = await resume_extractor.extract_resume(resume_data_raw_input)
            resume_json = json.loads(extracted_resume_data.messages[-1].content)
            cache_response = cacheHandler.cache_data(data=resume_json, key=cache_key, expiry=expire_time, username=username)
            print("Cached extracted resume for id", cache_key, cache_response)
        # resume_json = {'achievements': [], 'candidate_information': {'contact_number': '+91-xxxxxxxx',
        #                                                              'email_id': 'prashantxxxxx@gmail.com',
        #                                                              'github_profile_link': 'GitHub Profile',
        #                                                              'linkedin_profile_link': 'LinkedIn Profile',
        #                                                              'name': 'Prashant Singh',
        #                                                              'other_information': 'Roll No.: xxxxxxx'},
        #                'certifications': [], 'company_projects': [], 'education': [
        #         {'duration': '2020-24', 'institution_name': 'Shri Ramdeobaba College of Engineering and Management',
        #          'location': 'Nagpur', 'marks': 'CGPA: xx',
        #          'other_information': 'Bachelor of Technology in Computer Science and Engineering(Cyber Security)'}],
        #                'experience': [{'company_name': 'AICTE-Eduskills', 'contributions': [
        #                    'In-depth understanding of AWS cloud computing services, including EC2, S3, RDS, Lambda, IAM, VPC, and more.',
        #                    'Proficient in designing, deploying, and managing fault-tolerant, highly available, and scalable AWS solutions.',
        #                    'Strong knowledge of architectural best practices, such as AWS Well-Architected Framework, security, performance, and cost optimization.',
        #                    'Hands-on experience in cloud infrastructure provisioning, monitoring, and automation using AWS Management Console and AWS CLI.'],
        #                                'designation': 'AWS Cloud Virtual Internship', 'duration': 'May - July 2023',
        #                                'technology': []}, {'company_name': 'AICTE-Eduskills', 'contributions': [
        #                    'Learned the fundamentals of Security Operations Center (SOC).',
        #                    'Learned basics of Network & Cloud Security.'],
        #                                                    'designation': 'Palo Alto Cybersecurity Virtual Internship',
        #                                                    'duration': 'Dec 2022 - Feb 2023', 'technology': []}],
        #                'personal_projects': [{'complete_description': [
        #                    'Facilitating users’ logins to websites without having to remember their credentials',
        #                    'Used Live detection techniques to create high order security.'], 'duration': 'NOT FOUND',
        #                                       'project_description': 'A website based facial authentication system, implemented using a Chrome Extension.',
        #                                       'project_name': 'Web Based Facial Authentication(Liveness Detection)',
        #                                       'technology': ['Python', 'Reactjs', 'Bootstrap']}, {
        #                                          'complete_description': [
        #                                              'Used Firebase Authentication(SDK) to facilitate authentication & Cloud Firestore to store data.'],
        #                                          'duration': 'NOT FOUND',
        #                                          'project_description': 'A react based web application which allow users to chat in real time.',
        #                                          'project_name': 'Realtime Chat App',
        #                                          'technology': ['Reactjs', 'Firebase', 'Bootstrap', 'HTML']}, {
        #                                          'complete_description': [
        #                                              'Tracking world-wide cases using google maps and live API stats and datasets.'],
        #                                          'duration': 'NOT FOUND',
        #                                          'project_description': 'Daily and weekly updated statistics tracking the number of COVID-19 cases, recovered, and deaths.',
        #                                          'project_name': 'Covid-19 Tracker',
        #                                          'technology': ['JavaScript', 'CSS', 'HTML', 'API']}],
        #                'skills': ['C/C++', 'Python', 'Javascript', 'HTML+CSS', 'C++ STL', 'Python Libraries', 'ReactJs',
        #                           'Nodejs', 'VScode', 'Git', 'Github', 'MongoDb', 'Firebase',
        #                           'Relational Database(mySql)', 'Data Structures & Algorithms', 'Operating Systems',
        #                           'Object Oriented Programming', 'Database Management System', 'Software Engineering']}
            return resume_json
    except Exception as e:
        raise ResumeExtractionException()

'''
Calculate resume score
'''
async def calculate_resume_score(resume_json, username):
    resume_scorer = ResumeScoringAgent()
    weights = {
        "candidate_information": 5,
        "education": 6,
        "company_projects": 3,
        "personal_projects": 7,
        "skills": 9,
        "experience": 9,
        "achievements": 4,
        "certifications": 4,
        "others": 5
    }
    try:
        content_hash = hashHandler.generate_hash(json.dumps(resume_json).encode('utf-8'))
        print("content_hash", content_hash)

        # Complete content caching
        complete_json_level_cache_key = "calculate_resume_score_complete:" + username + ":" + content_hash
        cached_resume_json = cacheHandler.get_from_cache(complete_json_level_cache_key, username=username, expiry=expire_time)
        if cached_resume_json:
            print("Found cached extracted resume")
            resume_score_description = cached_resume_json
        else:
            # partial content check
            uncached_resume_score_json = dict()
            cached_resume_score_json = dict()

            for key, val in resume_json.items():
                json_component_hash = hashHandler.generate_hash(json.dumps(val).encode('utf-8'))
                print("json_component_hash", json_component_hash)

                # component level
                component_wise_cache_key = "calculate_resume_score_partial_" + key + ":" + username + ":" + json_component_hash
                cached_resume_json = cacheHandler.get_from_cache(component_wise_cache_key, username=username, expiry=expire_time)
                if cached_resume_json:
                    print("Found cached resume score, component - " + key)
                    cached_resume_score_json[key] = cached_resume_json
                else:
                    uncached_resume_score_json[key] = val

            # Keep only uncached sections, will join with cached sections at the end
            resume_scoring_input = {
                "resume_json": uncached_resume_score_json
            }
            resume_scores = await resume_scorer.score_resume(resume_scoring_input)
            resume_score_description = json.loads(resume_scores.messages[-1].content)

            if "scoring_sections" in resume_score_description:
                # Cache uncached components
                for key, val in uncached_resume_score_json.items():
                    # generate hash and link input to the output.
                    component_input_content = val
                    component_cache_content_filtered = [section for section in resume_score_description["scoring_sections"] if section["category"]==key]
                    if len(component_cache_content_filtered)>0:
                        json_component_wise_hash = hashHandler.generate_hash(json.dumps(component_input_content).encode('utf-8'))

                        component_cache_content_json = component_cache_content_filtered[0]
                        component_wise_cache_key = "calculate_resume_score_partial_" + key + ":" + username + ":" + json_component_wise_hash
                        cache_response = cacheHandler.cache_data(key=component_wise_cache_key, data=component_cache_content_json, expiry=expire_time, username=username)
                        print("Cached extracted resume for id", component_wise_cache_key, cache_response)

            # Join with cached sections
            for key, val in cached_resume_score_json.items():
                resume_score_description["scoring_sections"].append(val)
            # resume_score_description = {"scoring_sections":[{"category":"candidate_information","score":7.5,"justification":"The candidate information includes essential details such as name, contact number, email, and links to GitHub and LinkedIn. However, placeholder texts (e.g., 'xxxxxxxx' for contact number and 'GitHub Profile') reduce clarity and completeness.","improvement_suggestions":["Use actual contact details instead of placeholders.","Provide direct links to GitHub and LinkedIn profiles for easy access."]},{"category":"education","score":6.0,"justification":"The education section provides institutional details and degree info but lacks specifics such as the exact graduation date and CGPA values, which lowers its quality.","improvement_suggestions":["Replace 'xx' in CGPA with actual score.","Add the month and year of graduation for clarity."]},{"category":"experience","score":8.0,"justification":"Experience is well-detailed with roles, duration, and contributions outlined. However, both experiences are from the same company, leading to a possible perception of limited workplace exposure.","improvement_suggestions":["Include more diversity in companies or roles to show broader experience.","Highlight specific achievements or outcomes from these roles."]},{"category":"skills","score":9.0,"justification":"The skills section is comprehensive and covers a wide range of technical abilities. There are no major grammatical issues, but the formatting can be improved for readability.","improvement_suggestions":["Consider categorizing skills by proficiency or relevance (e.g., Programming Languages, Frameworks, Tools) for better organization."]},{"category":"personal_projects","score":7.0,"justification":"Personal projects are diverse and showcase the candidate's initiative. However, the 'duration' field is noted as 'NOT FOUND,' which diminishes clarity regarding commitment and completion.","improvement_suggestions":["Provide actual time frames for each project.","Include links to live projects or GitHub repositories for users to verify applications."]},{"category":"certifications","score":0.0,"justification":"There are no certifications listed in the resume, resulting in a complete absence of relevant credentials.","improvement_suggestions":["Obtain and include relevant certifications to enhance technical credibility."]},{"category":"achievements","score":0.0,"justification":"No achievements are mentioned, which is a significant missed opportunity as achievements can help demonstrate the candidate's impact and successes.","improvement_suggestions":["Add relevant achievements such as awards, recognitions, or milestones attained in academic or project environments."]},{"category":"company_projects","score":0.0,"justification":"There are no company projects listed. Company projects can provide insight into collaboration, responsibility, and professional experiences.","improvement_suggestions":["Include any significant company projects that demonstrate the ability to work in a team or lead tasks in a professional setting."]}]}

            cache_response = cacheHandler.cache_data(data=resume_score_description, key=complete_json_level_cache_key,
                                                     expiry=expire_time, username=username)
            print("Cached complete resume score", complete_json_level_cache_key, cache_response)

        resumeScoreCalculator = ResumeScoreCalculator(weights)
        max_score_per_category = 10
        resume_score, component_wise_score = resumeScoreCalculator.calculate_score(resume_score_description,
                                                                                   max_score_per_category)
        ## Update scoring data and include weights for those
        return resume_score, component_wise_score, resume_score_description
    except Exception as e:
        raise ResumeScoringException(f"Could not calculate score for the components in the resume!, {e}")

'''
Calculates the similarity score between the job description and resume content
'''
async def jd_resume_similarity_score_calculator(jd_json, resume_json, username):
    similarityScoreCalculationAgent = SimilarityScoreCalculationAgent()

    weights = {
        "experience": 8,
        "skills": 9,
        "projects": 7,
        "others": 5
    }

    similarity_score_input = {
        "job_description": jd_json,
        "resume_json": resume_json
    }
    try:
        ################## Hashing code
        content_hash = hashHandler.generate_hash(json.dumps(similarity_score_input).encode('utf-8'))
        print("content_hash", content_hash)

        complete_jd_json_level_cache_key = "calculate_jd_score_complete:" + username + ":" + content_hash
        cached_jd_json = cacheHandler.get_from_cache(complete_jd_json_level_cache_key, username=username,
                                                         expiry=expire_time)
        if cached_jd_json:
            print("Found cached extracted job description")
            similarity_score_description = cached_jd_json
        else:
            uncached_jd_score_json = dict()
            cached_jd_score_json = dict()

            #################### Check JD cache component-wise
            for key, val in jd_json.items():
                json_component_hash = hashHandler.generate_hash(json.dumps(val).encode('utf-8'))
                print("json_component_hash", json_component_hash)

                # component level
                component_wise_cache_key = "calculate_jd_score_partial_" + key + ":" + username + ":" + json_component_hash
                cached_resume_json = cacheHandler.get_from_cache(component_wise_cache_key, username=username, expiry=expire_time)
                if cached_resume_json:
                    print("Found cached resume score, component - " + key)
                    cached_jd_score_json[key] = cached_resume_json
                else:
                    uncached_jd_score_json[key] = val

            #################### Check JD cache component-wise

            similarity_jd_score_input = {
                "job_description": uncached_jd_score_json,
                "resume_json": resume_json
            }

            extracted_similarity_data = await similarityScoreCalculationAgent.calculate_similarity_score(
                similarity_jd_score_input)
            similarity_score_description = json.loads(extracted_similarity_data.messages[-1].content)
            # similarity_score_description = {"scoring_sections":[{"category":"Skills","similarity_score":4,"justification":"The candidate has experience with Git, HTML, and JavaScript which overlap with some of the skills listed in the job description. However, they lack direct experience in Java, Spring Boot, Hibernate, RESTful APIs, and SQL, which greatly reduces the score.","suggestions":["Gain experience with Java and Spring Boot through coursework or personal projects.","Complete relevant certifications or online courses focusing on RESTful APIs and SQL."]},{"category":"Experience","similarity_score":2,"justification":"The candidate's experience primarily revolves around cloud computing and cybersecurity, which are not directly aligned with the Java Developer role that emphasizes web application development. Their projects do not demonstrate relevant experience with the required technologies.","suggestions":["Seek internships or projects specifically focused on Java, Spring Boot, and web application development.","Participate in hackathons or coding competitions that involve Java development."]},{"category":"Projects","similarity_score":3,"justification":"While the candidate has relevant personal projects that involve web development components, they do not specifically align with the technologies and frameworks stated in the job description, such as Java or Spring Boot. The projects utilize React and Firebase instead.","suggestions":["Develop a project that utilizes Java and Spring Boot to showcase relevant skills.","Participate in collaborative coding projects with an emphasis on Java to broaden project experience."]},{"category":"Qualifications","similarity_score":6,"justification":"The candidate holds a Bachelor of Technology in Computer Science, which meets the educational requirement listed in the job description. They also possess a general understanding of object-oriented principles but lack specific experience in Java or Spring Boot.","suggestions":["Consider pursuing further education or certifications in Java/Spring Boot development to strengthen qualifications.","Engage in coursework that enhances knowledge of design patterns and databases."]}]}

            if "scoring_sections" in similarity_score_description:
                # Cache uncached components
                for key, val in uncached_jd_score_json.items():
                    # generate hash and link input to the output.
                    component_input_content = val
                    component_cache_content_filtered = [section for section in
                                                        similarity_score_description["scoring_sections"] if
                                                        section["category"] == key]
                    if len(component_cache_content_filtered) > 0:
                        json_component_wise_hash = hashHandler.generate_hash(
                            json.dumps(component_input_content).encode('utf-8'))

                        component_cache_content_json = component_cache_content_filtered[0]

                        component_wise_cache_key = "calculate_jd_score_partial_" + key + ":" + username + ":" + json_component_wise_hash
                        cache_response = cacheHandler.cache_data(key=component_wise_cache_key, data=component_cache_content_json, expiry=expire_time,
                                                                 username=username)
                        print("Cached extracted resume for id", component_wise_cache_key, cache_response)

            # Join with cached sections
            for key, val in cached_jd_score_json.items():
                similarity_score_description["scoring_sections"].append(val)
            # resume_score_description = {"scoring_sections":[{"category":"candidate_information","score":7.5,"justification":"The candidate information includes essential details such as name, contact number, email, and links to GitHub and LinkedIn. However, placeholder texts (e.g., 'xxxxxxxx' for contact number and 'GitHub Profile') reduce clarity and completeness.","improvement_suggestions":["Use actual contact details instead of placeholders.","Provide direct links to GitHub and LinkedIn profiles for easy access."]},{"category":"education","score":6.0,"justification":"The education section provides institutional details and degree info but lacks specifics such as the exact graduation date and CGPA values, which lowers its quality.","improvement_suggestions":["Replace 'xx' in CGPA with actual score.","Add the month and year of graduation for clarity."]},{"category":"experience","score":8.0,"justification":"Experience is well-detailed with roles, duration, and contributions outlined. However, both experiences are from the same company, leading to a possible perception of limited workplace exposure.","improvement_suggestions":["Include more diversity in companies or roles to show broader experience.","Highlight specific achievements or outcomes from these roles."]},{"category":"skills","score":9.0,"justification":"The skills section is comprehensive and covers a wide range of technical abilities. There are no major grammatical issues, but the formatting can be improved for readability.","improvement_suggestions":["Consider categorizing skills by proficiency or relevance (e.g., Programming Languages, Frameworks, Tools) for better organization."]},{"category":"personal_projects","score":7.0,"justification":"Personal projects are diverse and showcase the candidate's initiative. However, the 'duration' field is noted as 'NOT FOUND,' which diminishes clarity regarding commitment and completion.","improvement_suggestions":["Provide actual time frames for each project.","Include links to live projects or GitHub repositories for users to verify applications."]},{"category":"certifications","score":0.0,"justification":"There are no certifications listed in the resume, resulting in a complete absence of relevant credentials.","improvement_suggestions":["Obtain and include relevant certifications to enhance technical credibility."]},{"category":"achievements","score":0.0,"justification":"No achievements are mentioned, which is a significant missed opportunity as achievements can help demonstrate the candidate's impact and successes.","improvement_suggestions":["Add relevant achievements such as awards, recognitions, or milestones attained in academic or project environments."]},{"category":"company_projects","score":0.0,"justification":"There are no company projects listed. Company projects can provide insight into collaboration, responsibility, and professional experiences.","improvement_suggestions":["Include any significant company projects that demonstrate the ability to work in a team or lead tasks in a professional setting."]}]}

            cache_response = cacheHandler.cache_data(data=similarity_score_description,
                                                     key=complete_jd_json_level_cache_key,
                                                     expiry=expire_time, username=username)
            print("Cached complete resume score", complete_jd_json_level_cache_key, cache_response)


        jdResumeSimilarityScoreCalculator = JDResumeSimilarityScoreCalculator(weights)
        total_score, component_wise_score = jdResumeSimilarityScoreCalculator.calculate_score(
            score_info=similarity_score_description, max_score_per_category=10)


        return total_score, component_wise_score, similarity_score_description

        ################## Hashing code

    except Exception as e:
        raise SimilarityCalculationException(f"Could not calculate the similarity score between job description and resume!, {e}")


'''
Extract the resume data, job description and calculate resume and similarity score 
'''
async def process_resume(resume_file_path, raw_job_description, username):
    scoring_result = dict()
    scoring_result["components"] = []
    if resume_file_path:
        resume_content = await read_pdf(resume_file_path)
        extracted_resume_json = await extract_resume_description(raw_resume_data=resume_content, username=username, expiry=expire_time)
        resume_total_score, resume_component_wise_score, resume_score_description = await calculate_resume_score(resume_json = extracted_resume_json, username=username)

        scoring_result["resume_total_score"] = resume_total_score
        scoring_result["resume_component_wise_score"] = resume_component_wise_score
        scoring_result["components"].append("resume_description")

        if raw_job_description:
            extracted_jd = await extract_job_description(job_description=raw_job_description, username=username, expiry=expire_time)
            similarity_total_score, component_wise_score_similarity, similarity_score_description = await jd_resume_similarity_score_calculator(resume_json=extracted_resume_json, jd_json=extracted_jd, username=username)

            scoring_result["similarity_total_score"] = similarity_total_score
            scoring_result["component_wise_score_similarity"] = component_wise_score_similarity
            scoring_result["components"].append("similarity_description")
    x = 1
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
    job_description = """
    Responsibilities
    Develop, test, and maintain web applications using Java and Spring Boot.
    Collaborate with cross-functional teams to define and implement new features.
    Ensure the performance, quality, and responsiveness of applications.
    Identify and correct bottlenecks and fix bugs.
    Document development processes, coding standards, and project requirements.
    Participate in code reviews to ensure adherence to best practices and coding standards.
    Stay up-to-date with emerging technologies and industry trends.
    Qualifications
    Bachelor's degree in Computer Science, Information Technology, or related field.
    Proven experience as a Java Developer, with expertise in Spring Boot.
    Strong understanding of object-oriented programming principles and design patterns.
    Experience with databases such as MySQL, PostgreSQL, or MongoDB.
    Knowledge of front-end technologies like HTML, CSS, and JavaScript is a plus.
    Excellent problem-solving skills and attention to detail.
    Good communication and teamwork abilities.
    Skills
    Java
    Spring Boot
    Hibernate
    RESTful APIs
    SQL
    Git
    Maven
    Unit Testing
    """
    file_path = "C:\\Users\\Spandan\\Downloads\\70__ATS_rating_Resume_Template_test.pdf"
    username = "user123"
    response = asyncio.run(process_resume(resume_file_path=file_path, raw_job_description=job_description, username=username))
    print(response)