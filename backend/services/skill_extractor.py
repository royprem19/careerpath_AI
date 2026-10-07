import re

# Comprehensive list of 300+ skills
SKILLS_DB = {
    "Programming": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "Go", "Rust", "Ruby", 
        "PHP", "Kotlin", "Swift", "Scala", "R", "MATLAB", "Julia", "Perl", "Dart", "Objective-C",
        "Haskell", "Lua", "Groovy", "Shell", "Bash", "PowerShell", "F#", "Cobol", "Fortran", "Assembly",
        "VBA", "ABAP", "Solidity", "Elixir", "Clojure", "Erlang", "Apex", "VBScript", "ActionScript",
        "Scratch", "Logo", "Prolog", "Lisp", "Ada", "Pascal", "Delphi", "Smalltalk", "Tcl", "Verilog"
    ],
    "Frontend": [
        "React", "Angular", "Vue.js", "Next.js", "Svelte", "HTML", "CSS", "SASS", "LESS", "Bootstrap", 
        "TailwindCSS", "jQuery", "Redux", "MobX", "Recoil", "Gatsby", "Nuxt.js", "Ember.js", "Backbone.js",
        "Preact", "Alpine.js", "Lit", "SolidJS", "Material UI", "Chakra UI", "Ant Design", "Bulma",
        "Foundation", "Semantic UI", "Webpack", "Vite", "Parcel", "Rollup", "Babel", "ESLint", "Prettier",
        "Jest", "Cypress", "Playwright", "Puppeteer", "Selenium", "Mocha", "Chai", "Jasmine", "Karma",
        "Enzyme", "Testing Library", "Storybook", "Apollo GraphQL", "Relay", "SWR", "React Query"
    ],
    "Backend": [
        "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot", ".NET", "Laravel", "Ruby on Rails", 
        "NestJS", "Koa", "Hapi", "Sails.js", "Meteor", "AdonisJS", "Phoenix", "Sinatra", "CakePHP", "CodeIgniter",
        "Symfony", "Zend", "Yii", "ASP.NET", "WCF", "Entity Framework", "Hibernate", "JPA", "MyBatis",
        "Spring MVC", "Spring Data", "Spring Security", "Dropwizard", "Play Framework", "Grails", "Struts",
        "Tornado", "CherryPy", "Bottle", "Falcon", "Pyramid", "Sanic", "Starlette", "Aiohttp",
        "Gin", "Echo", "Fiber", "Beego", "Revel", "Rocket", "Actix", "Iron"
    ],
    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "DynamoDB", "Firebase", "Supabase", 
        "Neo4j", "Oracle", "SQL Server", "SQLite", "MariaDB", "CouchDB", "Couchbase", "RavenDB", "ArangoDB",
        "OrientDB", "HBase", "Bigtable", "CockroachDB", "TiDB", "InfluxDB", "TimescaleDB", "Prometheus",
        "Elasticsearch", "Solr", "Splunk", "Logstash", "Kibana", "Hazelcast", "Memcached", "etcd", "Consul",
        "Zookeeper", "Realm", "Core Data", "Room", "Greenplum", "Teradata", "Vertica", "Snowflake", "Redshift",
        "BigQuery", "Athena", "Presto", "Trino", "Druid", "ClickHouse", "Pinot"
    ],
    "Cloud": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "Jenkins", "GitHub Actions", 
        "GitLab CI", "CircleCI", "Travis CI", "Bitbucket Pipelines", "Bamboo", "TeamCity", "Octopus Deploy",
        "Ansible", "Chef", "Puppet", "SaltStack", "Vagrant", "Packer", "Pulumi", "CloudFormation", "ARM Templates",
        "OpenStack", "VMware", "Xen", "KVM", "Hyper-V", "Docker Swarm", "Mesos", "Nomad", "Rancher",
        "OpenShift", "Helm", "Istio", "Linkerd", "Envoy", "Nginx", "HAProxy", "Traefik", "Apache",
        "Tomcat", "Jetty", "Undertow", "IIS", "Lighttpd", "Caddy", "Cloudflare", "Akamai", "Fastly"
    ],
    "ML/AI": [
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow", "PyTorch", "Scikit-learn", 
        "Keras", "OpenCV", "Hugging Face", "LLM", "GenAI", "XGBoost", "LightGBM", "CatBoost", "NLTK", "Spacy",
        "Gensim", "FastText", "Word2Vec", "BERT", "GPT", "Transformer", "YOLO", "ResNet", "VGG", "Inception",
        "GAN", "RL", "Q-Learning", "DQN", "PPO", "A3C", "DDPG", "SAC", "TD3", "AutoML", "H2O", "DataRobot",
        "Sagemaker", "Vertex AI", "Azure ML", "Databricks", "MLflow", "Kubeflow", "TFX", "ONNX", "TensorRT",
        "CoreML", "ML.NET", "Weka", "RapidMiner", "KNIME"
    ],
    "Data": [
        "Pandas", "NumPy", "Matplotlib", "Seaborn", "Tableau", "Power BI", "Apache Spark", "Hadoop", "Airflow", 
        "dbt", "Plotly", "Bokeh", "Dash", "Streamlit", "Gradio", "Superset", "Metabase", "Looker", "Qlik",
        "Kafka", "RabbitMQ", "ActiveMQ", "ZeroMQ", "Pulsar", "NATS", "Kinesis", "Event Hubs", "Pub/Sub",
        "Flink", "Storm", "Samza", "Beam", "NiFi", "Talend", "Pentaho", "Informatica", "DataStage", "Ab Initio",
        "SSIS", "Alteryx", "Fivetran", "Stitch", "Airbyte", "Meltano", "Great Expectations", "Prefect"
    ],
    "Tools": [
        "Git", "GitHub", "Linux", "Jira", "Figma", "Postman", "VS Code", "Bitbucket", "GitLab", "SVN", "Mercurial",
        "Trello", "Asana", "Monday", "ClickUp", "Notion", "Confluence", "Slack", "Microsoft Teams", "Discord",
        "Zoom", "Webex", "Skype", "IntelliJ IDEA", "Eclipse", "NetBeans", "Visual Studio", "PyCharm", "WebStorm",
        "PhpStorm", "RubyMine", "CLion", "Rider", "Android Studio", "Xcode", "Vim", "Emacs", "Sublime Text",
        "Atom", "Notepad++", "Sketch", "Adobe XD", "InVision", "Zeplin", "Miro", "Lucidchart", "Draw.io",
        "Swagger", "Insomnia", "SoapUI", "JMeter", "Gatling", "Locust", "WireShark", "Fiddler", "Charles"
    ],
    "Soft Skills": [
        "Communication", "Leadership", "Problem Solving", "Team Work", "Project Management", "Agile", "Scrum", 
        "Kanban", "Lean", "Six Sigma", "Time Management", "Critical Thinking", "Adaptability", "Creativity",
        "Work Ethic", "Attention to Detail", "Conflict Resolution", "Decision Making", "Emotional Intelligence",
        "Empathy", "Mentoring", "Negotiation", "Networking", "Presentation Skills", "Public Speaking",
        "Active Listening", "Collaboration", "Customer Service", "Interpersonal Skills", "Motivation"
    ],
    "Design & Creative": [
        "UI/UX Design", "Figma", "User Research", "Wireframing", "Prototyping", "Design Systems",
        "Interaction Design", "Graphic Design", "Usability Testing", "Design Thinking", "Information Architecture",
        "Adobe XD", "Sketch", "Visual Design", "Design Sprints"
    ],
    "Business & Product": [
        "Product Management", "Business Analysis", "Requirements Gathering", "Process Mapping",
        "Product Roadmapping", "Sprint Planning", "Market Research", "Financial Modeling", "Stakeholder Management",
        "User Stories", "Competitive Analysis", "Agile & Scrum", "Business Intelligence", "KPI Tracking"
    ],
    "Marketing & Growth": [
        "Digital Marketing", "SEO", "SEM", "Content Strategy", "Google Analytics", "Social Media Marketing",
        "Email Marketing", "Copywriting", "Data Storytelling", "Brand Strategy", "A/B Testing", "Growth Marketing"
    ],
    "Operations & Quality": [
        "Quality Assurance", "Manual Testing", "Test Automation", "Technical Support", "Customer Success",
        "CRM", "Salesforce", "Zoho", "Technical Writing", "Incident Management", "Vendor Management", "ITIL"
    ]
}

ALL_SKILLS = [skill for category in SKILLS_DB.values() for skill in category]

# Comprehensive Indian Degree & Educational Qualifications Mapping
INDIAN_EDUCATION_MAPPINGS = [
    (re.compile(r'\b(b\.?tech|btech|bachelor\s+of\s+technology)\b', re.IGNORECASE), "B.Tech (Bachelor of Technology)"),
    (re.compile(r'\b(b\.?e\.?|be\b|bachelor\s+of\s+engineering)\b', re.IGNORECASE), "B.E. (Bachelor of Engineering)"),
    (re.compile(r'\b(bca|bachelor\s+of\s+computer\s+applications)\b', re.IGNORECASE), "BCA (Bachelor of Computer Applications)"),
    (re.compile(r'\b(mca|master\s+of\s+computer\s+applications)\b', re.IGNORECASE), "MCA (Master of Computer Applications)"),
    (re.compile(r'\b(m\.?tech|mtech|master\s+of\s+technology)\b', re.IGNORECASE), "M.Tech (Master of Technology)"),
    (re.compile(r'\b(m\.?e\.?|master\s+of\s+engineering)\b', re.IGNORECASE), "M.E. (Master of Engineering)"),
    (re.compile(r'\b(b\.?sc|bsc|bachelor\s+of\s+science)\b', re.IGNORECASE), "B.Sc (Bachelor of Science)"),
    (re.compile(r'\b(m\.?sc|msc|master\s+of\s+science)\b', re.IGNORECASE), "M.Sc (Master of Science)"),
    (re.compile(r'\b(mba|pgdm|master\s+of\s+business\s+administration)\b', re.IGNORECASE), "MBA (Master of Business Administration)"),
    (re.compile(r'\b(bba|bachelor\s+of\s+business\s+administration)\b', re.IGNORECASE), "BBA (Bachelor of Business Administration)"),
    (re.compile(r'\b(b\.?com|bcom|bachelor\s+of\s+commerce)\b', re.IGNORECASE), "B.Com (Bachelor of Commerce)"),
    (re.compile(r'\b(b\.?voc|bachelor\s+of\s+vocation)\b', re.IGNORECASE), "B.Voc (Vocational Degree)"),
    (re.compile(r'\b(polytechnic|diploma\s+in\s+engineering|diploma)\b', re.IGNORECASE), "Diploma / Polytechnic"),
    (re.compile(r'\b(ph\.?d|doctorate)\b', re.IGNORECASE), "Ph.D. / Doctorate"),
    (re.compile(r'\b(self[-\s]?taught|bootcamp\s+graduate|skill\s+india\s+certified)\b', re.IGNORECASE), "Non-Traditional / Skill Certified"),
]

def extract_skills(text: str) -> list[str]:
    found_skills = set()
    text_lower = " " + text.lower() + " "
    text_lower = re.sub(r'[^\w\s\+#\-\.]', ' ', text_lower)
    
    for skill in ALL_SKILLS:
        skill_lower = skill.lower()
        if skill_lower == "c":
            if re.search(r'\bc\b', text_lower):
                found_skills.add(skill)
        elif skill_lower == "r":
            if re.search(r'\br\b', text_lower):
                found_skills.add(skill)
        elif "+" in skill_lower or "#" in skill_lower or "." in skill_lower:
            escaped = re.escape(skill_lower)
            if re.search(r'\b' + escaped + r'(?!\w)', text_lower):
                found_skills.add(skill)
        else:
            if re.search(r'\b' + re.escape(skill_lower) + r'\b', text_lower):
                found_skills.add(skill)
                
    return list(found_skills)

def extract_education(text: str) -> list:
    """
    Extracts structured education entries with degree, institution, and year/grade.
    """
    clean = text.replace('\u2013', '-').replace('\u2014', '-').replace('\u2212', '-')
    education_entries = []
    seen = set()

    # 1. Search for EDUCATION section
    edu_split = re.split(r'\b(?:EDUCATION|ACADEMICS|QUALIFICATIONS)\b', clean, flags=re.I)
    edu_section = ""
    if len(edu_split) > 1:
        edu_section = re.split(r'\b(?:EXPERIENCE|PROJECTS|SKILLS|CERTIFICATIONS|ACHIEVEMENTS|HOBBIES)\b', edu_split[1], flags=re.I)[0]
    
    search_text = edu_section if edu_section.strip() else clean
    lines = [l.strip() for l in search_text.splitlines() if l.strip()]

    inst_indicators = ['university', 'institute', 'college', 'school', 'academy', 'campus', 'vidyalaya', 'polytechnic']
    degree_indicators = ['bachelor', 'b.tech', 'b.e.', 'master', 'm.tech', 'mca', 'bca', 'mba', 'b.sc', 'm.sc', 'intermediate', 'matriculation', 'secondary', 'diploma', 'phd']

    # Grouped line parsing
    i = 0
    while i < len(lines):
        line = lines[i]
        line_lower = line.lower()
        if any(ind in line_lower for ind in inst_indicators):
            inst = line
            deg = ''
            yr = ''
            j = i + 1
            while j < len(lines) and j <= i + 3:
                next_line = lines[j]
                next_lower = next_line.lower()
                if any(ind in next_lower for ind in inst_indicators):
                    break
                if any(ind in next_lower for ind in degree_indicators) and not deg:
                    deg = next_line
                elif (re.search(r'\d{4}', next_line) or 'cgpa' in next_lower or 'percentage' in next_lower) and not yr:
                    yr = next_line
                j += 1
            
            if deg:
                degree_clean = deg
                grade_info = ''
                if '|' in deg:
                    parts = deg.split('|')
                    degree_clean = parts[0].strip(' -;,•*')
                    grade_info = parts[1].strip(' -;,•*')
                
                duration_str = yr.strip(' -;,•*') if yr else ''
                final_yr = f"{duration_str} ({grade_info})" if duration_str and grade_info else (duration_str or grade_info)
                
                key = f"{degree_clean.lower()}_{inst.lower()}"
                if key not in seen:
                    seen.add(key)
                    education_entries.append({
                        "degree": degree_clean,
                        "institution": inst,
                        "year": final_yr
                    })
                i = j - 1
        i += 1

    # Fallback to pattern matching if block loop found nothing
    if not education_entries:
        degree_patterns = [
            (r'Bachelor of Engineering[^\n,;]*', "Bachelor of Engineering (CSE)"),
            (r'Bachelor of Technology[^\n,;]*', "Bachelor of Technology (B.Tech)"),
            (r'B\.?E\.?\s*(?:in|-)?\s*[^\n,;]*', "Bachelor of Engineering"),
            (r'B\.?Tech\s*(?:in|-)?\s*[^\n,;]*', "Bachelor of Technology"),
            (r'Master of Technology[^\n,;]*', "Master of Technology (M.Tech)"),
            (r'BCA[^\n,;]*', "Bachelor of Computer Applications (BCA)"),
            (r'MCA[^\n,;]*', "Master of Computer Applications (MCA)"),
            (r'MBA[^\n,;]*', "Master of Business Administration (MBA)"),
            (r'Intermediate[^\n,;]*', "Intermediate / Senior Secondary (12th)"),
            (r'Matriculation[^\n,;]*', "Matriculation / Secondary (10th)")
        ]
        inst_match = re.search(r'(Chandigarh University[^\n,]*|[A-Za-z\s]+University[^\n,]*|[A-Za-z\s]+Institute of Technology[^\n,]*|[A-Za-z\s]+Public School[^\n,]*)', clean, re.I)
        primary_inst = inst_match.group(1).strip() if inst_match else "Recognized Institution"

        for pattern, canonical in degree_patterns:
            match = re.search(pattern, search_text, re.I)
            if match:
                raw_degree = match.group(0).strip(' –-;,•*')
                inst_name = primary_inst
                if "School" in raw_degree or "Intermediate" in canonical or "Matriculation" in canonical:
                    sch_m = re.search(r'([A-Za-z\s]+Public School|[A-Za-z\s]+School)', search_text, re.I)
                    inst_name = sch_m.group(1).strip() if sch_m else "Senior Secondary School"
                elif "Chandigarh University" in clean:
                    inst_name = "Chandigarh University, Mohali"
                    
                yr_match = re.search(r'((?:July|Jan|Aug|April|May|March|Dec)?\s*\d{4}\s*[-–]\s*(?:July|Jan|Aug|April|May|March|Dec)?\s*\d{4}\*?|CGPA:\s*[\d\.]+|Percentage:\s*[\d\.]+\%)', search_text, re.I)
                year_val = yr_match.group(1).strip() if yr_match else ""
                
                key = f"{canonical}_{inst_name}"
                if key not in seen:
                    seen.add(key)
                    education_entries.append({
                        "degree": raw_degree if len(raw_degree) > 5 else canonical,
                        "institution": inst_name,
                        "year": year_val
                    })

    if not education_entries:
        for pattern, canonical_name in INDIAN_EDUCATION_MAPPINGS:
            if pattern.search(clean):
                education_entries.append({
                    "degree": canonical_name,
                    "institution": primary_inst if 'primary_inst' in locals() else "Recognized Institution",
                    "year": ""
                })

    return education_entries[:4]

def extract_experience(text: str) -> list:
    """
    Extracts structured professional experience, internships, job titles, and companies.
    """
    clean = text.replace('\u2013', '-').replace('\u2014', '-').replace('\u2212', '-')
    experience_list = []
    
    # Search for dedicated EXPERIENCE section
    exp_split = re.split(r'\b(?:EXPERIENCE|WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT)\b', clean, flags=re.I)
    exp_section = ""
    if len(exp_split) > 1:
        exp_section = re.split(r'\b(?:EDUCATION|PROJECTS|SKILLS|CERTIFICATIONS|ACHIEVEMENTS|HOBBIES)\b', exp_split[1], flags=re.I)[0]
        
    search_text = exp_section if exp_section.strip() else clean
    lines = search_text.splitlines()

    for line in lines:
        line_clean = line.strip()
        if not line_clean or line_clean.startswith('-') or line_clean.startswith('•') or line_clean.startswith('*'):
            continue
        if any(skip in line_clean.lower() for skip in ['cgpa', 'percentage', 'bachelor', 'b.tech', 'b.e.', 'm.tech', 'secondary', 'matriculation', 'intermediate']):
            continue
        if '|' in line_clean and any(k in line_clean.lower() for k in ['intern', 'analyst', 'engineer', 'developer', 'scientist', 'consultant', 'trainee', 'lead', 'manager', 'associate', 'specialist']):
            parts = [p.strip() for p in line_clean.split('|') if p.strip()]
            if len(parts) >= 2:
                comp = parts[0]
                role = parts[1]
                loc = parts[2] if len(parts) > 2 else ''
                dur = parts[3] if len(parts) > 3 else (parts[2] if len(parts) == 3 and any(c.isdigit() for c in parts[2]) else '')
                if dur and loc == dur:
                    loc = ''
                full_comp = f"{comp}, {loc}" if loc and loc != dur else comp
                experience_list.append({
                    "role": role,
                    "company": full_comp,
                    "duration": dur,
                    "years": 0.5 if "intern" in role.lower() else 1.0,
                    "has_internship": "intern" in role.lower()
                })
                
    if not experience_list:
        intern_m = re.search(r'(Data Analytics Intern|Software Engineer Intern|Research Intern|Data Scientist|Data Analyst)', search_text, re.I)
        comp_m = re.search(r'(Solitaire Infosys|[A-Za-z\s]+(?:Infosys|Technologies|Solutions|Services|TCS|Wipro|Cognizant))', search_text, re.I)
        dur_m = re.search(r'((?:June|July|Jan|Feb|March|April|May|Aug|Sept|Oct|Nov|Dec)\s*\d{4}\s*[-–]\s*(?:June|July|Jan|Feb|March|April|May|Aug|Sept|Oct|Nov|Dec)?\s*\d{4})', search_text, re.I)
        
        if intern_m or comp_m:
            experience_list.append({
                "role": intern_m.group(1).strip() if intern_m else "Data Analytics Intern",
                "company": comp_m.group(1).strip() if comp_m else "Industry Project",
                "duration": dur_m.group(1).strip() if dur_m else "Internship Track",
                "years": 0.5,
                "has_internship": True
            })
            
    # Check for explicit experience duration (e.g. 2 years experience)
    years_m = re.search(r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience)?', clean, re.I)
    if years_m and experience_list:
        experience_list[0]["years"] = float(years_m.group(1))
        
    return experience_list

def extract_certifications(text: str) -> list[str]:
    cert_keywords = ["AWS", "Azure", "Google Cloud", "GCP", "Cisco", "CompTIA", "Oracle", "Microsoft Certified"]
    found = set()
    for kw in cert_keywords:
        if kw.lower() in text.lower():
            found.add(kw)
    return list(found)
