const {Variables, Client, logger } = require('camunda-external-task-client-js');

// configuration for the Client:
//  - 'baseUrl': url to the Process Engine
//  - 'logger': utility to automatically log important events
const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger };

// create a Client instance with custom configuration
const client = new Client(config);

// susbscribe to the topic: 'calculate-cost'
client.subscribe('calculate-cost', async function({ task, taskService }) {
  // Put your business logic here

  // Get a process variable
  const distance = task.variables.get('distance');
  const item = task.variables.get('item');
  cost = distance*10000;
  console.log(`Lewat calculate-cost`);
  console.log(`The cost to send '${item}' is Rp ${cost},- `);

  const variables = new Variables();
  variables.set('user_id', task.variables.getTyped('user_id'));
  variables.set('item', task.variables.getTyped('item'));
  variables.setTyped('cost', {
                          value: cost,
                          type: "long",
                        });
  // Complete the task
  await taskService.complete(task, variables);
});


// susbscribe to the topic: 'check-balance'
client.subscribe('check-balance', async function({ task, taskService }) {
  // Put your business logic here

  // Get a process variable
  const cost = task.variables.get('cost');
  console.log(`Lewat check-balance`);

  sufficient = true;
  if (cost > 1000000) {
    sufficient = false;
  }

  const variables = new Variables();
  variables.set('user_id', task.variables.getTyped('user_id'));
  variables.set('item', task.variables.getTyped('item'));
  variables.set('cost', task.variables.getTyped('cost'));
  variables.setTyped('sufficient', {
                          value: sufficient,
                          type: "boolean",
                        });
  // Complete the task
  await taskService.complete(task, variables);
});

// susbscribe to the topic: 'deduct-balance'
client.subscribe('deduct-balance', async function({ task, taskService }) {
  // Put your business logic here

  // Get a process variable
  const cost = task.variables.get('cost');
  console.log(`Lewat deduct-balance`);
  console.log(`Balance deducted by ${cost}`);


  const variables = new Variables();
  variables.set('user_id', task.variables.getTyped('user_id'));
  variables.set('item', task.variables.getTyped('item'));
  variables.set('cost', task.variables.getTyped('cost'));
  // Complete the task
  await taskService.complete(task, variables);
});