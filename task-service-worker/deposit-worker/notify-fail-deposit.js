const { Variables } = require('camunda-external-task-client-js');
const request = require('request');
var soap = require('soap');

async function notifyFailDeposit({ task, taskService }) {
	let processVariables = new Variables();
	// notify fail ke user
  var emailText = "Fail";
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
    subject: 'Deposit Status',
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
  console.log("Deposit aborted by payment gateway")
}

module.exports = notifyFailDeposit;
