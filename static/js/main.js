document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("reviewForm");
    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            Swal.fire({
                title: "Submit Feedback?",
                text: "Please make sure your feedback is honest before submitting.",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "Yes, Submit",
                cancelButtonText: "Review Again",
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        });
    }
});
// =========================
// ADMIN PASSWORD TOGGLE
// =========================

const togglePassword = document.getElementById("togglePassword");

const passwordInput = document.getElementById("password");


if (togglePassword && passwordInput) {

    togglePassword.addEventListener("click", function () {

        const isPassword =
            passwordInput.getAttribute("type") === "password";


        passwordInput.setAttribute(
            "type",
            isPassword ? "text" : "password"
        );


        const icon =
            this.querySelector("i");


        if (isPassword) {

            icon.classList.remove("fa-eye");

            icon.classList.add("fa-eye-slash");

        } else {

            icon.classList.remove("fa-eye-slash");

            icon.classList.add("fa-eye");

        }

    });

}