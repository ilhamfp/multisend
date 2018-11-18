const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function calculateCost({ task, taskService }) {
	const COST = 100;
	let from_lat = task.variables.get('from_lat')
	let from_lng = task.variables.get('from_lng')
	let to_lat = task.variables.get('destination').split(',')[0]
	let to_lng = task.variables.get('destination').split(',')[1]
	let processVariables = new Variables();
	// console.log(task.variables.getAllTyped());
	processVariables.setAllTyped(task.variables.getAllTyped());

	let calculatedDistance = Math.floor( Math.sqrt( ((to_lat-from_lat)*(to_lat-from_lat)) + ((to_lng-from_lng)*(to_lng-from_lng)) ) );
	processVariables.setTyped('cost', {
										  value: COST*calculatedDistance,
										  type: "long",
										  valueInfo: {}
										});
	// console.log("Test\n"+processVariables.get('receiver_name'))
	console.log("Cost to send an item for "+calculatedDistance+"KM is "+processVariables.get('cost'));
	taskService.complete(task, processVariables, null);
}

module.exports = calculateCost;
