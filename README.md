# CS Internship and job finder. + Resume analyser with feedback 
**Note** - This is a work in progress and is not 100% complete. 

- This project is a tool that helps people specifically computer graduates to find jobs and apply to them.
- It also helps you to analyse your resume to see what you can improve to make you chances better at landing a job.
- It sends updates via a discord webhook .
- Opens linkedin and filters for a job which then keeps track of how many you applied to (manually) . ( To not violate Linkedin ToS and not harm employers ) 
- Runs a T5 model from hugging face which reads your resume and then analyses where you can do better.

## Workflow 
- Tool extract keyword from resume.txt
- It then opens linkedin website
- Filters for jobs based on keyword
- You manually apply for 'n' number of jobs per keyword ( This is to prevent violating Linkedin ToS and keep employers safe while also being a limitation of my code due to being inexperienced )
- A T5 model reads your resume, it then provides feedback via terminal or discord webhook on where you can improve. ( Still a WIP ) 

## Roadmap 
- Add support for PDF resumes
- Add GUI 
- Have a table to keep track of the jobs you applied to.

## Contributing
This is a solo project made by me just for experimenting with python, selenium, hugging face and AI to maybe expand into a business
  
  
