import { createClient} from 'redis';

const client = createClient();

client.on('connect',() => console.log('Redis client connected to the server'));

client.on( 'error', err => console.log('Redis client not connected to the server:', err));

const print = (error, reply) => {
  if (error) {
    console.error(error);
} else {
  if (reply === 'OK') {
    console.log('Reply:', reply);
 } else {
  console.log(reply);
  }
}
};

async function setNewSchool(schoolName, value, print) {
 try{
    await client.set(schoolName, value, print);
} catch (error) {
    console.error('Error:', error);
 }
}

function displaySchoolValue(schoolName,print) {
  const value = client.get(schoolName, print);
  console.log(value);
}

displaySchoolValue('Holberton', print);
setNewSchool('HolbertonSanFrancisco', '100', print);
displaySchoolValue('HolbertonSanFrancisco', print);
