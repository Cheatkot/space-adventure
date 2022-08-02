const roomName = JSON.parse(document.getElementById('chat-room-name').textContent);
const userName = JSON.parse(document.getElementById('user-name').textContent);

let chatField = document.querySelector("#chat-field");
let chatMessageInput = document.querySelector("#chat-message-input");
let chatMessageSubmit = document.querySelector("#chat-message-submit");
let onlineUsers = document.querySelector("#online-users");

function onlineUsersAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsers.appendChild(newOption);
}

function onlineUsersRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

chatMessageInput.focus();
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13 && !e.shiftKey) {
        chatMessageSubmit.click();
    }
};

chatMessageSubmit.onclick = function(e) {
    if (chatMessageInput.value.length === 0) return;

    const message = chatMessageInput.value;

    // let timestamp = new Date();
    // console.log(timestamp)
    // const timestampString = timestamp.getFullYear() + "-" + (timestamp.getMonth() + 1) + "-" + timestamp.getDate() + " " + timestamp.getHours() + ":" + timestamp.getMinutes() + ":" + timestamp.getSeconds();
    // console.log(timestampString)
    console.log(message);

    chatSocket.send(JSON.stringify({
        'message': message,
        // 'timestamp': timestampString //TODO: Prüfen
    }));
    chatMessageInput.value = "";
};


let chatSocket = null;

function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");

    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the Chat-WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("Chat-WebSocket connection closed unexpectedly. Trying to reconnect in 3s...");

        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 3000);
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        let options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        let color = "alert-secondary";
        let posEnd = false;

        if (data.username === userName) {
            color = "alert-primary";
            posEnd = true;
        }

        switch (data.type) {
            case "chat_message":
                if (posEnd) {
                    chatField.innerHTML += '<div class="row"><div class="col-3"></div><div class="col-9 alert w-75 ' + color + '" role="alert"><p>'+ data.message +'</p><hr><p class="mb-0 text-end"><b>' + data.username + '</b>  @  ' + new Date(data.timestamp).toLocaleTimeString([], options) + '</p></div></div>';
                } else {
                    chatField.innerHTML += '<div class="row"><div class="col-9 alert w-75 ' + color + '" role="alert"><hp>'+ data.message +'</p><hr><p class="mb-0 text-end"><b>' + data.username + '</b>  @  ' + new Date(data.timestamp).toLocaleTimeString([], options) + '</p></div><div class="col-3"></div></div>';
                }
                window.scrollTo(0, document.body.scrollHeight);

                break;
            default:
                console.error("Unknown message type!");
                break;
        }
    };

    chatSocket.onerror = function(err) {
        console.log("Chat-WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}

connect();
