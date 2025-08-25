

class ResumeScoreCalculator:
    def __init__(self, weights):
        self.weights = weights

    def calculate_score(self, score_info, max_score_per_category):
        total_score = 0
        resume_score = 0
        component_wise_score = dict()
        for key, val in score_info.items():
            if key in self.weights:
                print(key, val["score"], "Weight - ", self.weights[key])
                resume_score += val["score"] * self.weights[key]
                total_score += max_score_per_category * self.weights[key]
                component_wise_score[key] = {
                    "weight": self.weights[key],
                    "component_score": val["score"]
                }
        x = 1
        return ((resume_score/total_score) * 100), component_wise_score


if __name__ == "__main__":
    weights = {
    "candidate_information" : 5,
    "education" : 6,
    "company_projects" : 3,
    "personal_projects" : 7,
    "skills" : 9,
    "experience" : 9,
    "achievements" : 4,
    "certifications" : 4,
    }
    resumeScoreCalculator = ResumeScoreCalculator(weights)
    dct = {"candidate_information":{"score":8.0,"justification":"The candidate information is mostly complete, including name, contact details, and links to professional profiles. However, it lacks more in-depth personal information that could enhance identification, such as address or a short personal statement.","improvement_suggestions":["Add a brief summary or objective statement that outlines career goals and aspirations.","Include a full address or at least city and state for geographical context.","Ensure that GitHub and LinkedIn profile links are actual URLs instead of placeholders."]},"education":{"score":7.5,"justification":"The education section contains relevant details about the degree, institution, duration, and field of study. However, the marks are not clearly presented, using a placeholder instead of an actual value.","improvement_suggestions":["Replace placeholder marks with actual CGPA or percentage if available.","Include any relevant coursework or projects that highlight skills learned during the education."]},"company_projects":{"score":2.0,"justification":"There are no entries in the company projects section, resulting in a low score. Company projects can significantly showcase practical experience and contributions.","improvement_suggestions":["Add at least one project from a company, detailing the project goals, your role, technologies used, and outcomes."]},"personal_projects":{"score":8.5,"justification":"The personal projects section is detailed with project names, descriptions, technologies used, and implementation methods. However, the 'duration' is marked as 'NOT FOUND' for all projects, which isn’t informative.","improvement_suggestions":["Provide the actual durations for each project, even if it's just the approximate time taken.","Highlight the impact or results of these projects, such as user adoption or performance improvements."]},"skills":{"score":9.0,"justification":"The skills section is extensive and covers a broad range of relevant technologies and programming languages, showcasing versatility. There are no apparent typos or errors.","improvement_suggestions":["Consider grouping skills into categories (e.g., programming languages, frameworks, databases) for clarity.","Prioritize or rank skills based on proficiency or relevance to the desired job."]},"experience":{"score":8.5,"justification":"The experience section is informative, outlining roles, contributions, and technologies. It effectively demonstrates relevant internships and the skills acquired during those roles. However, inclusion of technology used is missing in job details.","improvement_suggestions":["List any tools or technologies used in each internship role to enhance specificity and context.","Quantify achievements or contributions when possible (e.g., 'Improved system efficiency by 20%')."]},"achievements":{"score":1.0,"justification":"The achievements section is currently empty, leading to a low score. This section should ideally highlight awards or recognitions that complement professional experience.","improvement_suggestions":["Include any academic honors, scholarships, or relevant personal achievements that demonstrate expertise and motivation.","Consider adding certifications or recognitions, especially those related to technology or programming."]},"certifications":{"score":1.0,"justification":"The certifications section is empty, reflecting no formal certifications listed. Certifications can significantly validate skills, especially in technical fields.","improvement_suggestions":["Add any relevant certifications completed, such as AWS Certified Solutions Architect or other IT-related credentials.","Consider pursuing and highlighting certifications that are industry-recognized."]}}
    max_score_per_category = 10
    total_score, component_wise_score = resumeScoreCalculator.calculate_score(dct, max_score_per_category)
    print(total_score)
    print(component_wise_score)
    x = 1