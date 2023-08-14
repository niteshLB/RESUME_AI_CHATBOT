

from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
from IPython.display import Markdown, display

def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

    index.save_to_disk('resume.json')

    return index



def ask_ai():
    index = GPTSimpleVectorIndex.load_from_disk('resume.json')
    default_questions = [
        "Tell me about yourself.",
        "What is your greatest strength?",
        "What is your biggest weakness?",
        "Why do you want to work here?",
        "Can you describe a challenging situation you've faced at work and how you handled it?",
        "Where do you see yourself in five years?",
        "Do you have any questions for us?"
    ]
    
    job_description_question = "What is the job description?"
    predefined_job_description_prompt = """
       
Job Description:
We are looking for an experienced Full Stack Engineer to join our development team. In this role, you will be responsible for the overall development and implementation of front and back-end software applications. Your responsibilities will extend from designing system architecture to high-level programming, performance testing, and systems integration. To ensure success as a full stack engineer, you should have advanced programming skills, experience with application development, and excellent troubleshooting skills. Top-rated full stack engineers create and implement advanced software systems that perfectly meet the needs of the company.

Responsibilities:
- Meeting with the software development team to define the scope and scale of software projects.
- Designing software system architecture.
.
- Writing technical documents.

Qualifications:
- Bachelor’s degree in computer engineering or computer science.
- Previous experience as a full stack engineer.


Skills:
- Strong problem-solving abilities.
- Team player with excellent interpersonal skills.


To apply, please submit your resume and a cover letter detailing your relevant experience and qualifications.

Location: [Lakebrains Technologu,Udaipur]
Contact NUmber:+919664353500
    """
    
    documents = SimpleDirectoryReader("C:/Users/nites/OneDrive/Desktop/AI_CHATBOT/resume").load_data()  # Update the path
    
    print("Options:")
    print("1. Ask a question")
    print("2. Select a resume")
    print("3. Exit")
    
    while True:
        choice = input("Enter the number of your choice: ")
        
        if choice == "1":
            query = input("What do you want to ask? ")
            if query.lower() == "what is the job description?":
                print(predefined_job_description_prompt)
            else:
                response = index.query(query)
                print("Response:", response.response)
            
        elif choice == "2":
            print("Select a resume:")
            for i, resume in enumerate(documents, start=1):
                print(f"{i}. {resume}")
            
            resume_choice = input("Enter the number of the resume you want to select: ")
            
            try:
                resume_index = int(resume_choice) - 1
                selected_resume = documents[resume_index]
            except (ValueError, IndexError):
                print("Invalid choice. Please enter a valid number.")
                continue
            
            print(f"Selected resume: {selected_resume}")
            
            # job_description_response = index.query(f"{job_description_question} {selected_resume}")
            # print(f"Job Description Prompt: {job_description_question}\nResponse: {job_description_response.response}\n")
            print(predefined_job_description_prompt)
            
            for question in default_questions:
                response = index.query(f"{question} {selected_resume}")
                print(f"Question: {question}\nResponse: {response.response}\n")
            
        elif choice == "3":
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please enter a valid number.")

os.environ["OPENAI_API_KEY"] = "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"
construct_index("resume")
ask_ai()



