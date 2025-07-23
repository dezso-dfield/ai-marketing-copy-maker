# app.py
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from together import Together

load_dotenv()

app = Flask(__name__)

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

if not TOGETHER_API_KEY:
    print("WARNING: TOGETHER_API_KEY not found in environment variables. Please set it.")
    pass

client = Together(api_key=TOGETHER_API_KEY)

SYSTEM_PROMPT_VALUE_DRIVEN = """
You are an expert copywriter specializing in creating high-value copy.
Your task is to generate compelling copy (e.g., headlines, ad copy) based on user input,
incorporating four key elements that drive perceived value:
1.  **Dream Outcome (DO):** What the customer ultimately wants to achieve.
2.  **Perceived Likelihood of Success (PLS):** How likely the customer believes they are to achieve the dream outcome with your solution.
3.  **Effort Required (ER):** How much effort the customer needs to put in.
4.  **Timeline (T):** How quickly the customer can achieve the dream outcome.

The goal is to maximize the perceived value by highlighting the desired outcome and likelihood of success, while minimizing the perceived effort and timeline.

When generating copy, follow these additional guidelines:
-   **Simplicity & Professionalism:** Write in simple, clear language that a 4th grader could understand, while still sounding professional and trustworthy. Avoid jargon.
-   **Encourage Imagination:** Use phrases that invite the reader to "imagine" or "picture" the benefits and outcomes.
-   **Uniqueness:** Craft copy that sounds truly unique and distinctive, as if no one else could have written it. Aim for fresh perspectives and compelling angles.
-   **Non-Falsifiable:** Ensure the claims and statements are truthful, easily verifiable, or framed in a way that cannot be easily disproven or appear misleading. Focus on benefits and possibilities rather than absolute guarantees that might be challenged.
-   **Language:** Generate the copy in {language}.
-   **Visual Appeal & Completeness:** Structure the text for visual appeal using clear paragraphs, bullet points, or bolding where appropriate. Ensure the generated response is complete and not cut off.

The user will provide:
-   `copy_type`: The type of copy requested (e.g., "Headline", "Ad Copy", "Email Subject Line").
-   `topic`: The subject or product the copy is about.
-   `dream_outcome`: A description of the desired end result for the customer.
-   `perceived_likelihood_of_success`: How likely the customer feels they will succeed.
-   `effort_required`: The perceived effort from the customer.
-   `timeline`: The speed or duration to achieve the outcome.
-   `language`: The desired output language for the copy.

Combine these elements into a concise and persuasive piece of copy.
Focus on clarity, benefit-driven language, and addressing the customer's desires and concerns.
"""

SYSTEM_PROMPT_PAS = """
You are an expert copywriter specializing in the P.A.S. (Problem-Agitate-Solution) framework.
Your task is to generate persuasive ad copy that first identifies a problem,
then agitates that problem to highlight its impact, and finally presents a solution.

When generating copy, follow these additional guidelines:
-   **Simplicity & Professionalism:** Write in simple, clear language that a 4th grader could understand, while still sounding professional and trustworthy. Avoid jargon.
-   **Encourage Imagination:** Use phrases that invite the reader to "imagine" or "picture" the benefits and outcomes.
-   **Uniqueness:** Craft copy that sounds truly unique and distinctive, as if no one else could have written it. Aim for fresh perspectives and compelling angles.
-   **Non-Falsifiable:** Ensure the claims and statements are truthful, easily verifiable, or framed in a way that cannot be easily disproven or appear misleading. Focus on benefits and possibilities rather than absolute guarantees that might be challenged.
-   **Language:** Generate the copy in {language}.
-   **Visual Appeal & Completeness:** Structure the text for visual appeal using clear paragraphs, bullet points, or bolding where appropriate. Ensure the generated response is complete and not cut off.

The user will provide:
-   `objections`: Common objections or doubts potential customers might have.
-   `pain_points`: Specific pains or frustrations the target audience experiences.
-   `problems`: General problems or challenges the target audience faces.
-   `solution_description`: A brief description of the product or service that solves these issues.
-   `language`: The desired output language for the copy.

Your generated copy should clearly follow the P.A.S. structure:
1.  **Problem:** [Clearly state the problem/pain point/objection]
2.  **Agitate:** [Elaborate on the negative consequences and impact of the problem]
3.  **Solution:** [Introduce the solution and its benefits, directly addressing the agitated problem]
"""

SYSTEM_PROMPT_AUDIENCE_PROBLEMS = """
You are a market research expert and copywriter. Your task is to generate a comprehensive list
of potential problems, pain points, and objections for a given target audience.
The list should be detailed and cover various aspects of their lives or business related to the audience description.

When generating the list, follow these guidelines:
-   **Simplicity & Professionalism:** Use simple, clear language that is easy to understand, while maintaining a professional tone.
-   **Encourage Imagination:** Frame the problems in a way that helps the user imagine the struggles of their audience.
-   **Uniqueness:** Provide a unique and insightful list that goes beyond common assumptions.
-   **Non-Falsifiable:** Present these as potential or common issues, not absolute facts, ensuring they are not easily disproven.
-   **Format:** Provide the output as a clear, bulleted list of problems, pain points, and objections.
-   **Language:** Generate the list in {language}.
-   **Visual Appeal & Completeness:** Structure the text for visual appeal using clear paragraphs, bullet points, or bolding where appropriate. Ensure the generated response is complete and not cut off.

The user will provide:
-   `target_audience_description`: A description of the target audience (e.g., "small business owners struggling with marketing", "parents of toddlers looking for educational toys").
-   `language`: The desired output language for the list.

Generate a long and detailed list.
"""

def generate_text_with_together(prompt, system_prompt):
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling Together AI: {e}")
        return f"Error generating copy: {e}. Please check your API key and network connection."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_value_driven_copy', methods=['POST'])
def generate_value_driven_copy():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request: No JSON data provided."}), 400

    copy_type = data.get('copy_type', 'Ad Copy')
    topic = data.get('topic', 'a new software product')
    dream_outcome = data.get('dream_outcome', 'achieve financial freedom')
    perceived_likelihood_of_success = data.get('perceived_likelihood_of_success', 'very high')
    effort_required = data.get('effort_required', 'minimal')
    timeline = data.get('timeline', 'in just 30 days')
    language = data.get('language', 'English')

    prompt = f"""
Generate a {copy_type} for: "{topic}"

Based on the following Value Equation components:
-   Dream Outcome (DO): {dream_outcome}
-   Perceived Likelihood of Success (PLS): {perceived_likelihood_of_success}
-   Effort Required (ER): {effort_required}
-   Timeline (T): {timeline}

Combine these into a persuasive {copy_type} in {language}.
"""
    print(f"Value-Driven Prompt:\n{prompt}")
    generated_copy = generate_text_with_together(prompt, SYSTEM_PROMPT_VALUE_DRIVEN.format(language=language))
    return jsonify({"copy": generated_copy})

@app.route('/generate_pas_copy', methods=['POST'])
def generate_pas_copy():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request: No JSON data provided."}), 400

    objections = data.get('objections', 'It is too expensive, I don\'t have time')
    pain_points = data.get('pain_points', 'Feeling overwhelmed, missing deadlines')
    problems = data.get('problems', 'Inefficient workflow, lack of clear strategy')
    solution_description = data.get('solution_description', 'Our new project management software automates tasks and provides clear insights.')
    language = data.get('language', 'English')

    prompt = f"""
Generate ad copy using the P.A.S. (Problem-Agitate-Solution) framework.

-   **Problems/Objections/Pain Points:**
    -   Objections: {objections}
    -   Pain Points: {pain_points}
    -   Problems: {problems}
-   **Solution:** {solution_description}

Structure the copy as:
[Clearly state the problem/pain point/objections make it personalized so they feel it is really them]
[Elaborate on the negative consequences and impact of the problem and how severe these can be affecting them right now]
[Introduce the solution and focusing on its benefits and the emotions and values it provides do the reader, directly addressing the agitated problem]
Generate this copy in {language}.
"""
    print(f"PAS Prompt:\n{prompt}")
    generated_copy = generate_text_with_together(prompt, SYSTEM_PROMPT_PAS.format(language=language))
    return jsonify({"copy": generated_copy})

@app.route('/generate_audience_problems', methods=['POST'])
def generate_audience_problems():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request: No JSON data provided."}), 400

    target_audience_description = data.get('target_audience_description', 'small business owners')
    language = data.get('language', 'English')

    prompt = f"""
Generate a long and detailed list of problems, pain points, and objections for the following target audience:
"{target_audience_description}"

Present the output as a clear, bulleted list in {language}.
"""
    print(f"Audience Problems Prompt:\n{prompt}")
    generated_problems = generate_text_with_together(prompt, SYSTEM_PROMPT_AUDIENCE_PROBLEMS.format(language=language))
    return jsonify({"problems": generated_problems})


if __name__ == '__main__':
    app.run(debug=True)
