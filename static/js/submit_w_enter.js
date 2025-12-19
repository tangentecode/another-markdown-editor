const textarea = document.getElementById("line");
const form = document.getElementById("editor-form");

textarea.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        form.submit();
    }
});
