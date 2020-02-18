window.onload = () => {
    modal = document.querySelector(".modal");
    set_page("Home");
    set_page("Forecast");
    set_dates();
    delete_expense();    
    change_modal();
};




function set_page(page) {
    if (document.title == page) {
        url = document.querySelector("#row-date-range").dataset.url;
        data = new FormData();
        data.append("page", page)
        data.append("start", document.querySelector(".start").value)
        data.append("end", document.querySelector(".end").value)
        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: data
        }).then(function (result) {
            return result.json();
        }).then(function (detail) {
            
            if(detail["error"])
                alert(detail["error"])
            else{
                if (detail["r_sq"]) {
                   
                    document.querySelector("p").innerHTML = "Coefficient of Determination: " + detail["r_sq"]
                }
                i = 0
                charts = ["chart1", "chart2", "chart3", "chart4"]
                detail["charts"].forEach(chart_data => {
                    set_chart(chart_data, charts[i])
                    i+=1 
                });
            }
        });
    }
}


function set_chart(chart_data, id) {
    var chart = document.getElementById(id);
    if (chart) {
        var ctx = document.getElementById(id).getContext('2d');
        var chart = new Chart(ctx, chart_data);
    }    
}


function set_dates(){
    if (document.title == "Home" || document.title == "Forecast") {
        document.querySelector("#date-button").onclick = () =>{
            page = document.title
            set_page(page);
        }    
    }
}


function delete_expense(){
    if (document.title == "Expenses") {
        document.querySelectorAll(".delete-expense").forEach(button => {
            button.onclick = e => {
                modal.style.display = "block";
                document.querySelector("#delete").onclick = () => {
                    modal.style.display = "none";
                    url = button.dataset.url
                    fetch(url, {
                        method: "GET",
                    }).then(function () {
                        e.target.parentElement.parentElement.remove();
                    });
                }
            }
        });
    }
}



function change_modal() {
    modal.querySelector(".close").onclick = () => {
        modal.style.display = "none";
    }

    window.onclick = e => {
        if (e.target == modal) {
            modal.style.display = "none";
        }
    }

    document.querySelector("#cancel").onclick = () => {
        modal.style.display = "none";
    }
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
