from pdfminer.high_level import extract_text
import re
import json

def parse_resume(pdf_path):
    text = extract_text(pdf_path)
    
    # Extract basic info using regex
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'\+?[\d\s\-\(\)]{7,}', text)
    name = text.strip().split('\n')[0]  # Assume name is first line
    
    # Define and extract sections with regex
    sections = {
        'education': extract_section(text, r'(?:EDUCATION|Education).*?(?=\n(?:EXPERIENCE|Skills|\Z))', True),
        'experience': extract_section(text, r'(?:EXPERIENCE|Experience).*?(?=\n(?:EDUCATION|Skills|\Z))', True),
        'skills': extract_section(text, r'(?:SKILLS|Skills).*?(?=\n(?:EDUCATION|EXPERIENCE|\Z))', False)
    }
    
    # Creates a dictionary for personal information
    result = {
        "personal_info": {
            "name": name,
            "email": email.group(0) if email else "",
            "phone": phone.group(0).strip() if phone else ""
        }
    }
    
    # Adding sections to result
    for section_name, content in sections.items():
        if content:
            if section_name == 'skills':
                                                                                            # Converting skills to list
                skills_list = re.split(r'[,•|\n]', content)
                result[section_name] = [skill.strip() for skill in skills_list if skill.strip()]
            else:
                result[section_name] = content
    
    return json.dumps(result, indent=4)

def extract_section(text, pattern, split_entries=False):
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    
    # Extract the matched content
    content = match.group(0)
    content = re.sub(r'^(?:EDUCATION|Education|EXPERIENCE|Experience|SKILLS|Skills)[:\s]*', '', content)
    content = content.strip()
    
    if split_entries:
        # Split content into individual entries
        entries = re.split(r'\n\s*\n', content)
        return [entry.strip() for entry in entries if entry.strip()]
    
    return content


pdf_path = 'resume/Ashish.pdf'
json_output = parse_resume(pdf_path)


print(json_output)
with open('resume_structured.json', 'w') as f:
    f.write(json_output)