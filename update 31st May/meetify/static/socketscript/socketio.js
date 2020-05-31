document.addEventListener('DOMContentLoaded',()=>{

	var socket=io();

	socket.on('connect',()=>{
		socket.send("connected");
	});

	socket.on('message',data=>{
		console.log(`Message recieved:${data}`)

	});
})