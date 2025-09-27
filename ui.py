import streamlit as st

import asyncio
from src.main import process_resume

import pandas as pd
import random
# from numpy.random import default_rng as rng
# import plotly.express as px
import plotly.graph_objects as go

# import sys
# sys.path.append('src.components.schemas')

def generate_random_color():
    return f'#{random.randint(0, 0xFFFFFF):06x}'

st.set_page_config(page_title="Resume ATS Application")

st.title("Resume ATS scorer")
st.set_page_config(layout="wide")
st.markdown("""
This application calculates resume score and gets you suggestion on the possible changes in the resume.
It also reads job descriptions and calculates similarity score.
Version: 1.4
""")

input_tab, analytics_tab = st.tabs(["Resume Input", "Analytics"])

response = {}

username = "user123"

with input_tab:

    uploaded_resume_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

    job_description = st.text_area("Enter your job description:", "")

    if st.button("Calculate Score"):
        if not uploaded_resume_file:
            st.markdown(":red[File Not found]")
        else:
            try:
                response = asyncio.run(process_resume(resume_file_path=uploaded_resume_file, raw_job_description=job_description, username=username))
                # response = {'components': ['resume_description', 'similarity_description'],
                # 'resume_total_score': 58.61702127659575,
                # 'resume_component_wise_score': [
                #     {'category': 'candidate_information', 'score': 7.5, 'justification': "The candidate information includes essential details such as name, contact number, email, and links to GitHub and LinkedIn. However, placeholder texts (e.g., 'xxxxxxxx' for contact number and 'GitHub Profile') reduce clarity and completeness.", 'improvement_suggestions': ['Use actual contact details instead of placeholders.', 'Provide direct links to GitHub and LinkedIn profiles for easy access.'], 'weight': 5, 'total_score': 10},
                #     {'category': 'education', 'score': 6.0, 'justification': 'The education section provides institutional details and degree info but lacks specifics such as the exact graduation date and CGPA values, which lowers its quality.', 'improvement_suggestions': ["Replace 'xx' in CGPA with actual score.", 'Add the month and year of graduation for clarity.'], 'weight': 6, 'total_score': 10},
                #     {'category': 'experience', 'score': 8.0, 'justification': 'Experience is well-detailed with roles, duration, and contributions outlined. However, both experiences are from the same company, leading to a possible perception of limited workplace exposure.', 'improvement_suggestions': ['Include more diversity in companies or roles to show broader experience.', 'Highlight specific achievements or outcomes from these roles.'], 'weight': 9, 'total_score': 10},
                #     {'category': 'skills', 'score': 9.0, 'justification': 'The skills section is comprehensive and covers a wide range of technical abilities. There are no major grammatical issues, but the formatting can be improved for readability.', 'improvement_suggestions': ['Consider categorizing skills by proficiency or relevance (e.g., Programming Languages, Frameworks, Tools) for better organization.'], 'weight': 9, 'total_score': 10},
                #     {'category': 'personal_projects', 'score': 7.0, 'justification': "Personal projects are diverse and showcase the candidate's initiative. However, the 'duration' field is noted as 'NOT FOUND,' which diminishes clarity regarding commitment and completion.", 'improvement_suggestions': ['Provide actual time frames for each project.', 'Include links to live projects or GitHub repositories for users to verify applications.'], 'weight': 7, 'total_score': 10},
                #     {'category': 'certifications', 'score': 0.0, 'justification': 'There are no certifications listed in the resume, resulting in a complete absence of relevant credentials.', 'improvement_suggestions': ['Obtain and include relevant certifications to enhance technical credibility.'], 'weight': 4, 'total_score': 10},
                #     {'category': 'achievements', 'score': 0.0, 'justification': "No achievements are mentioned, which is a significant missed opportunity as achievements can help demonstrate the candidate's impact and successes.", 'improvement_suggestions': ['Add relevant achievements such as awards, recognitions, or milestones attained in academic or project environments.'], 'weight': 4, 'total_score': 10},
                #     {'category': 'company_projects', 'score': 0.0, 'justification': 'There are no company projects listed. Company projects can provide insight into collaboration, responsibility, and professional experiences.', 'improvement_suggestions': ['Include any significant company projects that demonstrate the ability to work in a team or lead tasks in a professional setting.'], 'weight': 3, 'total_score': 10}],
                # 'similarity_total_score': 35.51724137931034,
                # 'component_wise_score_similarity': [
                #     {'category': 'skills', 'similarity_score': 4, 'justification': 'The candidate has experience with Git, HTML, and JavaScript which overlap with some of the skills listed in the job description. However, they lack direct experience in Java, Spring Boot, Hibernate, RESTful APIs, and SQL, which greatly reduces the score.', 'suggestions': ['Gain experience with Java and Spring Boot through coursework or personal projects.', 'Complete relevant certifications or online courses focusing on RESTful APIs and SQL.'], 'weight': 9, 'total_score': 10},
                #     {'category': 'experience', 'similarity_score': 2, 'justification': "The candidate's experience primarily revolves around cloud computing and cybersecurity, which are not directly aligned with the Java Developer role that emphasizes web application development. Their projects do not demonstrate relevant experience with the required technologies.", 'suggestions': ['Seek internships or projects specifically focused on Java, Spring Boot, and web application development.', 'Participate in hackathons or coding competitions that involve Java development.'], 'weight': 8, 'total_score': 10},
                #     {'category': 'projects', 'similarity_score': 3, 'justification': 'While the candidate has relevant personal projects that involve web development components, they do not specifically align with the technologies and frameworks stated in the job description, such as Java or Spring Boot. The projects utilize React and Firebase instead.', 'suggestions': ['Develop a project that utilizes Java and Spring Boot to showcase relevant skills.', 'Participate in collaborative coding projects with an emphasis on Java to broaden project experience.'], 'weight': 7, 'total_score': 10},
                #     {'category': 'qualifications', 'similarity_score': 6, 'justification': 'The candidate holds a Bachelor of Technology in Computer Science, which meets the educational requirement listed in the job description. They also possess a general understanding of object-oriented principles but lack specific experience in Java or Spring Boot.', 'suggestions': ['Consider pursuing further education or certifications in Java/Spring Boot development to strengthen qualifications.', 'Engage in coursework that enhances knowledge of design patterns and databases.'], 'weight': 5, 'total_score': 10}
                # ]}
                # st.markdown(response)
            except Exception as e:
                st.markdown(f":red[Something is wrong! Could not perform the analysis] \n {e}")

with analytics_tab:
    if "components" in response and len(response["components"]) == 2:
        resume_tab, similaity_tab = st.tabs(["Resume Score", "Similarity Score"])

        with resume_tab:
            # st.write(response["resume_score_description"])
            # resume_dict = response["resume_component_wise_score"]

            ############### Donut chart ###############

            # labels = [label["category"] for label in response["resume_component_wise_score"]]
            labels = ["Resume score", "Scope of improvements"]
            # labels.append("scope of improvements")
            # labels = ['resume score', 'scope of improvements']

            # values = [label["score"] for label in response["resume_component_wise_score"]]
            values = [response["resume_total_score"], 100 - response["resume_total_score"]]
            # values.append(100 - response["resume_total_score"])
            # values = [response["resume_total_score"], 100 - response["resume_total_score"]]
            colors = ['rgb(43, 171, 103)', 'rgb(138, 150, 144)']

            # colors = [generate_random_color() for _ in range(2)]

            # Use `hole` to create a donut-like pie chart
            # fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors)])
            resume_donut_chart_column, resume_line_chart_column = st.columns([1, 1])

            with resume_donut_chart_column:
                ############### Donut chart ###############
                fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors)])
                fig.update_traces(hoverinfo='label+percent', textinfo='none', hole=.8)
                fig.update_layout(
                    annotations=[dict(text=(str(round(response["resume_total_score"], 2))), x=0.5, y=0.5,
                                      font_size=20, showarrow=False, xanchor="center"),
                                 dict(text="TOTAL", x=0.5, y=0.4,
                                      font_size=20, showarrow=False, xanchor="center")
                                 ])
                st.plotly_chart(fig)
                ############### Donut chart ###############

            with resume_line_chart_column:

                ############### Line chart ################
                df = pd.DataFrame(
                    {
                        "Sections": [section["category"] for section in response["resume_component_wise_score"]],
                        "Scores": [section["score"] for section in
                                   response["resume_component_wise_score"]],
                        "Colors": [generate_random_color() for _ in range(len(response["resume_component_wise_score"]))]
                    }
                )

                # st.bar_chart(df, x="Features", y="Scores")
                st.bar_chart(df, x="Sections", y="Scores", color="Colors")

                ############### Line chart ################

            ############## Columns ##############
            st.divider()
            for resume_section in response["resume_component_wise_score"]:
                line_col, description_col = st.columns([0.2, 0.8])

                with line_col:
                    st.progress(int(resume_section["score"]) * 10, text=resume_section["category"] + " | Score - :red[" + str(int(resume_section["score"])) + "]")
                    # st.markdown("")

                with description_col:
                    st.markdown(resume_section["justification"])

                    with st.expander("Suggestions"):
                        st.write('\n'.join([" - " + suggestion for suggestion in resume_section["improvement_suggestions"]]))

                st.divider()
            ############## Containers ##############

            ############### Pie chart ###############
            # data = {'category': ['A', 'B', 'C', 'D'],
            #         'value': [30, 20, 40, 10]}
            # df_pie = pd.DataFrame(data)
            # fig = px.pie(df_pie, values='value', names='category', title='My Pie Chart')
            # st.plotly_chart(fig)
            ############### Pie chart ###############

        with similaity_tab:
            labels = [section["category"] for section in response["component_wise_score_similarity"]]

            values = [section["similarity_score"] for section in response["component_wise_score_similarity"]]
            # colors = ['rgb(33, 75, 99)', 'rgb(18, 36, 37)']

            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_traces(hoverinfo="label+value", textinfo='label+value', hole=.8)
            fig.update_layout(
                annotations=[dict(text=(str(round(response["similarity_total_score"], 2))), x=0.5, y=0.5,
                                  font_size=20, showarrow=False, xanchor="center"),
                             dict(text="OVERALL", x=0.5, y=0.4,
                                  font_size=20, showarrow=False, xanchor="center")
                             ])
            st.plotly_chart(fig)

            ################ Suggestions ##############
            st.divider()
            for resume_section in response["component_wise_score_similarity"]:
                line_col, description_col = st.columns([0.2, 0.8])

                with line_col:
                    st.progress(int(resume_section["similarity_score"]) * 10,
                                text=resume_section["category"] + " | Score - :red[" + str(
                                    int(resume_section["similarity_score"])) + "]")
                    # st.markdown("")

                with description_col:
                    st.markdown(resume_section["justification"])

                    with st.expander("Suggestions"):
                        st.write(
                            '\n'.join([" - " + suggestion for suggestion in resume_section["suggestions"]]))

                st.divider()
            ################ Suggestions ##############

    elif "components" in response and len(response["components"]) == 0:
        st.markdown(":red[Could not analyse the resume]")

    elif "components" in response and "resume_description" in response["components"]:
        st.header("Resume Score")
        st.write(response["resume_score_description"])

    elif "components" in response and "similarity_description" in response["components"]:
        st.header("Similarity Score")
        st.write(response["similarity_score_description"])


