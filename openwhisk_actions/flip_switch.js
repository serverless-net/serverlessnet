var rp = require('request-promise');

function main(params) {
    var relayerPort = params.relayerPort ? params.relayerPort : 4999;
    if (params.target) 
        var target = params.target;
    else 
        throw('No target host port provided.');
    // sends a request back to relayer app
    var options = {
        method: 'POST',
        uri: 'http://172.17.0.1:' + relayerPort + '/relay', // Directly trigger actuator to test
        body: {
            url: 'http://172.17.0.1:' + '/state', // To generalize this, receive a target thorugh param, hard code for now
            target: target
        },
        json: true // Automatically stringifies the body to JSON
    };

    return rp(options) // 172.17.0.1 is the docker0 ip, need to automate this later
    .then(function (htmlString) {
        return {msg: htmlString};
    })
    .catch(function (err) {
        throw err;
    });
}
