from flask import Flask, render_template, request, Response
import requests
import pandas as pd
import io 


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        url = request.form.get('url')

        try:
            
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            
            df_list = pd.read_html(io.StringIO(response.text))

            if not df_list:
                return "No tables found on the page.", 400

            
            df = df_list[0]

            
            output = io.StringIO()
            df.to_csv(output, index=False)
            output.seek(0) 

            
            return Response(
                output,
                mimetype="text/csv",
                headers={"Content-Disposition": "attachment;filename=data.csv"}
            )

        except Exception as e:
            
            return f"An error occurred: {e}", 500

    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
