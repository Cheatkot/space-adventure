let activeCardId = null;
let markedField = null;
let joker_active = false;

function size(){
    let divs = $('.play-field');
    let gameFigures = $('.game-figure');
    let cardImages = $('.card-img-top');
    let playArea = $('#play-area');
    let divsWidth = 0;
    // let divsWidth = divs[0].offsetWidth;
    let divsContentWidth = 0;
    // let divsWidth = playArea.offsetWidth / 9;

    for (let i = 0; i < divs.length; i++) {
        if (divs[i].innerHTML === "") {
            divsWidth = divs[i].offsetWidth;
            divsContentWidth = divs[i].clientWidth;
        }
    }

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
        gameFigures[i].style.height = divsContentWidth + 'px';
        gameFigures[i].style.width = divsContentWidth + 'px';
    }

    for (let i = 0; i < cardImages.length; i++) {
        console.log(cardImages[i].width);
        cardImages[i].height = cardImages[i].width.toString();
    }
}

function setPlayerPoints(userName, user, playerNumber, points) {
    if (userName === user) {
        if (playerNumber === 1) {
            $('#your-points').text("Punkte: " + points[playerNumber - 1]);
            $('#enemy-points').text("Punkte: " + points[playerNumber]);
        } else {
            $('#your-points').text("Punkte: " + points[playerNumber - 1]);
            $('#enemy-points').text("Punkte: " + points[playerNumber - 2]);
        }
    } else {
        if (playerNumber === 1) {
            $('#your-points').text("Punkte: " + points[playerNumber]);
            $('#enemy-points').text("Punkte: " + points[playerNumber - 1]);
        } else {
            $('#your-points').text("Punkte: " + points[playerNumber - 2]);
            $('#enemy-points').text("Punkte: " + points[playerNumber - 1]);
        }
    }
}

function setPlayerJoker(userName, user, playerNumber, playerOneJoker, playerTwoJoker) {
    if (userName === user) {
        if (playerNumber === 1) {
            $('#your-joker').text("Joker: " + playerOneJoker);
            $('#enemy-joker').text("Joker: " + playerTwoJoker);
        } else {
            $('#your-joker').text("Joker: " + playerTwoJoker);
            $('#enemy-joker').text("Joker: " + playerOneJoker);
        }
    } else {
        if (playerNumber === 1) {
            $('#your-joker').text("Joker: " + playerTwoJoker);
            $('#enemy-joker').text("Joker: " + playerOneJoker);
        } else {
            $('#your-joker').text("Joker: " + playerOneJoker);
            $('#enemy-joker').text("Joker: " + playerTwoJoker);
        }
    }
}

function getCompassImageSrc(pointOfTheCompass) {
    switch (pointOfTheCompass) {
        case 'N':
            return  '/static/game/images/compassNorth.png';
        case 'NE':
            return  '/static/game/images/compassNorthEast.png';
        case 'E':
            return '/static/game/images/compassEast.png';
        case 'SE':
            return '/static/game/images/compassSouthEast.png';
        case 'S':
            return '/static/game/images/compassSouth.png';
        case 'SW':
            return '/static/game/images/compassSouthWest.png';
        case 'W':
            return '/static/game/images/compassWest.png';
        case 'NW':
            return '/static/game/images/compassNorthWest.png';
    }
}

function activateLastPlayed() {
    let lastPlayed = $('.last-played')

    lastPlayed.removeClass("d-none");
    lastPlayed.removeClass("last-played");
}

function setActivePlayer(userName, user) {
    if (userName === user) {
        $('#your-username').css('background-color', '#a370f7');
        $('#enemy-username').css('background-color', '');
    } else {
        $('#enemy-username').css('background-color', '#a370f7');
        $('#your-username').css('background-color', '');
    }
}

function setBrezelStones(stones) {
    $('#brezelStones').text('Brezeln: ' + stones);
}

function playCard(userName, data) {
    targetField = $('#f' + data.target_position[0] + '-' + data.target_position[1]);

    $('#beer-mug').remove();

    activateLastPlayed();
    putCardOnDiscardPile(userName, data.username, data.card_id, data.played_card);
    targetField.html('<img src="/static/game/images/Brezel' + data.player_number + '.png" class="last-played d-none game-figure player_' + data.player_number + '"><img id="beer-mug" src="/static/game/images/Bier.png" class="game-figure">');
    size();

    setPlayerPoints(userName, data.username, data.player_number, data.points);

    setBrezelStones(data.brezel_stones);
    setActivePlayer(userName, data.active_player);
}

function putCardOnDiscardPile(userName, user, cardId, playedCard) {
    if (userName === user) {
        $("#p1-" + cardId).addClass('invisible');
    } else {
        $("#p2-" + cardId).addClass('invisible');
    }

    $('#discard-pile-img').attr('src', getCompassImageSrc(playedCard[0]));
    $('#discard-pile-txt').text(playedCard[1]);

    if ($('#discard-pile').hasClass('invisible')) {
        $('#discard-pile').removeClass('invisible');
    }
}

$(document).ready((e) => {
    const gameId =  JSON.parse(document.getElementById('game-id').textContent);
    const userName =  JSON.parse(document.getElementById('user-name').textContent);

    const playArea = $('#play-area');

    let divs = $('.play-field');
    divs.css('padding', '0');
    divs.css('display', 'inline-block');

    document.body.setAttribute('style', 'background-color: #479f76 !important;');

    // $("#f4-4").html('<img src="/static/game/images/Bier.png" class="game-figure">');
    // $("#f5-6").html('<img src="/static/game/images/Brezel1.png" class="game-figure">');
    // $("#f2-3").html('<img src="/static/game/images/Brezel2.png" class="game-figure">');

    $('#mainModalFooterButton').click((e) => {
        console.log(e.currentTarget.textContent);
        if (e.currentTarget.textContent === 'Zurück zur Hauptseite!') {
            location.href = '/';
        } else if (e.currentTarget.textContent === 'Setze Joker ein!') {
            // gameSocket
        }
    });

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

        id = id.replace('-img', '').replace('-txt', '');

        console.log("nowID: ", id);

        let pattern = /p1-\d/;
        let pattern2 = /draw-pile/;
        console.log(pattern.test(id));
        console.log("draw:", pattern2.test(id));

        let activeCard = null;

        size();

        if (pattern.test(id) || pattern2.test(id)) {
            console.log(1);

            if (activeCardId === null) {
                console.log(2);
                activeCardId = id;
                activeCard = $('#' + activeCardId);
                activeCard.css('background-color', '#a370f7');

                gameSocket.send(JSON.stringify({
                        'type': 'check_move',
                        'message': {
                            'card_id': activeCardId.split('-')[1],
                        },
                    }));
            } else if (activeCardId === id) {
                console.log(3);
                // send message to websocket
                activeCard = $('#' + activeCardId);
                activeCard.css('background-color', '#e9ecef');

                if (pattern2.test(id)) {
                    gameSocket.send(JSON.stringify({
                        'type': 'draw_card',
                        'message': '',
                    }));
                } else if (!activeCard.hasClass('invisible') && joker_active) {
                    gameSocket.send(JSON.stringify({
                        'type': 'play_joker_card',
                        'message': {
                            'card_id': activeCardId.split('-')[1],
                        },
                    }));
                } else if (!activeCard.hasClass('invisible')) {
                    gameSocket.send(JSON.stringify({
                        'type': 'play_card',
                        'message': {
                            'card_id': activeCardId.split('-')[1],
                        },
                    }));
                }

                activeCardId = null;
            } else {
                console.log(4);
                activeCard = $('#' + activeCardId);
                activeCard.css('background-color', '#e9ecef');
                activeCardId = id;
                activeCard = activeCard = $('#' + activeCardId);
                activeCard.css('background-color', '#a370f7');

                gameSocket.send(JSON.stringify({
                        'type': 'check_move',
                        'message': {
                            'card_id': activeCardId.split('-')[1],
                        },
                    }));
            }
        }
    });


    let gameSocket = null;

    function connect() {
        gameSocket = new WebSocket("ws://" + window.location.host + "/ws/game/" + gameId + "/");

        gameSocket.onopen = function(e) {
            console.log("Successfully connected to the Game-WebSocket.");
        }

        gameSocket.onclose = function(e) {
            console.log("Game-WebSocket connection closed unexpectedly. Trying to reconnect in 3s...");

            setTimeout(function() {
                console.log("Reconnecting...");
                connect();
            }, 3000);
        };

        gameSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log(data);

            let targetField = null;

            switch (data.type) {
                case "start_game":
                    console.log("start_game");

                    let playerNumber = null;

                    if (data.player_one === userName) {
                        $('#enemy-username').text(data.player_two);
                    } else {
                        $('#enemy-username').text(data.player_one);
                    }

                    setPlayerPoints(userName, data.username, data.player_number, data.points);

                    if (data.username === userName) {
                        playerNumber = data.player_number;
                    } else {
                        if (data.player_number === 1) {
                            playerNumber = 2;
                        } else {
                            playerNumber = 1;
                        }
                    }

                    $('#f' + data.target_position[0] + "-" + data.target_position[1]).html('<img id="beer-mug" src="/static/game/images/Bier.png" class="game-figure">');
                    size();

                    if (userName !== data.username) {
                        for (let i = 0; i < 5; i++) {
                            $('#p1-' + (i + 1) + '-img').attr('src', getCompassImageSrc(data.cards[0][i + 1][0]));
                            $('#p1-' + (i + 1) + '-img').attr('alt', data.cards[0][i + 1][0]);
                            $('#p1-' + (i + 1) + '-txt').text(data.cards[0][i + 1][1]);
                            $('#p1-' + (i + 1)).removeClass('invisible');

                            $('#p2-' + (i + 1) + '-img').attr('src', getCompassImageSrc(data.cards[1][i + 1][0]));
                            $('#p2-' + (i + 1) + '-img').attr('alt', data.cards[1][i + 1][0]);
                            $('#p2-' + (i + 1) + '-txt').text(data.cards[1][i + 1][1]);
                            $('#p2-' + (i + 1)).removeClass('invisible');
                        }
                    } else {
                        for (let i = 0; i < 5; i++) {
                            $('#p2-' + (i + 1) + '-img').attr('src', getCompassImageSrc(data.cards[0][i + 1][0]));
                            $('#p2-' + (i + 1) + '-img').attr('alt', data.cards[0][i + 1][0]);
                            $('#p2-' + (i + 1) + '-txt').text(data.cards[0][i + 1][1]);
                            $('#p2-' + (i + 1)).removeClass('invisible');

                            $('#p1-' + (i + 1) + '-img').attr('src', getCompassImageSrc(data.cards[1][i + 1][0]));
                            $('#p1-' + (i + 1) + '-img').attr('alt', data.cards[1][i + 1][0]);
                            $('#p1-' + (i + 1) + '-txt').text(data.cards[1][i + 1][1]);
                            $('#p1-' + (i + 1)).removeClass('invisible');
                        }
                    }

                    setActivePlayer(userName, data.active_player);

                    break;
                case "draw_card":
                    console.log("draw card.");

                    console.log(data.drawn_card);

                    if (userName === data.username) {
                        $('#p1-' + data.drawn_card[0] + '-img').attr('src', getCompassImageSrc(data.drawn_card[1][0]));
                        $('#p1-' + data.drawn_card[0] + '-img').attr('alt', data.drawn_card[1][0]);
                        $('#p1-' + data.drawn_card[0] + '-txt').text(data.drawn_card[1][1]);
                        $('#p1-' + data.drawn_card[0]).removeClass('invisible');
                    } else {
                        $('#p2-' + data.drawn_card[0] + '-img').attr('src', getCompassImageSrc(data.drawn_card[1][0]));
                        $('#p2-' + data.drawn_card[0] + '-img').attr('alt', data.drawn_card[1][0]);
                        $('#p2-' + data.drawn_card[0] + '-txt').text(data.drawn_card[1][1]);
                        $('#p2-' + data.drawn_card[0]).removeClass('invisible');
                    }

                    size();
                    setActivePlayer(userName, data.active_player);

                    break;
                case "play_card":
                    console.log("play card.");

                    playCard(userName, data);

                    break;
                case "play_joker_card":
                    console.log("play joker card.");

                    playCard(userName, data);
                    setPlayerJoker(userName, data.username, data.player_number, data.joker_player_one, data.joker_player_two);

                    break;
                case "check_move":
                    console.log("check move.");

                    joker_active = false;

                    if (userName === data.username) {
                        markedField = '#f' + data.target_position[0] + '-' + data.target_position[1];
                        targetField = $(markedField);

                        if (data.possible) {
                            if (data.joker_use) {
                                targetField.css('background-color', '#ffc107');
                                joker_active = true;
                            } else {
                                targetField.css('background-color', '#20c997');
                            }
                        } else {
                            targetField.css('background-color', '#dc3545');
                        }
                    }

                    break;
                case "game_error":
                    if (data.username === userName) {
                        console.log(data.message);
                        showModal('Fehler', data.message);
                    }

                    break;
                case "game_over":
                    let title;
                    let message;

                    if (userName === data.username) {
                        title = 'Gewonnen!';

                        if (userName === data.player_one) {
                            message = 'Herzlichen Glückwunsch! Sie haben gegen "' + data.player_two + '" mit ' + data.points[0] + ' zu ' + data.points[1] + ' Punkten gewonnen! :)';
                        } else {
                            message = 'Herzlichen Glückwunsch! Sie haben gegen "' + data.player_one + '" mit ' + data.points[1] + ' zu ' + data.points[0] + ' Punkten gewonnen! :)';
                        }
                    } else {
                        title = 'Verloren!';

                        if (userName === data.player_one) {
                            message = 'Schade! Sie haben gegen "' + data.player_two + '" mit ' + data.points[0] + ' zu ' + data.points[1] + ' Punkten verloren! :(';
                        } else {
                            message = 'Schade! Sie haben gegen "' + data.player_one + '" mit ' + data.points[1] + ' zu ' + data.points[0] + ' Punkten verloren! :(';
                        }
                    }

                    showModalWithButton(title, message, 'Zurück zur Hauptseite!');

                    break;
                default:
                    console.error("Unknown message type!");
                    break;
            }
        };

        gameSocket.onerror = function(err) {
            console.log("Game-WebSocket encountered an error: " + err.message);
            console.log("Closing the socket.");
            gameSocket.close();
        }
    }

    connect();
});
