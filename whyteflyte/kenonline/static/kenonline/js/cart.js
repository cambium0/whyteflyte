function set_evs() {

    var updateBtns = document.getElementsByClassName('update-cart')

    for (i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function() {
            var productId = this.dataset.product
            var action = this.dataset.action
            console.log("user is " + user)
            if (user == 'AnonymousUser'){
                addCookieItem(productId, action)
            }
            else{
                updateUserOrder(productId, action)
            }

        })
    }
}


function updateUserOrder(productId, action) {

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken, 
     },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        location.reload()
    });
}

function addCookieItem(productId, action) {

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity':1}
        }
        else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    }
    //alert('CART:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}


function getModal() {
// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

}
