const textarea = document.getElementById("line");
const form = document.getElementById("editor-form");

textarea.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        form.submit();
    }
});

textarea.addEventListener("keydown", function (e) {
    if (e.key === "Backspace" && textarea.value.length === 0) {
        e.preventDefault();
        document.getElementById("backspace-form").submit();
    }
});


textarea.addEventListener("input", () => {
  textarea.style.height = "auto";
  textarea.style.height = textarea.scrollHeight + "px";
});


