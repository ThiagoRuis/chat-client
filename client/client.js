var user = {
    "name": 'thiago ruis',
    "email": 'teste@teste.com',
  };

  
  chatConnection = io.connect('http://127.0.0.1:5000/chat');
  identifyConnection = io.connect('http://127.0.0.1:5000/identify');
  commandConnection = io.connect('http://127.0.0.1:5000/command');
  
  var messages = document.getElementById('messages');
  var form = document.getElementById('form');
  var input = document.getElementById('input');
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    if (input.value) {
      if (input.value.startsWith('/')) {
        temp = input.value.split(' ');
        command = temp[0].slice(1);
        temp.shift();
        msg = temp.join(' ');

        if(command.startsWith('stock')) {
          msg = command.split('=')[1];
          command = command.split('=')[0];
        }

        commandConnection.emit(command, {'msg':msg, 'user':user});
      } else {
        chatConnection.emit('send_message', {'msg':input.value, 'user':user});
      }
      input.value = '';
    }
  });

  chatConnection.on('connect', function(){
    chatConnection.emit('login', user);
  });

  setInterval(function(){
    chatConnection.emit('list_messages', user);
  }, 10000);

  messageTextComposition = function(msg) {
    content = msg.text;
    author = 'ChatAPI';
    if('user' in msg){
        author = JSON.stringify(msg.user);
    } 
    return author + ': ' + content;
  }

  chatConnection.on('broadcast_message', function(msg) {
    decoded_msg = JSON.parse(msg);
    var item = document.createElement('li');
    item.textContent = msg;
    messages.appendChild(item);
    window.scrollTo(0, document.body.scrollHeight);
  });

  chatConnection.on('list_messages_reply', function(msg) {
    decoded_msgs = JSON.parse(msg);
    messages.innerHTML = '';
    for(i=0; i<decoded_msgs.length;i++) {
        msg = messageTextComposition(decoded_msgs[i]);
        var item = document.createElement('li');
        item.textContent = msg;
        messages.appendChild(item);
    }
    window.scrollTo(0, document.body.scrollHeight);
  });

