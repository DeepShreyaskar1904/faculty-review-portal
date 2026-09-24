// ==================================================
// STUDENT REVIEW FORM CONFIRMATION
// ==================================================

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


    // ==================================================
    // ADMIN PASSWORD TOGGLE
    // ==================================================

    const togglePassword =
        document.getElementById("togglePassword");

    const passwordInput =
        document.getElementById("password");


    if (togglePassword && passwordInput) {

        togglePassword.addEventListener(
            "click",
            function () {

                const isPassword =
                    passwordInput.getAttribute("type")
                    === "password";


                passwordInput.setAttribute(
                    "type",
                    isPassword ? "text" : "password"
                );


                const icon =
                    this.querySelector("i");


                if (icon) {

                    if (isPassword) {

                        icon.classList.remove(
                            "fa-eye"
                        );

                        icon.classList.add(
                            "fa-eye-slash"
                        );

                    } else {

                        icon.classList.remove(
                            "fa-eye-slash"
                        );

                        icon.classList.add(
                            "fa-eye"
                        );

                    }

                }

            }
        );

    }


    // ==================================================
    // FULL REVIEW MODAL
    // ==================================================

    const reviewModalElement =
        document.getElementById("reviewModal");


    if (!reviewModalElement) {
        return;
    }


    const reviewModal =
        new bootstrap.Modal(reviewModalElement);


    // Find all View buttons

    document
        .querySelectorAll(".view-review-btn")
        .forEach(function (button) {


            button.addEventListener(
                "click",
                function () {


                    // ==========================================
                    // GET REVIEW ID
                    // ==========================================

                    const reviewId =
                        this.getAttribute(
                            "data-review-id"
                        );


                    console.log(
                        "Opening review:",
                        reviewId
                    );


                    // ==========================================
                    // RESET MODAL
                    // ==========================================

                    document.getElementById(
                        "reviewLoading"
                    ).style.display = "block";


                    document.getElementById(
                        "reviewContent"
                    ).style.display = "none";


                    document.getElementById(
                        "reviewError"
                    ).style.display = "none";


                    // ==========================================
                    // OPEN MODAL
                    // ==========================================

                    reviewModal.show();


                    // ==========================================
                    // FETCH REVIEW
                    // ==========================================

                    fetch(
                        `/review-detail/${reviewId}/`,
                        {
                            method: "GET",

                            headers: {
                                "X-Requested-With":
                                    "XMLHttpRequest"
                            }
                        }
                    )


                    .then(function (response) {


                        console.log(
                            "Review response status:",
                            response.status
                        );


                        if (!response.ok) {

                            throw new Error(
                                "Unable to load review."
                            );

                        }


                        return response.json();

                    })
.then(function (data) {

    // Hide any previous error
    document.getElementById(
        "reviewError"
    ).style.display = "none";


    // ==========================================
    // STUDENT INFORMATION
    // ==========================================

    document.getElementById(
        "detailStudentName"
    ).textContent =
        data.student_name || "N/A";

    document.getElementById(
        "detailStudentEmail"
    ).textContent =
        data.student_email || "N/A";

    // ...rest of your code

                    .then(function (data) {


                        console.log(
                            "Review data:",
                            data
                        );


                        // ==========================================
                        // STUDENT INFORMATION
                        // ==========================================

                        document.getElementById(
                            "detailStudentName"
                        ).textContent =
                            data.student_name || "N/A";


                        document.getElementById(
                            "detailStudentEmail"
                        ).textContent =
                            data.student_email || "N/A";


                        document.getElementById(
                            "detailCourse"
                        ).textContent =
                            data.course || "N/A";


                        document.getElementById(
                            "detailBatch"
                        ).textContent =
                            data.batch || "N/A";


                        // ==========================================
                        // RATINGS
                        // ==========================================

                        document.getElementById(
                            "detailRating"
                        ).textContent =
                            `${data.rating}/5 ⭐`;


                        document.getElementById(
                            "detailTeaching"
                        ).textContent =
                            `${data.teaching_quality}/5 ⭐`;


                        document.getElementById(
                            "detailCommunication"
                        ).textContent =
                            `${data.communication}/5 ⭐`;


                        document.getElementById(
                            "detailPractical"
                        ).textContent =
                            `${data.practical_knowledge}/5 ⭐`;


                        document.getElementById(
                            "detailDoubt"
                        ).textContent =
                            `${data.doubt_solving}/5 ⭐`;


                        // ==========================================
                        // SENTIMENT
                        // ==========================================

                        const sentiment =
                            data.sentiment || "neutral";


                        document.getElementById(
                            "detailSentiment"
                        ).textContent =
                            sentiment
                                .charAt(0)
                                .toUpperCase()
                            +
                            sentiment.slice(1);


                        // ==========================================
                        // FEEDBACK
                        // ==========================================

                        document.getElementById(
                            "detailFeedback"
                        ).textContent =
                            data.feedback ||
                            "No feedback provided.";


                        // ==========================================
                        // DATE
                        // ==========================================

                        document.getElementById(
                            "detailCreatedAt"
                        ).textContent =
                            data.created_at || "N/A";


                        // ==========================================
                        // SHOW CONTENT
                        // ==========================================

                        document.getElementById(
                            "reviewLoading"
                        ).style.display = "none";


                        document.getElementById(
                            "reviewContent"
                        ).style.display = "block";


                    })


                    .catch(function (error) {


                        console.error(
                            "Review loading error:",
                            error
                        );


                        // Hide loading

                        document.getElementById(
                            "reviewLoading"
                        ).style.display = "none";


                        // Show error

                        const errorBox =
                            document.getElementById(
                                "reviewError"
                            );


                        errorBox.textContent =
                            "Unable to load this review. Please try again.";


                        errorBox.style.display =
                            "block";

                    });

                }
            );

        });

});