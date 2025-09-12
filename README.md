Social FastAPI

A production-ready FastAPI application with PostgreSQL database, tested via pytest and deployed automatically to Railway using GitHub Actions CI/CD.

Features
	FastAPI backend with async support
	PostgreSQL as the database
	JWT Authentication with refresh tokens
	Automated testing with pytest + GitHub Actions
	Continuous deployment to Railway
	Ready for containerization with Docker & Kubernetes

Tech Stack
	FastAPI
	PostgreSQL
	SQLAlchemy
 	ORM
	Alembic
 		migrations
	Pydantic
 		for validation
	Pytest
 		for testing
	Railway
 		for deployment

⚙️ Setup & Installation
1️⃣ Clone the repository
	git clone https://github.com/your-username/social_fastapi.git
	cd social_fastapi

2️⃣ Create a virtual environment
	python -m venv venv
	source venv/bin/activate   # On Linux/Mac
	venv\Scripts\activate      # On Windows

3️⃣ Install dependencies
	pip install -r requirements.txt

4️⃣ Setup environment variables
	Create a .env file in the root directory:
	DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<dbname>
	SECRET_KEY=<your_secret_key>
	ALGORITHM=HS256
	ACCESS_TOKEN_EXPIRES_MINUTES=30
 
5️⃣ Run migrations
	alembic upgrade head

6️⃣ Start the application
	uvicorn app.main:app --reload
	Visit: 👉 http://localhost:8000/docs

🧪 Running Tests
	pytest
	GitHub Actions automatically runs tests on each PR and push to main.

🚀 Deployment
	This project is deployed on Railway using GitHub Actions.
	Deploy manually:
		railway up --service api
	GitHub Actions workflow:
		On each push to main, tests are executed
		If successful, the app is deployed to Railway (prod environment)

🔑 Environment Variables
	DATABASE_URL:	PostgreSQL connection string
	SECRET_KEY:	Secret for JWT signing
	ALGORITHM:	Hashing algorithm (e.g., HS256)
	ACCESS_TOKEN_EXPIRES_MINUTES:	JWT expiration time
