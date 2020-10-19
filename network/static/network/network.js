function Edit(){
  if (event.target.innerHTML === "Edit") {
    postBody = document.querySelector(`#${event.target.value}`);
    editing_texarea = document.createElement('textarea');
    editing_texarea.id = event.target.value;
    editing_texarea.value = postBody.innerHTML;
    editing_texarea.className = "editing_texarea";

    editing_texarea.rows = postBody.offsetHeight / 20;



    postBody.parentNode.replaceChild(editing_texarea, postBody);
    editing_texarea.focus();
    event.target.innerHTML = "Save";

  }else if (event.target.innerHTML === "Save") {
    edited_body = document.querySelector(`#${event.target.value}`)
    paragraph = document.createElement('p');
    paragraph.id = event.target.value;
    paragraph.innerHTML = edited_body.value;

    edited_body.parentNode.replaceChild(paragraph, edited_body);

    fetch(`/Edit/${parseInt(event.target.value.substring(2))}`, {
      method: 'PUT',
      body: JSON.stringify({
      text: edited_body.value
      })
    });

    event.target.innerHTML = "Edit";
  }
}
function like(){

  fetch(`/Edit/${parseInt(event.target.value.substring(2))}`, {
    method: 'PUT',
    body: JSON.stringify({
    like: event.target.className.includes("-o")
    })
  });


  if (event.target.className.includes("-o")) {
    event.target.className = "fa fa-heart Obtn";
    inc = parseInt(event.target.innerHTML) + 1;
    event.target.innerHTML = inc;
  }else {
    event.target.className = "fa fa-heart-o Obtn";
    inc = parseInt(event.target.innerHTML) - 1;
    event.target.innerHTML = inc;
  }
}
