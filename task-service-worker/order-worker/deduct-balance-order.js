const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');
BASE_URL = 'http://127.0.0.1:9999/';


async function deductBalanceOrder({ task, taskService }) {
	let processVariables = new Variables();
	// console.log(task.variables.getAllTyped());
	processVariables.setAllTyped(task.variables.getAllTyped());

	let secret_key = task.variables.get('secret_key');
	let cost = task.variables.get('cost');

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
                                "amount" : cost
                            })
    };

    request(options, function(error, response, body) {
        // console.log(JSON.parse(response.body))
        if (response.statusCode === 200) {
            response = JSON.parse(response.body)
            if (!response.error) {
                current_balance = response.balance
                console.log("Current balance is deducted by: " + cost);
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

    // Komen di bawah merupakan peninggalan sebelum diganti ke REST
	// var url = 'http://localhost:5006/?wsdl';
	// var args = {
	// 	request:{
	// 		secret_key : secret_key,
 //            bank_detail : '23523423423',
 //            payment_method : 'BCA',
 //            amount : cost,
	// 	}
	// };
	// soap.createClient(url, function(err, client) {
	//     client.withdraw(args, function(err, result) {
	//         // console.log(JSON.stringify(result))
	//         current_balance = result.withdrawResult.current_balance;
	//         console.log("Current balance is deducted by: " + cost);
	//         console.log("Current balance is: " + current_balance);
	//         taskService.complete(task, processVariables, null);
	//     });
	// });
}

module.exports = deductBalanceOrder;
