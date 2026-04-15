let cart = [];

async function send() {
  const msg = document.getElementById("msg").value;

  const res = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: msg, cart})
  });

  const data = await res.json();
  cart = data.cart;

  document.getElementById("chat").innerHTML += `<p>${data.message}</p>`;
}
