

class ResumeScoreCalculator:
    def __init__(self, weights):
        self.weights = weights

    def calculate_score(self, score_info, max_score_per_category):
        total_score = 0
        resume_score = 0
        resume_analysis = []
        for section in score_info["scoring_sections"]:
            temp_dict = dict(section)
            if section["category"].lower() in self.weights:
                print(section["category"].lower(), section["score"], "Weight - ", self.weights[section["category"].lower()])
                resume_score += section["score"] * self.weights[section["category"].lower()]
                total_score += max_score_per_category * self.weights[section["category"].lower()]

                temp_dict["weight"] = self.weights[section["category"].lower()]
                temp_dict["total_score"] = max_score_per_category

            else:
                print(section["category"].lower(), section["score"], "Weight - ",
                      self.weights["others"])
                resume_score += section["score"] * self.weights["others"]
                total_score += max_score_per_category * self.weights["others"]

                temp_dict["weight"] = self.weights["others"]
                temp_dict["total_score"] = max_score_per_category
            resume_analysis.append(temp_dict)
        x = 1
        if total_score == 0:
            return 0, []
        return ((resume_score/total_score) * 100), resume_analysis

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
    resume_score_description = {'scoring_sections': [
            {'category': 'candidate_information', 'score': 7.5, 'justification': "The candidate information includes essential details such as name, contact number, email, and links to GitHub and LinkedIn. However, placeholder texts (e.g., 'xxxxxxxx' for contact number and 'GitHub Profile') reduce clarity and completeness.", 'improvement_suggestions': ['Use actual contact details instead of placeholders.', 'Provide direct links to GitHub and LinkedIn profiles for easy access.'
                ]
            },
            {'category': 'education', 'score': 6.0, 'justification': 'The education section provides institutional details and degree info but lacks specifics such as the exact graduation date and CGPA values, which lowers its quality.', 'improvement_suggestions': [
                    "Replace 'xx' in CGPA with actual score.", 'Add the month and year of graduation for clarity.'
                ]
            },
            {'category': 'experience', 'score': 8.0, 'justification': 'Experience is well-detailed with roles, duration, and contributions outlined. However, both experiences are from the same company, leading to a possible perception of limited workplace exposure.', 'improvement_suggestions': ['Include more diversity in companies or roles to show broader experience.', 'Highlight specific achievements or outcomes from these roles.'
                ]
            },
            {'category': 'skills', 'score': 9.0, 'justification': 'The skills section is comprehensive and covers a wide range of technical abilities. There are no major grammatical issues, but the formatting can be improved for readability.', 'improvement_suggestions': ['Consider categorizing skills by proficiency or relevance (e.g., Programming Languages, Frameworks, Tools) for better organization.'
                ]
            },
            {'category': 'personal_projects', 'score': 7.0, 'justification': "Personal projects are diverse and showcase the candidate's initiative. However, the 'duration' field is noted as 'NOT FOUND,' which diminishes clarity regarding commitment and completion.", 'improvement_suggestions': ['Provide actual time frames for each project.', 'Include links to live projects or GitHub repositories for users to verify applications.'
                ]
            },
            {'category': 'certifications', 'score': 0.0, 'justification': 'There are no certifications listed in the resume, resulting in a complete absence of relevant credentials.', 'improvement_suggestions': ['Obtain and include relevant certifications to enhance technical credibility.'
                ]
            },
            {'category': 'achievements', 'score': 0.0, 'justification': "No achievements are mentioned, which is a significant missed opportunity as achievements can help demonstrate the candidate's impact and successes.", 'improvement_suggestions': ['Add relevant achievements such as awards, recognitions, or milestones attained in academic or project environments.'
                ]
            },
            {'category': 'company_projects', 'score': 0.0, 'justification': 'There are no company projects listed. Company projects can provide insight into collaboration, responsibility, and professional experiences.', 'improvement_suggestions': ['Include any significant company projects that demonstrate the ability to work in a team or lead tasks in a professional setting.'
                ]
            }
        ]
    }
    max_score_per_category = 10
    # total_score, component_wise_score = resumeScoreCalculator.calculate_score(resume_score_description, max_score_per_category)
    total_score = 58.62
    resume_component_wise_score = [{'category': 'candidate_information', 'improvement_suggestions': ['Use actual contact details instead of placeholders.', 'Provide direct links to GitHub and LinkedIn profiles for easy access.'], 'justification': "The candidate information includes essential details such as name, contact number, email, and links to GitHub and LinkedIn. However, placeholder texts (e.g., 'xxxxxxxx' for contact number and 'GitHub Profile') reduce clarity and completeness.", 'score': 7.5, 'total_score': 10, 'weight': 5},
{'category': 'education', 'improvement_suggestions': ["Replace 'xx' in CGPA with actual score.", 'Add the month and year of graduation for clarity.'], 'justification': 'The education section provides institutional details and degree info but lacks specifics such as the exact graduation date and CGPA values, which lowers its quality.', 'score': 6.0, 'total_score': 10, 'weight': 6},
{'category': 'experience', 'improvement_suggestions': ['Include more diversity in companies or roles to show broader experience.', 'Highlight specific achievements or outcomes from these roles.'], 'justification': 'Experience is well-detailed with roles, duration, and contributions outlined. However, both experiences are from the same company, leading to a possible perception of limited workplace exposure.', 'score': 8.0, 'total_score': 10, 'weight': 9},
{'category': 'skills', 'improvement_suggestions': ['Consider categorizing skills by proficiency or relevance (e.g., Programming Languages, Frameworks, Tools) for better organization.'], 'justification': 'The skills section is comprehensive and covers a wide range of technical abilities. There are no major grammatical issues, but the formatting can be improved for readability.', 'score': 9.0, 'total_score': 10, 'weight': 9},
{'category': 'personal_projects', 'improvement_suggestions': ['Provide actual time frames for each project.', 'Include links to live projects or GitHub repositories for users to verify applications.'], 'justification': "Personal projects are diverse and showcase the candidate's initiative. However, the 'duration' field is noted as 'NOT FOUND,' which diminishes clarity regarding commitment and completion.", 'score': 7.0, 'total_score': 10, 'weight': 7},
{'category': 'certifications', 'improvement_suggestions': ['Obtain and include relevant certifications to enhance technical credibility.'], 'justification': 'There are no certifications listed in the resume, resulting in a complete absence of relevant credentials.', 'score': 0.0, 'total_score': 10, 'weight': 4},
{'category': 'achievements', 'improvement_suggestions': ['Add relevant achievements such as awards, recognitions, or milestones attained in academic or project environments.'], 'justification': "No achievements are mentioned, which is a significant missed opportunity as achievements can help demonstrate the candidate's impact and successes.", 'score': 0.0, 'total_score': 10, 'weight': 4},
{'category': 'company_projects', 'improvement_suggestions': ['Include any significant company projects that demonstrate the ability to work in a team or lead tasks in a professional setting.'], 'justification': 'There are no company projects listed. Company projects can provide insight into collaboration, responsibility, and professional experiences.', 'score': 0.0, 'total_score': 10, 'weight': 3}]
    print(total_score)
    # updated_resume_analysis = resumeScoreCalculator.club_with_suggestions(resume_component_wise_score, resume_score_description)
    print(resume_component_wise_score)
    x = 1