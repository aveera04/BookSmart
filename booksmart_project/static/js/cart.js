// ===== CART PAGE JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function () {

    // ===== QUANTITY CONTROLS =====
    // Handle the +/- buttons for each cart item
    const qtyGroups = document.querySelectorAll('.cart-qty-controls');
    qtyGroups.forEach(function (group) {
        const minusBtn = group.querySelector('.cart-qty-minus');
        const plusBtn = group.querySelector('.cart-qty-plus');
        const input = group.querySelector('.cart-qty-value');
        const form = group.closest('.cart-qty-form');

        if (!minusBtn || !plusBtn || !input) return;

        const min = parseInt(input.getAttribute('min')) || 1;
        const max = parseInt(input.getAttribute('max')) || 5;

        function updateBtnStates() {
            const val = parseInt(input.value) || min;
            minusBtn.disabled = val <= min;
            plusBtn.disabled = val >= max;
        }

        minusBtn.addEventListener('click', function (e) {
            e.preventDefault();
            let val = parseInt(input.value) || min;
            if (val > min) {
                input.value = val - 1;
                updateBtnStates();
                if (form) form.submit();
            }
        });

        plusBtn.addEventListener('click', function (e) {
            e.preventDefault();
            let val = parseInt(input.value) || min;
            if (val < max) {
                input.value = val + 1;
                updateBtnStates();
                if (form) form.submit();
            }
        });

        // Prevent manual input beyond bounds
        input.addEventListener('change', function () {
            let val = parseInt(input.value);
            if (isNaN(val) || val < min) input.value = min;
            if (val > max) input.value = max;
            updateBtnStates();
        });

        updateBtnStates();
    });


    // ===== DELETE CONFIRMATION =====
    const deleteForms = document.querySelectorAll('.cart-delete-form');
    deleteForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const itemName = form.getAttribute('data-item-name') || 'this item';
            if (!confirm('Remove "' + itemName + '" from your cart?')) {
                e.preventDefault();
            }
        });
    });


    // ===== COUPON CODE (UI ONLY — NO BACKEND) =====
    const couponBtn = document.getElementById('coupon-apply-btn');
    const couponInput = document.getElementById('coupon-input');
    if (couponBtn && couponInput) {
        couponBtn.addEventListener('click', function () {
            const code = couponInput.value.trim();
            if (!code) {
                showCartToast('Please enter a coupon code.', 'info');
                return;
            }
            // Simulated feedback (no backend endpoint yet)
            showCartToast('Coupon "' + code + '" is not valid.', 'error');
        });
    }


    // ===== SIMPLE TOAST HELPER =====
    function showCartToast(message, type) {
        // Reuse existing toast system from base.js if available
        if (typeof renderDjangoMessages === 'function') {
            renderDjangoMessages([{ type: type, text: message }]);
        } else {
            alert(message);
        }
    }


    // ===== RAZORPAY PAYMENT =====
    const payButton = document.getElementById('pay-button');
    if (payButton) {
        payButton.addEventListener('click', function (e) {
            e.preventDefault();

            const amountField = document.getElementById('tamount');
            const addressField = document.getElementById('address');

            if (!amountField || !addressField) return;

            const amount = amountField.value;
            const address = addressField.value.trim();

            // Validation
            if (!address) {
                showCartToast('Please enter your delivery address.', 'error');
                addressField.focus();
                return;
            }

            if (!amount || parseInt(amount) <= 0) {
                showCartToast('Cart is empty. Please add items before making payment.', 'error');
                return;
            }

            // Get CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
            if (!csrfToken) return;

            // Show loading state
            payButton.disabled = true;
            payButton.innerHTML = '<span class="cart-pay-icon">⏳</span> Processing...';

            // AJAX request to initiate payment
            fetch('/initiate-payment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken.value
                },
                body: 'amount=' + encodeURIComponent(amount) + '&address=' + encodeURIComponent(address)
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                const options = {
                    key: data.key,
                    amount: data.amount,
                    currency: data.currency,
                    order_id: data.id,
                    name: data.name,
                    description: data.description,
                    image: data.image,
                    handler: function (response) {
                        if (response.razorpay_payment_id) {
                            window.location.href = '/payment-success/';
                        } else {
                            showCartToast('Payment failed. Please try again.', 'error');
                        }
                    },
                    prefill: {
                        name: 'Card Holder Name',
                    },
                    modal: {
                        ondismiss: function () {
                            payButton.disabled = false;
                            payButton.innerHTML = '<span class="cart-pay-icon">🔒</span> Pay Now — ₹' + amount;
                        }
                    }
                };

                var rzp = new Razorpay(options);
                rzp.open();

                // Reset button after Razorpay opens
                payButton.disabled = false;
                payButton.innerHTML = '<span class="cart-pay-icon">🔒</span> Pay Now — ₹' + amount;
            })
            .catch(function (error) {
                console.error('Error initiating payment:', error);
                showCartToast('Something went wrong. Please try again.', 'error');
                payButton.disabled = false;
                payButton.innerHTML = '<span class="cart-pay-icon">🔒</span> Pay Now — ₹' + amount;
            });
        });
    }
});
