const { Variables } = require('camunda-external-task-client-js');
const request = require('request');

async function searchAvailableRooms({ task, taskService }) {
	let room_type_id = task.variables.get('room_type_id');
	let check_in = task.variables.get('check_in');
	let check_out = task.variables.get('check_out');
	let min_price = task.variables.get('min_price');
	let max_price = task.variables.get('max_price');

	let processVariables = new Variables();

	const headers = {
		'Content-Type': 'application/json'
	};
	
	const query = {
		'room_type_id': room_type_id,
		'check_in': check_in,
		'check_out': check_out,
		'min_price': min_price,
		'max_price': max_price
	}

	const options = {
		url: 'http://127.0.0.1:5000/rooms',
		method: 'GET',
		headers: headers,
		qs: query
	}

	request(options, function(error, response, body) {
		if (body.length == 0) {
			processVariables.set('available', false);
			processVariables.set('message', 'There is no available room.');
		} else {
			processVariables.set('available', true);
			processVariables.set('rooms', body);
		}
		taskService.complete(task, processVariables, null);
	});
}

module.exports = searchAvailableRooms;
