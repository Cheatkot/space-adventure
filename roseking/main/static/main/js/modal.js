function showModal(title, message) {
    $('#mainModalLabel').text(title);
    $('#mainModalBody').text(message);
    $('#mainModalFooterButton').addClass('d-none');
    $('#mainModalButton').click();
}

function showModalWithButton(title, message, buttonText) {
    $('#mainModalLabel').text(title);
    $('#mainModalBody').text(message);
    $('#mainModalFooterButton').text(buttonText);
    $('#mainModalFooterButton').removeClass('d-none');
    $('#mainModalButton').click();
}