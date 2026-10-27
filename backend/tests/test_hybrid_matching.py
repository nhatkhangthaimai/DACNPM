import pytest
from app.ai.pipeline import calculate_hybrid_match, normalize_skill, compute_cosine_similarity


class TestHybridJobMatching:
    """
    Test suite for Hybrid Job Matching algorithm as specified in Section 7.
    Validates TC01 to TC06 test cases.
    """

    def test_tc01_python_backend_high_match(self):
        """TC01: CV (Python, FastAPI, PostgreSQL) vs JD (Python Backend) -> Kỳ vọng: Phù hợp cao"""
        cv_data = {
            "summary": "Senior Python developer with strong experience building scalable REST APIs and relational databases.",
            "hard_skills": ["Python", "FastAPI", "PostgreSQL"],
            "experience": [{"job_title": "Python Developer", "description": "Developed backend microservices with FastAPI and Postgres."}]
        }
        job_data = {
            "title": "Python Backend Developer",
            "description": "Looking for a Python Backend Engineer proficient in FastAPI, SQL and relational databases.",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
            "preferred_skills": ["Docker"]
        }

        result = calculate_hybrid_match(cv_data, job_data)

        assert result["overall_score"] >= 85.0, f"Expected high match >= 85, got {result['overall_score']}"
        assert result["hard_skills_score"] == 100.0
        assert len(result["missing_required_skills"]) == 0
        assert len(result["matched_skills"]) >= 3
        assert "xuất sắc" in result["ai_explanation"].lower() or "tương thích" in result["ai_explanation"].lower()

    def test_tc02_frontend_react_high_match(self):
        """TC02: CV (React, JavaScript, CSS) vs JD (Frontend React) -> Kỳ vọng: Phù hợp cao"""
        cv_data = {
            "summary": "Frontend specialist focused on React components, CSS architecture and modern JavaScript.",
            "hard_skills": ["React", "JavaScript", "CSS"],
            "experience": [{"job_title": "Frontend Engineer", "description": "Built responsive user interfaces with React and Tailwind CSS."}]
        }
        job_data = {
            "title": "Frontend React Developer",
            "description": "Build high-performance web applications using React, JavaScript and modern CSS.",
            "required_skills": ["React", "JavaScript", "CSS"],
            "preferred_skills": ["TypeScript"]
        }

        result = calculate_hybrid_match(cv_data, job_data)

        assert result["overall_score"] >= 85.0, f"Expected high match >= 85, got {result['overall_score']}"
        assert result["hard_skills_score"] == 100.0
        assert len(result["missing_required_skills"]) == 0

    def test_tc03_partial_match(self):
        """TC03: CV (Python, Machine Learning) vs JD (Python Backend) -> Kỳ vọng: Phù hợp một phần"""
        cv_data = {
            "summary": "AI researcher and Python programmer with experience in machine learning models.",
            "hard_skills": ["Python", "Machine Learning", "PyTorch"],
            "experience": [{"job_title": "ML Engineer", "description": "Trained machine learning models using Python."}]
        }
        job_data = {
            "title": "Python Backend Engineer",
            "description": "Backend engineer responsible for database APIs, FastAPI and PostgreSQL services.",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
            "preferred_skills": ["Docker"]
        }

        result = calculate_hybrid_match(cv_data, job_data)

        # Python matches (1/3 required), FastAPI and PostgreSQL missing
        assert 45.0 <= result["overall_score"] < 80.0, f"Expected partial match between 45 and 80, got {result['overall_score']}"
        assert "FastAPI" in result["missing_required_skills"]
        assert "PostgreSQL" in result["missing_required_skills"]
        assert len(result["recommendations"]) >= 2

    def test_tc04_irrelevant_cv_low_match(self):
        """TC04: CV (Graphic Design, Photoshop) vs JD (Backend Python) -> Kỳ vọng: Phù hợp thấp"""
        cv_data = {
            "summary": "Creative graphic designer skilled in visual arts, Adobe Photoshop and marketing illustrations.",
            "hard_skills": ["Graphic Design", "Photoshop", "Illustrator"],
            "experience": [{"job_title": "Graphic Designer", "description": "Designed banners, social media artwork and vector illustrations."}]
        }
        job_data = {
            "title": "Senior Backend Python Developer",
            "description": "Develop high-scale backend microservices with Python, FastAPI, Docker, and PostgreSQL databases.",
            "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
            "preferred_skills": ["Kubernetes"]
        }

        result = calculate_hybrid_match(cv_data, job_data)

        assert result["overall_score"] < 40.0, f"Expected low match < 40, got {result['overall_score']}"
        assert result["hard_skills_score"] == 0.0
        assert len(result["missing_required_skills"]) == 4

    def test_tc05_empty_skills_detected(self):
        """TC05: CV (Không có kỹ năng) vs JD (Backend Python) -> Kỳ vọng: Phát hiện thiếu kỹ năng"""
        cv_data = {
            "summary": "New applicant seeking opportunities in tech.",
            "hard_skills": [],
            "experience": []
        }
        job_data = {
            "title": "Backend Python Developer",
            "description": "Looking for Python backend engineers.",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
            "preferred_skills": []
        }

        result = calculate_hybrid_match(cv_data, job_data)

        assert result["overall_score"] <= 20.0, f"Expected near zero score <= 20, got {result['overall_score']}"
        assert result["hard_skills_score"] == 0.0
        assert len(result["missing_required_skills"]) == 3
        assert "Python" in result["missing_required_skills"]

    def test_tc06_synonym_semantic_matching(self):
        """TC06: CV có kỹ năng đồng nghĩa (ReactJS vs React, NodeJS vs Node.js, Postgres vs PostgreSQL) -> Semantic Matching hoạt động"""
        cv_data = {
            "summary": "Full-stack engineer using ReactJS, NodeJS and Postgres in production.",
            "hard_skills": ["ReactJS", "NodeJS", "Postgres"],
            "experience": [{"job_title": "Full Stack Dev", "description": "Built full-stack web application using React.js and Node.js."}]
        }
        job_data = {
            "title": "Full Stack Engineer",
            "description": "Looking for a full stack developer skilled in React, Node.js and PostgreSQL.",
            "required_skills": ["React", "Node.js", "PostgreSQL"],
            "preferred_skills": []
        }

        result = calculate_hybrid_match(cv_data, job_data)

        assert result["overall_score"] >= 85.0, f"Expected high score >= 85 for synonyms, got {result['overall_score']}"
        assert result["hard_skills_score"] == 100.0, f"All synonyms should normalize to match: {result['missing_required_skills']}"
        assert len(result["missing_required_skills"]) == 0
