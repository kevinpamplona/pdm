// Simulate a POST request by creating a hidden HTML form and submitting it
function logout() {
    // Create the form
    var logout_form = document.createElement("form");
    logout_form.setAttribute("method", "post");
    logout_form.setAttribute("action", "/login/");

    // Create a field that simulates the logout button
    var field = document.createElement("input")
    field.setAttribute("type", "hidden");
    field.setAttribute("name", "logout");
    field.setAttribute("value","logout");
    logout_form.appendChild(field);

    // Submit the form
    logout_form.submit();
}