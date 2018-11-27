function main() {
    $('#nav-view-submit').click(() => {
        location = '/view/' + encodeURI($('#nav-view-short-code-input').val());
    });
}

$(main);
