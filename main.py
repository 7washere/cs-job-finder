import re 
import os

def skills_extract(resume.txt):         # Func to extract skills from a resume like python,java,django,c++ etc.
     with open(file_path, 'r') as file:
        content = file.read().lower() # Makes chracters lowercase


         known_skills = ["python", "java", "c++", "html", "css", "javascript", "git",
        "github", "machine learning", "deep learning", "nlp", 
        "data structures", "algorithms", "linux", "sql", "django", 
        "flask", "react", "node.js", "c", "data science", "computer vision", "php"]     # List of skills that are most well known in the CS job field

        found_skills = [skill for skill in known_skills if skill in content] # Finds the skills that are in the resume

        return found_skills # Now returns all the various skills found in the resume 


def job_url_gen(skills): # A func to give us job urls 
    base = "https://www.linkedin.com/jobs/search/?keywords=" # Every linkedin job search starts with this 
    urls = [] # The generated urls will be stored here
    for skill in skills:    # Creates a loop with each skill in the list skills
        keyword = skill.replace(" ", "+") # Replaces the blank area with each keyword
        url = base_url + keyword # Adds the keywords to the base url
        urls.append(url) # Changes the urls list adding the new url

