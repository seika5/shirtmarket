// Get Stripe publishable key
fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // Event handler
  const purchase = document.querySelector("#purchase");
  if(purchase){
    purchase.addEventListener("click", () => {
    // Get Checkout Session ID
      fetch("create-checkout-session/")
      .then((result) => { return result.json(); })
      .then((data) => {
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
    });
  }
});