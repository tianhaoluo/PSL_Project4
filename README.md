# PSL_Project4

## Introduction

### Online webapp

https://dash-app-psl.azurewebsites.net/ (closed after course to save cost)

### Genre-based recommendation

<ul>
  <li> 'Rating' method: return top 8 movies based on average rating (for movies with more than 100 ratings only) </li>
  <li> 'Popularity' method: The top 8 movies based on recency (for larger categories like Comedy, can afford to look at most recent 2 years (1999,2000 since it's an old dataset) ; for smaller categories, the lookback window will include more years).</li> 
</ul>

### IBCF-based recommendation
  
<ul>
  <li> When you don't rate anything, it will return movies with id 1-8 (they're all movies users might like, that's why I ask users to rate). </li>
  <li> Otherwise, Surprise will try to return top-8 results based on predicted rating</li>
  <li> A movie recommended CAN appear in the section where the program asks the user to rate, as long as it's not rated. </li>
</ul>

## Usage

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

The logic of generating some partial results can be found at prepare_loaded_data.py. It can be run like this
```
python prepare_loaded_data.py
```

Start the webapp, it should show you something like Dash is running on http://127.0.0.1:8050/
```
python app.py
```

If port 8050 is already in use (if you're openning another students' app etc.), it might not let you start the program. You need to close that program first.

Paste http://127.0.0.1:8050/ to the browser. Enjoy the app!

Finally, deactivate the virtual environment

```
deactivate
```


