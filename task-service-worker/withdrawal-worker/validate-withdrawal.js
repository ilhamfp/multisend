const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function validateWithdrawal({ task, taskService }) {
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
	    url: BASE_URL  + "balance",
	    method: 'GET',
	    headers: headers
	};

	request(options, function(error, response, body) {
	    // console.log(JSON.parse(response.body))
	    if (response.statusCode === 200) {
	        response = JSON.parse(response.body)
	        if (!response.error) {
	            current_balance = response.balance
    	        console.log("Current balance is: "+current_balance)
    	        if (amount < 0 || current_balance < amount) {
    	        	processVariables.set('sufficient', false);
    	        	console.log("Invalid withdrawal")
    	        } else {
    	        	processVariables.set('sufficient', true);
    	        	console.log("Valid withdrawal")
    	        }
    	        taskService.complete(task, processVariables, null);
	        } else {
	            console.log(response.error);
	        }
	    } else {
	        console.log("ERROR VALIDATE WITHDRAWAL: " + response.statusCode);
	    }
	});

    // Komen di bawah merupakan peninggalan sebelum diganti ke REST
	// var url = 'http://localhost:5006/?wsdl';
	// var args = {
	// 	request:{
	// 		secret_key : 'vIywNgjTJTNwIHZCXyHTZgfBepWwCx'
	// 	}
	// };
	// soap.createClient(url, function(err, client) {
	//     client.get_balance(args, function(err, result) {
	//         // result = JSON.stringify(result);
	//         current_balance = result.get_balanceResult.current_balance
	//         console.log("Current balance is: "+current_balance)
	//         if (amount < 0 || current_balance < amount) {
	//         	processVariables.set('sufficient', false);
	//         	console.log("Invalid withdrawal")
	//         } else {
	//         	processVariables.set('sufficient', true);
	//         	console.log("Valid withdrawal")
	//         }
	//         taskService.complete(task, processVariables, null);
	//     });
	// });
}

module.exports = validateWithdrawal;
