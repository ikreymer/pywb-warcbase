

function insert_list(contents)
{
    if (contents) {
        contents = contents.trimRight("\n");

        var colls = contents.split("\n");

        colls = colls.map(function(coll) {
            return "<li><a href=\"/" + coll + "/\">" + coll + "</a></li>";
        });

        contents = colls.join("\n");
    }

    document.body.innerHTML += "<p>Available Collections: <ul>" + contents + "</ul></p>";
}

function run()
{
     var ajax = new XMLHttpRequest();
     ajax.onreadystatechange = function() {
        if (ajax.readyState == XMLHttpRequest.DONE) {
            if (ajax.status == 200) {
                insert_list(ajax.responseText);
            }
        }
     }

     ajax.open("GET", "/cdx$?listColls=true", true);
     ajax.send();
}


run();
