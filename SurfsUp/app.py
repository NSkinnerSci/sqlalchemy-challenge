from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precip():
    


@app.route("/api/v1.0/stations")
def station():
    
    
@app.route("/api/v1.0/tobs")
def tobs():
    

@app.route("/api/v1.0/<start>")
def start():
    
@app.route("/api/v1.0/<start>/<end>")
def end():



if __name__ == "__main__":
    app.run(debug=True)
