from flask import Flask,request,app,jsonify,url_for,render_template
import pickle
import numpy as np
import pandas as pd
import json


app = Flask(__name__)
#model = pickle.load(open(""))

@app.route('/')
def home():
    return render_template("index.html")

df = pd.read_csv('df_average.csv')

@app.route('/get_teams', methods=['GET'])
def get_teams():
    teams = df['Team'].unique().tolist()
    return jsonify({'teams': teams})

@app.route('/get_players', methods=['POST'])
def get_players():
    data = request.json
    selected_team = data['selected_team']
    selected_players = df[df['Team'] == selected_team]['Player'].unique().tolist()
    return jsonify({'players': selected_players})

@app.route('/get_grounds', methods=['GET'])
def get_grounds():
    grounds = df['Ground'].unique().tolist()
    return jsonify({'grounds': grounds})

# grounds = df[(df['Team'] == selected_team) & (df['Player'] == selected_player)]['Ground'].unique().tolist()
#submit player list
@app.route('/submit_players', methods=['POST'])
def submit_players():
    data = request.get_json()
    selected_players = data.get('selected_players', [])
    response = {'message': 'Players received successfully.'}
    return jsonify(response) 



@app.route('/submit_selection', methods=['POST'])
def submit_selection():
    data = request.json
    selected_team = data['selected_team']
    selected_player = data['selected_player']
    selected_ground = data['selected_ground']
    # Process the selected data as required
    print(f'Selected Team: {selected_team}')
    print("Selected Player",selected_player)
    print(f'Selected Ground: {selected_ground}')
    predicted_scores = {
        "player1": 85,
        "player2": 92,
        "player3": 78
        # Add more players and their predicted scores
    }
    print(predicted_scores)
    predicted = predict(selected_player,selected_ground)
    return jsonify(predicted_scores)

# @app.route('/get_average_strikerate', methods=['POST'])
# def get_average_strikerate():
#     data = request.json
#     player_name = data['player_name']
#     ground = data['ground']
#     opposition_team = data['opposition_team']

#     # Filter the dataframe based on user input
#     filtered_df = df[
#         (df['Player'] == player_name) &
#         (df['Ground'] == ground) &
#         (df['Opposition'] == opposition_team)
#     ]

#     # Calculate the average strikerate for the filtered rows
#     average_strikerate = filtered_df['SR'].mean()

#     # Return the result as JSON
#     return jsonify({'average_strikerate': average_strikerate})

def predict(selected_player,selected_ground):
    with open('columns.json') as f:
        columns = json.load(f)
        x = columns["data_columns"]
    location="Mirpur"
    selected_player,selected_ground
    loc_index_ground = np.where(x==location)[0][0]
    # loc_index_Player = np.where(x==Player)[0][0]
    # loc_index_Opposition = np.where(x==Opposition)[0][0]

    print(loc_index_ground)
    predict_column = np.zeros(len(x))

    predict_column[0] = BF
    predict_column[1] = Pospo




























if __name__ =="__main__":
    app.run(debug=True)
