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
    print("APP.py file")
    teams = df['Team'].unique().tolist()
    print(teams)
    return jsonify({'teams': teams})

@app.route('/get_players', methods=['POST'])
def get_players():
    data = request.json
    selected_team = data['selected_team']
    selected_players = df[df['Team'] == selected_team]['Player'].unique().tolist()
    return jsonify({'players': selected_players})

@app.route('/get_grounds', methods=['POST'])
def get_grounds():
    data = request.json

    grounds = df['Ground'].unique().tolist()
    return jsonify({'grounds': grounds})

# grounds = df[(df['Team'] == selected_team) & (df['Player'] == selected_player)]['Ground'].unique().tolist()
#submit player list
@app.route('/submit_players', methods=['POST'])
def submit_players():
    data = request.get_json()
    selected_players = data.get('selected_players', [])
    print(selected_players)
    response = {'message': 'Players received successfully.'}
    return jsonify(response) 



# @app.route('/submit_selection', methods=['POST'])
# def submit_selection():
#     data = request.json
#     selected_team = data['selected_team']
#     selected_player = data['selected_player']
#     selected_ground = data['selected_ground']
#     # Process the selected data as required
#     print(f'Selected Team: {selected_team}')
#     print(f'Selected Player: {selected_player}')
#     print(f'Selected Ground: {selected_ground}')
#     return jsonify({'message': 'Selection submitted successfully!'})

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

# with open('columns.json') as f:
#         columns = json.load(f)
#         Opposition = columns["data_columns"][152:167]
#         Player = columns["data_columns"][2:151]
#         Ground = columns["data_columns"][167:]


# @app.route('/get_teams', methods=['GET'])
# def get_teams():
#     return jsonify({'teams': Opposition})



# @app.route('/get_teams', methods=['GET'])
# def get_teams():
#     with open('columns.json') as f:
#         teams = json.load(f)
#         print("json file ",teams)
#     return jsonify(teams) 

@app.route('/select_team', methods=['POST'])
def select_team():
    data = request.get_json()
    selected_team = data.get('team')
    print(f'Selected team: {selected_team}')
    return jsonify({'message': f'Team "{selected_team}" selected successfully!'})




if __name__ =="__main__":
    app.run(debug=True)
