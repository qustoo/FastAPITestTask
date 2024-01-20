create_env:
	@echo "Creating  virtual environment..."
	python -m venv venv
	.\venv\Scripts\activate
	@echo "Virtual environment created"
install_depends:
	@echo "Installing dependencies..."
	pip install -r .\requirements.txt
	@echo "Done"
black:
	python -m black ./app
flake8:
	python -m flake8 ./app
isort:
	python -m isort ./app
up:
	docker-compose -f docker-compose.yml up -dependencies
down:
	docker-compose -f docker-compose.yml down
run:
	@echo "Running the app..."
	uvicorn app.main:app --reload --port 8000 
tests:
	@echo "Ruiing the tests..."
	pytest app/tests/ -v