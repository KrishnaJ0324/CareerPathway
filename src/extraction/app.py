import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from google import genai
from open_processor import openresume
from flask import Flask, render_template, redirect, request, jsonify
import time

model = SentenceTransformer("all-MiniLM-L6-v2")
df = pd.read_csv('jd_unstructured_data.csv')

app = Flask(__name__)
app.secret_key = 'dreaserous'

# Global variable to store processing steps status
processing_steps = {
    "OpenResume": False,
    "MiniLM + Dataset": False,
    "Gemini API (Flowchart)": False,
    "Gemini API (Descriptions)": False,
    "Frontend": False
}

@app.route('/')
def hello():
    return render_template("model.html", processing_steps=processing_steps)

@app.route("/home")
def home():
    return redirect('/')

@app.route('/submit', methods=['POST'])
def submit_data():
    global processing_steps
    processing_steps = {
        "OpenResume": False,
        "MiniLM + Dataset": False,
        "Gemini API (Flowchart)": False,
        "Gemini API (Descriptions)": False,
        "Frontend": False
    }

    if request.method == 'POST':
        f = request.files['userfile']
        f.save(f.filename)

        # OpenResume
        resume_text = openresume(os.path.join(os.getcwd(), f.filename))
        processing_steps["OpenResume"] = True

        # MiniLM similarity
        resume_embedding = model.encode(resume_text, convert_to_tensor=True)

        def compute_similarity(row):
            job_desc = row['Job_Description']
            job_embedding = model.encode(job_desc, convert_to_tensor=True)
            return util.cos_sim(resume_embedding, job_embedding).item()

        df['similarity'] = df.apply(compute_similarity, axis=1)
        processing_steps["MiniLM + Dataset"] = True

        top_5 = df.sort_values(by='similarity', ascending=False).head(5)
        df2 = top_5[['Position', 'Company', 'Location', 'similarity']]

        dropdown_locations = sorted(df2['Location'].unique())
        job_list = []
        for index, row in df2.iterrows():
            job_list.append({
                'Position': row['Position'],
                'Company': row['Company'],
                'Location': row['Location']
            })

        # Gemini Flowchart
        client = genai.Client(api_key="")
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f"can u give me a flowchart for a job role \"{job_list[0]['Position']}\". the flowchart should be specific with skills and courses to learn. it should be in this format \"Start → Data Analysis Fundamentals → Advanced Excel → SQL → Data Visualization → Statistical Analysis → Python/R → Big Data Tools → Business Acumen → Advanced SQL → Project Management → End\". it should be very summarised and should not include any optional thing. do not give any explanation or reply apart from the flowchart."
        )
        steps = response.text.split(" → ")[1:-1]
        processing_steps["Gemini API (Flowchart)"] = True

        # Gemini Descriptions
        step_string = ", ".join(steps)
        desc_prompt = (
            f"Give a short 1-sentence description and a course link (very important) for each of the following career steps: "
            f"{step_string}. Respond in the format:\n\n"
            "Step Title: Description\nLink: <URL if available>\n\n"
            "If no course is available, leave the Link line but the link is very important try to get it as to the best of your ability. do not give any explanation or reply apart from the format specified"
        )

        desc_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=desc_prompt
        )
        processing_steps["Gemini API (Descriptions)"] = True

        raw_blocks = desc_response.text.strip().split("\n\n")
        career_path = []

        for block in raw_blocks:
            lines = block.strip().split("\n")
            if len(lines) >= 1:
                title, description = lines[0].split(":", 1)
                link = None
                if len(lines) == 2 and lines[1].startswith("Link:"):
                    url = lines[1][5:].strip()
                    if url.lower().startswith("http"):
                        link = url
                career_path.append({
                    "title": title.strip(),
                    "description": description.strip(),
                    "link": link
                })

        processing_steps["Frontend"] = True
        time.sleep(3)

        return render_template(
            'model.html',
            job_list=job_list,
            dropdown_locations=dropdown_locations,
            career_path=career_path,
            processing_steps=processing_steps
        )

@app.route('/processing-status')
def processing_status():
    return jsonify(processing_steps)

if __name__ == "__main__":
    app.run(debug=True)
