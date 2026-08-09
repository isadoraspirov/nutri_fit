document.addEventListener("DOMContentLoaded", function () {
    /*
     * Automatically close Django/Bootstrap messages
     * after five seconds.
     */
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bootstrapAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bootstrapAlert.close();
        }, 5000);
    });


    /*
     * Ask the user to confirm destructive actions
     * before submitting the form.
     */
    const deleteForms = document.querySelectorAll(".delete-confirm-form");

    deleteForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const confirmed = window.confirm(
                "Are you sure you want to delete this?"
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });


    /*
     * Prevent the checkout form from being submitted
     * multiple times.
     */
    const checkoutForm = document.querySelector("#checkout-form");

    if (checkoutForm) {
        checkoutForm.addEventListener("submit", function () {
            const button = checkoutForm.querySelector(
                'button[type="submit"]'
            );

            if (button) {
                button.disabled = true;
                button.innerText = "Processing...";
            }
        });
    }
});