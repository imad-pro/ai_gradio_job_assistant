from g4f.client import Client
import gradio as gr
from langdetect import detect

# Initialize the client outside of the if statement
client = Client()

def chatbot_response(job_description, cv):
    # Your predefined prompt
    initial_prompt = """
    You are an expert career coach who provides personalized and humanized responses. Given the following job description and CV, generate a comprehensive interview preparation guide. Focus on helping the candidate tell their experience and skills as a story that addresses the company's pain points. Address the candidate personally as "you" to create a coaching-like feel. Please Fill every requirement here and make your answer look like a real human expert really reflecting and iterating before giving a humanized, simple, concise and really insightful interview preparation

    ### Sections:

    1. **Self-Presentation:**
       - Present the candidate's experience as a concise and specific story related to the job.
       - Use the “SHE” formula: Succinct, Honest, Engaging.
       - Highlight required skills and experiences from the job description.
       - Provide examples that show problem-solving and interpersonal skills.

    2. **Company's Challenges & Candidate as a Solution:**
       - Analyze potential challenges the company might face.
       - Explain how the candidate’s skills and experiences make them a solution to these challenges.
       - Include three to four qualifications and experiences relevant to the job.

    3. **Tailored Questions and Answers:**
       - Create the 5 most relevant interview questions for the candidate based on their profile and the job description.
       - Provide detailed and personalized sample answers for each question.
       - Ensure each answer showcases the candidate's qualifications and how they align with the job requirements.

    4. **Disqualifying Question: 'Do you have any questions for me?':**
       - Emphasize the importance of this question.
       - Provide tips on how to show engagement, intelligence, and interest.
       - Suggest specific questions related to the job, team, or company that demonstrate the candidate's interest and understanding.

    5. **Key Points and Strategies:**
       - Highlight specific experiences that align with the job requirements.
       - Demonstrate understanding of the company's challenges and how the candidate's skills can address them.
       - Showcase problem-solving abilities with concrete examples.
       - Emphasize adaptability and willingness to learn.
       - Avoid generic answers and negative comments about past employers.
       - Maintain a balance between modesty and confidence.
       - Provide concise and to-the-point answers.
    """

    # Combine the initial prompt with the job description and CV
    combined_input = f"{initial_prompt}\nJob Description:\n{job_description}\n\nCV:\n{cv}"

    # Detect the language of the combined input
    input_lang = detect(combined_input)

    # Set the model language based on the detected language
    model = "gpt-3.5-turbo"
    if input_lang == "zh-cn":
        model = "gpt-3.5-turbo-chinese"

    # Get response from the chatbot
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": combined_input}],
    )

    # Return the response
    return response.choices[0].message.content

# Define the interface with two text boxes for job description and CV
interface = gr.Interface(
    fn=chatbot_response,
    inputs=[
        gr.Textbox(label="Job Description", placeholder="Enter the job description here..."),
        gr.Textbox(label="CV", placeholder="Enter your CV here...")
    ],
    outputs=gr.Textbox(),
    title="AI Assistant Interview Prep",
    description="Enter the job description and your CV, and the AI assistant will help you prepare for your interview."
)

interface.launch()
