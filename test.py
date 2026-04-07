import asyncio
from src.main import process_resume, authenticate

if __name__ == "__main__":
    uploaded_resume_file = "C:\\Users\\spandan\\Downloads\\ML_Spandan_2_Page_resume_Internal_NTT (5).pdf"
    job_description = """
    Job Summary:
    We are seeking a skilled Generative AI Engineer to join our team to build innovative AI-driven applications. You will work on designing, training, and deploying advanced models to solve complex, real-world problems. The ideal candidate will bridge the gap between cutting-edge research and practical application, focusing on LLMs and generative models. 
    Key Responsibilities:
    Model Development: Design, fine-tune, and deploy generative models (e.g., GPT-4, Stable Diffusion, Llama 3) for text, image, or voice generation.
    Prompt Engineering: Develop and optimize advanced prompting strategies to maximize AI output quality.
    Application Integration: Integrate Generative AI models into production workflows and applications, utilizing APIs and microservices.
    Performance Optimization: Optimize existing models for latency, scalability, and cost-efficiency.
    Data Handling: Prepare and preprocess unstructured datasets for model training, ensuring data quality and safety.
    Research: Stay updated with the latest advancements in AI/ML to implement cutting-edge techniques.
    """
    username = "user111"
    response = asyncio.run(
        process_resume(resume_file_path=uploaded_resume_file, raw_job_description=job_description, username=username))
    x = 1