$(document).ready(
    (e) => {
        $("#post-textarea").on("input", (event)=>{
            var max_length = $("#post-textarea").attr("maxlength");
            var curr_length = $("#post-textarea").val().length;

            document.getElementById("used-chars").innerText = "";
            document.getElementById("used-chars").innerText = curr_length + "/" + max_length;
        })
    }
)

function remainingChars(id){
    $("#comment-area-"+id).on("input", (event)=>{
        var max_length = $("#comment-area-"+id).attr("maxlength");
        var curr_length = $("#comment-area-"+id).val().length;
        document.getElementById("cChars-"+id).innerText = "";
        document.getElementById("cChars-"+id).innerText = curr_length + "/" + max_length;
    })
}


function selectFiles(){
    $("#select-files").click();

    $("#select-files").change(
        (event)=>{
            var length = event.target.files.length;
            var child = document.createElement("b");
            child.innerHTML = length;
            if(length > 4){
                alert("You are only Allowed to upload 4 images in one post");
                return;
            }
            if (length == 1){
                child.innerHTML += " image";
            }else{
                child.innerHTML += " images";
            }
            document.getElementById("selected-files").innerHTML = "";
            document.getElementById("selected-files").style.fontSize = "12px";
            document.getElementById("selected-files").appendChild(child);
        }
    )
}


