@echo on
git clone https://github.com/jmolinap2/Pegasus-Vet.git
cd Pegasus-Vet
git checkout dda551e
python -m venv venv
call venv\Scripts\activate.bat
pip install -r deploy/txt/requirements.txt
