import re

TECHNOLOGIES = [
    "Django",
    "Flask",
    "FastAPI",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "SciPy",
    "SQLAlchemy",
    "Django ORM",
    "MongoDB",
    "Pytest",
    "unittest",
    "Celery",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "Google Cloud Platform",
    "TensorFlow",
    "Keras",
    "PyTorch",
    "Scikit-learn",
    "NLTK",
    "Spacy",
    "GraphQL",
    "RESTful API",
    "Redis",
    "Elasticsearch",
    "React",
    "Angular",
    "Vue.js",
    "HTML",
    "CSS",
    "JavaScript",
    "TypeScript",
    "Git",
    "Jenkins",
    "Travis CI",
    "Agile",
    "Scrum",
    "Kanban",
    "Pyramid",
    "CherryPy",
    "Tornado",
    "Peewee ORM",
    "Couchbase",
    "Robot Framework",
    "Splinter",
    "Prometheus",
    "Grafana",
    "Splunk",
    "Ansible",
    "Puppet",
    "Chef",
    "Fabric",
    "Pandas",
    "Scrapy",
    "Beautiful Soup",
    "XGBoost",
    "LightGBM",
    "React Native",
    "Electron",
    "Jupyter Notebooks",
    "Flask",
    "Dash",
    "Falcon",
    "Airflow",
    "Click",
    "Marshmallow",
    "Pydantic",
    "SQl",
    "MySQL",
    "MongoDB",
    "DRF",
    "PostgresSQL",
    "Clouds",
    "SQLite",
    "Microsoft SQL Server",
    "Oracle Database",
    "IBM Db2",
    "MariaDB",
    "Cassandra",
    "Elasticsearch",
    "Firebase",
    "Neo4j",
    "Golang",
    "Terraform",
    "k8s",
    "CI/CD",
    "Data Modeling",
    "Microservices",
    "Rest API",
    "REST",
    "linux",
    "JS",
    "Machine learning",
    "OOP",
    "NoSQL",
    "Algorithms",
    "Asyncio",
]

regex_pattern = r'\b(?:' + '|'.join(re.escape(tech) for tech in TECHNOLOGIES) + r')\b'