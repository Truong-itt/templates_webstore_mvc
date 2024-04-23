var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(e) {
        
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('producId',productId,'action',action)
        console.log('user:',user)
        if (user === "AnonymousUser") {
            console.log('User not logged in');
        }
        else {
            updateUserOrder(productId,action)
        }
    })
}

function updateUserOrder(productId, action) {
    console.log('User logged in successfully');
    var url = '/update_item/';
    fetch(url, {
        method: 'POST',   //nhap du lieu len   
        headers: {        //xac dinh kieu du lieu dang gui 
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({   // chinh sua du lieu de gui den server
            'productId':productId,
            'action':action
        })
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log(data)
        location.reload()
    })
}

// JSON.stringify chuyen du lieu dang goc thanh kieu du lieu json 

