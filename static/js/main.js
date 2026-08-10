document.addEventListener("DOMContentLoaded", function () {
    /*
     * Automatically close Bootstrap/Django messages
     * after five seconds.
     */
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            if (typeof bootstrap !== "undefined") {
                const bootstrapAlert =
                    bootstrap.Alert.getOrCreateInstance(alert);

                bootstrapAlert.close();
            }
        }, 5000);
    });


    /*
     * Prevent checkout from being submitted
     * more than once.
     */
    const checkoutForm = document.querySelector("#checkout-form");

    if (checkoutForm) {
        checkoutForm.addEventListener("submit", function () {
            const submitButton = checkoutForm.querySelector(
                'button[type="submit"]'
            );

            if (submitButton) {
                submitButton.disabled = true;

                submitButton.innerHTML =
                    '<span class="spinner-border spinner-border-sm me-2" ' +
                    'aria-hidden="true"></span>Processing...';
            }
        });
    }
});


/*
 * Confirmation before destructive actions.
 *
 * Event delegation is used so any form with
 * class="delete-confirm-form" will work.
 */
document.addEventListener("submit", function (event) {
    const form = event.target;

    if (!form.classList.contains("delete-confirm-form")) {
        return;
    }

    const confirmed = window.confirm(
        "Are you sure you want to remove this item?"
    );

    if (!confirmed) {
        event.preventDefault();
    }
});