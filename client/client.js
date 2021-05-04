  chatConnection = io.connect('http://127.0.0.1:5000/chat');
  identifyConnection = io.connect('http://127.0.0.1:5000/identify');
  commandConnection = io.connect('http://127.0.0.1:5000/command');
  
  var messages = document.getElementById('messages');
  var form = document.getElementById('form');
  var input = document.getElementById('input');
  var user = {};
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    if (input.value) {
      if (input.value.startsWith('/')) {
        commands(input.value)
      } else {
        chatConnection.emit('send_message', {'msg':input.value, 'user':user});
      }
      input.value = '';
    }
  });

  function commands(user_input) { 
    data = {
        "args": user_input.split('=')[1],
        "user": user,
    };
    data.args = data.args.split('"').join('').split("'").join(''); // Hack to clean quotes  
    action = user_input.split('=')[0].slice(1);

    if(action === 'stock') {
      commandConnection.emit('stock', data);
    }

    if(action === 'create_user') {
        identifyConnection.emit('create_user', data)
    }
  }

  chatConnection.on('connect', function(){
    chatConnection.emit('login', user);
  });  
  
  chatConnection.on('teste', function(){
    alert("AE CARAIO");
  });

  setInterval(function(){
    chatConnection.emit('list_messages', user);
  }, 2000);

  messageTextComposition = function(msg) {
    content = msg.text;
    author = 'ChatAPI';
    if('user' in msg){
        author = JSON.stringify(msg.user);
    }
    if('error' in msg) {
        content = msg.error;
    } 
    return author + ': ' + content;
  }

  identifyConnection.on('create_user_reply', function(msg){
      decoded_msg = JSON.parse(msg);
      if ('error' in decoded_msg) {
        msg = messageTextComposition(decoded_msg);  
        alert(msg);
      } else {
        user = decoded_msg;
      }
  });

  chatConnection.on('broadcast_message', function(msg) {
    decoded_msg = JSON.parse(msg);
    appendMessage(decoded_msg);
  });

  chatConnection.on('list_messages_reply', function(msg) {
    decoded_msgs = JSON.parse(msg);
    cleanMessages()
    for(i=0; i<decoded_msgs.length;i++) {
        msg = messageTextComposition(decoded_msgs[i]);
        appendMessage(msg);
    }
  });

  function cleanMessages() {
    messages.innerHTML = '';
  }

  function appendMessage(msg) {
    var item = document.createElement('li');
    item.textContent = msg;
    messages.appendChild(item);
    window.scrollTo(0, document.body.scrollHeight);
  }
