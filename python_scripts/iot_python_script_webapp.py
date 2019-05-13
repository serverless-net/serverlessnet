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
    data = requests.get(url='http://128.59.22.210:4001/config').text
    data = json.loads(data)
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
                        $("#circle""" + actuators[i][j] + """").attr("class", "red");
                    }
                    else if (response[\"""" + actuators[i][j] + """\"] == 1) {
                        $("#circle""" + actuators[i][j] + """").attr("class", "black");
                    }
                    else {
                        setTimeout(function() {
                            if ($("#circle""" + actuators[i][j] + """").attr("class") == "red") {
                                $("#circle""" + actuators[i][j] + """").attr("class", "black");
                            }
                            else {
                                $("#circle""" + actuators[i][j] + """").attr("class", "red")
                            }
                        }, interval);
                        setTimeout(function() {
                            if ($("#circle""" + actuators[i][j] + """").attr("class") == "red") {
                                $("#circle""" + actuators[i][j] + """").attr("class", "black");
                            }
                            else {
                                $("#circle""" + actuators[i][j] + """").attr("class", "red");
                            }
                        }, interval);
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
    for i in range(len(port_numbers)):
        html.write("""        $('#box""" + port_numbers[i] + """').change(function() {
          var status = $('#box""" + port_numbers[i] + """').prop("checked");
          $.ajax({
                url: "/get_toggled_status",
                type: "GET",
                data: {status: status, port: """ + port_numbers[i] + """},
            });
        });\n""")
    html.write("""      });
    </script>
</html>""")
    html.close()

    return render_template('node_1.html')

# proxy
@app.route('/access', methods=['GET'])
def accessor():
    result = requests.get(url='http://128.59.22.210:4000/state')
    print(result.text)
    return result.text

# check which one sent the toggled status
@app.route('/get_toggled_status')
def toggled_status():
    current_status = request.args.get('status')
    port_number = request.args.get('port')

    result = requests.post(url="http://128.59.22.210:4001", data={'port_number': port_number})

    return render_template('node_1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
