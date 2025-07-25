from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_preview():
    if request.method == "POST":
        excel_file = request.files.get("excel_file")
        if excel_file:
            df = pd.read_excel(excel_file)
            table_html = df.to_html(classes='table table-bordered', index=False)
            return render_template("preview.html", tables=table_html)
    return render_template("preview.html", tables=None)

if __name__ == "__main__":
    app.run(debug=True)



