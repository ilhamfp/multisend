const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function notifySuccessDeposit({ task, taskService }) {
	let amount = task.variables.get('amount');
	let processVariables = new Variables();
	// notify success ke user
	taskService.complete(task, processVariables, null);
    console.log("Deposit " + amount + " success")
}

module.exports = notifySuccessDeposit;
