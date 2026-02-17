import asyncio
import json
import inspect
import os
import sys

import logging

from config.database.MySQLDB import MysqlDB
from security.Auth import authenticate_user, create_access_token

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

current_directory = os.getcwd()
logger.info(f"Current working directory: {current_directory}")

# List all files and directories in the current directory
contents = os.listdir(current_directory)

logger.info("\nFiles and Directories (distinguished):")
for item in contents:
    path = os.path.join(current_directory, item)
    if os.path.isfile(path):
        logger.info(f"File: {item}")
    elif os.path.isdir(path):
        logger.info(f"Directory: {item}")

if source_file_name == "pages.py":
    # sys.path.append("src")
    config_file_path = 'config.properties'
    # print("configuring for pages.py caller")
    logger.info("configuring for pages.py caller")
    sys.path.append("src")
elif source_file_name == "main.py":
    config_file_path = '../config.properties'
    logger.info("configuring for main.py caller")
else:
    config_file_path = 'config.properties'
    logger.info("configuring for other callers")


# from components.agents.JDExtractionAgent import JDExtractionAgent
# from components.agents.ResumeScoringAgent import ResumeScoringAgent
# from components.agents.ResumeExtractionAgent import ResumeDataExtractingAgent
# from components.agents.SimilarityScoreCalculationAgent import SimilarityScoreCalculationAgent
# from components.utils.ResumeScoreCalculator import ResumeScoreCalculator
# from components.utils.JDResumeSimilarityScoreCalculator import JDResumeSimilarityScoreCalculator
# from components.utils.HashHandler import HashHandler
# from components.utils.CacheHandler import CacheHandler
# from components.exceptions.CustomExceptions import ResumeExtractionException, ResumeScoringException, JDExtractionException, SimilarityCalculationException
# from components.DataExtraction.PDFContentReader import PDFContentReader

from src.components.agents.JDExtractionAgent import JDExtractionAgent
from src.components.agents.ResumeScoringAgent import ResumeScoringAgent
from src.components.agents.ResumeExtractionAgent import ResumeDataExtractingAgent
from src.components.agents.SimilarityScoreCalculationAgent import SimilarityScoreCalculationAgent
from src.components.utils.ResumeScoreCalculator import ResumeScoreCalculator
from src.components.utils.JDResumeSimilarityScoreCalculator import JDResumeSimilarityScoreCalculator
from src.components.utils.HashHandler import HashHandler
from src.components.utils.CacheHandler import CacheHandler
from src.components.exceptions.CustomExceptions import ResumeExtractionException, ResumeScoringException, JDExtractionException, SimilarityCalculationException
from src.components.DataExtraction.PDFContentReader import PDFContentReader


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

# self.cnx = mysql.connector.connect(
#     host=props["mysql_hostname"],
#     port=props["mysql_port"],
#     user=props["mysql_username"],
#     password=props["mysql_password"],
#     database=props["mysql_database"]
# )

mysqlDB = MysqlDB(host = parser['MYSQL']['mysql_hostname'],
                port = parser['MYSQL']['mysql_port'],
                username = parser['MYSQL']['mysql_username'],
                password = parser['MYSQL']['mysql_password'],
                database = parser['MYSQL']['mysql_database'])

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
    logging.info("Called extract_resume_description()")
    resume_extractor = ResumeDataExtractingAgent()
    resume_data_raw_input = {
        "resume_content": raw_resume_data
    }
    try:
        content_hash = hashHandler.generate_hash(raw_resume_data.encode('utf-8'))
        # logging.info("content_hash")
        # logging.info(content_hash)

        cache_key = "extract_resume_description:" + username + ":" + content_hash
        cached_resume_json = cacheHandler.get_from_cache(cache_key, username, expiry)
        if cached_resume_json:
            logging.info("Found cached extracted resume")
            return cached_resume_json
        else:
            logging.info("Could not find cached extracted resume")
            extracted_resume_data = await resume_extractor.extract_resume(resume_data_raw_input)
            resume_json = json.loads(extracted_resume_data.messages[-1].content)
            cache_response = cacheHandler.cache_data(data=resume_json, key=cache_key, expiry=expire_time, username=username)
            logging.info("Cached extracted resume for id", cache_key, cache_response)
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
        # logging.info("resume_content")
        # logging.info(resume_content)
        extracted_resume_json = await extract_resume_description(raw_resume_data=resume_content, username=username, expiry=expire_time)
        # logging.info("extracted_resume_json")
        # logging.info(extracted_resume_json)
        resume_total_score, resume_component_wise_score, resume_score_description = await calculate_resume_score(resume_json = extracted_resume_json, username=username)
        # logging.info("resume_total_score, resume_component_wise_score, resume_score_description")
        # logging.info(resume_total_score)
        # logging.info(resume_component_wise_score)
        # logging.info(resume_score_description)

        scoring_result["resume_total_score"] = resume_total_score
        scoring_result["resume_component_wise_score"] = resume_component_wise_score
        scoring_result["components"].append("resume_description")

        if raw_job_description:
            extracted_jd = await extract_job_description(job_description=raw_job_description, username=username, expiry=expire_time)
            similarity_total_score, component_wise_score_similarity, similarity_score_description = await jd_resume_similarity_score_calculator(resume_json=extracted_resume_json, jd_json=extracted_jd, username=username)
            logging.info("similarity_total_score, component_wise_score_similarity, similarity_score_description")
            logging.info(similarity_total_score)
            logging.info(component_wise_score_similarity)
            logging.info(similarity_score_description)

            scoring_result["similarity_total_score"] = similarity_total_score
            scoring_result["component_wise_score_similarity"] = component_wise_score_similarity
            scoring_result["components"].append("similarity_description")
    x = 1
    return scoring_result

'''
Authenticate user
'''
async def authenticate(username, password):
    response = authenticate_user(username, password, mysqlDB)
    if response:
        print("main - authenticate()")
        print(response)
        data = {"sub": username}
        token = create_access_token(data, parser['ENCRYPTION']['SECRET_KEY'], parser['ENCRYPTION']['ALGORITHM'], int(parser['ENCRYPTION']['ACCESS_TOKEN_EXPIRE_MINUTES']))
        return token
    return response

if __name__ == "__main__":
    resume_data = """
    

    """
    job_description = """
    Responsibilities
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
    file_path = "path.pdf"
    username = "user123"
    response = asyncio.run(process_resume(resume_file_path=file_path, raw_job_description=job_description, username=username))
    print(response)