const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function checkDeliveryCompletionn({ task, taskService }) {
	let processVariables = new Variables();
    // console.log(task.variables.getAllTyped());
    processVariables.setAllTyped(task.variables.getAllTyped());
	// Asumsikan selalu berhasil
	console.log("Item delivered!");
	processVariables.set('deliveryComplete', true);
	taskService.complete(task, processVariables, null);
}

module.exports = checkDeliveryCompletionn;
