// variables
 $(document).ready(function(){
    // Insert body text, reconstruct <p> structure
    var body=document.getElementById("text")
    var bodySents=body.innerText.split("<sent>").filter(function(entry){ return entry.trim() !='';});
    var bodySentsClean=[];
    for (var i=0;i<bodySents.length;i++){
        var newsent=bodySents[i].split("</sent>").filter(function(entry){ return entry.trim() !='';});
        bodySentsClean.push(newsent[0]);
    }
    body.removeChild(body.childNodes[0]);
    for (var i=0;i<bodySentsClean.length;i++){
        if(bodySentsClean[i]=="<br>"){
            asent=document.createElement("br");
            body.appendChild(asent)
            asent=document.createElement("br");
            body.appendChild(asent)
        }
        else{
            if(bodySentsClean[i].startsWith(" ")){
                var asent=document.createElement("SENT");
                asent.classList.add('normal');
                asent.appendChild(document.createTextNode(bodySentsClean[i].substring(1,)));
                body.appendChild(asent);
                var space=document.createTextNode(" ");
                body.insertBefore(space, asent);
            }
            else{
            var asent=document.createElement("SENT");
            asent.classList.add('normal');
            asent.appendChild(document.createTextNode(bodySentsClean[i]));
            body.appendChild(asent);
        }}
    }
    // Give id to each sentence 
    sents=document.getElementById("text").getElementsByTagName("sent");
    for (var i=0;i<sents.length;i++){
        thissent=sents[i];
        thissent.setAttribute("id","sent"+i.toString());
        $("#sent"+i.toString()).on({
            mouseenter: function(){
            if(thissent.classList.contains('selectable')){
                this.style.backgroundColor="#FCF3CF";
            }},
            mouseleave: function(){
                if(thissent.classList.contains('selectable')){
                    this.style.backgroundColor="transparent";
                 }
            }
        });
    }
    body.style.display="inline";
    // jQuery AJAX set up
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#addQbutton').tooltip({
        placement: 'right',
        title: 'Click if you have a question or want further information.',
        animation: true,
        delay: {show:200, hide:10}
    })
    $('#addQbutton').popover({
        html:true,
        content:'<div class="popoverrow">What is your question? Or what do you want to know?</div><div class="popoverrow"><div id="newQ"><input type="text" id="newQinput" placeholder="Type in your question"style="width:75%;height:30px"><button class="btn" id="newQbutton" onclick="addnewQ()">Add</button></div></div>',
        placement:'right',
    }).on('shown.bs.popover', function(){
        $('#newQinput').focus();        
        document.getElementById("addbuttons").classList.add('fixedbutton') 
        $('#addQbutton').tooltip('hide');
        $('#addQbutton').tooltip('disable');
    }).on('hidden.bs.popover',function(){
        document.getElementById("addbuttons").classList.remove('fixedbutton') 
        $('#addQbutton').tooltip('toggleEnabled');
    })
    reconSidebar();
    // adjust position with prompted questions 
    promY=$("#sent5").offset().top;
    promX=$("#Questions").offset().left;
    console.log(promY)
    $("#sent5prompt").offset({top:promY});

}); // End of document ready clause 


// Move addbuttons along with mouse
$(document).bind('mousemove', function(e){
    mousey=e.pageY
    texttop=document.getElementById('text').offsetTop;
    textheight=document.getElementById('text').offsetHeight;
    addbuttons=document.getElementById("addbuttons");
    if(addbuttons.classList.contains('fixedbutton')){}
    else{
    buttontop=0;
    topmargin=document.getElementById("top-margin").offsetHeight;
    realtexttop=topmargin+texttop;
    if(mousey<realtexttop){
        buttontop=0;
    }else{
        if(mousey>realtexttop+textheight){
            buttontop=textheight;
        }else{
            buttontop=Math.floor((mousey-realtexttop)/100)*100
            }
        }
    addbuttons.style.top=buttontop.toString()+"px";
}})

function reconSidebar(){
 //Floating sidebar
    console.log("Hello")
    var topPosition = $("#floating-div").offset().top - 10;
    var parentwidth = $('#sidebar-container').width();
    var floatingDiv = $('#floating-div')[0];
    window.onresize = function(){
    parentwidth=$('#sidebar-container').width();
    floatingDiv.style.width=parentwidth.toString()+"px"    
    }
    floatingDiv.style.width=parentwidth.toString()+"px"    
    var floatingDivHeight = $('#floating-div').outerHeight();
    var footerFromTop = $('#footer').offset().top;
    var absPosition = footerFromTop - floatingDivHeight - 20;
    var win = $(window);
    win.scroll(function() {
        if ((win.scrollTop() > topPosition) && (win.scrollTop() < absPosition)) {
        floatingDiv.style.position="fixed";
        floatingDiv.style.width=parentwidth.toString()+"px";
        } else if ((win.scrollTop() > topPosition) && (win.scrollTop() > absPosition)) {
        floatingDiv.style.position="absolute";
        floatingDiv.style.width=parentwidth.toString()+"px";
        } else {
        floatingDiv.style.position=""
        floatingDiv.style.width=parentwidth.toString()+"px";
        }
    // Prompt suggested questions based on scroll 
    var y = win.scrollTop();
    win.height();
    var tsenttop=$("#sent5").offset().top
    var wh=win.height();
    var prompt=document.getElementById("sent5prompt");
    if((y>Math.max(0, tsenttop-3*wh/4))&&(y<tsenttop-wh/3)){
        if($("#sent5prompt").css("display")=="none"){
            $("#sent5prompt").fadeIn(500);
        }
    }else{
        if($("#sent5prompt").css("display")=="block"){
            $("#sent5prompt").fadeOut(500);
        }
    }
    });
/*    var questholder=document.getElementById("selected_questions");
   var qrows=document.getElementsByClassName("qrow");
   for (var i=0; i<qrows.length;i++){
       thisqrow=qrows[i];
       thisqrow.style.width=(questholder.offsetWidth-36).toString()+"px";
   }
 */} // end of sidebar reconstruction 
    window.addEventListener('scroll', function(e){})



function addnewQ(possiblequestion){
    possiblequestion=document.getElementById("newQinput").value;
    if(possiblequestion.length>2){
        var questholder=document.getElementById("raised_questions");
        curlen=questholder.childNodes.length-1;
        newQholder=document.createElement("div");
        newQholder.className="card";
        newQholder.style.width="100%";
        newQ=document.createElement("div");
        newQ.className="row qrow";
        newQdelete=document.createElement("div");
        newQdelete.setAttribute("class","col-1 deleteholder")
        newQdeletebutton=document.createElement("button");
        newQdeletebutton.setAttribute("class","btn deletebutton");
        newQdeletebutton.innerHTML='<i class="fa fa-times-circle"></i>';

        newQdeletebutton.addEventListener("click", function(){
            var questholder=document.getElementById("raised_questions");
            questholder.removeChild(this.parentElement.parentElement.parentElement);
            document.getElementById("qnumtotal").innerHTML=questholder.childNodes.length;   
            showbutton=document.getElementById("showless");
            
            if((questholder.childNodes.length<6)&&(questholder.childNodes.length>1)){
                $("#submitQuizbutton")[0].disabled=true;
                $("#submitQuizbutton")[0].style.backgroundColor="white";
                $("#submitQuizbutton")[0].style.color="black";            
                }
        });
        newQdelete.appendChild(newQdeletebutton);
        newQtext=document.createElement("div");
        newQtext.setAttribute("class","qlist col-10");
        newQtext.innerHTML=possiblequestion;
    
        newQ.appendChild(newQtext);
        newQ.appendChild(newQdelete);
        newQholder.appendChild(newQ);
        questholder.appendChild(newQholder);

        document.getElementById("qnumtotal").innerHTML=questholder.childNodes.length;
        $('#addQbutton').popover('hide');
    }
    else{
        document.getElementById("newQinput").value='';
    };
};

function takeQ(elem){
    possiblequestion=$(elem).parent().prev()[0].innerHTML;
    var questholder=document.getElementById("raised_questions");
    curlen=questholder.childNodes.length-1;
    newQholder=document.createElement("div");
    newQholder.className="card";
    newQholder.style.width="100%";
    newQ=document.createElement("div");
    newQ.className="row qrow";
    newQdelete=document.createElement("div");
    newQdelete.setAttribute("class","col-1 deleteholder")
    newQdeletebutton=document.createElement("button");
    newQdeletebutton.setAttribute("class","btn deletebutton");
    newQdeletebutton.innerHTML='<i class="fa fa-times-circle"></i>';

    newQdeletebutton.addEventListener("click", function(){
        var questholder=document.getElementById("raised_questions");
        questholder.removeChild(this.parentElement.parentElement.parentElement);
        document.getElementById("qnumtotal").innerHTML=questholder.childNodes.length;   
        showbutton=document.getElementById("showless");
        
        if((questholder.childNodes.length<6)&&(questholder.childNodes.length>1)){
            $("#submitQuizbutton")[0].disabled=true;
            $("#submitQuizbutton")[0].style.backgroundColor="white";
            $("#submitQuizbutton")[0].style.color="black";            
            }
    });
    newQdelete.appendChild(newQdeletebutton);
    newQtext=document.createElement("div");
    newQtext.setAttribute("class","qlist col-10");
    newQtext.innerHTML=possiblequestion;

    newQ.appendChild(newQtext);
    newQ.appendChild(newQdelete);
    newQholder.appendChild(newQ);
    questholder.appendChild(newQholder);

    document.getElementById("qnumtotal").innerHTML=questholder.childNodes.length;
    $(elem).parent().parent().parent().parent().remove();
}

function discard(elem){
    $(elem).parent().parent().parent().parent().remove();    
}