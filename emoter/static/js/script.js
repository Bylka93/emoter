(function() {
    
    var TIMEOUT = 150000;
    var loadingImg = '<img id="loadingImage" src="/static/img/ajax-loader.gif" />';

    var getSentimentText = function(score){
        var elem = "<span class='sentiment' style = 'color: grey'>" +
        "<h4 style = 'color: grey; font-size: .8em'>(listing the strongest tones detected) </h4>" +
        score[0][0] + " : " + score[0][1] +"%" + "<br>" + score[1][0] + " : " + score[1][1] +"%" + "<br>" + score[2][0] + " : " + score[2][1] + "%" + "<br>" +
        score[3][0] + " : " + score[3][1] +"%" + "<br>" + score[4][0] + " : " + score[4][1] +"%" + "<br>" + score[5][0] + " : " + score[5][1] + "%" + "<br>" +
        "</span>";
        return elem;
    };


    var getSentimentElement = function(score){
        // console.log(res.result)
        console.log(score)
        var elem = "<span class='sentiment' style = 'color: grey'>" +
        "<h4 style = 'color: grey; font-size: .8em'>(listing the strongest tones detected) </h4>" +
        score[0][0] + " : " + score[0][1] +"%" + "<br>" + score[1][0] + " : " + score[1][1] +"%" + "<br>" + score[2][0] + " : " + score[2][1] + "%" + "<br>" +
        score[3][0] + " : " + score[3][1] +"%" + "<br>" + score[4][0] + " : " + score[4][1] +"%" + "<br>" + score[5][0] + " : " + score[5][1] + "%" + "<br>" +
        "</span>";
        console.log(elem)
        return elem;
    };



    var errored = function(xml, status, message, $elem){
        if (status === "timeout"){
            $elem.html("Timed out. Try again.");
        } else {
            $elem.html("Something went wrong. Try again.");
        }
        return null;
    };

    var updateValue = function(url, text, $elem, success){
        $elem.append(loadingImg);
        $.ajax({
            url: url,
            type: "POST",
            timeout: TIMEOUT,
            data: {"text": text},
            dataType: "json",
            success: success,
            error: function(xml, status, message){
                errored(xml, status, message, $elem);
            }
        });
    };

    var updateNounPhrases = function(text){
        $nounList = $("#nounPhrasesValue");
        updateValue("api/noun_phrases", text, $nounList, function(res){
            $nounList.empty();
            var nounPhrases = res.result;
            if (!text) {
                $nounList.append("No text.");
            }
            else if (nounPhrases.length <= 0){
                $nounList.append("<em>None found.</em>");
            } else{
                nounPhrases.forEach(function(elem, index) {
                    $nounList.append("<li>" + elem + "</li>");
                });
            }
        });
    };

    var updateSentiment = function(text){
        $sentValue = $("#sentimentValue");
        $("#sentencesSentiment").hide();
        updateValue("api/sentiment", text, $sentValue, function(res) {
            $sentValue.empty();
            if (!text){
                $("#breakdown").hide();
                $sentValue.append("<em>No text.</em>");
            } else {
                $sentValue.append(getSentimentText(res.result));
                $("#breakdown").show();
            }
        });
    };

    // Event handlers
    var timeout;
    $("#text").on("paste input", function() {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            var text = $("textarea[name='text']")[0].value;
            updateSentiment(text);
            updateNounPhrases(text);
        }, 250);
    });

    var toggleSentences = function() {
        var $sentDiv = $("#sentencesSentiment");
        $sentBtn = $("#breakdownBtn");
        if ($sentDiv.is(":visible")){
            $sentDiv.hide();
            $sentBtn.removeClass("active");
        } else{
            var text = $("textarea[name='text']")[0].value;
            $sentDiv.show();
            var $sentTable = $("#sentencesSentiment table");
            var $tbody = $sentTable.children("tbody");
            updateValue("api/sentiment/sentences", text, $tbody, function(res){
                $sentBtn.addClass("active");
                $tbody.empty();
                var sentences = res.results;
                console.log(sentences)
                if (sentences.length <= 0){
                    $sentTable.append("No sentences.");
                } else {
                    for (var key in sentences) {
                    // sentences.forEach(function(elem, index){
                        $tbody.append("<tr>" +
                            "<td>" + key + "</td>" +
                            "<td>" + sentences[key][0][0] + " : " + sentences[key][0][1] + "%; " + 
                             sentences[key][1][0] + " : " + sentences[key][1][1] + "%; " +
                             sentences[key][2][0] + " : " + sentences[key][2][1] + "%; " +
                             sentences[key][3][0] + " : " + sentences[key][3][1] + "%; " +
                             sentences[key][4][0] + " : " + sentences[key][4][1] + "%; " +
                             sentences[key][5][0] + " : " + sentences[key][5][1] + "% " +
                            "</tr>");
                    // });
                }
            }
            });
        }
    };

    $("#breakdown").on('click', function(e){
        e.preventDefault();
        toggleSentences();
    });
}).call(this);
