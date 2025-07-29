from google import genai
client = genai.Client(api_key="AIzaSyCWj5rj5WQ7dHz8Bnl1iU-LPBGd68Sxi8E")
x  = "game engine developer"

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=f"can u give me a flowchart for a job role \"{x}\". the flowchart should be specific with skills and courses to learn. it should be in this format \"Start → Data Analysis Fundamentals → Advanced Excel → SQL → Data Visualization → Statistical Analysis → Python/R → Big Data Tools → Business Acumen → Advanced SQL → Project Management → End\". it should be very summarised and should not include any optional thing. do not give any explanation."
)
print(response.text)