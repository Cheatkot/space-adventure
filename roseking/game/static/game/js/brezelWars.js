let activeCardId = null;

function size(){
    let divs = $('.play-field');
    let gameFigures = $('.game-figure');
    let cardImages = $('.card-img-top');
    let divsWidth = divs[0].offsetWidth;

    // $('#card-stacks').css('height', divsWidth * 9 + 'px');
    $('#draw-pile').css('height', divsWidth * 4.5 + 'px');
    $('#discard-pile').css('height', divsWidth * 4.5 + 'px');
    $('#draw-pile-img').css('height', divsWidth * 4.5 + 'px');

    for (let i = 0; i < divs.length; i++) {
        divs[i].style.height = divsWidth + 'px';
        if (i % 2 === 0) {
            divs[i].style.backgroundColor = '#6ea8fe';
        } else {
            divs[i].style.backgroundColor = '#cfe2ff';
        }
    }

    for (let i = 0; i < gameFigures.length; i++) {
        gameFigures[i].style.height = (divsWidth - 2) + 'px';
        gameFigures[i].style.width = (divsWidth - 2) + 'px';
    }

    for (let i = 0; i < cardImages.length; i++) {
        console.log(cardImages[i].width);
        cardImages[i].height = cardImages[i].width.toString();
    }
}

function setPlayerPoints(user, playerNumber, points) {
    if (userName === user) {
        if (playerNumber === 1) {
            $('#your-points').text(points[playerNumber - 1]);
            $('#enemy-points').text(points[playerNumber]);
        } else {
            $('#your-points').text(points[playerNumber - 2]);
            $('#enemy-points').text(points[playerNumber - 1]);
        }
    } else {
        if (playerNumber === 1) {
            $('#your-points').text(points[playerNumber]);
            $('#enemy-points').text(data.points[playerNumber - 1]);
        } else {
            $('#your-points').text(points[playerNumber - 1]);
            $('#enemy-points').text(points[playerNumber - 2]);
        }
    }
}

function activateLastPlayed() {
    let lastPlayed = $('.last-played')

    lastPlayed.removeClass("d-none");
    lastPlayed.removeClass("last-played");
}

$(document).ready((e) => {
    const gameId =  JSON.parse(document.getElementById('game-id').textContent);
    const userName =  JSON.parse(document.getElementById('user-name').textContent);

    const playArea = $('#play-area');

    let divs = $('.play-field');
    divs.css('padding', '0');
    divs.css('display', 'inline-block');

    document.body.setAttribute('style', 'background-color: #479f76 !important;');

    $("#f4-4").html('<img src="/static/game/images/Bier.png" class="game-figure">');
    $("#f5-6").html('<img src="/static/game/images/Brezel1.png" class="game-figure">');
    $("#f2-3").html('<img src="/static/game/images/Brezel2.png" class="game-figure">');

    size();
    $(window).resize((e) => {
        size();
    });

    playArea.click((e) => {
        let id = null;

        if (e.target.id === '') {
            if (e.target.parentElement.id === '') {
                id = e.target.parentElement.parentElement.id;
            } else {
                id = e.target.parentElement.id;
            }
        } else {
            id = e.target.id;
        }

        console.log(id);

        let pattern = /p1-\d/;
        console.log(pattern.test(id));

        let activeCard = null;

        if (pattern.test(id)) {
            console.log(1);

            if (activeCardId === null) {
                console.log(2);
                activeCardId = id;
                activeCard = $('#' + activeCardId);
                activeCard.css('background-color', '#dc3545');
                // mark field in playfield if ok; send message to websocket
            } else if (activeCardId === id) {
                console.log(3);
                // send message to websocket
                activeCard = $('#' + activeCardId);
                activeCard.css('background-color', '#e9ecef');
                activeCardId = null;
            } else {
                console.log(4);
                activeCard = $('#' + activeCardId);
                activeCard.css('background-color', '#e9ecef');
                activeCardId = id;
                activeCard = activeCard = $('#' + activeCardId);
                activeCard.css('background-color', '#dc3545');
            }
        }
    });


    let chatSocket = null;

    function connect() {
        chatSocket = new WebSocket("ws://" + window.location.host + "/ws/game/" + gameId + "/");

        chatSocket.onopen = function(e) {
            console.log("Successfully connected to the Game-WebSocket.");
        }

        chatSocket.onclose = function(e) {
            console.log("Game-WebSocket connection closed unexpectedly. Trying to reconnect in 3s...");

            // setTimeout(function() { # TODO: 2-Spieler-Sperre improven
            //     console.log("Reconnecting...");
            //     connect();
            // }, 3000);
        };

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log(data);

            let targetField = null;

            switch (data.type) {
                case "draw_card":
                    console.log("draw card.");

                    // nothing until now

                    break;
                case "play_card":
                    console.log("play card.");

                    targetField = $('#f' + data.target_position[0] + '-' + data.target_position[0]);

                    targetField.html('<img src="/static/game/images/Brezel' + data.player_number + '.png" class="last-played d-none game-figure player_' + data.player_number + '">');
                    targetField.html('<img src="/static/game/images/Bier.png" class="game-figure">');
                    activateLastPlayed();
                    setPlayerPoints(userName, data.player_number, data.points);

                    break;
                case "play_joker_card":
                    console.log("play joker card.");

                    targetField = $('#f' + data.target_position[0] + '-' + data.target_position[0]);

                    activateLastPlayed();
                    setPlayerPoints(userName, data.player_number, data.points);

                    break;
                case "game_error":
                    console.log(data.message);
                    break;
                default:
                    console.error("Unknown message type!");
                    break;
            }
        };

        chatSocket.onerror = function(err) {
            console.log("Game-WebSocket encountered an error: " + err.message);
            console.log("Closing the socket.");
            chatSocket.close();
        }
    }

    connect();
});
