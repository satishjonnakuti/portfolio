## To-Do CLI

A simple Python command-line app to manage your to-do list. Tasks are stored in a JSON file in your user data directory by default, or at a custom path via `--db`.

### Install / Run

Use directly with Python:

```bash
python -m todo_cli --help
```

Optionally, install in editable mode:

```bash
pip install -e .
```

### Usage

```bash
# Add tasks
python -m todo_cli add "Buy milk"
python -m todo_cli add "Write report"

# List pending (default)
python -m todo_cli list

# List all
python -m todo_cli list --all

# Mark done / undone
python -m todo_cli done 1
python -m todo_cli undone 1

# Edit title
python -m todo_cli edit 2 "Write Q3 report"

# Delete
python -m todo_cli delete 1

# Use a custom database path
python -m todo_cli --db /tmp/todos.json list --all
```

### Data Location

- Linux/macOS: `$XDG_DATA_HOME/todo_cli/todos.json` or `~/.todo_cli/todos.json`
- Override with `--db` to specify a path.

# 📊 Satish Jonnakuti - Data Analyst Portfolio

Welcome to my portfolio website! 🚀  
This site showcases my work as a **Data Analyst** with 5+ years of experience in SQL, Power BI, Tableau, and Python.  
I specialize in **data wrangling, visualization, reporting, and analytics** that help businesses make better decisions.  

🔗 **Live Portfolio:** [Visit Website](https://satishjonnakuti.github.io/portfolio/)

---

## 🧑‍💻 About Me
I am passionate about turning raw data into meaningful insights.  
Skilled in:
- SQL (advanced queries, optimization, stored procedures, ETL pipelines)
- Power BI (dashboards, DAX, reporting automation)
- Tableau (visual storytelling, KPIs, advanced charts)
- Python (data wrangling with Pandas, ML basics, visualization)

---

## 📂 Portfolio Highlights

### 🔹 [Sales Dashboard (Power BI)](https://github.com/yourusername/sales-dashboard)
📌 Interactive dashboard tracking KPIs, revenue trends, and regional performance.  

### 🔹 [SQL Query Optimization](https://github.com/yourusername/sql-projects)
📌 Reduced query execution time by 60% using indexing and restructuring.  

### 🔹 [Customer Segmentation (Python)](https://github.com/yourusername/python-ml-projects)
📌 Applied clustering (K-means) and RFM analysis for targeted marketing.  

---

## 📝 Blog Posts
- **[Optimizing SQL Joins](#)** – Writing efficient SQL queries.  
- **[Power BI vs Tableau](#)** – Choosing the right BI tool.  
- **[Python for Data Wrangling](#)** – Cleaning & transforming messy data.  

---

## 📬 Contact Me
📧 Email: [satishjonnakuti123@gmail.com](mailto:satishjonnakuti123@gmail.com)  
💻 GitHub: [github.com/satishjonnakuti](https://github.com/satishjonnakuti)  
🔗 Portfolio: [satishjonnakuti.github.io/portfolio](https://satishjonnakuti.github.io/portfolio/)  

---

💡 *This portfolio is built using HTML, CSS, and GitHub Pages.*  
⭐ If you like my work, don’t forget to **star this repo**!
