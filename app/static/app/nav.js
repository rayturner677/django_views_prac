function main() {
    $("#nav-view-submit").click(() => {
        location = "/link/" + encodeURI($("#nav-view-short-code-input").val());
    });
}

$(main);
