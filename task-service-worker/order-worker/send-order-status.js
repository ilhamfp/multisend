const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function sendOrderStatus({ task, taskService }) {
	let processVariables = new Variables();
    // console.log(task.variables.getAllTyped());
    processVariables.setAllTyped(task.variables.getAllTyped());
	// Kirim ke pemannggil
    var emailText = "Failed";
    if (task.variables.get('deliveryComplete')) {
        emailText = "Success";
    }
    var nodemailer = require('nodemailer');

    var transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: 'tubespplbs@gmail.com',
        pass: 'tubespplbs123'
      }
    });

    var mailOptions = {
      from: 'tubespplbs@gmail.com',
      to: 'tubespplbs@gmail.com',
      subject: 'Order Status',
      text: emailText
    };

    transporter.sendMail(mailOptions, function(error, info){
      if (error) {
        console.log(error);
      } else {
        console.log('Email sent: ' + info.response);
      }
    });
	taskService.complete(task, processVariables, null);
}

module.exports = sendOrderStatus;
