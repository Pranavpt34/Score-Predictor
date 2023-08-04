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


@app.route('/get_opposition', methods=['POST'])
def get_opposition():
    data = request.json
    selected_team = data['selected_team']
    opposition = df['Opposition'].unique().tolist()
    opposition_team = [country for country in opposition if country != selected_team]
    return jsonify({'opposition': opposition_team})



@app.route('/get_grounds', methods=['GET'])
def get_grounds():
    grounds = df['Ground'].unique().tolist()
    return jsonify({'grounds': grounds})



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
    selected_opposition = data['selected_opposition']
    # Process the selected data as required
    print(f'Selected Team: {selected_team}')
    print("Selected Player",selected_player)
    print(f'Selected Ground: {selected_ground}')
    print(f'Selected Opposition :{selected_opposition}')
    import sklearn
    print(sklearn.__version__)
    import sys
    print(sys.version)
    
    predicted_scores = team_score(selected_player,selected_ground,selected_opposition)
    return jsonify(predicted_scores)


#function for the prediction


def team_score(player_list,location,Opposition):
    df_copy = pd.read_csv("df_average.csv")
    # global df_copy
    with open('avg_performance_team.json', 'r') as json_file:
        player_avg_performance = json.load(json_file)

    with open('total_avg_performance.json', 'r') as json_file:
        avg_performance_dict = json.load(json_file)
    

    global gb_regressor_wo_sr
    with open("score_prediction_model.pickle", 'rb') as f:
        gb_regressor_wo_sr = pickle.load(f)

    def predict_run(location,BF,Pos,Opposition,Player):
        with open('columns.json') as f:
            columns = json.load(f)
            x = columns["data_columns"]

        loc_index_ground = x.index(location)
        loc_index_Player = x.index(Player)
        loc_index_Opposition = x.index(Opposition)

        predict_column = np.zeros(len(x))

        predict_column[0] = BF
        predict_column[1] = Pos

        predict_column[loc_index_ground] = 1
        predict_column[loc_index_Opposition] = 1
        predict_column[loc_index_Player] = 1

        print("Runs predicted by GB  without SR : ",gb_regressor_wo_sr.predict([predict_column])[0])
        return gb_regressor_wo_sr.predict([predict_column])[0]

    runs = 0
    Total_balls = 0
    wickets =0
    score_card = {}
    for Player in player_list:
        BF= np.round(df_copy[(df_copy["Opposition"] == Opposition) & ((df_copy["Ground"] == location)&(df_copy["Player"] == Player))]["BF"].mean())
        if np.isnan(BF):
            if Player in player_avg_performance and Opposition in player_avg_performance[Player]:
                BF = np.round(player_avg_performance[Player][Opposition][1])

            else:
                BF = np.round(avg_performance_dict[Player]["BF"])


        print("Player Name : ", Player)
        Pos = player_list.index(Player) + 1
        if (Total_balls + BF) <= 120:
            Total_balls = Total_balls + BF
            wickets += 1
            print("Total Balls : ",Total_balls)
            print("Number of Balls faced by the Player ",BF)
            runs += np.round(predict_run(location,BF,Pos,Opposition,Player))
            score_card[Player] = [int(np.round(predict_run(location, BF, Pos, Opposition, Player))),int(BF)]
        else:
            if 120 - Total_balls == 0:
                break
            else:
                BF = 120 - Total_balls
                print("Number of Balls faced by the Player ",BF)
                wickets +=1
                runs += np.round(predict_run(location, BF, Pos, Opposition, Player))
                Total_balls = Total_balls + BF
                score_card[Player] = [int(np.round(predict_run(location, BF, Pos, Opposition, Player))),int(BF)]
                break

        print()
        print()
    score_card["Total Score"] = [int(runs), int(Total_balls)]
    print(score_card)
    print("Runs Scored By Team  based on the Average performance of each Player  : ",np.round(runs), "with in ",Total_balls," Balls loosing ",wickets," Wickets")
    return score_card



if __name__ =="__main__":
    app.run(debug=False,host='0.0.0.0')
