import re


SKILLS = [

    # Programming
    "python",
    "java",
    "c++",
    "c",
    "c#",
    "javascript",
    "typescript",

    # Data
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "excel",

    # Python ecosystem
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scikit-learn",

    # Machine Learning
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "nlp",
    "natural language processing",
    "computer vision",

    # Web
    "flask",
    "django",
    "fastapi",
    "rest api",
    "api",

    # Data Engineering
    "spark",
    "pyspark",
    "airflow",
    "etl",

    # Visualization
    "power bi",
    "tableau",

    # DevOps
    "docker",
    "kubernetes",
    "git",
    "github",
    "linux",

    # Testing
    "pytest",
    "selenium",
    "automation",
    "testing",

    # AI
    "artificial intelligence",
    "generative ai",
    "llm",

    # Cloud
    "aws",
    "azure",
    "gcp",

    # Core
    "oop",
    "data structures",
    "algorithms"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []


    for skill in SKILLS:

        # Special regex handling for symbols
        pattern = r"\b" + re.escape(skill) + r"\b"


        if re.search(pattern, text):

            found_skills.append(skill.title())


    return sorted(found_skills)