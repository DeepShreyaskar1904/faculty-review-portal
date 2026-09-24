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