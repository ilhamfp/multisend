const { Variables } = require('camunda-external-task-client-js');
const request = require('request');

async function confirmBookingInformation({ task, taskService }) {
    let room_id = task.variables.get('room_id');
    let guest_id = task.variables.get('guest_id');
    let name = task.variables.get('name');
    let mobile_phone = task.variables.get('mobile_phone');
    let identity_number = task.variables.get('identity_number');
    let email = task.variables.get('email');

	let processVariables = new Variables();

	const headers = {
		'Content-Type': 'application/json'
	};

	const options = {
		url: 'http://127.0.0.1:5000/rooms/' + room_id,
		method: 'GET',
		headers: headers
	}
	
	request(options, function(error, response, body) {
        processVariables.set('room_id', body.id);
        processVariables.set('number', body.number);
        processVariables.set('bed_number', body.type.bed_number);
        processVariables.set('facilities', body.type.facilites);
        processVariables.set('name', body.type.name);
        processVariables.set('price', body.type.price);

		taskService.complete(task, processVariables, null);
	});
}

module.exports = confirmBookingInformation;
