from flask import Flask, render_template, request, redirect, url_for
import requests, argparse
from time import sleep
import json
import os
import fileinput

app = Flask(__name__)
data = {}
port_numbers = []
actuators = []

@app.route('/', methods=['GET'])
def node_1_get():
    # reads in config JSON file
    with open('sample_config.json') as json_file:
        data = json.load(json_file)
        for key in data.keys():
            current_actuators = []
            if "sw" in key:
                port_numbers.append(str(data[key]['port']))
                current_actuators = list(map(str, data[key]['outgoing']))
                actuators.append(current_actuators.copy())
    
    html = None
    if os.stat('templates/node_1.html').st_size == 0:
        html = open('templates/node_1.html', "w+")
    else:
        html = open('templates/node_1.html', "w")

    html.write("""<html>
    <body>
        <head>
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css">
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js"></script>
          <link href="https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css" rel="stylesheet">
          <script src="https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js"></script>
          <link rel="stylesheet" href="../static/node_1.css">
        </head>\n""")
    for i in range(len(port_numbers)):
        html.write("""        <div><input type="checkbox" class='toggle' id='box""" + port_numbers[i] + """' checked data-toggle="toggle"></div>\n""")
        for j in range(len(actuators[i])):
            html.write("""        <div class="red", id="circle""" + actuators[i][j] + """" style="margin-bottom:20px;"></div>\n""")
    html.write("""
    </body>
    <script>
    $(document).ready(function() {
        var interval = 1000; 
        function get_status() {
            $.ajax({
            type: "GET",
            url: "http://localhost:5000/access",
            success: function(response) {
                console.log(response);
                response = JSON.parse(response);
                console.log(response);""")
    for i in range(len(port_numbers)):
        for j in range(len(actuators[i])):
            html.write("""
                if (Object.keys(response).indexOf(\"""" + actuators[i][j] + """\") >= 0){
                    if (response[\"""" + actuators[i][j] + """\"] == 0) {
                        $("#circle""" + actuators[i][j] + """").attr("class", "black");
                    }
                    else {
                        $("#circle""" + actuators[i][j] + """").attr("class", "red");
                    }
                }
            """)
    html.write("""
            },
            complete: function(response) {
                setTimeout(get_status, interval);
            }
        });
        }
        setTimeout(get_status, interval);\n""")
    html.write("""      });
    </script>
</html>""")
    html.close()

    return render_template('node_1.html')

# proxy
@app.route('/access', methods=['GET'])
def accessor():
    result = requests.get(url='http://128.59.22.210:4000/state')
    return result.text

if __name__ == '__main__':
    app.run(host='0.0.0.0')
