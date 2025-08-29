import streamlit as st

import asyncio
from src.main import process_resume

import pandas as pd
from numpy.random import default_rng as rng
import plotly.express as px

# import sys
# sys.path.append('src.components.schemas')

st.title("Resume ATS scorer")
st.markdown("""
This application calculates resume score and gets you suggestion on the possible changes in the resume.
It also reads job descriptions and calculates similarity score.
""")

uploaded_resume_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

job_description = st.text_area("Enter your job description:", "")

if st.button("Calculate Score"):
    if not uploaded_resume_file:
        st.markdown(":red[File Not found]")
    else:
        # response = asyncio.run(process_resume(resume_file_path=uploaded_resume_file, raw_job_description=job_description))
        response = {'components': ['resume_description', 'similarity_description'], 'resume_total_score': 58.61702127659575, 'resume_component_wise_score': {'candidate_information': {'weight': 5, 'component_score': 7.5, 'total_score': 10}, 'education': {'weight': 6, 'component_score': 6.0, 'total_score': 10}, 'experience': {'weight': 9, 'component_score': 8.0, 'total_score': 10}, 'skills': {'weight': 9, 'component_score': 9.0, 'total_score': 10}, 'personal_projects': {'weight': 7, 'component_score': 7.0, 'total_score': 10}, 'certifications': {'weight': 4, 'component_score': 0.0, 'total_score': 10}, 'achievements': {'weight': 4, 'component_score': 0.0, 'total_score': 10}, 'company_projects': {'weight': 3, 'component_score': 0.0, 'total_score': 10}}, 'resume_score_description': {'scoring_sections': [{'category': 'candidate_information', 'score': 7.5, 'justification': "The candidate information includes essential details such as name, contact number, email, and links to GitHub and LinkedIn. However, placeholder texts (e.g., 'xxxxxxxx' for contact number and 'GitHub Profile') reduce clarity and completeness.", 'improvement_suggestions': ['Use actual contact details instead of placeholders.', 'Provide direct links to GitHub and LinkedIn profiles for easy access.']}, {'category': 'education', 'score': 6.0, 'justification': 'The education section provides institutional details and degree info but lacks specifics such as the exact graduation date and CGPA values, which lowers its quality.', 'improvement_suggestions': ["Replace 'xx' in CGPA with actual score.", 'Add the month and year of graduation for clarity.']}, {'category': 'experience', 'score': 8.0, 'justification': 'Experience is well-detailed with roles, duration, and contributions outlined. However, both experiences are from the same company, leading to a possible perception of limited workplace exposure.', 'improvement_suggestions': ['Include more diversity in companies or roles to show broader experience.', 'Highlight specific achievements or outcomes from these roles.']}, {'category': 'skills', 'score': 9.0, 'justification': 'The skills section is comprehensive and covers a wide range of technical abilities. There are no major grammatical issues, but the formatting can be improved for readability.', 'improvement_suggestions': ['Consider categorizing skills by proficiency or relevance (e.g., Programming Languages, Frameworks, Tools) for better organization.']}, {'category': 'personal_projects', 'score': 7.0, 'justification': "Personal projects are diverse and showcase the candidate's initiative. However, the 'duration' field is noted as 'NOT FOUND,' which diminishes clarity regarding commitment and completion.", 'improvement_suggestions': ['Provide actual time frames for each project.', 'Include links to live projects or GitHub repositories for users to verify applications.']}, {'category': 'certifications', 'score': 0.0, 'justification': 'There are no certifications listed in the resume, resulting in a complete absence of relevant credentials.', 'improvement_suggestions': ['Obtain and include relevant certifications to enhance technical credibility.']}, {'category': 'achievements', 'score': 0.0, 'justification': "No achievements are mentioned, which is a significant missed opportunity as achievements can help demonstrate the candidate's impact and successes.", 'improvement_suggestions': ['Add relevant achievements such as awards, recognitions, or milestones attained in academic or project environments.']}, {'category': 'company_projects', 'score': 0.0, 'justification': 'There are no company projects listed. Company projects can provide insight into collaboration, responsibility, and professional experiences.', 'improvement_suggestions': ['Include any significant company projects that demonstrate the ability to work in a team or lead tasks in a professional setting.']}]}, 'similarity_total_score': 35.51724137931034, 'component_wise_score_similarity': {'skills': {'weight': 9, 'component_score': 4, 'total_score': 10}, 'experience': {'weight': 8, 'component_score': 2, 'total_score': 10}, 'projects': {'weight': 7, 'component_score': 3, 'total_score': 10}, 'qualifications': {'weight': 5, 'component_score': 6, 'total_score': 10}}, 'similarity_score_description': {'scoring_sections': [{'category': 'Skills', 'similarity_score': 4, 'justification': 'The candidate has experience with Git, HTML, and JavaScript which overlap with some of the skills listed in the job description. However, they lack direct experience in Java, Spring Boot, Hibernate, RESTful APIs, and SQL, which greatly reduces the score.', 'suggestions': ['Gain experience with Java and Spring Boot through coursework or personal projects.', 'Complete relevant certifications or online courses focusing on RESTful APIs and SQL.']}, {'category': 'Experience', 'similarity_score': 2, 'justification': "The candidate's experience primarily revolves around cloud computing and cybersecurity, which are not directly aligned with the Java Developer role that emphasizes web application development. Their projects do not demonstrate relevant experience with the required technologies.", 'suggestions': ['Seek internships or projects specifically focused on Java, Spring Boot, and web application development.', 'Participate in hackathons or coding competitions that involve Java development.']}, {'category': 'Projects', 'similarity_score': 3, 'justification': 'While the candidate has relevant personal projects that involve web development components, they do not specifically align with the technologies and frameworks stated in the job description, such as Java or Spring Boot. The projects utilize React and Firebase instead.', 'suggestions': ['Develop a project that utilizes Java and Spring Boot to showcase relevant skills.', 'Participate in collaborative coding projects with an emphasis on Java to broaden project experience.']}, {'category': 'Qualifications', 'similarity_score': 6, 'justification': 'The candidate holds a Bachelor of Technology in Computer Science, which meets the educational requirement listed in the job description. They also possess a general understanding of object-oriented principles but lack specific experience in Java or Spring Boot.', 'suggestions': ['Consider pursuing further education or certifications in Java/Spring Boot development to strengthen qualifications.', 'Engage in coursework that enhances knowledge of design patterns and databases.']}]}}
        # st.markdown(response)
        if len(response["components"]) == 2:
            col1, col2 = st.columns(2)
            with col1:
                st.header("Resume Score")
                # st.write(response["resume_score_description"])
                # resume_dict = response["resume_component_wise_score"]
                df = pd.DataFrame(
                {
                    "Features": [key for key, val in response["resume_component_wise_score"].items()],
                    "Scores": [val["component_score"] for key, val in
                               response["resume_component_wise_score"].items()]
                }
                )

                st.bar_chart(df, x="Features", y="Scores")

                data = {'category': ['A', 'B', 'C', 'D'],
                        'value': [30, 20, 40, 10]}
                df_pie = pd.DataFrame(data)
                fig = px.pie(df_pie, values='value', names='category', title='My Pie Chart')
                st.plotly_chart(fig)

            with col2:
                st.header("Similarity Score")

                # st.write(response["similarity_score_description"])
                df = pd.DataFrame(
                    {
                        "Features": [key for key, val in response["component_wise_score_similarity"].items()],
                        "Scores": [val["component_score"] for key, val in
                                   response["component_wise_score_similarity"].items()]
                    }
                )

                st.bar_chart(df, x="Features", y="Scores")

        elif len(response["components"]) == 0:
            st.markdown(":red[Could not analyse the resume]")

        elif "resume_description" in response["components"]:
            st.header("Resume Score")
            st.write(response["resume_score_description"])

        elif "similarity_description" in response["components"]:
            st.header("Similarity Score")
            st.write(response["similarity_score_description"])


