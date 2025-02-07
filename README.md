``` bash
pip freeze > requirements.txt
```
### To run local
Create environment
``` bash
python -m venv env
# For Windows:
env\Scripts\activate
# For macOS/Linux:
source env/bin/activate
# Install the dependencies
pip install -r requirements.txt
# Run your project
flask run
```