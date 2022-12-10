# PSL_Project4

## Usage

### Online webapp

https://psl-proj-2pages.onrender.com/

### Testing on your own computer

On terminal, CD into a directory that you want to work on

```
git clone https://github.com/tianhaoluo/PSL_Project4.git
```

CD into PSL_Project4 folder
```
cd PSL_Project4
```

Create a virtual environment so you have all the packages needed, and it won't mess with your own environment

```
python3 -m venv tluo3-venv
```

Do this to activate the virtual environment if on Windows
```
tluo3-venv\Scripts\activate.bat
```

Do this to activate the virtual environment if on Mac
```
source tluo3-venv/bin/activate
```

If you still see (base) environment active on your terminal
```
conda deactivate
```

Install packages on the virtual environment
```
pip install -r requirements.txt
```

Run the program, it should show you something like Dash is running on http://127.0.0.1:8050/
```
python app.py
```

If port 8050 is already in use (if you're openning another students' app etc.), it might not let you start the program. You need to close that program first.

Paste http://127.0.0.1:8050/ to the browser. Enjoy the app!

Finally, deactivate the virtual environment

```
deactivate
```


