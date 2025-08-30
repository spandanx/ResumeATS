

class JDResumeSimilarityScoreCalculator:
    def __init__(self, weights):
        self.weights = weights

    def calculate_score(self, score_info, max_score_per_category):
        total_score = 0
        similarity_score = 0
        similarity_analysis = []
        for section in score_info["scoring_sections"]:
            temp_dict = dict(section)
            if section["category"].lower() in self.weights:
                print(section["category"], section["similarity_score"], "Weight - ", self.weights[section["category"].lower()])
                similarity_score += section["similarity_score"] * self.weights[section["category"].lower()]
                total_score += max_score_per_category * self.weights[section["category"].lower()]

                temp_dict["weight"] = self.weights[section["category"].lower()]
                temp_dict["total_score"] = max_score_per_category

            else:
                print(section["category"].lower(), section["similarity_score"], "Weight - ",
                      self.weights["others"])
                similarity_score += section["similarity_score"] * self.weights["others"]
                total_score += max_score_per_category * self.weights["others"]

                temp_dict["weight"] = self.weights["others"]
                temp_dict["total_score"] = max_score_per_category

            similarity_analysis.append(temp_dict)

        if total_score == 0:
            return 0, []
        return ((similarity_score/total_score) * 100), similarity_analysis

if __name__ == "__main__":
    weights = {
    "experience" : 8,
    "skills" : 9,
    "projects" : 7,
    "others" : 5
    }
    similarityScoreCalculator = JDResumeSimilarityScoreCalculator(weights)
    similarity_score_description = {"scoring_sections":[
        {"category":"skills","similarity_score":4,"justification":"The candidate has experience with Git, HTML, and JavaScript which overlap with some of the skills listed in the job description. However, they lack direct experience in Java, Spring Boot, Hibernate, RESTful APIs, and SQL, which greatly reduces the score.","suggestions":["Gain experience with Java and Spring Boot through coursework or personal projects.","Complete relevant certifications or online courses focusing on RESTful APIs and SQL."]},
        {"category":"experience","similarity_score":2,"justification":"The candidate's experience primarily revolves around cloud computing and cybersecurity, which are not directly aligned with the Java Developer role that emphasizes web application development. Their projects do not demonstrate relevant experience with the required technologies.","suggestions":["Seek internships or projects specifically focused on Java, Spring Boot, and web application development.","Participate in hackathons or coding competitions that involve Java development."]},
        {"category":"projects","similarity_score":3,"justification":"While the candidate has relevant personal projects that involve web development components, they do not specifically align with the technologies and frameworks stated in the job description, such as Java or Spring Boot. The projects utilize React and Firebase instead.","suggestions":["Develop a project that utilizes Java and Spring Boot to showcase relevant skills.","Participate in collaborative coding projects with an emphasis on Java to broaden project experience."]},
        {"category":"qualifications","similarity_score":6,"justification":"The candidate holds a Bachelor of Technology in Computer Science, which meets the educational requirement listed in the job description. They also possess a general understanding of object-oriented principles but lack specific experience in Java or Spring Boot.","suggestions":["Consider pursuing further education or certifications in Java/Spring Boot development to strengthen qualifications.","Engage in coursework that enhances knowledge of design patterns and databases."]}]}
    max_score_per_category = 10
    total_score, similarity_component_wise_score = similarityScoreCalculator.calculate_score(similarity_score_description, max_score_per_category)
    # updated_similarity_analysis = similarityScoreCalculator.club_with_suggestions(similarity_component_wise_score, similarity_score_description)
    print(total_score)
    print(similarity_component_wise_score)
    x = 1