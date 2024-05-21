# testing embeddings


import requests
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


job_description="Senior Quality Assurance Engineer We are on the hunt for an exceptional Senior QA Engineer to join and elevate our team. This role is perfect for someone who is not just looking for a job but an opportunity to make a significant impact. Key Responsibilities: Develop, enhance, and maintain both front-end and back-end automated testing frameworks using cutting-edge tools and technologies, alongside conducting manual testing when necessary. Take charge of our CI/CD processes, crafting a comprehensive test strategy, and embedding quality standards within automated pipelines. Define, track, and optimize quality and performance metrics for our applications to ensure they meet our high standards. Lead by example, reviewing test procedures and mentoring team members on best practices in automated testing. Serve as the linchpin for quality control, ensuring application changes meet our rigorous standards for excellence. Requirements: Proven track record as a Quality Assurance Engineer, boasting a deep understanding of automated testing frameworks for both front-end (e.g., Playwright) and back-end (e.g., xUnit) development. Experience with AWS DevOps, cloud services, and an ability to seamlessly integrate test cases into comprehensive suites for automation. Familiarity with test design, methodologies, and tools, with ISTQB or similar certifications being a huge plus. A strong team player with outstanding analytical abilities, you pride yourself on being independent, solution-focused, and proactive. Excellent communication skills in English, both verbal and written, are essential. What We Offer: Competitive salaries that stand above market standards. Annual bonuses reflecting both personal and company performance. A generous learning and development budget to support your professional growth. 25 days of paid leave annually to ensure work-life balance."

candidate_description='''


SQA Automation Lead
DP World
08/2022 - Present,
Implementation Project Logistics, ensuring coordination with the development team and stakeholders to align with project objectives. Designed a tailored Automation Architecture in accordance with the demands of the project, resulting efficient testing processes. Conducted rigorous manual and automated testing procedures, guaranteeing the high quality of the project deliverables.
Managed the QA Jira board, ensuring the accurate tracking and timely resolution of identified issues .
Fostered a collaborative environment by engaging with both the internal team and the client, facilitating communication and the smooth execution of project milestones.
Senior SQA Automation Engineer
Afiniti
10/2020 - 07/2022,
Contributed to the development of the Call Center Switch system, handling a high volume of agent calls.
Gathered project requirements and devised a detailed test plan along with test cases.
Developed automation framework and automated test cases to enhance overall test coverage and accuracy.
Supervised a dynamic QA team comprising six members, delegating daily tasks and ensuring adherence to project requirements.
Senior SQA Automation Engineer
Northbay Solutions
09/2019 - 09/2020,
Contributed to the development of a Data Lake project, initiating the seamless extraction of data from diverse AWS S3 buckets, facilitating data transformation, and enabling efficient loading into distinct zones.
Leveraged a diverse set of AWS services to execute comprehensive automation testing, ensuring efficient testing procedures. Amplified test coverage measures to ensure the delivery of an error-free project, fostering client satisfaction and trust.
SQA Automation Engineer
Devsinc
09/2017 - 08/2019,
Played a key role in the development of an HR platform facilitating streamlined onboarding, offboarding, and task allocation for team members.
Gathered Clients requirements and applied advanced testing methodologies to ensure seamless implementation.
Executed automation testing to enhance test coverage and Communicated potential issues, contributing to an error-free product. Facilitated meetings with both clients and the internal team, fostering open communication and collaboration to ensure project success.
SQA Automation Engineer
Broker Genius
08/2016 - 08/2017,
Contributed to the development of an automated pricing tool tailored for brokers, enhancing efficiency in pricing strategies and operations. Conducted both manual and automated testing , ensuring the accuracy of the auto pricing tool to meet industry standards.
PROJECTS I HAVE WORKED ON
World Logistic Passport - Web
Leveraged a tech stack featuring ReactJS, Java, Azure, Cypress, Appium, Android Studio, and MailSlurp to drive efficient and effective project development and testing processes.
Orchestrated the development of a comprehensive Cypress automation framework, implementing the Page Object Model (POM) to seamlessly integrate with the React frontend, and delivered an insightful demonstration to project leadership.
Created and executed JavaScript-based automation test cases, ensuring the robustness and reliability of software solutions.
Integrated the MailSlurp plugin to facilitate email verification through automation scripts, enhancing the comprehensiveness of the testing process.
Expanded test coverage to systematically identify and address potential issues, guaranteeing the delivery of high-quality and error-free software products.
Designed and established an automation pipeline within the Microsoft Azure environment, streamlining software development and testing procedures for enhanced efficiency and productivity.
Actively participated in daily status calls and team meet ups, fostering effective communication to address and resolve project-related challenges in a collaborative team environment.
World Logistic Passport - Mobile App
Conducted comprehensive automation testing of the WLP mobile app, leveraging Appium, Android Studio, and Appium Inspector to ensure seamless functionality and performance.
Developed precise automation scripts in Java, ensuring a robust and efficient testing process for the WLP mobile application.
Executed thorough testing of APK files, guaranteeing the accuracy and functionality of the application package, and providing actionable insights for enhancements.
Mega Avaya
Employed a diverse array of technologies, including ReactJS, NodeJS, and Docker for project development, and leveraged Cypress, Postman, and Jenkins for comprehensive testing procedures.
Established a robust automation framework from the ground up in Cypress for comprehensive web and API automation testing, ensuring streamlined and efficient testing processes.
Orchestrated the creation of CI/CD pipelines in Jenkins, enabling the seamless execution of test cases against development builds for thorough and efficient testing procedures.
Strategically devised and managed automation tasks on the Jira board, delegating tasks to team members and ensuring the timely and effective completion of project milestones.
Effectively oversaw and managed a dynamic QA team comprising six members, fostering a collaborative and productive environment for the successful execution of project deliverables.
Data Lake Accelerator
Leveraged Python Django framework and a range of AWS services for efficient and effective project development and deployment.
Developed a comprehensive automation framework in Python, ensuring streamlined and efficient testing processes for the project.
Crafted automation test cases using Boto3, Athena, and Glue, facilitating thorough and precise testing procedures and enhancing the overall robustness of the project.
Conducted meticulous API testing using the Python Request Library, ensuring seamless integration and functionality of API components within the project.
Sapling
Implemented Ruby on Rails and AngularJS technologies for the development of the HR platform, while utilizing RSpec, Capybara, PhantomJS, and CircleCI for comprehensive automation testing procedures.
Developed precise automation scripts using RSpec and Capybara, ensuring the efficiency and accuracy of the testing process for the HR platform.
Orchestrated the creation of an automation pipeline build utilizing CircleCI, streamlining the testing and deployment processes for enhanced efficiency and productivity.
Conducted thorough execution of test cases and promptly shared detailed reports with stakeholders, providing valuable insights and facilitating informed decision-making processes.
BrokerGenius
Contributed to the development of an automated pricing tool for brokers, built using the Laravel framework, ensuring efficient and effective pricing strategies.
Developed a comprehensive automation framework in Codeception and Selenium WebDriver, enhancing the testing process for the auto pricer tool and ensuring robust performance.
Established pipelines on Jenkins to facilitate the execution of test cases and seamless sharing of comprehensive reports with stakeholders, enabling informed decision-making.
Integrated Zephyr for Jira for effective test management, ensuring streamlined processes and accurate tracking of testing procedures and results.
Fabletics
Contributed to the development of the Fabletics clothing brand, ensuring the seamless execution of tasks and operations.
Conducted comprehensive automation testing of APIs using PactumJS, ensuring the accuracy and functionality of the APIs for the clothing brand. Configured various test environments to facilitate thorough and efficient testing procedures, ensuring the robustness and reliability of the project. Effectively oversaw and managed Jenkins pipeline builds, ensuring the efficient and timely execution of tasks and projects for the clothing brand.
SuperNova Brands
Conducted meticulous manual testing of a beauty products website, ensuring the seamless functionality and user experience of the platform.
Developed precise manual test cases and meticulously executed them to validate the performance and reliability of the website.
Effectively documented and reported identified bugs, ensuring clear communication and prompt resolution for an enhanced user experience.
Actively collaborated with the team to discuss and address identified bugs, fostering a collaborative environment and ensuring the timely resolution of issues.
Traxidy
Contributed to Traxidy, a comprehensive project management tool, ensuring efficient task management and streamlined operations.
Conducted thorough analysis of requirements, leading to the formulation of comprehensive test plans and meticulous test cases for Traxidy.
Implemented automation testing using Playwright, ensuring the accuracy and reliability of the project management tool.
Developed precise automation test scripts in Playwright using JavaScript, ensuring efficient and effective testing procedures for Traxidy.
Fostered effective collaboration with both the internal team and the client, facilitating productive communication and the successful execution of project milestones.

EDUCATION
Bachelors in Computer Science
University of Sargodha.
08/2012 - 08/2016
SKILLS
Automation Testing Cypress Playwright Selenium WebDriver Robot TestCafe Codeception Cucumber BDD Rspec Capybara Javascript Python Java PHP CSharp ASP.NET
Manual Testing
Rest Assured
Jmeter
ReactJS
AWS Services
GitHub ETL Testing Katalon Studio

Test Execution Jenkins
Android Studio
Jira CircleCI
Flutter Azure
Test Management Github Actions
Dart Tosca PhantomJS
API Testing Postman AWS Code Pipeline
Test Planning Test Cases Python Request Library CICD
Mobile Testing Appium
TestNG Sales Force
Maven
'''




import requests
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os  # Import the os module

def get_embeddings(text, model="text-embedding-ada-002"):
    url = "https://api.openai.com/v1/embeddings"
    api_key = os.getenv("")  # Get the API key from environment variables
    if not api_key:
        print("API key not found. Please set the OPENAI_API_KEY environment variable.")
        return None
    headers = {
        'Authorization': f'Bearer {api_key}',  # Use the API key from environment variable
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "input": text,
        "model": model
    })
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return np.array(response.json()['data'][0]['embedding'])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Example use
job_description = "Senior Quality Assurance Engineer..."
candidate_description = "Details about the candidate's experience..."

embeddings_job = get_embeddings(job_description)
embeddings_candidate = get_embeddings(candidate_description)

if embeddings_job is not None and embeddings_candidate is not None:
    similarity_score = cosine_similarity([embeddings_job], [embeddings_candidate])
    print(f"Cosine Similarity: {similarity_score[0][0]}")
else:
    print("Failed to retrieve embeddings for comparison.")
