const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function notifyFailWithdrawal({ task, taskService }) {
	let secret_key = task.variables.get('secret_key');
	let amount = task.variables.get('amount');
	let processVariables = new Variables();
	processVariables.set('secret_key', secret_key);
	processVariables.set('amount', amount);
    console.log("Fail")
	// notify fail ke user
	taskService.complete(task, processVariables, null);
}

module.exports = notifyFailWithdrawal;
