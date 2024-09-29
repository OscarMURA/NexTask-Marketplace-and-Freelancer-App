const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/messaging/' + conversationId + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#message-container').innerHTML += (
        '<div class="message"><strong>' + data.sender + '</strong>: ' + data.message + '</div>'
    );
};

document.querySelector('#message-form').onsubmit = function(e) {
    e.preventDefault();
    const messageInputDom = document.querySelector('#message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};
