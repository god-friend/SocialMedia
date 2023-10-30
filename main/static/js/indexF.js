function remainingChars(id, eleId){
    console.log(id, eleId);
    var element = document.getElementById(eleId);
    id = "#" + id;
    eleId = "#" + eleId;
    $(id).on("input", (event)=>{
        var max_length = $(id).attr("maxlength");
        var curr_length = $(id).val().length;
        console.log(max_length, " " , curr_length);
        element.innerText = "";
        element.innerText = curr_length + "/" + max_length;
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


