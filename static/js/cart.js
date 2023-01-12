var updateBtns = document.getElementsByClassName("update-cart")

for(var i=0; i <= updateBtns.length; i++){
    updateBtns[i].addEventListener("click", function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log("id: ", productID, "action: ", action)

        console.log("User: ", user)

        if (user == "AnonymousUser"){
            addCookieItem(productID, action)
        }
        else{
            updateUserOrder(productID, action)
        }
    })

}

function addCookieItem(id, action) {
    
    if(action == "add"){
        if(cart[id] == undefined){
            cart[id] = {"quantity": 1}
        }
        else{
            cart[id]["quantity"]++
        }
    }

    if(action == "remove"){
        cart[id]["quantity"]--
        if(cart[id]["quantity"] <= 0){
            console.log("Remove item")
            delete cart[id]
        }
    }

    console.log("Cart= ", cart)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(id, action){
    console.log("User is logged in, sending data")

    var url = "/update_item/"
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type":"application/json",
            "X-CSRFToken":csrftoken,
        },
        body: JSON.stringify({
            "id": id,
            "action": action
        })
    }).then((response) => {
        return response.json()
    }).then((data) => {
        console.log("data: ", data)
        location.reload()
    })
}