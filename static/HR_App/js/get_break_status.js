break_set = (onbreak) => {
    break_button = document.getElementById("break_button")
    if ((onbreak && break_button.innerHTML === "Start Break") || (!onbreak && break_button.innerHTML === "End Break")) {
        location.reload();
    }
}

break_check = ({url, userid}) => {
    $.ajax(
        {
            url: url,
            type: "GET",
            data: {
                user_id : userid,
            },
            success: function (data) {
                console.log(data);
                try {
                    break_set(data['is_on_break']);
                }
                catch (err) {
                    console.log("err");
                }

            },
            error: function (xhr, status, error) {
                console.log("Error: " + error);
            },
            complete: function () {
                console.log("Request completed");
            }
        }
    ) // Make an AJAX request
}