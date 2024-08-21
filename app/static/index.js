function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

window.setTimeout(function () {
  $(".alert").fadeTo(500, 0);
}, 4000);

var input = document.getElementById("note");

input.addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    document.getElementById("note_button").click();
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const colorPicker = document.getElementById("choose_pr_color");

  colorPicker.oninput = function () {
    root.style.setProperty("--primary-color", colorPicker.value);
  };
});
