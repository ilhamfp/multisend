const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function deductBalance({ task, taskService }) {
	let secret_key = task.variables.get('secret_key');
	let amount = task.variables.get('amount');
	let processVariables = new Variables();
	processVariables.set('secret_key', secret_key);
	processVariables.set('amount', amount);

	const headers = {
        'Content-Type': 'application/json',
        'Authorization' : secret_key
    };

    const options = {
        url: BASE_URL  + "balance/withdraw",
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
                                "bank" : '23523423423',
                                "payment_method" : 'BCA',
                                "amount" : amount
                            })
    };

    request(options, function(error, response, body) {
        // console.log(JSON.parse(response.body))
        if (response.statusCode === 200) {
            response = JSON.parse(response.body)
            if (!response.error) {
                current_balance = response.balance
                console.log("Current balance is deducted by: " + amount);
                console.log("Current balance is: " + current_balance);
                processVariables.set('balance_has_deducted', true);
                taskService.complete(task, processVariables, null);
            } else {
                console.log(response.error);
            }
        } else {
            console.log("ERROR DEDUCT BALANCE: " + response.statusCode);
        }
    });

	// var url = 'http://localhost:5006/?wsdl';
	// var args = {
	// 	request:{
	// 		secret_key : secret_key,
	// 		bank_detail : '23523423423',
	// 		payment_method : 'BCA',
	// 		amount : amount,
	// 	}
	// };
	// soap.createClient(url, function(err, client) {
	//     client.withdraw(args, function(err, result) {
	//         // console.log(JSON.stringify(result))
	//         current_balance = result.withdrawResult.current_balance;
	//         console.log("Current balance is deducted by: " + amount);
	//         console.log("Current balance is: " + current_balance);
	//         taskService.complete(task, processVariables, null);
	//     });
	// });
}

module.exports = deductBalance;
