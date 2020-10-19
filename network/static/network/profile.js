function follow_unfollow(){
  var btn_name = event.target.innerHTML;

  fetch(`/${event.target.name}`, {
    method: 'PUT',
    body: JSON.stringify({
    follow: btn_name === "Follow"
    })
  });

  followersCount = document.querySelector("#followersCount");
  if (btn_name === "Follow") {
      event.target.innerHTML = "Unfollow";
      followersCount.innerHTML = parseInt(followersCount.innerHTML) + 1;
  }else if (btn_name === "Unfollow" ) {
    event.target.innerHTML = "Follow";
    followersCount.innerHTML = parseInt(followersCount.innerHTML) - 1;
  }
}
